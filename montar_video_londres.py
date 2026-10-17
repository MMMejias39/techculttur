#!/usr/bin/env python3
"""
montar_video_londres.py — Monta o vídeo "London Tech Week 2026 + Turismo + Cultura".

Lê um manifesto JSON com as cenas (foto + legenda + seção) e gera um vídeo
1920x1080 (30 fps, H.264) com efeito Ken Burns, crossfades e cartelas de
seção no padrão TechLocal.

Uso:
    python3 montar_video_londres.py manifesto.json saida.mp4

Formato do manifesto (JSON):
{
  "titulo": "LONDON TECH WEEK 2026",
  "subtitulo": "Tecnologia, turismo e cultura com o TechLocal",
  "titulo_dur": 5.5,               # opcional (padrão 4.0) — ajustar à narração
  "cenas": [
    {"arquivo": "/caminho/foto.jpg", "legenda": "Tower Bridge", "secao": "Turismo",
     "dur": 5.0,                   # opcional em fotos (padrão 3.2) — ajustar à narração
     "narr_arquivo": "narracao_wavs/01.wav"},  # opcional, usado pelo gerar_audio
    {"arquivo": "/caminho/clipe.mp4", "video": true, "inicio": 12.0,
     "dur": 6, "legenda": "Estande de robótica", "secao": "Tech Week"},
    ...
  ]
}

Seções conhecidas (cores do identificador na barra):
    Tech Week  -> azul tech
    Turismo    -> verde
    Cultura    -> âmbar
"""

import json
import sys

import cv2
import numpy as np

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
FOTO_SEGS = 3.2          # duração padrão de cada foto (sem narração)
XFADE_SEGS = 0.6         # crossfade entre cenas
TITULO_SEGS = 4.0        # cartela de abertura (sem narração)
DIVISOR_SEGS = 2.2       # cartela de divisão de seção
ZOOM = 1.14              # zoom máx. do Ken Burns (1.0 = sem zoom)

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fonte(tamanho):
    return ImageFont.truetype(FONTE, tamanho)


def texto_central(img, texto, tamanho, cor, y, sombra=(0, 0, 0)):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb)
    d = ImageDraw.Draw(pil)
    f = fonte(tamanho)
    box = d.textbbox((0, 0), texto, font=f)
    x = (W - (box[2] - box[0])) // 2
    d.text((x + 3, y + 3), texto, font=f, fill=sombra)
    d.text((x, y), texto, font=f, fill=cor)
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)

CORES_SECAO = {  # cores em RGB (uso via PIL)
    "tech week": ((20, 80, 200), (255, 255, 255)),    # azul, texto branco
    "turismo": ((60, 140, 40), (255, 255, 255)),      # verde
    "cultura": ((200, 160, 40), (30, 30, 30)),        # âmbar, texto escuro
}
COR_PADRAO = ((20, 80, 200), (255, 255, 255))   # azul do canal, texto branco


def cor_secao(nome):
    return CORES_SECAO.get(nome.strip().lower(), COR_PADRAO)


def cartela(titulo, subtitulo, segs, cor_barra=None, texto_barra=None):
    """Gera frames de uma cartela (abertura ou divisão de seção)."""
    cor_barra = cor_barra or (20, 80, 200)
    n = int(segs * FPS)
    for i in range(n):
        fade = min(1.0, i / (0.5 * FPS), (n - i) / (0.5 * FPS))
        img = np.zeros((H, W, 3), np.uint8)
        img[:] = (22, 18, 18)
        img = texto_central(img, titulo, 96, (235, 230, 230), int(H * 0.40))
        if subtitulo:
            img = texto_central(img, subtitulo, 42, (175, 170, 170), int(H * 0.56))
        if texto_barra:
            img[int(H * 0.68):int(H * 0.68) + 90] = cor_barra[::-1]
            img = texto_central(img, texto_barra, 58, (255, 255, 255), int(H * 0.68) + 16)
        yield (img * fade).astype(np.uint8)


