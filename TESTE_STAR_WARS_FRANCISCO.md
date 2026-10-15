# 🎬 Teste de Recurso Visual — Star Wars Crawl com Francisco Costa

## 📋 Objetivo

Validar aplicação do **clássico efeito de abertura Star Wars** (perspectiva 3D + texto scrollando para trás) como abertura para vídeos TechLocal, utilizando a fala de Francisco Costa (Engenheiro da Vida) como narração.

**Inspiração:** A New Hope (1977) — abertura épica com "A long time ago in a galaxy far, far away..." seguida de crawl de texto em perspectiva.

---

## 🎯 Conceito do Teste

### Estrutura:
1. **Fade in escuro** (0-2s)
2. **"A long time ago in a galaxy far, far away..."** (música tema Star Wars)
3. **Crawl de texto** (3-8s):
   - Título centralizado em perspectiva 3D
   - Scrollando para trás (como se saísse do viewport)
   - Cor: amarelo/dourado (tema Star Wars clássico) ou azul elétrico (TechLocal)
4. **Fade out para a primeira imagem do Francisco** (8-12s)
5. **Início da fala do Francisco** (com efeito holográfico leve)

---

## 📊 Dados do Material Disponível

### Imagens de Francisco (WhatsApp Images):
```
✓ WhatsApp Image 2026-10-14 at 10.25.15.jpeg — Plenária da 81ª SOEA (cenário)
✓ WhatsApp Image 2026-10-14 at 10.25.22.jpeg — Selfie do Francisco na plateia
✓ WhatsApp Image 2026-10-14 at 10.25.22 (1).jpeg — Francisco com colegas (crachá)
✓ WhatsApp Image 2026-10-14 at 10.25.22 (2).jpeg — Grupo de colegas
✓ WhatsApp Image 2026-10-14 at 10.25.46.jpeg — Outra foto do evento
✓ WhatsApp Image 2026-10-14 at 10.25.46 (1).jpeg — Detalhe do evento
✓ WhatsApp Image 2026-10-14 at 10.26.32.jpeg — Outra perspectiva
```

### Áudio de Francisco (WhatsApp Ptt + Vídeos):
```
✓ WhatsApp Ptt 2026-10-11 at 19.56.46.ogg — Mensagem de voz 1
✓ WhatsApp Ptt 2026-10-14 at 10.26.17.ogg — Mensagem de voz 2
✓ WhatsApp Ptt 2026-10-14 at 10.30.45.ogg — Mensagem de voz 3
✓ WhatsApp Video 2026-10-13 at 21.37.51.mp4 — Vídeo com áudio
✓ WhatsApp Video 2026-10-14 at 10.25.21.mp4 — Vídeo curto
✓ WhatsApp Video 2026-10-14 at 10.25.41.mp4 — Vídeo com fala
✓ WhatsApp Video 2026-10-14 at 10.25.45.mp4 — Depoimento/entrevista
```

### Vídeos Produzidos (NÃO MEXER):
```
✓ Facosta_Engenharia_81SOEA_v2.mp4 — Versão anterior
✓ Facosta_Engenharia_81SOEA_v3.mp4 — Versão atual (usar como referência)
✓ Facosta_Engenharia_81SOEA_v4_teste.mp4 — Teste anterior (com efeito TV analógica)
```

---

## 🎨 Especificações do Efeito Star Wars Crawl

