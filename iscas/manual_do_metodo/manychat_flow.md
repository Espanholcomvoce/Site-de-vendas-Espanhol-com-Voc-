# ManyChat Flow — Manual do Metodo (Palavra-chave: MANUAL)

## Visao Geral

- **Trigger:** Palavra-chave `MANUAL` nos comentarios de qualquer post
- **Objetivo:** Capturar email, entregar o PDF "Manual do Metodo" (22 paginas) e iniciar sequencia de 5 emails que leva ao VSL (AULA)
- **Nivel de consciencia do lead:** Consciente da solucao (sabe que precisa de um metodo, ainda nao conhece o nosso)
- **Transicao:** Apos sequencia de emails, direciona para AULA (VSL)

---

## Fluxo Completo

### STEP 1 — Resposta Automatica no DM (imediata)

**Condicao:** Usuario comenta `MANUAL` em qualquer post.

**Mensagem do bot:**

```
Oi! 😊 Que bom que voce quer o Manual do Metodo!

Esse PDF tem 22 paginas com:
✅ Os 3 erros que travam o cerebro na hora de falar espanhol
✅ O mecanismo que destrava a fala de verdade
✅ O passo a passo do metodo que ja ajudou +2.000 alunos

Para eu te enviar, preciso do seu melhor email. Pode digitar aqui embaixo? 👇
```

**Acao tecnica:**
- Enviar mensagem via DM automatico
- Ativar campo de captura de email (User Input > Email)
- Timeout: 24 horas para resposta

---

### STEP 2 — Captura de Email e Aplicacao de Tags

**Condicao:** Usuario digita um email valido.

**Validacao:**
- Verificar formato de email valido (contem @ e dominio)
- Se formato invalido, enviar mensagem de erro (ver Tratamento de Erros abaixo)

**Tags aplicadas:**
- `lead_manual_metodo` — identifica a isca que gerou o lead
- `nivel_consciente_solucao` — nivel de consciencia no funil
- `origem_instagram` — canal de origem
- `lead_ativo` — status do lead
- Se houver tag de avatar de interacoes anteriores, manter (ex: `avatar_profissional`, `avatar_viajante`)

**Campos personalizados atualizados:**
- `email` — email capturado
- `isca_entrada` — "Manual do Metodo"
- `data_captura` — data atual
- `fonte_post_id` — ID do post onde comentou (se disponivel)

**Mensagem do bot:**

```
Perfeito! Ja estou enviando o Manual do Metodo para {email} 📩

Confere sua caixa de entrada (e o spam tambem, vai que ne 😅).

Nos proximos dias vou te mandar mais conteudos exclusivos por email que vao te ajudar a destravar seu espanhol. Fica de olho! 🔥
```

**Acao tecnica:**
- Salvar email no campo personalizado do ManyChat
- Aplicar todas as tags listadas
- Disparar integracao com Mailchimp (ver Step 3)

---

### STEP 3 — Integracao Mailchimp (envio do PDF + inicio da automacao)

**Acao:** Enviar dados do lead para Mailchimp via integracao nativa ou Zapier.

**Configuracao Mailchimp:**
- **Lista/Audiencia:** Leads Espanhol com Voce
- **Tag Mailchimp:** `manual_metodo`, `sequencia_manual_ativa`
- **Grupo:** Isca - Manual do Metodo
- **Merge Fields:**
  - `FNAME` — primeiro nome (do perfil Instagram)
  - `ISCA` — "Manual do Metodo"
  - `ORIGEM` — "Instagram"

**Email de boas-vindas (Dia 0) — enviado imediatamente:**

- **Assunto:** Seu Manual do Metodo esta aqui 📖
- **Conteudo:** Link para download do PDF + introducao breve da Ale
- **CTA do email:** "Baixe agora e leia a pagina 7 — la esta o erro que 90% dos brasileiros cometem"

---

### STEP 4 — Sequencia de 5 Emails (Automacao Mailchimp)

**Nome da automacao:** `SEQ_MANUAL_METODO_5_EMAILS`

| Dia | Assunto (sugestao) | Objetivo | CTA |
|-----|---------------------|----------|-----|
| Dia 0 | Seu Manual do Metodo esta aqui 📖 | Entregar o PDF, gerar primeira impressao | Baixar PDF |
| Dia 2 | O erro da pagina 7 — voce ja leu? | Reforcar o conteudo do PDF, gerar curiosidade | Reler o PDF, responder email |
| Dia 4 | Por que voce entende mas trava (a ciencia explica) | Aprofundar a dor, mostrar que existe solucao | Assistir mini-conteudo |
| Dia 6 | O que a Maria fez para destravar em 4 meses | Prova social, mostrar resultado real | Conhecer o metodo |
| Dia 8 | Ale preparou uma aula especial para voce | Transicao para VSL (AULA) | Assistir aula gratuita (link VSL VTurb) |