def carregar_foto(caminho):
    img = cv2.imread(caminho, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"não consegui ler {caminho}")
    # recorta para 16:9 (centro) e redimensiona para a tela
    h, w = img.shape[:2]
    alvo = W / H
    if w / h > alvo:            # larga demais -> corta laterais
        nw = int(h * alvo)
        x0 = (w - nw) // 2
        img = img[:, x0:x0 + nw]
    else:                        # alta demais -> corta topo/base
        nh = int(w / alvo)
        y0 = (h - nh) // 2
        img = img[y0:y0 + nh, :]
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)


def ken_burns(img_base, n, zoom_in=True):
    """Gera n frames com zoom suave a partir da foto 16:9 já redimensionada."""
    for i in range(n):
        t = i / max(1, n - 1)
        z = 1.0 + (ZOOM - 1.0) * t if zoom_in else ZOOM - (ZOOM - 1.0) * t
        nw, nh = int(W / z), int(H / z)
        x0 = (W - nw) // 2
        y0 = (H - nh) // 2
        crop = img_base[y0:y0 + nh, x0:x0 + nw]
        frame = cv2.resize(crop, (W, H), interpolation=cv2.INTER_LINEAR)
        yield frame


def ajustar_frame(frame):
    """Recorta para 16:9 (centro) e redimensiona para a tela."""
    h, w = frame.shape[:2]
    alvo = W / H
    if w / h > alvo:
        nw = int(h * alvo)
        x0 = (w - nw) // 2
        frame = frame[:, x0:x0 + nw]
    else:
        nh = int(w / alvo)
        y0 = (h - nh) // 2
        frame = frame[y0:y0 + nh, :]
    return cv2.resize(frame, (W, H), interpolation=cv2.INTER_AREA)


def frames_video(caminho, inicio, dur):
    """Extrai dur segundos de um vídeo a partir de `inicio` (segundos)."""
    cap = cv2.VideoCapture(caminho)
    if not cap.isOpened():
        raise ValueError(f"não consegui abrir {caminho}")
    fps_orig = cap.get(cv2.CAP_PROP_FPS) or 30
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(inicio * fps_orig))
    for _ in range(int(dur * FPS)):
        ok, frame = cap.read()
        if not ok:
            break
        yield ajustar_frame(frame)
    cap.release()


def dur_cena(cena):
    """Duração nominal da cena em segundos (corta clipes; estica fotos)."""
    return float(cena.get("dur", FOTO_SEGS))


def contar_frames_cena(cena):
    """Quantos frames a cena renderizaria (lê o vídeo para contar, se for o caso)."""
    if not cena.get("video"):
        return int(dur_cena(cena) * FPS)
    cap = cv2.VideoCapture(cena["arquivo"])
    if not cap.isOpened():
        raise ValueError(f"não consegui abrir {cena['arquivo']}")
    fps_orig = cap.get(cv2.CAP_PROP_FPS) or 30
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(float(cena.get("inicio", 0)) * fps_orig))
    n = 0
    for _ in range(int(dur_cena(cena) * FPS)):
        ok, _ = cap.read()
        if not ok:
            break
        n += 1
    cap.release()
    return n


def blocos(man):
    """Timeline em blocos, na ordem de gravação.

    Cartelas (abertura/divisória) quebram o crossfade: a cena seguinte entra
    com fade a partir da cauda escurecida da cartela — sem 'pulo' de imagem.
    """
    cenas = man["cenas"]
    lista = [{"tipo": "cartela", "segs": float(man.get("titulo_dur", TITULO_SEGS)),
              "titulo": True, "subtitulo": man.get("subtitulo", "")}]
    secao_atual = None
    prev_cena = False
    for idx, cena in enumerate(cenas):
        secao = cena.get("secao", "")
        if secao != secao_atual and idx > 0:
            lista.append({"tipo": "cartela", "segs": DIVISOR_SEGS, "secao": secao})
            prev_cena = False
        if secao != secao_atual:
            secao_atual = secao
        n = contar_frames_cena(cena)
        lista.append({"tipo": "cena", "cena": cena, "n": n, "blend": prev_cena and n > 0})
        prev_cena = n > 0
    return lista


