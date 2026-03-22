# DESIGN BRIEF — Quiz Diagnóstico "Espanhol com Você"
## "Descubra por que você trava na hora de falar espanhol"

**Versão:** 1.0
**Data:** 2026-03-20
**Cliente:** @espanholcomvoce (Ale)
**Formato:** Single-page app (HTML/CSS/JS)
**Tráfego principal:** Mobile via Instagram (80%+)

---

## SUMÁRIO

1. [Identidade Visual Geral](#1-identidade-visual-geral)
2. [Página de Entrada / Intro](#2-página-de-entrada--intro)
3. [Telas de Perguntas — Design de Progressão](#3-telas-de-perguntas--design-de-progressão)
4. [Página de Resultado — O Clímax](#4-página-de-resultado--o-clímax)
5. [Responsivo & Mobile](#5-responsivo--mobile)
6. [Micro-interações & Animações](#6-micro-interações--animações)
7. [Técnicas CSS Específicas](#7-técnicas-css-específicas)
8. [Especificações de Componentes](#8-especificações-de-componentes)

---

## 1. IDENTIDADE VISUAL GERAL

### 1.1 Paleta de Cores — Regras de Uso

```
CORES PERMITIDAS:
--navy-900:    #0a1628   (fundo principal)
--navy-800:    #111d32   (fundo de cards, elevação nível 1)
--navy-700:    #1a2740   (bordas sutis, separadores)
--gold:        #fbbf24   (acento principal, destaques, CTAs)
--gold-glow:   rgba(251, 191, 36, 0.15)  (halo dourado)
--gold-soft:   rgba(251, 191, 36, 0.08)  (fundo sutil dourado)
--sky:         #38bdf8   (links, elementos informativos, barra de compreensão)
--emerald:     #10b981   (acerto, sucesso, barra de produção quando alta)
--white:       #ffffff   (texto principal)
--slate-400:   #94a3b8   (texto secundário, labels)
--slate-600:   #475569   (texto desabilitado, placeholders)
--red-soft:    #ef4444   (erro — SOMENTE para indicar resposta incorreta)

CORES PROIBIDAS — NUNCA USAR:
--PROIBIDO-1:  #ff421c
--PROIBIDO-2:  #36c551
```

### 1.2 Jornada Emocional

O quiz não é um formulário. É uma **experiência narrativa em 3 atos** que leva o usuário por:

| Fase | Emoção | Sensação Visual |
|------|--------|-----------------|
| Intro | Curiosidade + urgência | Escuro, misterioso, convite íntimo |
| Ato 1 (Q1-3) | Confiança crescente | Quente, dourado, acolhedor |
| Transição A1→A2 | Momento "opa..." | Shift visual perceptível, tensão |
| Ato 2 (Q4-7) | Confronto, desconforto produtivo | Mais frio, sky blue aparece, pressão |
| Ato 3 (Q8-10) | Alívio, intimidade | Calmo, pessoal, Caveat aparece |
| Resultado | Revelação + esperança | Dramático, dados visuais, CTA forte |

### 1.3 O Que Diferencia de um Quiz Genérico

- **Sem fundo branco.** Tudo escuro, imersivo, como uma sala de cinema antes do filme.
- **Sem opções coloridas genéricas.** Cards de opção são glass-morphism sobre navy.
- **Feedback educativo inline.** Cada resposta ensina algo — não é só "certo/errado".
- **Progressão visual narrativa.** A paleta muda entre atos. O usuário SENTE a mudança.
- **Tipografia expressiva.** Headlines em Inter 900, palavras emocionais em Caveat dourado.
- **Foto da Ale** como âncora de confiança — não genérico, tem rosto humano.

### 1.4 Tratamento de Fotos da Ale

- Foto principal (intro e resultado): recortada do peito pra cima, olhando para a câmera ou levemente para o lado.
- **Tratamento:** fundo removido (transparente), emergindo do fundo navy escuro.
- **Efeito:** borda inferior da foto com gradient fade para `#0a1628` (a foto "nasce" do fundo).
- **Iluminação:** leve rim-light dourado simulado via CSS:
  ```css
  .ale-photo {
    filter: drop-shadow(0 0 20px rgba(251, 191, 36, 0.3));
  }
  ```
- Na página de resultado: foto menor (80px redonda) ao lado da assinatura.
- Formato: WebP, max 400px largura, lazy loaded.

### 1.5 Estilo de Ícones e Elementos Visuais

- **Ícones:** Lucide Icons (linha fina, 1.5px stroke), cor `#94a3b8` no estado normal, `#fbbf24` quando ativo.
- **Tamanho padrão de ícones:** 20px (mobile), 24px (desktop).
- **Elementos decorativos:** linhas sutis douradas (1px, `rgba(251, 191, 36, 0.2)`) como separadores.
- **Sem ilustrações cartoon.** Somente: ícones de linha, fotos reais, tipografia expressiva, gradients.
- **Aspas/destaques:** usar aspas estilizadas em Caveat, tamanho grande, cor gold, opacidade 0.3 como elemento decorativo de fundo.

---

## 2. PÁGINA DE ENTRADA / INTRO

### 2.1 Layout e Hierarquia (Mobile-First)

A intro é uma tela única, sem scroll (100vh no mobile). Tudo visível de uma vez.

```
┌─────────────────────────────┐
│                             │
│   [Logo pequeno - 32px]     │  ← topo, centralizado
│                             │
│   ━━━━━━━━━━━━━━━━━━━━━━    │  ← linha dourada decorativa (1px)
│                             │
│   "Você ENTENDE espanhol    │  ← headline Inter 900
│    mas TRAVA na hora        │     28px mobile / 42px desktop
│    de falar?"               │     "TRAVA" em #fbbf24
│                             │
│   Descubra em 3 minutos     │  ← subtítulo Inter 400
│   qual é o REAL bloqueio    │     16px, cor #94a3b8
│   que te impede de falar    │     "REAL" em #fbbf24
│   com confiança.            │
│                             │
│      ┌─────────────┐        │
│      │  Foto Ale   │        │  ← 200px altura, fade inferior
│      │  (emerge do │        │     centralizada
│      │   fundo)    │        │
│      └─────────────┘        │
│                             │
│   ┌───────────────────────┐ │
│   │  DESCOBRIR MEU NÍVEL  │ │  ← CTA principal
│   │        →              │ │     56px altura, full-width
│   └───────────────────────┘ │
│                             │
│   🔒 Gratuito • 3 min •    │  ← trust line
│   +2.847 diagnósticos       │     14px, #94a3b8
│                             │
└─────────────────────────────┘
```

### 2.2 Detalhes do CTA Principal

```css
.cta-primary {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #0a1628;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 16px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  padding: 0 32px;
  height: 56px;
  border: none;
  border-radius: 16px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100%;
  max-width: 360px;
  box-shadow:
    0 0 20px rgba(251, 191, 36, 0.3),
    0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cta-primary:hover {
  transform: translateY(-2px);
  box-shadow:
    0 0 30px rgba(251, 191, 36, 0.5),
    0 8px 20px rgba(0, 0, 0, 0.4);
}

.cta-primary:active {
  transform: translateY(0);
  box-shadow:
    0 0 15px rgba(251, 191, 36, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.3);
}

/* Shimmer effect no botão */
.cta-primary::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}
```

### 2.3 Elementos de Confiança

Abaixo do CTA, linha única com ícones pequenos:

- Ícone de cadeado (Lucide `Lock`, 14px) + "Gratuito"
- Ícone de relógio (Lucide `Clock`, 14px) + "3 minutos"
- Ícone de users (Lucide `Users`, 14px) + "+2.847 diagnósticos"
- Tudo em `#94a3b8`, `font-size: 13px`, separado por bullet `•`
- Espaçamento: `gap: 6px` entre ícone e texto, `gap: 12px` entre itens

### 2.4 Background da Intro

```css
.intro-page {
  background: #0a1628;
  min-height: 100vh;
  min-height: 100dvh; /* dynamic viewport height para mobile */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 20px;
  position: relative;
  overflow: hidden;
}

/* Glow sutil atrás da foto da Ale */
.intro-page::before {
  content: '';
  position: absolute;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.08) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -60%);
  pointer-events: none;
}

/* Textura noise sutil para o fundo não ficar flat */
.intro-page::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* noise pattern inline */
  opacity: 0.03;
  pointer-events: none;
}
```

---

## 3. TELAS DE PERGUNTAS — DESIGN DE PROGRESSÃO

### 3.1 Layout Base de Cada Pergunta

```
┌─────────────────────────────────┐
│  [Progress]  ───────────── 3/10 │  ← barra de progresso + contador
│                                 │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │  Pergunta aqui em Inter   │  │  ← card da pergunta
│  │  700, 20px mobile         │  │     glass-morphism card
│  │                           │  │
│  │  [Audio player se houver] │  │
│  │                           │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │  A) Opção 1               │  │  ← cards de opção
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │  B) Opção 2               │  │     empilhados, full-width
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │  C) Opção 3               │  │
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │  D) Opção 4               │  │
│  └───────────────────────────┘  │
│                                 │
└─────────────────────────────────┘
```

### 3.2 Barra de Progresso

Não usar barra numérica comum. Usar um design que reforce a narrativa:

```css
.progress-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  width: 100%;
}

.progress-bar-track {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  margin-right: 12px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* A cor da barra muda por ato */
.act-1 .progress-bar-fill {
  background: linear-gradient(90deg, #fbbf24, #f59e0b);
  box-shadow: 0 0 8px rgba(251, 191, 36, 0.4);
}

.act-2 .progress-bar-fill {
  background: linear-gradient(90deg, #38bdf8, #0ea5e9);
  box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
}

.act-3 .progress-bar-fill {
  background: linear-gradient(90deg, #10b981, #059669);
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
}

.progress-counter {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 13px;
  color: #94a3b8;
  white-space: nowrap;
  min-width: 36px;
  text-align: right;
}
```

**Comportamento:** A barra NÃO mostra "Pergunta 4 de 10" — mostra apenas `4/10` pequeno + a barra visual. Motivo: não intimidar o usuário com "faltam 6". O preenchimento gradual é reward suficiente.

### 3.3 Variação Visual por Ato

#### ATO 1 — Confiança (Q1-3)

**Mood:** Quente, acolhedor, encorajador. O usuário está acertando e se sentindo bem.

```css
.act-1 {
  /* Background levemente mais quente */
  background: linear-gradient(180deg, #0a1628 0%, #0f1b2e 100%);
}

.act-1 .question-card {
  background: rgba(251, 191, 36, 0.04);
  border: 1px solid rgba(251, 191, 36, 0.1);
  border-radius: 20px;
  padding: 24px 20px;
  backdrop-filter: blur(10px);
}

.act-1 .question-label {
  /* Label acima da pergunta: "Expressão" ou "Falso cognato" */
  font-family: 'Caveat', cursive;
  color: #fbbf24;
  font-size: 18px;
  margin-bottom: 8px;
}

.act-1 .feedback-correct {
  background: rgba(16, 185, 129, 0.1);
  border-left: 3px solid #10b981;
  color: #ffffff;
}
```

**Feedback no Ato 1:** Após responder, um card de feedback desliza de baixo (300ms ease-out) mostrando:
- Ícone de check verde (se acertou) ou info azul (se errou)
- Explicação curta (2-3 linhas) em Inter 400 16px
- A expressão/cognato ensinado em **negrito gold**
- Botão "Próxima →" aparece dentro do feedback

#### ATO 2 — Confronto (Q4-7)

**Mood:** Tensão crescente. O fundo fica mais frio. A pressão é palpável.

**TRANSIÇÃO PIVOTAL (entre Q3 e Q4):**

Após o feedback da Q3, antes de mostrar Q4, inserir uma **tela de transição** (2-3 segundos):

```
┌─────────────────────────────┐
│                             │
│                             │
│   "Até aqui, tudo bem..."   │  ← Caveat, 24px, gold, fade-in
│                             │
│   "Mas entender é só        │  ← Inter 400, 16px, white
│    metade da história."     │     fade-in com 0.5s delay
│                             │
│         ↓                   │  ← seta pulsante, fade-in 1s delay
│                             │
│                             │
└─────────────────────────────┘
```

Essa tela aparece por 3 segundos e auto-avança (ou o usuário toca para continuar).

```css
.act-2 {
  /* Background mais frio, sky blue aparece */
  background: linear-gradient(180deg, #0a1628 0%, #0b1a30 50%, #0d1f38 100%);
}

.act-2 .question-card {
  background: rgba(56, 189, 248, 0.04);
  border: 1px solid rgba(56, 189, 248, 0.1);
  border-radius: 20px;
  padding: 24px 20px;
  backdrop-filter: blur(10px);
}

.act-2 .question-label {
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  color: #38bdf8;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 8px;
}

/* Timer visual para perguntas de produção (Q5-Q6) */
.act-2 .pressure-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #94a3b8;
  margin-top: 12px;
}

.act-2 .pressure-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #38bdf8;
  animation: pulse-dot 1.5s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.3); }
}
```

**Feedback no Ato 2:** O feedback aqui é mais longo e mais impactante:
- Fundo: `rgba(56, 189, 248, 0.06)` com borda esquerda sky blue
- Título do feedback em Caveat gold: _"Isso é o bloqueio em ação"_
- Explicação do MECANISMO (por que travou) em 3-4 linhas
- Palavras-chave do mecanismo em **bold sky blue**

#### ATO 3 — Contexto Pessoal (Q8-10)

**Mood:** Calmo, íntimo, pessoal. As perguntas são sobre o usuário, não sobre espanhol.

```css
.act-3 {
  background: linear-gradient(180deg, #0a1628 0%, #0e1a2b 100%);
}

.act-3 .question-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 24px 20px;
}

.act-3 .question-text {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 20px;
  line-height: 1.5;
}

/* Toque pessoal: assinatura da Ale no canto */
.act-3 .personal-touch {
  font-family: 'Caveat', cursive;
  color: rgba(251, 191, 36, 0.6);
  font-size: 16px;
  margin-top: 16px;
  text-align: right;
}
```

**Sem feedback** nas perguntas do Ato 3. Apenas transição suave para a próxima pergunta. Sem certo/errado.

### 3.4 Cards de Opção de Resposta

```css
.option-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 52px;
  -webkit-tap-highlight-color: transparent;
}

.option-letter {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
  font-size: 14px;
  color: #94a3b8;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.option-text {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 15px;
  color: #ffffff;
  line-height: 1.4;
}

/* Hover (desktop) */
.option-card:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(251, 191, 36, 0.2);
  transform: translateX(4px);
}

.option-card:hover .option-letter {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

/* Selecionado */
.option-card.selected {
  background: rgba(251, 191, 36, 0.08);
  border-color: rgba(251, 191, 36, 0.4);
}

.option-card.selected .option-letter {
  background: #fbbf24;
  color: #0a1628;
}

/* Correto (após feedback) */
.option-card.correct {
  background: rgba(16, 185, 129, 0.08);
  border-color: rgba(16, 185, 129, 0.4);
}

.option-card.correct .option-letter {
  background: #10b981;
  color: #ffffff;
}

/* Incorreto (após feedback) */
.option-card.incorrect {
  background: rgba(239, 68, 68, 0.06);
  border-color: rgba(239, 68, 68, 0.3);
  opacity: 0.7;
}

.option-card.incorrect .option-letter {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}
```

### 3.5 Audio Player (para perguntas com áudio)

Design minimalista que não compete com as opções:

```
┌─────────────────────────────────┐
│  🔊  ▶  ━━━━━━●━━━━━━━  0:04   │
└─────────────────────────────────┘
```

```css
.audio-player {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 14px 18px;
  margin: 16px 0;
}

.audio-icon {
  color: #fbbf24;
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}

.audio-play-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(251, 191, 36, 0.15);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  color: #fbbf24;
  transition: all 0.2s ease;
}

.audio-play-btn:hover {
  background: rgba(251, 191, 36, 0.25);
  transform: scale(1.05);
}

.audio-play-btn:active {
  transform: scale(0.95);
}

.audio-track {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  position: relative;
  cursor: pointer;
}

.audio-track-fill {
  height: 100%;
  background: #fbbf24;
  border-radius: 2px;
  position: relative;
}

.audio-track-fill::after {
  content: '';
  position: absolute;
  right: -5px;
  top: 50%;
  transform: translateY(-50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #fbbf24;
  box-shadow: 0 0 6px rgba(251, 191, 36, 0.4);
}

.audio-time {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 500;
  color: #94a3b8;
  min-width: 32px;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
```

### 3.6 Card de Feedback (pós-resposta)

O feedback aparece inline, logo abaixo das opções, com animação slide-up + fade-in.

```css
.feedback-card {
  margin-top: 16px;
  padding: 20px;
  border-radius: 16px;
  animation: slideUpFade 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  transform: translateY(20px);
  opacity: 0;
}

@keyframes slideUpFade {
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Variante: Correto (Ato 1) */
.feedback-card.correct {
  background: rgba(16, 185, 129, 0.06);
  border-left: 3px solid #10b981;
}

/* Variante: Informativo (Ato 2 — não é "errado", é revelação) */
.feedback-card.insight {
  background: rgba(56, 189, 248, 0.06);
  border-left: 3px solid #38bdf8;
}

.feedback-title {
  font-family: 'Caveat', cursive;
  font-size: 20px;
  color: #fbbf24;
  margin-bottom: 8px;
}

.feedback-text {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 15px;
  line-height: 1.6;
  color: #e2e8f0;
}

.feedback-highlight {
  color: #fbbf24;
  font-weight: 600;
}

.feedback-mechanism {
  /* Usado no Ato 2 para destacar o mecanismo do bloqueio */
  color: #38bdf8;
  font-weight: 600;
}

.feedback-next-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px 24px;
  background: rgba(251, 191, 36, 0.12);
  border: 1px solid rgba(251, 191, 36, 0.25);
  border-radius: 12px;
  color: #fbbf24;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.feedback-next-btn:hover {
  background: rgba(251, 191, 36, 0.2);
  transform: translateX(4px);
}
```

### 3.7 Transições entre Perguntas

```css
/* Pergunta saindo */
.question-exit {
  animation: questionOut 0.3s ease-in forwards;
}

@keyframes questionOut {
  to {
    opacity: 0;
    transform: translateX(-30px);
  }
}

/* Pergunta entrando */
.question-enter {
  animation: questionIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
  animation-delay: 0.15s;
  opacity: 0;
  transform: translateX(30px);
}

@keyframes questionIn {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

**Timing:** Ao clicar "Próxima →", a pergunta atual faz exit (300ms), pausa 150ms, nova pergunta faz enter (400ms). Total: ~850ms entre perguntas.

---

## 4. PÁGINA DE RESULTADO — O CLÍMAX

### 4.1 Animação de Carregamento (Calculando Resultado)

Após a Q10, mostrar uma tela de "cálculo" por 4-5 segundos. Isso cria **anticipation** e faz o resultado parecer personalizado.

```
┌─────────────────────────────┐
│                             │
│                             │
│     ◌  ◌  ◌  ◌             │  ← dots pulsantes em sequência
│                             │
│   "Analisando suas          │  ← texto que muda a cada 1.5s
│    respostas..."            │
│                             │
│   ━━━━━━━━━━━━━━━━━         │  ← barra que enche em steps
│                             │
│                             │
└─────────────────────────────┘
```

**Textos que rotacionam (fade in/out a cada 1.5s):**
1. "Analisando suas respostas..."
2. "Calculando nível de compreensão..."
3. "Medindo capacidade de produção..."
4. "Gerando seu diagnóstico personalizado..."

```css
.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  min-height: 100dvh;
  background: #0a1628;
  padding: 24px;
}

.loading-dots {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
}

.loading-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #fbbf24;
  animation: dotPulse 1.2s ease-in-out infinite;
}

.loading-dot:nth-child(2) { animation-delay: 0.15s; }
.loading-dot:nth-child(3) { animation-delay: 0.3s; }
.loading-dot:nth-child(4) { animation-delay: 0.45s; }

@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1.2); }
}

.loading-text {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 16px;
  color: #94a3b8;
  text-align: center;
  min-height: 48px;
  display: flex;
  align-items: center;
}

.loading-text span {
  animation: textFade 1.5s ease-in-out;
}

@keyframes textFade {
  0% { opacity: 0; transform: translateY(8px); }
  15% { opacity: 1; transform: translateY(0); }
  85% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-8px); }
}

.loading-bar-track {
  width: 200px;
  height: 3px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  margin-top: 24px;
  overflow: hidden;
}

.loading-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #fbbf24, #38bdf8);
  border-radius: 2px;
  animation: loadFill 4.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes loadFill {
  0% { width: 0%; }
  25% { width: 30%; }
  50% { width: 55%; }
  75% { width: 80%; }
  100% { width: 100%; }
}
```

### 4.2 Layout da Página de Resultado

A página de resultado é **scrollável** (diferente das perguntas que são paginadas). O conteúdo revela em seções conforme o scroll.

```
┌─────────────────────────────────┐
│                                 │
│  SEÇÃO 1: DIAGNÓSTICO          │
│  ─────────────────────          │
│                                 │
│  "Seu Diagnóstico"             │  ← Caveat 28px gold
│   de Espanhol                   │  ← Inter 900 32px white
│                                 │
│  ┌─────────────────────────┐   │
│  │ Compreensão              │   │
│  │ ████████████████░░░ 78%  │   │  ← barra sky blue
│  │                          │   │
│  │ Produção                 │   │
│  │ ██████░░░░░░░░░░░░ 32%  │   │  ← barra gold (ou red-soft)
│  │                          │   │
│  │  GAP: 46 pontos          │   │  ← destaque dramático
│  └─────────────────────────┘   │
│                                 │
│  "Você entende muito mais       │
│   do que consegue falar."       │  ← frase de impacto
│                                 │
│                                 │
│  SEÇÃO 2: OS 3 ERROS            │
│  ─────────────────────          │
│                                 │
│  "Por que você trava"           │  ← Inter 900 24px
│                                 │
│  ┌─ Erro 1 ─────────────────┐  │
│  │ 🔴 Tradução Mental        │  │  ← cream card
│  │ Você pensa em português...│  │
│  └───────────────────────────┘  │
│                                 │
│  ┌─ Erro 2 ─────────────────┐  │
│  │ 🔴 Estudo Passivo         │  │
│  │ Você consome mas não...   │  │
│  └───────────────────────────┘  │
│                                 │
│  ┌─ Erro 3 ─────────────────┐  │
│  │ 🔴 Falta de Estrutura     │  │
│  │ Sem um método que...      │  │
│  └───────────────────────────┘  │
│                                 │
│                                 │
│  SEÇÃO 3: SOLUÇÃO + CAPTURA    │
│  ─────────────────────          │
│                                 │
│  ┌───────────────────────────┐ │
│  │                            │ │
│  │  [Foto Ale redonda 80px]  │ │
│  │                            │ │
│  │  "Eu criei um manual      │ │  ← Caveat 20px
│  │   gratuito que explica    │ │
│  │   como destravar o        │ │
│  │   seu espanhol."          │ │
│  │                            │ │
│  │       — Ale               │ │  ← assinatura Caveat gold
│  │                            │ │
│  │  📘 Manual do Método      │ │
│  │  Espanhol com Você        │ │
│  │                            │ │
│  │  ┌──────────────────────┐ │ │
│  │  │ seu@email.com        │ │ │
│  │  └──────────────────────┘ │ │
│  │                            │ │
│  │  ┌──────────────────────┐ │ │
│  │  │ RECEBER MEU MANUAL   │ │ │
│  │  │ GRATUITO   →         │ │ │
│  │  └──────────────────────┘ │ │
│  │                            │ │
│  │  🔒 Seu email está seguro │ │
│  │  Enviamos apenas o manual │ │
│  │                            │ │
│  └───────────────────────────┘ │
│                                 │
│  +2.847 pessoas já baixaram    │  ← social proof
│                                 │
│  ┌───────────────────────────┐ │
│  │ Compartilhar resultado 📤│ │  ← botão share (secundário)
│  └───────────────────────────┘ │
│                                 │
└─────────────────────────────────┘
```

### 4.3 Barras de Diagnóstico (Compreensão vs Produção)

O elemento mais impactante da página. Deve ser dramático.

```css
.diagnostic-container {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 28px 24px;
  margin: 24px 0;
}

.diagnostic-label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.diagnostic-value {
  font-weight: 800;
  font-size: 24px;
}

.diagnostic-value.comprehension {
  color: #38bdf8;
}

.diagnostic-value.production {
  color: #fbbf24;
}

.bar-track {
  width: 100%;
  height: 14px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 7px;
  overflow: hidden;
  margin-bottom: 24px;
}

.bar-fill {
  height: 100%;
  border-radius: 7px;
  transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.bar-fill.comprehension {
  background: linear-gradient(90deg, #38bdf8, #0ea5e9);
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.3);
}

.bar-fill.production {
  background: linear-gradient(90deg, #fbbf24, #f59e0b);
  box-shadow: 0 0 12px rgba(251, 191, 36, 0.3);
}

/* Gap indicator */
.gap-indicator {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.gap-label {
  font-family: 'Caveat', cursive;
  font-size: 18px;
  color: #94a3b8;
}

.gap-value {
  font-family: 'Inter', sans-serif;
  font-weight: 900;
  font-size: 48px;
  background: linear-gradient(135deg, #fbbf24, #ef4444);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}

.gap-unit {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  color: #94a3b8;
  margin-top: 4px;
}
```

**Animação das barras:** As barras começam em 0% e animam até o valor final com um delay staggered:
- Barra de compreensão: delay 0.3s, duração 1.5s
- Barra de produção: delay 1s, duração 1.5s
- Gap value: fade in após ambas as barras terminarem (delay 2.5s)

Isso cria o efeito dramático: primeiro o usuário vê a compreensão alta, depois a produção baixa... e então o GAP aparece.

### 4.4 Cards dos 3 Erros

Estilo "cream paper" inspirado na referência @mariadurancontent — cards claros sobre fundo escuro para contraste máximo.

```css
.error-card {
  background: linear-gradient(135deg, #fef9ef 0%, #fdf6e3 100%);
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
  /* Reveal animation triggered by scroll */
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.error-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.error-card:nth-child(1) { transition-delay: 0s; }
.error-card:nth-child(2) { transition-delay: 0.15s; }
.error-card:nth-child(3) { transition-delay: 0.3s; }

.error-number {
  font-family: 'Inter', sans-serif;
  font-weight: 900;
  font-size: 48px;
  color: rgba(10, 22, 40, 0.06);
  position: absolute;
  top: 12px;
  right: 16px;
  line-height: 1;
}

.error-label {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #ef4444;
  margin-bottom: 6px;
}

.error-title {
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 18px;
  color: #0a1628;
  margin-bottom: 10px;
  line-height: 1.3;
}

.error-description {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  font-size: 14px;
  color: #374151;
  line-height: 1.6;
}

.error-description strong {
  color: #0a1628;
  font-weight: 700;
}
```

### 4.5 Conteúdo Personalizado por Avatar

Baseado nas respostas do Ato 3 (objetivo, tempo de estudo, disponibilidade), o resultado mostra variações:

- **Avatar "Viajante":** foco em situações práticas, frase personalizada menciona viagens
- **Avatar "Profissional":** foco em reuniões e emails, linguagem mais formal
- **Avatar "Estudante":** foco em provas e certificação
- **Avatar "Apaixonado":** foco em consumir mídia, séries, música

Implementação visual: um badge/tag no topo do resultado:

```css
.avatar-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 100px;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 16px;
}

.avatar-badge.viajante {
  background: rgba(56, 189, 248, 0.1);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.2);
}

.avatar-badge.profissional {
  background: rgba(251, 191, 36, 0.1);
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.2);
}

.avatar-badge.estudante {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.avatar-badge.apaixonado {
  background: rgba(168, 85, 247, 0.1);
  color: #a855f7;
  border: 1px solid rgba(168, 85, 247, 0.2);
}
```

### 4.6 Seção de Captura de Email

Deve parecer **continuação natural** do diagnóstico, não um portão. A Ale está "oferecendo ajuda", não "pedindo dados".

```css
.capture-section {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(251, 191, 36, 0.12);
  border-radius: 24px;
  padding: 32px 24px;
  text-align: center;
  margin: 32px 0;
  position: relative;
}

/* Glow sutil dourado ao redor */
.capture-section::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 24px;
  background: linear-gradient(135deg,
    rgba(251, 191, 36, 0.15),
    transparent 40%,
    transparent 60%,
    rgba(251, 191, 36, 0.1));
  z-index: -1;
  filter: blur(1px);
}

.ale-photo-small {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 2px solid rgba(251, 191, 36, 0.3);
  object-fit: cover;
  margin-bottom: 16px;
}

.capture-quote {
  font-family: 'Caveat', cursive;
  font-size: 20px;
  color: #ffffff;
  line-height: 1.5;
  margin-bottom: 8px;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}

.capture-signature {
  font-family: 'Caveat', cursive;
  font-size: 18px;
  color: #fbbf24;
  margin-bottom: 24px;
}

.email-input {
  width: 100%;
  max-width: 320px;
  height: 52px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 14px;
  padding: 0 18px;
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  color: #ffffff;
  outline: none;
  transition: all 0.2s ease;
  margin-bottom: 12px;
}

.email-input::placeholder {
  color: #475569;
}

.email-input:focus {
  border-color: rgba(251, 191, 36, 0.4);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.08);
}

.capture-cta {
  width: 100%;
  max-width: 320px;
  height: 52px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #0a1628;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 15px;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  box-shadow:
    0 0 20px rgba(251, 191, 36, 0.25),
    0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.capture-cta:hover {
  transform: translateY(-2px);
  box-shadow:
    0 0 30px rgba(251, 191, 36, 0.4),
    0 8px 20px rgba(0, 0, 0, 0.3);
}

.capture-privacy {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 12px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  color: #94a3b8;
}

.capture-privacy svg {
  width: 14px;
  height: 14px;
  color: #94a3b8;
}
```

### 4.7 Micro Social Proof

```css
.social-proof {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  color: #94a3b8;
}

/* Mini avatares empilhados */
.social-proof-avatars {
  display: flex;
  margin-right: 4px;
}

.social-proof-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #0a1628;
  margin-left: -8px;
  object-fit: cover;
}

.social-proof-avatar:first-child {
  margin-left: 0;
}

.social-proof-count {
  font-weight: 700;
  color: #fbbf24;
}
```

### 4.8 Assinatura da Ale no Resultado

```css
.ale-signature {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
  padding: 12px 0;
}

.ale-signature-photo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1.5px solid rgba(251, 191, 36, 0.3);
  object-fit: cover;
}

.ale-signature-text {
  font-family: 'Caveat', cursive;
  font-size: 22px;
  color: #fbbf24;
}
```

---

## 5. RESPONSIVO & MOBILE

### 5.1 Breakpoints

```css
/* Mobile first — design base é mobile */
/* Tablet */
@media (min-width: 640px) { ... }
/* Desktop */
@media (min-width: 1024px) { ... }
```

### 5.2 Container Principal

```css
.quiz-container {
  width: 100%;
  max-width: 480px;  /* nunca mais largo que isso, mesmo em desktop */
  margin: 0 auto;
  padding: 0 20px;
}

/* No desktop, centralizar verticalmente o quiz numa janela */
@media (min-width: 1024px) {
  .quiz-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #070e1a; /* um tom ainda mais escuro atrás */
  }

  .quiz-container {
    background: #0a1628;
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    max-height: 90vh;
    overflow-y: auto;
    padding: 0 32px;
  }
}
```

### 5.3 Touch-Friendly Tap Targets

```css
/* Mínimo 48px para todos os elementos clicáveis (WCAG) */
.option-card {
  min-height: 52px; /* acima do mínimo */
  padding: 16px 20px;
}

.cta-primary,
.capture-cta,
.feedback-next-btn {
  min-height: 48px;
}

/* Área de toque expandida para elementos pequenos */
.audio-play-btn {
  min-width: 44px;
  min-height: 44px;
}
```

### 5.4 Thumb Zone

O quiz prioriza a "zona do polegar" — a área inferior da tela onde o polegar alcança naturalmente.

```
┌─────────────────────────┐
│                         │
│    PERGUNTA             │  ← zona de leitura (topo)
│    (só texto)           │
│                         │
│─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│
│                         │
│    OPÇÕES               │  ← zona de interação (meio-inferior)
│    (clicáveis)          │
│                         │
│    [ PRÓXIMA → ]        │  ← zona do polegar (inferior)
│                         │
└─────────────────────────┘
```

Regra: **nenhum botão de ação primária deve ficar no topo 40% da tela no mobile.**

### 5.5 Swipe — Não Implementar

Decisão de design: NÃO usar swipe para navegar entre perguntas. Motivos:
- O quiz tem feedback inline que precisa ser lido antes de avançar
- Swipe acidental pode pular conteúdo educativo
- O botão "Próxima →" cria um micro-compromisso intencional

### 5.6 Audio no Mobile

- Botão play grande (44px), fácil de tocar
- Auto-play PROIBIDO (browsers bloqueiam)
- Mostrar texto "Toque para ouvir" na primeira pergunta com áudio
- Waveform simplificada (só a barra de progresso, sem waveform visual complexa)
- Ao tocar play: ícone muda para pause, barra progride
- Se a pergunta tem áudio, as opções aparecem com opacity 0.5 até o áudio ser tocado pelo menos uma vez, com label: "Ouça o áudio para responder"

```css
.options-locked {
  opacity: 0.5;
  pointer-events: none;
  position: relative;
}

.options-locked::before {
  content: '🎧 Ouça o áudio para responder';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: #fbbf24;
  background: rgba(10, 22, 40, 0.9);
  padding: 10px 20px;
  border-radius: 10px;
  white-space: nowrap;
  z-index: 1;
}
```

### 5.7 Scroll na Página de Resultado

A página de resultado é a ÚNICA tela com scroll. Todas as perguntas são paginadas (uma por tela, sem scroll).

```css
/* Resultado: scroll suave */
.result-page {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
}

/* Scroll snap suave nas seções */
.result-section {
  scroll-margin-top: 24px; /* para links âncora */
}
```

---

## 6. MICRO-INTERAÇÕES & ANIMAÇÕES

### 6.1 Hover/Tap em Botões

```css
/* Desktop hover */
@media (hover: hover) {
  .option-card:hover {
    background: rgba(255, 255, 255, 0.07);
    border-color: rgba(251, 191, 36, 0.2);
    transform: translateX(4px);
    transition: all 0.2s ease;
  }
}

/* Mobile tap — usar :active em vez de :hover */
.option-card:active {
  background: rgba(251, 191, 36, 0.08);
  transform: scale(0.98);
  transition: all 0.1s ease;
}
```

### 6.2 Seleção de Resposta

Ao selecionar uma opção:

1. **Imediato (0ms):** opção selecionada ganha borda gold, letra ganha fundo gold
2. **50ms:** outras opções ficam com `opacity: 0.5` e `pointer-events: none`
3. **300ms:** se Ato 1/2, card de feedback aparece com slide-up (Ato 3: avança direto)
4. **Botão "Próxima →"** aparece dentro do feedback card

```javascript
// Timing de seleção
const OPTION_SELECT_DELAY = 0;        // highlight imediato
const OTHER_OPTIONS_FADE = 50;         // fade das outras opções
const FEEDBACK_APPEAR = 300;           // feedback slide-up
const AUTO_SCROLL_TO_FEEDBACK = 400;   // scroll suave até feedback visível
```

### 6.3 Barra de Progresso

```css
.progress-bar-fill {
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Pulse sutil quando avança */
@keyframes progressPulse {
  0% { box-shadow: 0 0 8px currentColor; }
  50% { box-shadow: 0 0 16px currentColor; }
  100% { box-shadow: 0 0 8px currentColor; }
}

.progress-bar-fill.advancing {
  animation: progressPulse 0.6s ease;
}
```

### 6.4 Transição entre Perguntas

Já detalhado em 3.7. Resumo do timing:

| Etapa | Duração | Easing |
|-------|---------|--------|
| Pergunta atual fade-out + slide-left | 300ms | ease-in |
| Gap entre perguntas | 150ms | — |
| Nova pergunta fade-in + slide-right | 400ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Opções stagger-in | 100ms cada | ease-out |

As opções da nova pergunta aparecem com stagger:
```css
.option-card:nth-child(1) { animation-delay: 0.45s; }
.option-card:nth-child(2) { animation-delay: 0.55s; }
.option-card:nth-child(3) { animation-delay: 0.65s; }
.option-card:nth-child(4) { animation-delay: 0.75s; }

.option-card {
  animation: optionIn 0.3s ease-out forwards;
  opacity: 0;
  transform: translateY(12px);
}

@keyframes optionIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 6.5 Loading do Resultado

Detalhado em 4.1.

### 6.6 Scroll-Triggered Reveals no Resultado

Usar Intersection Observer para revelar seções conforme scroll:

```javascript
const observerOptions = {
  threshold: 0.2,
  rootMargin: '0px 0px -50px 0px'
};

// Cada .result-section começa com:
// opacity: 0; transform: translateY(30px);
// Ao entrar no viewport, adiciona classe .visible
```

```css
.result-section {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.result-section.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger nos error cards dentro de uma seção */
.result-section.visible .error-card:nth-child(1) { transition-delay: 0s; }
.result-section.visible .error-card:nth-child(2) { transition-delay: 0.15s; }
.result-section.visible .error-card:nth-child(3) { transition-delay: 0.3s; }
```

### 6.7 Animação das Barras de Diagnóstico

As barras animam quando entram no viewport (não no page load):

```javascript
// Quando a seção de diagnóstico fica visível:
// 1. Barra de compreensão cresce de 0% até valor (1.5s, delay 0.3s)
// 2. Barra de produção cresce de 0% até valor (1.5s, delay 1.0s)
// 3. Número do GAP faz count-up de 0 até valor (0.8s, delay 2.5s)
// 4. Frase de impacto fade-in (0.5s, delay 3.5s)
```

```css
.bar-fill {
  width: 0%;
  transition: width 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.bar-fill.animate {
  /* width é setado via JS inline style */
}

.gap-value {
  opacity: 0;
  transform: scale(0.5);
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.gap-value.visible {
  opacity: 1;
  transform: scale(1);
}
```

---

## 7. TÉCNICAS CSS ESPECÍFICAS

### 7.1 Gold Glow Effect

Usado em headlines, botões, e elementos de destaque.

```css
/* Glow em texto */
.gold-glow-text {
  color: #fbbf24;
  text-shadow:
    0 0 10px rgba(251, 191, 36, 0.3),
    0 0 30px rgba(251, 191, 36, 0.1);
}

/* Glow em boxes/cards */
.gold-glow-box {
  box-shadow:
    0 0 15px rgba(251, 191, 36, 0.1),
    0 0 30px rgba(251, 191, 36, 0.05),
    inset 0 1px 0 rgba(251, 191, 36, 0.08);
}

/* Glow pulsante para CTAs */
@keyframes goldPulse {
  0%, 100% {
    box-shadow:
      0 0 20px rgba(251, 191, 36, 0.2),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }
  50% {
    box-shadow:
      0 0 30px rgba(251, 191, 36, 0.35),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }
}

/* Halo radial dourado (fundo decorativo) */
.gold-radial {
  background: radial-gradient(
    ellipse at center,
    rgba(251, 191, 36, 0.08) 0%,
    transparent 60%
  );
}
```

### 7.2 Glass-Morphism para Cards

```css
.glass-card {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
}

/* Variante com borda luminosa no topo */
.glass-card-lit {
  background: rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
```

### 7.3 Text Shadow e Glow para Headlines

```css
.headline-primary {
  font-family: 'Inter', sans-serif;
  font-weight: 900;
  color: #ffffff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.headline-gold-word {
  color: #fbbf24;
  text-shadow:
    0 0 10px rgba(251, 191, 36, 0.3),
    0 2px 10px rgba(0, 0, 0, 0.3);
}

/* Palavras emocionais em Caveat */
.emotional-word {
  font-family: 'Caveat', cursive;
  color: #fbbf24;
  font-size: 1.15em; /* ligeiramente maior que o texto ao redor */
  display: inline;
}
```

### 7.4 Background Navy com Vida

O fundo `#0a1628` precisa parecer vivo, não um bloco flat. Técnicas:

```css
body {
  background: #0a1628;
}

/* Camada 1: Gradient vertical sutil */
.quiz-bg {
  background: linear-gradient(
    180deg,
    #0a1628 0%,
    #0d1b30 30%,
    #0a1628 70%,
    #080f1f 100%
  );
}

/* Camada 2: Noise texture (muito sutil, 2-3% opacity) */
.quiz-bg::after {
  content: '';
  position: fixed;
  inset: 0;
  opacity: 0.025;
  pointer-events: none;
  /* Inline SVG noise ou imagem de 200x200 tiled */
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
  background-size: 256px 256px;
}

/* Camada 3: Orbs de luz sutis (posicionados atrás do conteúdo) */
.light-orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}

.light-orb-gold {
  width: 300px;
  height: 300px;
  background: rgba(251, 191, 36, 0.03);
  top: 20%;
  right: -100px;
}

.light-orb-blue {
  width: 250px;
  height: 250px;
  background: rgba(56, 189, 248, 0.02);
  bottom: 30%;
  left: -80px;
}
```

### 7.5 Gradient de Transição entre Atos

Na transição do Ato 1 para o Ato 2, o background muda suavemente:

```css
.quiz-bg {
  transition: background 1s ease;
}

.quiz-bg.act-1 {
  background: linear-gradient(180deg, #0a1628 0%, #10192d 50%, #0a1628 100%);
}

.quiz-bg.act-2 {
  background: linear-gradient(180deg, #0a1628 0%, #0b1a33 50%, #0a1628 100%);
}

.quiz-bg.act-3 {
  background: linear-gradient(180deg, #0a1628 0%, #0d1b2a 50%, #0a1628 100%);
}
```

---

## 8. ESPECIFICAÇÕES DE COMPONENTES

### 8.1 Escala Tipográfica

| Elemento | Mobile | Desktop | Weight | Font |
|----------|--------|---------|--------|------|
| Headline principal (intro) | 28px / 36px lh | 42px / 50px lh | 900 | Inter |
| Headline seção (resultado) | 24px / 32px lh | 32px / 40px lh | 900 | Inter |
| Texto pergunta | 20px / 28px lh | 22px / 30px lh | 700 | Inter |
| Texto opção | 15px / 22px lh | 16px / 24px lh | 500 | Inter |
| Texto feedback | 15px / 24px lh | 15px / 24px lh | 400 | Inter |
| Label/tag | 13px / 18px lh | 13px / 18px lh | 600-700 | Inter |
| Label Caveat | 18px / 24px lh | 20px / 26px lh | 400 | Caveat |
| Texto de apoio/trust | 13px / 18px lh | 13px / 18px lh | 400 | Inter |
| Botão CTA | 15-16px | 16px | 800 | Inter |
| Número GAP | 48px / 52px lh | 56px / 60px lh | 900 | Inter |

### 8.2 Sistema de Espaçamento

Base: 4px grid.

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 28px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
}
```

**Uso padrão:**
- Padding de página: `20px` (mobile), `32px` (desktop)
- Gap entre opções de resposta: `10px`
- Gap entre seções do resultado: `40px`
- Margem entre label e pergunta: `8px`
- Margem entre pergunta e opções: `20px`
- Padding interno de cards: `20px-24px`

### 8.3 Border Radius

```css
:root {
  --radius-sm: 8px;     /* pequenos elementos inline */
  --radius-md: 12px;    /* botões, inputs */
  --radius-lg: 14px;    /* option cards, feedback cards */
  --radius-xl: 16px;    /* CTAs grandes */
  --radius-2xl: 20px;   /* question cards, result cards */
  --radius-3xl: 24px;   /* container principal desktop, capture section */
  --radius-full: 9999px; /* badges, pills, avatares */
}
```

### 8.4 Sombras

```css
:root {
  /* Elevação nível 1 — cards sutis */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.15);

  /* Elevação nível 2 — cards destacados */
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.2);

  /* Elevação nível 3 — modais, container desktop */
  --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.3);

  /* Elevação especial — CTAs com glow */
  --shadow-gold: 0 0 20px rgba(251, 191, 36, 0.25), 0 4px 12px rgba(0, 0, 0, 0.2);

  /* Elevação especial — sky blue glow */
  --shadow-sky: 0 0 15px rgba(56, 189, 248, 0.2), 0 4px 12px rgba(0, 0, 0, 0.2);
}
```

### 8.5 Botões — Todos os Estilos

```css
/* PRIMARY — CTA principal (fundo dourado, texto escuro) */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 52px;
  padding: 0 28px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #0a1628;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 15px;
  letter-spacing: 0.3px;
  text-transform: uppercase;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  box-shadow: var(--shadow-gold);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* SECONDARY — ações secundárias (outline gold) */
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 48px;
  padding: 0 24px;
  background: transparent;
  color: #fbbf24;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: rgba(251, 191, 36, 0.08);
  border-color: rgba(251, 191, 36, 0.5);
}

