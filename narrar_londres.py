#!/usr/bin/env python3
"""
narrar_londres.py — Gera narrações TTS e ajusta o manifesto ao tamanho delas.

Para cada "narracao" do manifesto (título + cenas), gera um WAV em
narracao_wavs/ com voz feminina pt-BR natural (Piper TTS, roda 100% local)
e injeta no manifesto:
  - "narr_arquivo": caminho do WAV (usado por gerar_audio_londres.py)
  - fotos: "dur" = duração da narração + margem (a cena não corta a voz)
  - título: "titulo_dur" = duração da narração + 0.5s

Avisa (não falha) se uma narração for longa demais pro clipe de vídeo.

Uso:
    python3 narrar_londres.py manifesto.json
"""

import json
import subprocess
import sys
from pathlib import Path

from montar_video_londres import FPS, FOTO_SEGS, TITULO_SEGS, contar_frames_cena

MODELO = "vozes_piper/pt_BR-faber-medium.onnx"   # feminina pt-BR, natural
MARGEM = 0.7                                     # respiro após cada narração
DIR = Path("narracao_wavs")


def gerar(texto, wav):
    # sem --stdin: com a flag, o Piper fragmenta o texto e sintetiza só o 1º pedaço
    subprocess.run(
        ["python3", "-m", "piper", "-m", MODELO, "-f", str(wav)],
        input=texto + "\n", text=True, check=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def dur_wav(arq):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(arq)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def obter_wav(nome, texto):
    wav = DIR / f"{nome}.wav"
    if not wav.exists():
        bruto = DIR / f"{nome}_bruto.wav"
        gerar(texto, bruto)
        # normaliza taxa/canais para o mix (Piper gera mono ~22050 Hz)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(bruto),
                        "-ac", "2", "-ar", "48000", str(wav)], check=True)
        bruto.unlink()
    return wav


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    caminho = sys.argv[1]
    with open(caminho, encoding="utf-8") as fh:
        man = json.load(fh)
    DIR.mkdir(exist_ok=True)

    tarefas = [("00_titulo", man.get("narracao", ""))]
    tarefas += [(f"{i + 1:02d}", c.get("narracao", ""))
                for i, c in enumerate(man["cenas"])]

    avisos = []
    for nome, texto in tarefas:
        if not texto:
            continue
        wav = obter_wav(nome, texto)
        d = dur_wav(wav)
        if nome == "00_titulo":
            man["narr_arquivo"] = str(wav)
            man["titulo_dur"] = round(max(TITULO_SEGS, d + 0.5), 2)
        else:
            i = int(nome) - 1
            c = man["cenas"][i]
            c["narr_arquivo"] = str(wav)
            if c.get("video"):
                disp = contar_frames_cena(c) / FPS
                if d > disp - 0.3:
                    avisos.append(f"cena {i + 1}: narração {d:.2f}s > clipe "
                                  f"{disp:.2f}s — encurte o texto")
            else:
                c["dur"] = round(max(FOTO_SEGS, d + MARGEM), 2)
        print(f"[{nome}] {d:5.2f}s  {texto[:60]}")

    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2)
    print(f"manifesto atualizado: {caminho}")
    for aviso in avisos:
        print(f"⚠️  {aviso}")


if __name__ == "__main__":
    main()
