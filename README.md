# TechLocal — Canal YouTube de Tecnologia + Turismo + Cultura

**Status:** Documentação estratégica pronta. Pipeline de montagem funcionando. Primeiro vídeo de cobertura entregue.

---

## 📋 O que está pronto

### ✅ Documentação
- **CONTEXTO.md** — Missão, visão, pilares e diretrizes gerais
- **ESTRUTURA_VIDEO.md** — Blueprint dos 9 segmentos obrigatórios
- **PREVIO_SCHNEIDER_ELETRIC.md** — Exemplo prático (evento ROGe 2026)
- **GUIA_HOLOGRAMA.md** — Instruções para criar vídeos com efeito holográfico
- **TESTE_STAR_WARS_FRANCISCO.md** — Conceito de efeito visual estilo Star Wars

### ✅ Scripts Python
- **criar_holograma_francisco.py** — Cria vídeo com fundo holográfico (azul/grid)
  - ✓ Testado: funciona
  - ✗ Qualidade: baixa (sem isolamento real)

- **isolar_francisco.py** — Isolamento de pessoa em vídeo (HSV color range)
  - ✓ Testado: funciona
  - ✗ Qualidade: muito baixa (cor-based, não IA)

- **montar_video_londres.py** — Montagem 1080p a partir de manifesto JSON
  - ✓ Testado em 16/10/2026: funciona (19 cenas, fotos + clipes + cartelas de seção)
  - ✗ Limitação: render lento (~3,5 min) e intermediário grande (MPEG-4 ~175 MB)

### ✅ Vídeo entregue (16/10/2026)
- **video_londres_final.mp4** — "London Tech Week 2026 + Turismo + Cultura"
  - 91s, 1920x1080 @ 30fps, H.264 + trilha ambiente (pad sintetizado via ffmpeg)
  - Manifesto: `manifesto_londres.json` (19 cenas: 5 clipes, 14 fotos, 3 seções)
  - Pipeline: render (OpenCV) → mux áudio (ffmpeg) → re-encode H.264
  - Arquivos grandes ficam fora do git (70 MB finais + ~350 MB de intermediários)

### ✅ Repositório GitHub
- https://github.com/MMMejias39/techculttur
- Scripts e documentação commitados; vídeos e mídia não entram no repositório

---

## ❌ O que foi tentado e FALHOU

### Segmentação de Vídeo com IA (rembg)
**O que foi tentado:**
- Instalar `rembg` (biblioteca Python para remoção de background com IA)
- Criar script `isolar_francisco_rembg.py` para isolamento profissional

**Por que falhou:**
1. Modelo ONNX (~1GB) demorou muito a baixar
2. Script começou processamento mas gerou arquivo corrompido (257KB inválido)
3. rembg não é estável em ambiente local
4. Processamento frame-by-frame é muito lento (~1min para alguns frames)

**Resultado:** Arquivo corrompido, sem saída útil.

---

## 🔍 Limites Identificados

### O que funciona bem (OpenCV + ffmpeg + PIL):
- Montagem estrutural: fotos/vídeos + cartelas + legendas + crossfades
- Trilhas sonoras sintetizadas (pads, tons) e mux de áudio
- Re-encode H.264 para YouTube

### O que NÃO funciona bem (delegar para ferramentas especializadas):
- **Modelos de IA pesados** — rembg, SAM, etc são lentos/instáveis sem GPU
- **Segmentação semântica** — isolar pessoa de fundo com qualidade profissional
- **Edição criativa fina** — DaVinci Resolve e Premiere são superiores

### Ferramentas recomendadas para o que está fora do escopo:
- **remove.bg API** — Cloud-based, robusto
- **DaVinci Resolve** — Editor de vídeo profissional (gratuito)
- **Adobe Premiere** — Padrão da indústria

---

## 📊 Consumo de Recursos

| Item | Status | Resultado |
|---|---|---|
| Documentação | ✅ Completo | 5 arquivos .md (pronto para usar) |
| Scripts básicos | ✅ Funcional | 3 scripts que funcionam |
| Vídeo de cobertura | ✅ Entregue | 91s 1080p H.264 com trilha e legendas |
| Segmentação IA | ❌ Falhou | 1 tentativa fracassada, arquivo corrompido |
| **Valor prático entregue** | ✅ Bom | Pipeline completo + primeiro vídeo real |

---

## 🎯 Lições Aprendidas (Para futuros trabalhos)

### Regras para IA (Claude):
1. **Sempre reportar falhas** — Não esconder o que não funcionou
2. **Documentar tentativas falhadas** — Incluir no README
3. **Reconhecer limites cedo** — Não insistir em tarefas fora de escopo
4. **Estimar viabilidade antes** — Questionar se a ferramenta é adequada
5. **Priorizar resultado prático** — Documentação é suporte, não resultado final

### Recomendações específicas:
- ❌ **Não use:** rembg local, HSV color range para segmentação profissional
- ❌ **Não tente:** Modelos pesados de IA em ambiente local sem GPU
- ❌ **Não gaste tokens em:** Tentativa-erro repetida sem conversa clara sobre limites
- ✅ **Use:** OpenCV+ffmpeg para montagem estrutural, APIs externas para segmentação

---

## 🚀 Próximos Passos Recomendados

1. **Revisar** `video_londres_final.mp4` e decidir se a trilha sintetizada deve ser trocada por música real
2. **Commitar** `montar_video_londres.py`, `manifesto_londres.json` e docs atualizados
3. **Segmentação do Conselho Jedi:** Usar remove.bg API ou DaVinci Resolve (fora do escopo local)
4. **Publicação:** Seguir estrutura dos 9 segmentos (documentado em ESTRUTURA_VIDEO.md)

---

## 📝 Resumo Executivo

**O que saiu bem:**
- Documentação estratégica completa
- Pipeline de montagem funcional (manifesto JSON → vídeo 1080p com áudio)
- Primeiro vídeo real entregue: cobertura London Tech Week 2026

**O que não deu:**
- Segmentação semântica de vídeo com IA (rembg) — continua fora do escopo local

**Recomendação final:**
Use este repositório como **pipeline de montagem rápida** (vídeos estruturados com fotos, clipes, cartelas e trilha) e como **guia de planejamento**. Para segmentação profissional e efeitos criativos, use ferramentas especializadas (remove.bg, DaVinci Resolve).

---

**Criado em:** 15 de outubro de 2026  
**Última atualização:** 16 de outubro de 2026 (vídeo London Tech Week entregue)  
**Próxima ação:** Revisar vídeo final e commitar arquivos novos
