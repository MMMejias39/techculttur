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
  "cenas": [
    {"arquivo": "/caminho/foto.jpg", "legenda": "Tower Bridge", "secao": "Turismo"},
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
FOTO_SEGS = 3.2          # duração de cada foto
XFADE_SEGS = 0.6         # crossfade entre fotos
TITULO_SEGS = 4.0        # cartela de abertura
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
COR_PADRAO = ((90, 90, 90), (255, 255, 255))


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

    cenas = man["cenas"]
    n_foto = int(FOTO_SEGS * FPS)
    n_xf = int(XFADE_SEGS * FPS)
    total = (int(TITULO_SEGS * FPS)
             + len(cenas) * (n_foto + n_xf)
             + sum(int(DIVISOR_SEGS * FPS) for i in range(1, len(cenas))
                   if cenas[i]["secao"] != cenas[i - 1]["secao"]))

    writer = cv2.VideoWriter(saida, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H))
    if not writer.isOpened():
        raise RuntimeError("não foi possível abrir o VideoWriter")

    try:
        gravar(writer, cartela(man["titulo"], man.get("subtitulo", ""),
                               TITULO_SEGS, texto_barra="TechLocal"))

        secao_atual = None
        frames_anteriores = None
        for idx, cena in enumerate(cenas):
            secao = cena.get("secao", "")
            if secao != secao_atual and idx > 0:
                cor_barra, _ = cor_secao(secao)
                gravar(writer, cartela(secao, "", DIVISOR_SEGS,
                                       cor_barra=cor_barra, texto_barra=secao))
            if secao != secao_atual:
                secao_atual = secao

            if cena.get("video"):
                dur = float(cena.get("dur", FOTO_SEGS))
                frames = [faixa_legenda(f, cena.get("legenda", ""), secao)
                          for f in frames_video(cena["arquivo"],
                                                float(cena.get("inicio", 0)), dur)]
            else:
                img = carregar_foto(cena["arquivo"])
                frames = []
                for i, f in enumerate(ken_burns(img, n_foto, zoom_in=(idx % 2 == 0))):
                    alfa = min(1.0, i / (0.4 * FPS))   # fade-in da legenda
                    com_faixa = faixa_legenda(f, cena.get("legenda", ""), secao)
                    frames.append(cv2.addWeighted(f, 1 - alfa, com_faixa, alfa, 0))

            if frames_anteriores is not None and frames:
                ini = max(0, len(frames_anteriores) - n_xf)
                for k in range(n_xf):
                    if k >= len(frames):
                        break
                    a = (k + 1) / (n_xf + 1)
                    blend = cv2.addWeighted(frames_anteriores[ini + k], 1 - a,
                                            frames[k], a, 0)
                    writer.write(blend)
            gravar(writer, frames)
            frames_anteriores = frames
            print(f"[{idx + 1}/{len(cenas)}] {cena['arquivo']}")
    finally:
        writer.release()

    print(f"OK -> {saida} (~{total // FPS}s a {FPS}fps)")


if __name__ == "__main__":
    main()
