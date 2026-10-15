#!/usr/bin/env python3
"""
Script para criar efeito holográfico estilo Conselho Jedi
Remove background de vídeo e adiciona efeitos holográficos, gerando .mp4

Uso: python3 criar_holograma_francisco.py <entrada.mp4> <saida.mp4>
"""

import cv2
import numpy as np
import sys
import os
from pathlib import Path
import random
import subprocess
import tempfile

print("=" * 60)
print("🎬 Criador de Hologramas v1.0 — Conselho Jedi")
print("=" * 60)

def criar_fundo_holografico(altura, largura, frame_idx=0):
    """Cria fundo holográfico com espaço + grid + efeitos"""

    fundo = np.zeros((altura, largura, 3), dtype=np.uint8)

    # Gradiente azul-escuro (espaço)
    for y in range(altura):
        valor = int(10 + (40 * y / altura))
        fundo[y, :] = [valor, valor // 2, 0]

    # Estrelas
    np.random.seed(42)
    for _ in range(200):
        x = np.random.randint(0, largura)
        y = np.random.randint(0, altura)
        brilho = np.random.randint(100, 255)
        cv2.circle(fundo, (x, y), 1, (brilho, brilho, brilho), -1)

    # Grid holográfico
    cor_grid = (0, 200, 255)
    for x in range(0, largura, 40):
        cv2.line(fundo, (x, 0), (x, altura), cor_grid, 1)
    for y in range(0, altura, 40):
        cv2.line(fundo, (0, y), (largura, y), cor_grid, 1)

    # Glitches ocasionais
    if frame_idx % 15 == 0:
        for _ in range(random.randint(2, 5)):
            y_g = random.randint(0, altura)
            h_g = random.randint(5, 20)
            x1, x2 = random.randint(0, largura//2), random.randint(largura//2, largura)
            cor = (random.randint(0, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.line(fundo, (x1, y_g), (x2, y_g + h_g), cor, 2)

    return fundo


def remover_background_simples(frame):
    """Remove background usando detecção de cor"""
    # Converter para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detectar áreas claras (típico de background branco/claro)
    lower = np.array([0, 0, 150])
    upper = np.array([180, 100, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Inverter e refinar
    mask = 255 - mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Aplicar máscara
    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    frame_rgba[:, :, 3] = mask

    return frame_rgba


def aplicar_efeito_holografico(frame_rgba, frame_idx):
    """Aplica efeitos holográficos"""

    mask = frame_rgba[:, :, 3]

    # Pixelação ocasional
    if frame_idx % 10 == 0 and random.random() > 0.5:
        tamanho = random.randint(3, 8)
        pequeno = cv2.resize(frame_rgba, (frame_rgba.shape[1]//tamanho, frame_rgba.shape[0]//tamanho))
        frame_rgba = cv2.resize(pequeno, (frame_rgba.shape[1], frame_rgba.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Scan lines
    if frame_idx % 20 == 0:
        for _ in range(random.randint(1, 3)):
            y = random.randint(0, frame_rgba.shape[0]-2)
            cor = (random.randint(0, 255), random.randint(100, 255), random.randint(100, 255))
            frame_rgba[y:y+2, :, :3] = cor

    # Cintilação
    if random.random() > 0.85:
        intensidade = random.uniform(0.7, 1.0)
        frame_rgba[:, :, :3] = (frame_rgba[:, :, :3] * intensidade).astype(np.uint8)

    return frame_rgba


def compositar(fundo, frame_rgba, x, y):
    """Compõe frame com transparência"""

    h_f, w_f = frame_rgba.shape[:2]
    y2, x2 = y + h_f, x + w_f

    # Clipping
    y1_c = max(0, y)
    x1_c = max(0, x)
    y2_c = min(fundo.shape[0], y2)
    x2_c = min(fundo.shape[1], x2)

    dy1 = max(0, -y)
    dx1 = max(0, -x)

    if y2_c <= y1_c or x2_c <= x1_c:
        return fundo

    alpha = frame_rgba[dy1:dy1+(y2_c-y1_c), dx1:dx1+(x2_c-x1_c), 3].astype(float) / 255.0

    for c in range(3):
        fundo[y1_c:y2_c, x1_c:x2_c, c] = (
            fundo[y1_c:y2_c, x1_c:x2_c, c].astype(float) * (1 - alpha) +
            frame_rgba[dy1:dy1+(y2_c-y1_c), dx1:dx1+(x2_c-x1_c), c].astype(float) * alpha
        ).astype(np.uint8)

    return fundo


def processar_video(entrada, saida):
    """Processa vídeo e cria .mp4"""

    cap = cv2.VideoCapture(entrada)

    if not cap.isOpened():
        print(f"❌ Erro ao abrir: {entrada}")
        return False

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"\n📹 Vídeo: {w}x{h} @ {fps}fps ({total} frames)")
    print(f"📂 Saída: {saida}\n")

    # Usar arquivo temporário
    temp_dir = tempfile.gettempdir()
    temp_avi = os.path.join(temp_dir, "holograma_temp.avi")

    # Escrever com OpenCV (AVI)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(temp_avi, fourcc, fps, (w, h))

    if not out.isOpened():
        print(f"❌ Erro ao criar vídeo temporário")
        return False

    frame_idx = 0
    print("🎬 Processando frames...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Remover fundo
        frame_rgba = remover_background_simples(frame)
        frame_rgba = cv2.resize(frame_rgba, (int(w*0.6), int(h*0.6)))

        # Efeitos
        frame_rgba = aplicar_efeito_holografico(frame_rgba, frame_idx)

        # Fundo
        fundo = criar_fundo_holografico(h, w, frame_idx)

        # Posicionar no centro
        x_pos = (w - frame_rgba.shape[1]) // 2
        y_pos = (h - frame_rgba.shape[0]) // 2

        # Compositar
        fundo = compositar(fundo, frame_rgba, x_pos, y_pos)

        # Escrever
        out.write(fundo)

        frame_idx += 1
        if frame_idx % 30 == 0:
            pct = (frame_idx / total) * 100
            print(f"  ⏳ {frame_idx}/{total} ({pct:.1f}%)")

    cap.release()
    out.release()

    print(f"\n✓ Vídeo temporário criado: {temp_avi}")

    # Converter AVI para MP4 com ffmpeg
    print(f"🔧 Convertendo para MP4...")

    cmd = [
        'ffmpeg', '-i', temp_avi,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-y',  # Overwrite
        saida
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            print(f"❌ Erro ao converter: {result.stderr}")
            return False

        # Remover temporário
        os.remove(temp_avi)

        # Verificar saída
        if os.path.exists(saida):
            tamanho = os.path.getsize(saida) / (1024*1024)
            print(f"\n✅ SUCESSO: {saida} ({tamanho:.1f} MB)")
            return True
        else:
            print(f"❌ Arquivo de saída não foi criado")
            return False

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout na conversão")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print("\n❌ Uso: python3 criar_holograma_francisco.py <entrada.mp4> <saida.mp4>\n")
        print("Exemplo:")
        print("  python3 criar_holograma_francisco.py entrada.mp4 saida.mp4\n")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    if not Path(entrada).exists():
        print(f"\n❌ Arquivo não encontrado: {entrada}\n")
        sys.exit(1)

    if not saida.endswith('.mp4'):
        saida = saida + '.mp4'

    Path(saida).parent.mkdir(parents=True, exist_ok=True)

    sucesso = processar_video(entrada, saida)
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
