#!/usr/bin/env python3
"""
gerar_audio_londres.py — Faixa de áudio do vídeo: narração + som original.

Lê o manifesto (com "narr_arquivo" injetado por narrar_londres.py) e reproduz
a MESMA timeline de montar_video_londres.blocos(): cada narração entra no
início do bloco da sua cena (o título, 0.4s após o fade-in da cartela) e o
áudio original de cada clipe de vídeo entra 12 dB abaixo (0.25) para não
competir com a voz. Fotos, cartelas e divisórias ficam em silêncio.

Uso:
    python3 gerar_audio_londres.py manifesto.json saida.wav

Requer: ffmpeg no PATH. Depois muxar:
    ffmpeg -i video.mp4 -i saida.wav -map 0:v -map 1:a -c:v libx264 -crf 21 \
           -pix_fmt yuv420p -c:a aac -b:a 192k final.mp4
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from montar_video_londres import FPS, XFADE_SEGS, blocos

SR = 48000
VOL_ORIGINAL = 0.25   # ≈ -12 dB sob a narração
VOL_MUSICA = 0.10     # ≈ -20 dB, apenas clima de fundo


def montar_faixa(man, saida):
    filtro = [f"anullsrc=r={SR}:cl=stereo[base]"]
    entradas = ["-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo"]
    mix = []
    n_in = 1          # próximo índice de input (0 = anullsrc)
    t = 0.0
    n_xf = int(XFADE_SEGS * FPS)

    def add_input(caminho):
        nonlocal n_in
        entradas.extend(["-i", caminho])
        k = n_in
        n_in += 1
        return k

    def add_narr(caminho, inicio_s):
        k = add_input(caminho)
        ms = round(inicio_s * 1000)
        filtro.append(f"[{k}:a]aformat=sample_rates={SR}:channel_layouts=stereo,"
                      f"adelay={ms}|{ms}[n{k}]")
        mix.append(f"[n{k}]")

    for bloco in blocos(man):
        if bloco["tipo"] == "cartela":
            if bloco.get("titulo") and man.get("narr_arquivo"):
                add_narr(man["narr_arquivo"], t + 0.4)
            t += bloco["segs"]
            continue
        cena, n = bloco["cena"], bloco["n"]
        if n == 0:
            continue
        m = min(n_xf, n) if bloco["blend"] else 0
        bloco_dur = (m + n) / FPS
        if cena.get("video"):
            k = add_input(cena["arquivo"])
            ms = round(t * 1000)
            filtro.append(
                f"[{k}:a]atrim=start={float(cena.get('inicio', 0))}:"
                f"duration={bloco_dur:.3f},asetpts=PTS-STARTPTS,"
                f"volume={VOL_ORIGINAL},adelay={ms}|{ms}[c{k}]")
            mix.append(f"[c{k}]")
        if cena.get("narr_arquivo"):
            add_narr(cena["narr_arquivo"], t)
        t += bloco_dur

    dur_total = t
    if man.get("musica"):
        k = add_input(man["musica"])
        filtro.append(
            f"[{k}:a]atrim=0:{dur_total:.3f},volume={VOL_MUSICA},"
            f"afade=t=in:st=0:d=3,afade=t=out:st={max(0, dur_total - 8):.3f}:d=8"
            f"[musica]")
        mix.append("[musica]")
    filtro.append(f"[base]{''.join(mix)}amix=inputs={len(mix) + 1}:normalize=0,"
                  f"atrim=end={dur_total:.3f},aformat=sample_rates={SR}[out]")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write(";\n".join(filtro))
        script = fh.name
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             *entradas, "-filter_complex_script", script,
             "-map", "[out]", "-t", f"{dur_total:.3f}",
             "-ac", "2", "-ar", str(SR), saida],
            check=True)
    finally:
        Path(script).unlink(missing_ok=True)
    return dur_total


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        man = json.load(fh)
    dur = montar_faixa(man, sys.argv[2])
    print(f"OK -> {sys.argv[2]} ({dur:.2f}s)")


if __name__ == "__main__":
    main()
