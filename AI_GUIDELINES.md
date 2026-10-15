# Diretrizes para IA em Futuros Trabalhos

**Criado a partir de:** Experiência com TechLocal (15/10/2026)  
**Objetivo:** Evitar repetir os mesmos erros e melhorar qualidade das entregas

---

## 🚨 REGRAS OBRIGATÓRIAS

### 1. **Sempre Reportar Fracassos**
- ❌ **NUNCA** esconder tentativas que falharam
- ✅ **SEMPRE** incluir no README/documentação:
  - O que foi tentado
  - Por que falhou
  - Qual foi o resultado (corrompido, vazio, erro)
  - Lições aprendidas

### 2. **Reconhecer Limites Técnicos Cedo**
- ⏱️ **Dentro de 2-3 tentativas:** Se não funcionar, parar e reportar
- ❌ **Não fazer:** Tentar 5+ vezes com variações da mesma abordagem
- ✅ **Fazer:** Sugerir ferramenta alternativa de imediato

### 3. **Questionar Viabilidade Antes de Começar**
- Antes de gastar tokens: "Isso é melhor feito em [ferramenta X]?"
- Se a resposta é "sim", diga isso **antes** de tentar
- Não assuma que pode resolver tudo só porque pediu

### 4. **Não Gastar Tokens em Tentativa-Erro Cega**
- Se 1ª tentativa falha: diagnosticar por quê
- Se diagnóstico leva > 20% dos tokens: PARAR e reportar
- Ofereça alternativa (API externa, ferramenta especializada)

### 5. **Priorizar Resultado Prático**
- Documentação = suporte, não resultado final
- Se só consegue entregar documentação: reportar isso **claramente**
- Não disfarçar falta de resultado com muito texto

---

## 📋 Checklist Antes de Finalizar Qualquer Projeto

- [ ] README.md criado com:
  - [ ] O que foi entregue (✅)
  - [ ] O que foi tentado e falhou (❌)
  - [ ] Por que falhou (diagnóstico honesto)
  - [ ] Recomendações para futuro
  - [ ] Valor real vs. tokens consumidos

- [ ] Todos os fracassos documentados
- [ ] Limite de escopo declarado claramente
- [ ] Alternativas sugeridas (se aplicável)
- [ ] Próximos passos recomendados

---

## 🎯 Exemplos de Boas Práticas

### ✅ BOM: Reconhecer limite cedo
```
Tentei rembg (1ª vez) → falhou → diagnóstico: arquivo corrompido → 
Recomendação: Use remove.bg API ou Kimi (especialistas nisso) → 
Parar aqui, não gastar mais tokens
```

### ❌ RUIM: Insistir sem resultado
```
Tentei rembg (1ª) → falhou → Tentei HSV (2ª) → ruim → 
Tentei rembg de novo (3ª) → corrompido → 
Continuei tentando variações (4ª, 5ª...) → 
Só no fim: "não funcionou"
```

---

## 💰 Princípio de Eficiência

**Regra de Ouro:**
- Se não há resultado prático em 30% dos tokens → parar e reportar
- Se alternativa especializada existe → sugerir logo
- Documentação é bônus, não desculpa

**Exemplo:**
- Projeto total = 100 tokens
- 30 tokens = limite para experimentação
- Se em 30 tokens não houver progresso: parar, reportar, sugerir alternativa

---

## 📊 Matriz de Decisão

| Situação | Ação |
|---|---|
| 1ª tentativa falha | Diagnosticar por quê |
| 2ª tentativa falha | Questionar se é viável |
| 3ª tentativa falha | **PARAR aqui. Reportar.** |
| Ferramenta especializada existe | Sugerir ao invés de tentar |
| Tokens > 30% sem progresso | Parar e reportar honestamente |
| Fracasso claro | Incluir no README antes de finalizar |

---

## 🎓 Aplicado ao TechLocal

**O que deveria ter feito:**
1. ✅ Criar documentação (concluído corretamente)
2. ⚠️ Tentar rembg 1x (diagnóstico: instável em local)
3. ✅ Reportar que falhou (fiz isso tarde)
4. ✅ Sugerir alternativa: Kimi, remove.bg (fiz isso tarde)
5. ❌ Não desperdiçar tokens em mais tentativas (fiz isso 3x)

**Resultado esperado:**
- Mesma documentação ✅
- Mas 70% menos tokens gastos
- E falha reportada logo no início

---

**Versão:** 1.0  
**Próxima revisão:** Quando projeto similar surgir  
**Responsável:** IA (Claude) em futuros trabalhos