/* GHOST — ações terciárias (sem borda) */
.btn-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 44px;
  padding: 0 16px;
  background: transparent;
  color: #94a3b8;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-ghost:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

/* FEEDBACK NEXT — botão dentro do feedback card */
.btn-feedback-next {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 12px 24px;
  background: rgba(251, 191, 36, 0.12);
  border: 1px solid rgba(251, 191, 36, 0.25);
  border-radius: 12px;
  color: #fbbf24;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-feedback-next:hover {
  background: rgba(251, 191, 36, 0.2);
  transform: translateX(4px);
}

.btn-feedback-next svg {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.btn-feedback-next:hover svg {
  transform: translateX(4px);
}
```

### 8.6 Cards — Todos os Estilos

```css
/* QUESTION CARD — contém a pergunta */
.card-question {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 24px 20px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* FEEDBACK CARD — aparece após responder */
.card-feedback {
  border-radius: 16px;
  padding: 20px;
  margin-top: 16px;
  border-left-width: 3px;
  border-left-style: solid;
}

/* RESULT CARD — seções do resultado */
.card-result {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 20px;
  padding: 28px 24px;
}

/* ERROR CARD — cards cream dos 3 erros */
.card-error {
  background: linear-gradient(135deg, #fef9ef 0%, #fdf6e3 100%);
  border-radius: 18px;
  padding: 24px;
  color: #0a1628;
}

/* CAPTURE CARD — seção de email */
.card-capture {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(251, 191, 36, 0.12);
  border-radius: 24px;
  padding: 32px 24px;
  text-align: center;
}
```

### 8.7 CSS Custom Properties — Resumo Completo

```css
:root {
  /* Colors */
  --color-navy-900: #0a1628;
  --color-navy-800: #111d32;
  --color-navy-700: #1a2740;
  --color-gold: #fbbf24;
  --color-gold-dark: #f59e0b;
  --color-sky: #38bdf8;
  --color-sky-dark: #0ea5e9;
  --color-emerald: #10b981;
  --color-emerald-dark: #059669;
  --color-white: #ffffff;
  --color-slate-200: #e2e8f0;
  --color-slate-400: #94a3b8;
  --color-slate-500: #64748b;
  --color-slate-600: #475569;
  --color-red: #ef4444;

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-hand: 'Caveat', cursive;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-7: 28px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 14px;
  --radius-xl: 16px;
  --radius-2xl: 20px;
  --radius-3xl: 24px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.15);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.2);
  --shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.3);
  --shadow-gold: 0 0 20px rgba(251, 191, 36, 0.25), 0 4px 12px rgba(0, 0, 0, 0.2);

  /* Transitions */
  --ease-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 600ms;

  /* Z-index scale */
  --z-bg: 0;
  --z-content: 1;
  --z-feedback: 10;
  --z-progress: 20;
  --z-transition-overlay: 50;
  --z-loading: 100;
}
```

---

## CHECKLIST DE IMPLEMENTAÇÃO

Antes de entregar, verificar:

- [ ] Fontes carregadas: Inter (400, 500, 600, 700, 800, 900) + Caveat (400, 700)
- [ ] Ícones: Lucide Icons via CDN ou SVG inline
- [ ] Todas as cores usadas estão na paleta aprovada
- [ ] Nenhuma instância de `#ff421c` ou `#36c551`
- [ ] Todos os tap targets >= 44px no mobile
- [ ] Animações respeitam `prefers-reduced-motion`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
- [ ] `100dvh` usado em vez de `100vh` para telas full-height no mobile
- [ ] Fotos da Ale em WebP, max 400px, lazy loaded
- [ ] Audio player funciona no iOS Safari (não auto-play)
- [ ] Meta viewport correta: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`
- [ ] Performance: todas as animações usam `transform` e `opacity` (GPU-accelerated)
- [ ] Sem layout shifts durante animações (tamanhos definidos previamente)
- [ ] Favicon e OG tags para compartilhamento

---

*Brief gerado para Espanhol com Você — Março 2026*
*Para ser implementado em HTML/CSS/JS como single-page application.*
