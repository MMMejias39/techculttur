# 🎬 Guia: Criar Vídeo Holográfico (Conselho Jedi)

## O que o script faz

Transforma um vídeo comum em um **efeito holográfico estilo Conselho Jedi**:
- ✅ Remove o fundo original
- ✅ Cria um fundo de espaço com grid holográfico
- ✅ Adiciona efeitos de glitch/defeitos de transmissão
- ✅ Coloca a pessoa no centro com brilho cianeto
- ✅ Exporta como vídeo `.mp4`

---

## Instalação

### 1. Instalar dependências

```bash
# Python 3.8+
pip install opencv-python numpy

# Opcional (RECOMENDADO para melhor qualidade):
pip install rembg torch

# Se usar rembg, também precisa de:
pip install onnxruntime-gpu  # ou onnxruntime para CPU
```

### 2. Verificar instalação

```bash
python3 -c "import cv2, numpy; print('✓ OpenCV e NumPy OK')"
python3 -c "from rembg import remove; print('✓ rembg OK')" 2>/dev/null || echo "⚠ rembg não instalado (opcional)"
```

---

## Como Usar

### Sintaxe básica:

```bash
python3 criar_holograma_francisco.py <video_entrada> <video_saida>
```

### Exemplo com Francisco:

```bash
cd ~/Documentos/techculttur

# Usar um dos vídeos WhatsApp dele
python3 criar_holograma_francisco.py ~/Documentos/Francisco/WhatsApp\ Video\ 2026-10-14\ at\ 10.25.45.mp4 francisco_holograma.mp4
```

### Ou com os vídeos produzidos:

```bash
python3 criar_holograma_francisco.py ~/Documentos/Francisco/Facosta_Engenharia_81SOEA_v3.mp4 francisco_engenharia_holograma.mp4
```

---

## O que esperar

### ⏱️ Tempo de processamento

Depende da duração e qualidade:
- **30 segundos de vídeo:** ~2-5 minutos (CPU) / ~30-60s (GPU)
- **1 minuto de vídeo:** ~5-10 minutos
- **Com rembg:** mais lento, mas muito melhor qualidade
- **Sem rembg:** mais rápido, menos preciso no isolamento

### 📊 Saída esperada

Vídeo `.mp4` com:
- Pessoa isolada (corpo inteiro/corpo em pé)
- Fundo azul-escuro com grid holográfico
- Efeitos de glitch ocasionais (pixelação, linhas de scan)
- Cintilação holográfica
- Tamanho: mesmo da entrada

---

## Ajustes e Personalizações

### 1. Mudar a escala (tamanho da pessoa)

No terminal, adicione parâmetro (padrão: 0.6):

```bash
# Pessoa maior (80% do vídeo)
python3 criar_holograma_francisco.py entrada.mp4 saida.mp4 --scale 0.8

# Pessoa menor (40% do vídeo)
python3 criar_holograma_francisco.py entrada.mp4 saida.mp4 --scale 0.4
```

**Nota:** Para ativar isso, o script precisa ser modificado. Por enquanto, edite a linha:
```python
processar_video(entrada, saida, escala=0.6)  # Mude 0.6 para outro valor
```

### 2. Mudar cores do holograma

Abra `criar_holograma_francisco.py` e procure por:

```python
cor_grid = (0, 200, 255)  # Azul cianeto (BGR format)
```

Exemplos de cores (em BGR):
- **Vermelho:** `(0, 0, 255)`
- **Verde:** `(0, 255, 0)`
- **Azul:** `(255, 0, 0)`
- **Cianeto:** `(255, 255, 0)`
- **Magenta:** `(255, 0, 255)`

### 3. Aumentar/diminuir efeitos de glitch

Procure por:
```python
if frame_idx % 15 == 0:  # Glitch a cada 15 frames
if frame_idx % 10 == 0:  # Pixelação a cada 10 frames
if frame_idx % 20 == 0:  # Scan lines a cada 20 frames
if random.random() > 0.85:  # Cintilação com 15% de chance
```

