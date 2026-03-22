# RELATÓRIO DE TESTE E2E — Quiz Espanhol com Você
**Data:** 2026-03-20 14:10
**Browser:** Microsoft Edge (Selenium)
**Viewport:** 414x896 (mobile)

---

## Resultado: 60/60 testes passaram ✅

| # | Teste | Status | Detalhe |
|---|-------|--------|---------|
| 1 | Página carregou sem erro | ✅ PASS | Title: Quiz — Espanhol com Você |
| 2 | Intro screen ativa | ✅ PASS |  |
| 3 | Botão CTA visível | ✅ PASS |  |
| 4 | Question screen oculta | ✅ PASS |  |
| 5 | Zero erros JS no carregamento | ✅ PASS |  |
| 6 | Question screen ativou após clicar CTA | ✅ PASS |  |
| 7 | Intro screen desativou | ✅ PASS |  |
| 8 | Pergunta 1 carregou | ✅ PASS | Texto: O que aconteceu com o gato?... |
| 9 | Progresso mostra 1/10 | ✅ PASS | Mostra: 1 / 10 |
| 10 | Q1: Opções renderizaram | ✅ PASS |  |
| 11 | Q1: Feedback apareceu | ✅ PASS |  |
| 12 | Q1: Feedback tem conteúdo | ✅ PASS | Texto: Muito bem! 👏
Voce entendeu "se escapo" pelo contexto. E apre... |
| 13 | Q1: Botão próxima funciona | ✅ PASS |  |
| 14 | Q2: Pergunta carregou | ✅ PASS | Texto: Um brasileiro na Espanha diz:
"Estoy embarazado po... |
| 15 | Q2: Selecionar opção | ✅ PASS |  |
| 16 | Q2: Feedback apareceu | ✅ PASS |  |
| 17 | Q2: Avançar | ✅ PASS |  |
| 18 | Q3: Pergunta carregou | ✅ PASS | Texto: "Quedarse de piedra" significa:... |
| 19 | Q3: Selecionar opção | ✅ PASS |  |
| 20 | Q3: Feedback apareceu | ✅ PASS |  |
| 21 | Q3: Avançar (deve ir para transição) | ✅ PASS |  |
| 22 | Transition screen ativa | ✅ PASS |  |
| 23 | Auto-avançou para Ato 2 | ✅ PASS |  |
| 24 | Q4: Pergunta carregou | ✅ PASS | Texto: Como voce diria em espanhol:
"Eu estava a toa em c... |
| 25 | Ato mudou para 2 | ✅ PASS | data-act=2 |
| 26 | Q4: Selecionar opção | ✅ PASS |  |
| 27 | Q4: Feedback apareceu | ✅ PASS |  |
| 28 | Q4: Avançar | ✅ PASS |  |
| 29 | Q5: Selecionar opção | ✅ PASS |  |
| 30 | Q5: Feedback apareceu | ✅ PASS |  |
| 31 | Q5: Avançar | ✅ PASS |  |
| 32 | Q6: Pergunta carregou | ✅ PASS | Texto: Alguem te para na rua e fala rapido:
"Oye, disculp... |
| 33 | Q6: Selecionar opção | ✅ PASS |  |
| 34 | Q6: Feedback apareceu | ✅ PASS |  |
| 35 | Q6: Avançar | ✅ PASS |  |
| 36 | Q7: Selecionar opção | ✅ PASS |  |
| 37 | Q7: Feedback apareceu | ✅ PASS |  |
| 38 | Q7: Avançar | ✅ PASS |  |
| 39 | Q8: Pergunta carregou | ✅ PASS | Texto: Qual o principal motivo pra voce querer falar espa... |
| 40 | Ato mudou para 3 | ✅ PASS | data-act=3 |
| 41 | Q8: Selecionar opção | ✅ PASS |  |
| 42 | Q9: Avançou automaticamente | ✅ PASS | Texto: Ha quanto tempo voce tenta aprender espanhol?... |
| 43 | Q9: Selecionar opção | ✅ PASS |  |
| 44 | Q10: Avançou automaticamente | ✅ PASS | Texto: Quanto tempo por dia voce tem disponivel?... |
| 45 | Q10: Selecionar opção | ✅ PASS |  |
| 46 | Loading screen ativa | ✅ PASS |  |
| 47 | Loading tem texto rotativo | ✅ PASS | Texto: Analisando suas respostas... |
| 48 | Result screen carregou após loading | ✅ PASS |  |
| 49 | Compreensão calculada | ✅ PASS | Valor: B2 |
| 50 | Produção calculada | ✅ PASS | Valor: A2 |
| 51 | GAP calculado | ✅ PASS | Valor: 50% |
| 52 | Avatar badge preenchido | ✅ PASS | Avatar: A Viajante |
| 53 | Erro #1 preenchido | ✅ PASS | Titulo: Seu cerebro nao tem blocos prontos |
| 54 | Erro #2 preenchido | ✅ PASS | Titulo: A ordem foi invertida |
| 55 | Erro #3 preenchido | ✅ PASS | Titulo: Sem calibracao, nao ha progresso |
| 56 | Campo de email visível | ✅ PASS |  |
| 57 | Botão submit visível | ✅ PASS |  |
| 58 | Email inválido não avança | ✅ PASS |  |
| 59 | Thank you screen aparece com email válido | ✅ PASS |  |
| 60 | Zero erros JS durante todo o quiz | ✅ PASS |  |

---

## Erros JavaScript

Nenhum erro JS detectado. ✅

---

## Screenshots

- `01_intro.png`
- `02_question1.png`
- `03_q1_feedback.png`
- `04_q3_feedback.png`
- `05_transition.png`
- `06_act2.png`
- `07_act3.png`
- `08_loading.png`
- `09_result_top.png`
- `10_result_errors.png`
- `11_result_email.png`
- `12_thankyou.png`
- `99_final_state.png`

---

## Fluxo testado

1. Página carregou → intro screen ativa
2. Clicou CTA → question screen ativa, Q1 apareceu
3. Q1-Q3 (Ato 1): seleção → feedback → próxima ✓
4. Transição Act 1→2: tela apareceu, auto-avançou
5. Q4-Q7 (Ato 2): seleção → feedback → próxima ✓
6. Q8-Q10 (Ato 3): seleção → auto-avanço sem feedback ✓
7. Loading: texto rotativo, 4.5s, avançou para resultado
8. Resultado: barras, GAP, avatar, 3 erros preenchidos ✓
9. Email inválido: bloqueado ✓
10. Email válido: thank you screen ✓

---

*Teste gerado automaticamente — Espanhol com Você*
