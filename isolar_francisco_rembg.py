#!/usr/bin/env python3
"""
ETAPA 1 v2: Isolar corpo de Francisco com rembg (IA)
Muito mais preciso que HSV color range
"""

import cv2
import numpy as np
import sys
from pathlib import Path
from rembg import remove

print("=" * 60)
print("ETAPA 1 v2: Isolamento com IA — rembg")
print("=" * 60)

def isolar_com_rembg(frame):
    """Remove background usando rembg (IA de segmentação)"""
    try:
        # rembg retorna RGBA
        frame_rgba = remove(frame)
        return frame_rgba
    except Exception as e:
        print(f"Erro em frame: {e}")
        return None


def processar_video_rembg(entrada, saida):
    """Processa vídeo com rembg"""

    cap = cv2.VideoCapture(entrada)

    if not cap.isOpened():
        print(f"\n❌ Erro ao abrir: {entrada}\n")
        return False

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"\n📹 Entrada: {w}x{h} @ {fps}fps ({total} frames)")
    print(f"📂 Saída:   {saida}")
    print(f"\n🔄 Processando com rembg (IA)...")
    print(f"   ⏳ Primeira execução carrega modelo (~300MB)...\n")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(saida, fourcc, fps, (w, h))

    if not out.isOpened():
        print(f"❌ Erro ao criar vídeo de saída\n")
        return False

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Converter BGR para RGB para rembg
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Remover background com rembg (retorna RGBA)
        frame_rgba = isolar_com_rembg(frame_rgb)

        if frame_rgba is None:
            print(f"❌ Erro processando frame {frame_idx}")
            continue

        # Criar fundo preto
        fundo = np.zeros((h, w, 3), dtype=np.uint8)

        # Redimensionar se necessário
        if frame_rgba.shape[0] != h or frame_rgba.shape[1] != w:
            frame_rgba = cv2.resize(frame_rgba, (w, h))

        # Extrair alpha channel
        alpha = frame_rgba[:, :, 3].astype(float) / 255.0

        # Extrair BGR (rembg retorna RGBA, então BGR está em [0:3])
        frame_bgr = cv2.cvtColor(frame_rgba[:, :, :3], cv2.COLOR_RGB2BGR)

        # Compositar: pessoa + fundo preto
        resultado = np.zeros((h, w, 3), dtype=np.uint8)
        for c in range(3):
            resultado[:, :, c] = (
                frame_bgr[:, :, c].astype(float) * alpha +
                fundo[:, :, c].astype(float) * (1 - alpha)
            ).astype(np.uint8)

        # Escrever
        out.write(resultado)

        frame_idx += 1
        if frame_idx % 10 == 0:
            pct = (frame_idx / total) * 100
            print(f"  ⏳ {frame_idx}/{total} ({pct:.1f}%)")

    cap.release()
    out.release()

    if Path(saida).exists():
        tamanho = Path(saida).stat().st_size / (1024*1024)
        print(f"\n✅ PRONTO: {saida}")
        print(f"   Tamanho: {tamanho:.1f} MB")
        print(f"   Qualidade: ALTA (IA rembg)\n")
        return True
    else:
        print(f"\n❌ Arquivo não foi criado\n")
        return False


def main():
    if len(sys.argv) < 3:
        print("\n❌ Uso: python3 isolar_francisco_rembg.py <entrada.mp4> <saida.mp4>\n")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    if not Path(entrada).exists():
        print(f"\n❌ Arquivo não encontrado: {entrada}\n")
        sys.exit(1)

    if not saida.endswith('.mp4'):
        saida = saida + '.mp4'

    Path(saida).parent.mkdir(parents=True, exist_ok=True)

    sucesso = processar_video_rembg(entrada, saida)
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