Números menores = mais efeitos, números maiores = menos efeitos.

---

## Troubleshooting

### ❌ "Erro ao abrir vídeo"

```
❌ Erro ao abrir vídeo: /path/to/file.mp4
```

**Solução:**
- Verificar se o caminho está correto
- Tentar com caminho absoluto (não relativo)
- Verificar permissões: `ls -l arquivo.mp4`

### ❌ "Erro ao criar vídeo de saída"

Significa que a pasta de saída não existe ou permissões insuficientes.

**Solução:**
```bash
# Criar pasta manualmente
mkdir -p ~/Documentos/techculttur/videos_saida

# Usar caminho absoluto
python3 criar_holograma_francisco.py entrada.mp4 ~/Documentos/techculttur/videos_saida/saida.mp4
```

### ⚠️ "rembg não instalado"

O script vai usar segmentação por cor HSV (menos preciso).

**Solução para melhor qualidade:**
```bash
pip install rembg torch onnxruntime-gpu
```

Primeira execução com rembg demora ~30s a 1 min (carrega modelo).

### 🐢 "Vídeo está muito lento a processar"

**Opções:**
1. Usar vídeo mais curto para teste
2. Reduzir resolução entrada (re-encode com ffmpeg)
3. Usar GPU se disponível

```bash
# Re-encode para 480p (mais rápido)
ffmpeg -i entrada.mp4 -vf "scale=854:480" entrada_pequeno.mp4
python3 criar_holograma_francisco.py entrada_pequeno.mp4 saida.mp4
```

---

## Exemplo Passo a Passo

```bash
# 1. Entrar no diretório
cd ~/Documentos/techculttur

# 2. Listar vídeos disponíveis
ls ~/Documentos/Francisco/*.mp4

# 3. Escolher um e processar
python3 criar_holograma_francisco.py \
  ~/Documentos/Francisco/WhatsApp\ Video\ 2026-10-14\ at\ 10.25.45.mp4 \
  teste_holograma.mp4

# 4. Aguardar processamento
# Você verá algo como:
#   📹 Vídeo: 1280x720 @ 30fps, 450 frames
#   🎬 Processando 450 frames...
#     ⏳ 30/450 (6.7%)
#     ⏳ 60/450 (13.3%)
#     ...
#   ✅ Vídeo criado: teste_holograma.mp4

# 5. Assistir resultado
vlc teste_holograma.mp4
# ou
ffplay teste_holograma.mp4
```

---

## Próximo Passo: Conselho Jedi Completo

Quando quiser adicionar **você, Bernardo e Francisco** ao redor de uma **mesa redonda**:

1. Processar vídeo individual de cada um com este script
2. Criar novo script que:
   - Desenha uma mesa redonda (OpenCV)
   - Coloca 3 vídeos holográficos ao redor dela
   - Sincroniza áudio de todos
   - Adiciona efeitos de comunicação

Vou criar isso assim que tiver os 3 vídeos processados!

---

## Verificar o Vídeo Gerado

```bash
# Usar ffmpeg para ver informações
ffprobe teste_holograma.mp4

# Converter para GIF para visualizar rápido (primeiros 5s)
ffmpeg -i teste_holograma.mp4 -t 5 -vf fps=10 preview.gif

# Abrir preview
open preview.gif  # macOS
eog preview.gif   # Linux
explorer preview.gif  # Windows
```

---

## 📝 Próximas Versões

**v2 (planejada):**
- [ ] Suporte a múltiplos vídeos (Conselho Jedi)
- [ ] Mesa redonda/oval
- [ ] Sincronização de áudio de múltiplas fontes
- [ ] Efeitos de comunicação (realce quando alguém fala)
- [ ] Configuração por linha de comando (cores, glitch, posição)

---

**Status:** Pronto para uso  
**Última atualização:** 15 de outubro de 2026  
**Mantidor:** TechLocal