### Visual:
- **Aspecto:** 16:9 (horizontal) ou 9:16 (vertical para Reels)
- **Fundo:** Espaço gradiente (preto → azul escuro com stars)
- **Texto:**
  - Fonte: SF Distant Galaxy (ou similar Star Wars)
  - Cor: Dourado clássico (#FFD700) ou Azul TechLocal (#00D9FF)
  - Tamanho: Começa pequeno (fundo) e cresce ao aproximar (perspectiva)
  - Alinhamento: Centralizado
  - Efeito: Perspectiva isométrica (3D transform CSS ou 2.5D em After Effects)

### Animação:
- **Duração:** 5-8 segundos
- **Movimento:** Y de +600px até -600px (scrollando para trás/cima)
- **Easing:** Linear (sem aceleração/desaceleração, tipo movimento de câmera)
- **Z-depth (perspectiva):** Text começa grande, distante (fundo escuro) e diminui conforme sai da tela

---

## 💡 Proposta de Teste

### **Teste 1: Abertura Pura (apenas efeito visual)**

**Arquivo de saída:** `TESTE_StarWars_Abertura_Silenciosa.mp4` (15s)

```
0:00-2:00 | Fade in, fundo preto gradiente (espaço)
2:00-3:00 | "A long time ago in a galaxy far, far away..." (legenda amarela, fade)
3:00-8:00 | Crawl do texto:
          |   "ENGENHARIA EM 1 MINUTO"
          |   "Francisco Costa | Conselheiro do Clube de Engenharia"
          |   "81ª SOEA — Aracaju/SE | Outubro 2026"
          |   "O futuro da engenharia está em inovação responsável"
8:00-15:00| Crossfade para foto do Francisco (primeira imagem)
```

### **Teste 2: Com Áudio (voz do Francisco + música)**

**Arquivo de saída:** `TESTE_StarWars_Com_Voz.mp4` (30s)

```
0:00-0:05 | Fade in + música tema Star Wars (5s, volume baixo)
0:05-0:10 | Legenda "A long time ago..." + música continua
0:10-0:15 | Início do Crawl de texto
0:15-0:25 | Voz do Francisco começa (áudio extraído de um Ptt/vídeo)
          | Conteúdo: "Olá, meu nome é Francisco Costa..."
0:25-0:30 | Imagem dele aparece (foto selecionada)
          | Crawl desaparece, transição limpa
```

### **Teste 3: Com Imagem Holográfica (efeito azul cianeto)**

**Arquivo de saída:** `TESTE_StarWars_Com_Holograma.mp4` (30s)

```
(Mesmo que Teste 2, mas aplicando:)
- Filter de cor azul/cianeto na foto
- Efeito de grid/linhas de distorção (opcional)
- Brilho/glow ao redor da imagem
- Voz com reverb leve (efeito "holográfico")
```

---

## 🛠️ Ferramentas para Implementação

### Opção A: **DaVinci Resolve** (Grátis)
```
1. Novo projeto, resolução 1920x1080 (ou 1080x1920 para vertical)
2. Novo fusão 3D (Fusion):
   - Importar texto como shape
   - Aplicar transformação 3D (perspectiva Y-axis)
   - Animar posição Y (de +500 a -500)
   - Add imagem de fundo (espaço/stars)
3. Timeline:
   - Colocar o Fusion como elemento
   - Sync com áudio (Ptt do Francisco)
   - Adicionar transição para foto (15s)
```

### Opção B: **After Effects** (Pago, mais fácil)
```
1. Novo comp, 1920x1080
2. Criar layer de texto: "ENGENHARIA..."
3. Aplicar efeito "Perspective" ou "3D Layer"
4. Keyframes:
   - 0s: Position Y = +1000, Scale = 200%
   - 6s: Position Y = -1000, Scale = 50%
5. Layer de fundo: gradiente + image de stars
6. Adicionar áudio do Francisco
7. Exportar como ProRes ou h264
```

### Opção C: **Python + OpenCV + FFmpeg** (Programático)
```python
import cv2
import numpy as np
from moviepy.editor import *

# Criar imagem de fundo (espaço)
background = np.zeros((1080, 1920, 3), dtype=np.uint8)
# Gradiente azul-preto
for y in range(1080):
    background[y, :] = [int(10 * y/1080), int(30 * y/1080), int(50 + 100 * y/1080)]

# Renderizar texto com perspectiva (skew vertical)
# ... (complex, usar After Effects ou Resolve é mais prático)

# Combinar com áudio
# ffmpeg -i video.mp4 -i audio.ogg -c:v copy -c:a aac output.mp4
```

---

## 📝 Roteiro Sugerido para Crawl (Teste 2)

```
ENGENHARIA EM 1 MINUTO
━━━━━━━━━━━━━━━━━━━━━━

Uma transmissão especial do
Clube de Engenharia do Brasil

Apresentação de
FRANCISCO COSTA
Engenheiro Eletricista | Sistemas de Potência
Conselheiro | Inovador

━━━━━━━━━━━━━━━━━━━━━━

"O futuro da engenharia está em inovação
responsável, não em hype vazio."

81ª SOEA — Aracaju/SE | Outubro 2026
```

---

## ✅ Checklist de Execução

**Fase 1: Preparação**
- [ ] Copiar imagens de Francisco para pasta `TESTES/`
- [ ] Selecionar melhores fotos (selfie clara + cenário evento)
- [ ] Extrair áudio de melhor Ptt/vídeo (claridade + sem ruído)
- [ ] Baixar música tema Star Wars (CC0 ou royalty-free) — ex: Audiojungle

**Fase 2: Design**
- [ ] Definir paleta (dourado clássico vs. azul TechLocal)
- [ ] Escolher fonte (SF Distant Galaxy ou alternativa livre)
- [ ] Descrever efeito de perspectiva (isometria 3D)
- [ ] Criar storyboard textual

**Fase 3: Produção**
- [ ] Abrir software (DaVinci/AE)
- [ ] Criar sequência Teste 1 (abertura silenciosa)
- [ ] Ajustar timing + transições
- [ ] Adicionar áudio (Teste 2)
- [ ] Aplicar efeitos (cores, glow, Teste 3)

**Fase 4: Validação**
- [ ] Exportar MP4 baixa compressão
- [ ] Visualizar em tela cheia
- [ ] Verificar legibilidade de texto em perspectiva
- [ ] Sincronismo áudio/vídeo correto
- [ ] Transição para imagem final suave

**Fase 5: Documentação**
- [ ] Anotar timing exato (cada frame)
- [ ] Guardar .aep / .drp (projeto editável)
- [ ] Criar "como fazer" simplificado para próximos vídeos

---

## 🎬 Resultado Esperado

Um vídeo de **30-45 segundos** que:
✓ Abre com efeito épico (Star Wars reconhecível)
✓ Apresenta Francisco de forma digna (holográfica/profissional)
✓ Transiciona suave para conteúdo principal
✓ Pode ser reutilizado em múltiplos vídeos (alterar apenas o crawl)
✓ É compartilhável em Reels/YouTube Shorts

---

## 📌 Referências

- **Star Wars: A New Hope (1977):** [Abertura no YouTube](https://www.youtube.com/watch?v=P3AnY8HYDPM) (primeiros 45s)
- **Efeito de perspectiva 3D:**
  - CSS 3D Transforms: https://developer.mozilla.org/en-US/docs/Web/CSS/perspective
  - After Effects: 3D Layer + Perspective tilt
  - DaVinci Fusion: 3D Node + Z-axis transform
- **Música tema:** Procurar "Star Wars Theme Royalty Free" no Freesound ou Epidemic Sound

---

## 🎯 Próximos Passos

1. **Validar conceito** com você → ajustar cores, timing, texto
2. **Produzir Teste 1** (abertura pura, 15s)
3. **Validar visual** → se aprovado, passar para Teste 2 (com áudio)
4. **Refinar efeitos** → adicionar holografia, cores, etc.
5. **Documentar processo** → criar template reutilizável

---

**Status:** Pronto para produção  
**Data:** 15 de outubro de 2026  
**Material:** Fotos + áudios de Francisco em `~/Documentos/Francisco/`  
**Vídeos originais:** NÃO ALTERADOS (`v2.mp4`, `v3.mp4`, `v4_teste.mp4` intactos)