def faixa_legenda(frame, legenda, secao):
    """Sobrepõe faixa semi-transparente com a legenda no rodapé (PIL/UTF-8)."""
    if not legenda:
        return frame
    cor_barra, cor_texto = cor_secao(secao or "")
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil = Image.fromarray(rgb).convert("RGBA")
    faixa = Image.new("RGBA", (W, 80), cor_barra + (185,))
    pil.paste(faixa, (0, H - 110), faixa)
    d = ImageDraw.Draw(pil)
    d.text((40, H - 102), legenda, font=fonte(40), fill=cor_texto)
    if secao:
        txt = secao.upper()
        f = fonte(30)
        box = d.textbbox((0, 0), txt, font=f)
        d.text((W - (box[2] - box[0]) - 40, H - 96), txt, font=f, fill=cor_texto)
    out = pil.convert("RGB")
    return cv2.cvtColor(np.array(out), cv2.COLOR_RGB2BGR)


def gravar(writer, frames):
    for f in frames:
        writer.write(f)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    manifesto_path, saida = sys.argv[1], sys.argv[2]
    with open(manifesto_path, encoding="utf-8") as fh:
        man = json.load(fh)

    n_xf = int(XFADE_SEGS * FPS)
    total_aprox = sum(int(b["segs"] * FPS) if b["tipo"] == "cartela"
                      else b["n"] + (n_xf if b["blend"] else 0)
                      for b in blocos(man))

    writer = cv2.VideoWriter(saida, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H))
    if not writer.isOpened():
        raise RuntimeError("não foi possível abrir o VideoWriter")

    try:
        foto_idx = 0
        escritos = 0
        frames_anteriores = None   # cauda do bloco anterior (para crossfade)
        for n_bloco, bloco in enumerate(blocos(man)):
            if bloco["tipo"] == "cartela":
                if bloco.get("titulo"):
                    frames = list(cartela(man["titulo"], bloco.get("subtitulo", ""),
                                          bloco["segs"], texto_barra="TechLocal"))
                else:
                    cor_barra, _ = cor_secao(bloco["secao"])
                    frames = list(cartela(bloco["secao"], "", bloco["segs"],
                                          cor_barra=cor_barra, texto_barra=bloco["secao"]))
                gravar(writer, frames)
                escritos += len(frames)
                frames_anteriores = frames[-n_xf:] if frames else None
                continue

            cena, n = bloco["cena"], bloco["n"]
            if n == 0:
                print(f"[{n_bloco}] SEM FRAMES: {cena['arquivo']}")
                continue
            secao = cena.get("secao", "")
            if cena.get("video"):
                frames = [faixa_legenda(f, cena.get("legenda", ""), secao)
                          for f in frames_video(cena["arquivo"],
                                                float(cena.get("inicio", 0)),
                                                dur_cena(cena))][:n]
            else:
                img = carregar_foto(cena["arquivo"])
                frames = []
                for i, f in enumerate(ken_burns(img, n, zoom_in=(foto_idx % 2 == 0))):
                    alfa = min(1.0, i / (0.4 * FPS))   # fade-in da legenda
                    com_faixa = faixa_legenda(f, cena.get("legenda", ""), secao)
                    frames.append(cv2.addWeighted(f, 1 - alfa, com_faixa, alfa, 0))
                foto_idx += 1

            if bloco["blend"] and frames_anteriores:
                m = min(n_xf, len(frames), len(frames_anteriores))
                ini = len(frames_anteriores) - m
                for k in range(m):
                    a = (k + 1) / (m + 1)
                    blend = cv2.addWeighted(frames_anteriores[ini + k], 1 - a,
                                            frames[k], a, 0)
                    writer.write(blend)
                    escritos += 1
            gravar(writer, frames)
            escritos += len(frames)
            frames_anteriores = frames[-n_xf:] if frames else frames_anteriores
            print(f"[{n_bloco}] {cena['arquivo']} ({n / FPS:.1f}s)")
    finally:
        writer.release()

    print(f"OK -> {saida} (~{escritos // FPS}s reais, ~{total_aprox // FPS}s previstos, {FPS}fps)")


if __name__ == "__main__":
    main()
