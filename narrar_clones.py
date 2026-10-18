#!/usr/bin/env python3
"""
narrar_clones.py — Narração com vozes clonadas (Coqui XTTS v2, CPU).

Lê "falas" do manifesto (título + cenas), sintetiza cada fala com a voz
correspondente ("marcelo"/"bernardo") a partir das amostras em amostras_voz/,
concatena as falas de cada bloco com pequenas pausas e injeta no manifesto:
  - "narr_arquivo": WAV do bloco (usado por gerar_audio_londres.py)
  - fotos: "dur" = duração total das falas + margem (a cena não corta a voz)
  - título: "titulo_dur" = duração total + 0.5s

Roda DENTRO do venv com TTS instalado:
    venv-tts/bin/python narrar_clones.py manifesto.json

Amostras: amostras_voz/marcelo.wav e amostras_voz/bernardo.wav
(15-30s de fala limpa cada; qualquer formato — converte para wav 24k primeiro)
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

# torchaudio 2.11 routeia load() para o torchcodec, cuja wheel exige libnvrtc.so.13
# (CUDA) mesmo em CPU — sem GPU, usamos soundfile para carregar o speaker_wav.
import torch
import torchaudio

def _load_com_soundfile(path, *args, **kwargs):
    dados, sr = sf.read(str(path), dtype="float32", always_2d=True)
    return torch.from_numpy(dados.T), sr

torchaudio.load = _load_com_soundfile

from montar_video_londres import FPS, FOTO_SEGS, TITULO_SEGS, contar_frames_cena

VOZES = {
    "marcelo": Path("amostras_voz/marcelo.wav"),
    "bernardo": Path("amostras_voz/bernardo.wav"),
}
CACHE = Path("narracao_wavs/falas")
MARGEM = 0.7      # respiro após o bloco de falas
GAP = 0.22        # pausa entre falas dentro do bloco

_tts = None


def tts():
    global _tts
    if _tts is None:
        from TTS.api import TTS
        _tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
    return _tts


def preparar_amostra(voz):
    """Garante wav mono 24k da amostra de voz (XTTS converte internamente,
    mas arquivo local padronizado evita surpresa)."""
    alvo = VOZES[voz]
    if not alvo.exists():
        originais = list(Path("amostras_voz").glob(f"{voz}.*"))
        if not originais:
            raise SystemExit(f"⚠️  amostra não encontrada: {alvo} "
                             "(grave amostras_voz/{voz}.wav com 15-30s de fala limpa)")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(originais[0]),
                        "-ac", "1", "-ar", "24000", str(alvo)], check=True)
    return str(alvo)


def sintetizar(voz, texto, amostra):
    CACHE.mkdir(parents=True, exist_ok=True)
    h = hashlib.md5(f"{voz}|{texto}".encode()).hexdigest()[:12]
    saida = CACHE / f"{voz}_{h}.wav"
    if not saida.exists():
        print(f"  [{voz}] sintetizando: {texto[:50]}")
        tts().tts_to_file(text=texto, file_path=str(saida),
                          speaker_wav=[amostra], language="pt")
    return saida


def concatenar(partes, destino):
    dados, sr = [], None
    for i, p in enumerate(partes):
        d, s = sf.read(str(p))
        if sr is None:
            sr = s
        elif s != sr:
            raise SystemExit(f"taxas diferentes na concatenação: {p}")
        dados.append(d)
        if i < len(partes) - 1:
            dados.append(np.zeros(int(GAP * sr)))
    sf.write(str(destino), np.concatenate(dados), sr)
    return len(dados and np.concatenate(dados)) / sr if dados else 0.0


def dur_wav(arq):
    d, s = sf.read(str(arq))
    return len(d) / s


def processar_bloco(nome, falas, amostras):
    if not falas:
        return None, None
    partes = [sintetizar(f["voz"], f["texto"], amostras[f["voz"]]) for f in falas]
    destino = Path("narracao_wavs") / f"{nome}.wav"
    concatenar(partes, destino)
    return destino, dur_wav(destino)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    caminho = sys.argv[1]
    with open(caminho, encoding="utf-8") as fh:
        man = json.load(fh)
    Path("narracao_wavs").mkdir(exist_ok=True)
    amostras = {v: preparar_amostra(v) for v in VOZES}

    avisos = []
    wav, d = processar_bloco("00_titulo", man.get("falas_titulo", []), amostras)
    if wav:
        man["narr_arquivo"] = str(wav)
        man["titulo_dur"] = round(max(TITULO_SEGS, d + 0.5), 2)
        print(f"[00_titulo] {d:5.2f}s")

    for i, c in enumerate(man["cenas"]):
        wav, d = processar_bloco(f"{i + 1:02d}", c.get("falas", []), amostras)
        if not wav:
            continue
        c["narr_arquivo"] = str(wav)
        if c.get("video"):
            disp = contar_frames_cena(c) / FPS
            if d > disp - 0.1:
                avisos.append(f"cena {i + 1}: falas {d:.2f}s > clipe {disp:.2f}s "
                              "(inclui crossfade de 0.6s)")
        else:
            c["dur"] = round(max(FOTO_SEGS, d + MARGEM), 2)
        print(f"[{i + 1:02d}] {d:5.2f}s")

    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=2)
    print(f"manifesto atualizado: {caminho}")
    for aviso in avisos:
        print(f"⚠️  {aviso}")


if __name__ == "__main__":
    main()
