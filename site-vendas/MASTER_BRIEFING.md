# MASTER BRIEFING — site-vendas/

## PRODUTO
Nome: Programa Imersão Nativa®
Versão: completa (app exclusivo 5 módulos + suporte WhatsApp 24h)
Jornada: 24 semanas — A1 ao C1
Preço âncora: R$1.497 | Com cupom: R$497
Garantia: 7 dias incondicional
Bônus: Pronúncia dos Sonhos + Ritmo Espanhol + Expressões Nativas
Plataforma de pagamento: Hotmart

## VOZ DA ALE
Tom: amiga nativa, direta, próxima — NUNCA professora distante
NUNCA usar: "Incrível", "Fácil", "Simples assim", "Fluente em 30 dias", tom formal
SEMPRE usar: "No espanhol real...", "Você trava porque...", "Como um nativo fala...", "O problema não é você, é o método"
REGRA TIPOGRÁFICA: NUNCA usar travessão longo (—) em nenhum texto do site. Substituir sempre por vírgula ou ponto. Humanos não usam isso na escrita natural.

## DESIGN — PADRÃO OBRIGATÓRIO
Referência visual: Módulo 1 (100% aprovado) e Módulo 6 (80% aprovado)
Paleta do site:
- Navy: #0a1628 (fundo — SEMPRE com camada de luz/gradiente, NUNCA sólido puro)
- Gold: #fbbf24 (destaques, CTAs secundários)
- Sky: #38bdf8 (elementos de info, bordas)
- Emerald: #10b981 (sucesso, checkmarks)
- Texto: #ffffff

REGRAS DE DESIGN:
- Módulo 1 (Hero): NÃO ALTERAR — aprovado 100%
- Módulo 6 (Mecanismo): NÃO ALTERAR design — só melhorar copy
- Módulos 02 a 13 (exceto 01 e 06): cada módulo deve ter sua própria cor de fundo
- O DESIGN_AGENT deve propor uma paleta de fundos variados para os 11 módulos restantes
- Regra geral de fundo: pode ser escuro (#0a1628 com gradiente) OU claro/médio
- Fundos claros permitidos: tons creme, off-white quente, azul muito claro, bege suave
- NUNCA fundo branco puro nem preto puro
- Sempre que o fundo for escuro: obrigatório ter camada de luz/gradiente sobre ele
- Sempre que o fundo for claro: garantir contraste suficiente para leitura
- Objetivo: página premium, leve, com ritmo visual — alternando escuro/claro/escuro
- Efeito LED/brilho nos elementos de destaque em TODOS os módulos
- Animação ponto piscante nos eyebrow tags em TODOS os módulos
- Botão CTA padrão: gradiente gold (#fbbf24) para laranja (#fb923c), texto navy, border-radius 50px
- Mobile-first, breakpoint 768px
- Fonte: Inter (900 headline / 400 body)

## AVATARES (prioridade)
1. Viajante — entende mas trava na fala, depende do tradutor
2. Vai morar fora — medo de se sentir perdido, não pertencer
3. Profissional — competente na área mas trava em reuniões em espanhol

## PROVAS SOCIAIS REAIS (usar no copy)
- Viajou sozinha sem tradutor
- 3 meses no Peru já falava
- Aposentada fluente em 6 meses
- Reuniões internacionais em 3 meses
- Eliane, 75 anos, foi morar na Espanha
- Wanderlei — 2 semanas, reuniões pararam de trocar pro inglês

## MÓDULOS DO SITE (ordem da página)
01 - Hero ← APROVADO 100%, não alterar design, só revisar copy se necessário
02 - Depoimentos Parte 1
03 - Dores / Identificação
04 - Objeções
05 - Comparativo
06 - 3 Pilares / Intro (eyebrow + título + subtítulo) ← APROVADO 80%, referência visual
06B - Pilar 1 Jornada (abas A1→C1) ← NÃO alterar design, só copy
06C - Pilar 2 App (5 funcionalidades do app) ← NÃO alterar design, só copy
06D - Pilar 3 Suporte (WhatsApp + IA 24h) ← NÃO alterar design, só copy
07 - Depoimentos de Transformação
08 - Quem Sou Eu
09 - Depoimentos Finais
10 - Bônus
11 - Preço
12 - Garantia
13 - FAQ

## REGRA PARA OS MÓDULOS 02 a 13 (exceto 01 e 06)
Padronizar design seguindo o padrão visual do Módulo 1 e Módulo 6.
Revisar copy seguindo a voz da Ale e os avatares acima.
NÃO alterar o design do Módulo 1.
Melhorar o copy do Módulo 6 mantendo seu design.

---

## HISTÓRICO DE ALTERAÇÕES

### 2026-03-21 — Paleta de fundos aprovada e aplicada

**O que foi feito:** Aplicação do ritmo visual completo na página, alternando fundos escuros e claros em todos os módulos (exceto 01, 06, 06B, 06C, 06D que não foram alterados).

**Módulos NÃO alterados (design protegido):**
- 01 Hero (aprovado 100%)
- 06 Mecanismo (aprovado 80%)
- 06B Pilar 1, 06C Pilar 2, 06D Pilar 3

**Módulos com fundo CLARO (aplicados):**
| Módulo | Fundo | Cor |
|--------|-------|-----|
| 02 Depoimentos 1 | Branco quente | `#fafaf8` |
| 04 Objeções | Cinza azulado claro | `#f0f4f8` |
| 07 Depoimentos Transformação | Creme quente | `#f5f0e8` |
| 09 Depoimentos Finais | Branco quente | `#fafaf8` |
| 12 Garantia | Verde muito suave | `#f0faf4` |
| 13 FAQ | Neutro quente | `#f5f5f0` |

Regras aplicadas nos claros:
- Texto principal: `#0a1628`
- Destaques: `#fbbf24` ou `#0090be`
- Eyebrow tag com ponto piscante animado
- CTA: gradiente `#fbbf24` → `#fb923c`, texto `#0a1628`, border-radius 50px
- Blobs decorativos sutis (radial-gradient) via ::before/::after

**Módulos com fundo ESCURO (aplicados):**
| Módulo | Fundo base | Gradiente |
|--------|-----------|-----------|
| 03 Dores | `#0a1628` | Blobs vermelho/rose (tensão emocional) |
| 05 Comparativo | `#0a1628` | Blobs sky/gold + LED glow no card destaque |
| 08 Quem Sou Eu | `#0a1628` | Blobs gold/orange (premium dourado) |
| 10 Bônus | `#0a1628` | Blobs emerald/gold (premium) |
| 11 Preço | `#0a1628` | Blobs gold intenso + glass-morphism (zona de decisão) |

Regras aplicadas nos escuros:
- SEMPRE gradiente radial ou blob de brilho (nunca sólido puro)
- Efeito LED nos elementos de destaque
- Texto: `#ffffff`
- Eyebrow tag com ponto piscante animado
- CTA: gradiente `#fbbf24` → `#fb923c`, texto `#0a1628`, border-radius 50px

**Ritmo visual da página (de cima pra baixo):**
01 escuro → 02 claro → 03 escuro → 04 claro → 05 escuro → 06/06B/06C/06D (existente) → 07 claro → 08 escuro → 09 claro → 10 escuro → 11 escuro → 12 claro → 13 claro