**Apos o dia 8:**
- Aplicar tag `sequencia_manual_completa`
- Remover tag `sequencia_manual_ativa`
- Se nao converteu, mover para lista de remarketing
- Se clicou no link do VSL, aplicar tag `assistiu_vsl`

---

## Tratamento de Erros

### Cenario 1: Email em formato invalido

**Mensagem do bot:**

```
Hmm, parece que esse email nao esta certinho 🤔

Pode digitar novamente? Preciso de um email valido para te enviar o PDF.

Exemplo: seunome@gmail.com
```

**Acao:** Solicitar novamente (maximo 2 tentativas).

### Cenario 2: Usuario nao fornece email (timeout 24h)

**Mensagem do bot (apos 24h):**

```
Oi! Voce pediu o Manual do Metodo ontem mas nao me mandou seu email ainda 😊

Se ainda quiser receber, e so digitar seu email aqui que eu envio na hora!
```

**Acao:** Aguardar mais 48h. Se nao responder, encerrar fluxo e aplicar tag `lead_abandonou_manual`.

### Cenario 3: Usuario ja e lead (email ja existe na base)

**Verificacao:** Checar se o email ja existe no ManyChat ou Mailchimp.

**Se ja e lead de outra isca:**

```
Oi! Voce ja faz parte da nossa comunidade 😊

Vou te enviar o Manual do Metodo agora mesmo no seu email. E um conteudo novo que vai complementar o que voce ja recebeu!
```

**Acao:**
- Adicionar tag `lead_manual_metodo` (sem duplicar lead)
- Enviar apenas o email do Dia 0 com o PDF
- Nao iniciar sequencia completa se ja esta em outra sequencia ativa
- Se nao esta em nenhuma sequencia ativa, iniciar sequencia normalmente

### Cenario 4: Usuario ja recebeu o Manual do Metodo antes

**Mensagem do bot:**

```
Voce ja recebeu o Manual do Metodo! 📖

Quer que eu reenvie no seu email? Ou se preferir, posso te mandar o link da aula demonstrativa gratuita — e o proximo passo para destravar seu espanhol de verdade. Comenta AULA se quiser!
```

**Acao:** Oferecer reenvio ou avancar no funil para AULA (VSL).

---

## Convencoes de Tags

### Padrao de nomenclatura

```
{categoria}_{especificacao}
```

### Tags do fluxo Manual do Metodo

| Tag | Descricao |
|-----|-----------|
| `lead_manual_metodo` | Lead gerado pela isca Manual do Metodo |
| `nivel_consciente_solucao` | Nivel de consciencia do lead |
| `origem_instagram` | Canal de captacao |
| `lead_ativo` | Lead com email capturado e valido |
| `lead_abandonou_manual` | Pediu o manual mas nao forneceu email |
| `sequencia_manual_ativa` | Esta recebendo a sequencia de 5 emails |
| `sequencia_manual_completa` | Completou a sequencia de 5 emails |
| `assistiu_vsl` | Clicou no link do VSL no email do dia 8 |
| `avatar_profissional` | Avatar identificado em interacoes anteriores |
| `avatar_viajante` | Avatar identificado em interacoes anteriores |
| `avatar_academico` | Avatar identificado em interacoes anteriores |
| `avatar_vai_morar_fora` | Avatar identificado em interacoes anteriores |

### Tags de outras iscas (referencia cruzada)

| Tag | Isca |
|-----|------|
| `lead_falsos_cognatos` | PDF Falsos Cognatos |
| `lead_espanhol_viagens` | PDF Espanhol para Viagens |
| `lead_guia_pronuncia` | PDF Guia de Pronuncia |
| `lead_20_erros` | Site Notion 20 Erros |

---

## Metricas para Acompanhar

- **Taxa de captura de email:** % dos que comentam MANUAL e fornecem email (meta: 70%)
- **Taxa de abertura email Dia 0:** meta 60%+
- **Taxa de abertura media da sequencia:** meta 40%+
- **Taxa de clique no VSL (Dia 8):** meta 15%+
- **Taxa de conversao VSL > compra:** meta 3%+
- **Leads abandonados:** % que comentam mas nao fornecem email (meta: <30%)
