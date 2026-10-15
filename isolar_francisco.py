#!/usr/bin/env python3
"""
ETAPA 1: Isolar corpo de Francisco - remover TUDO que não é corpo
Sem efeitos, sem fundo decorativo - apenas corpo limpo
"""

import cv2
import numpy as np
import sys
from pathlib import Path

print("=" * 60)
print("ETAPA 1: Isolamento de Corpo — Francisco Costa")
print("=" * 60)

def remover_background_agressivo(frame):
    """Remove background agressivamente, deixando apenas o corpo"""

    # Converter para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detectar pele (aproximação)
    lower_pele = np.array([0, 20, 70])
    upper_pele = np.array([20, 255, 255])
    mask_pele1 = cv2.inRange(hsv, lower_pele, upper_pele)

    lower_pele2 = np.array([170, 20, 70])
    upper_pele2 = np.array([180, 255, 255])
    mask_pele2 = cv2.inRange(hsv, lower_pele2, upper_pele2)

    mask_pele = cv2.bitwise_or(mask_pele1, mask_pele2)

    # Detectar roupas (cores mais saturadas)
    lower_roupa = np.array([0, 30, 30])
    upper_roupa = np.array([180, 255, 255])
    mask_roupa = cv2.inRange(hsv, lower_roupa, upper_roupa)

    # Combinar: pele + roupas
    mask = cv2.bitwise_or(mask_pele, mask_roupa)

    # Refinar com morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    # Dilatar levemente para incluir bordas
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mask, kernel2, iterations=1)

    return mask


def processar_video_isolamento(entrada, saida):
    """Processa vídeo removendo background"""

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
    print(f"\n🔄 Processando (removendo fundo)...\n")

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

        # Remover background
        mask = remover_background_agressivo(frame)

        # Criar fundo preto
        fundo = np.zeros_like(frame)

        # Aplicar máscara (corpo sobre fundo preto)
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        resultado = np.where(mask_3ch > 127, frame, fundo)
        resultado = resultado.astype(np.uint8)

        # Escrever
        out.write(resultado)

        frame_idx += 1
        if frame_idx % 30 == 0:
            pct = (frame_idx / total) * 100
            print(f"  ⏳ {frame_idx}/{total} ({pct:.1f}%)")

    cap.release()
    out.release()

    if Path(saida).exists():
        tamanho = Path(saida).stat().st_size / (1024*1024)
        print(f"\n✅ PRONTO: {saida}")
        print(f"   Tamanho: {tamanho:.1f} MB\n")
        return True
    else:
        print(f"\n❌ Arquivo não foi criado\n")
        return False


def main():
    if len(sys.argv) < 3:
        print("\n❌ Uso: python3 isolar_francisco.py <entrada.mp4> <saida.mp4>\n")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    if not Path(entrada).exists():
        print(f"\n❌ Arquivo não encontrado: {entrada}\n")
        sys.exit(1)

    if not saida.endswith('.mp4'):
        saida = saida + '.mp4'

    Path(saida).parent.mkdir(parents=True, exist_ok=True)

    sucesso = processar_video_isolamento(entrada, saida)
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()
