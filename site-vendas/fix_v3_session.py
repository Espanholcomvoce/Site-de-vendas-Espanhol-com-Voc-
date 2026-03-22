# -*- coding: utf-8 -*-
"""Aplica todas as correcoes da sessao na v3"""

with open("D:/EspanholComVoce/site-vendas/index_v3.html", "r", encoding="utf-8") as f:
    html = f.read()

import re

# === CORRECOES ANTERIORES DA SESSAO ===

# M03 headline
html = html.replace("e na hora de abrir a boca, trava.", "e na hora de falar, trava.")

# M03 micro-provas primeira pessoa
html = html.replace("A Cassia fez sua primeira viagem", "Fiz minha primeira viagem")
html = html.replace("O Jo\u00e3o em seis meses j\u00e1 conseguiu", "Em seis meses j\u00e1 consegui")

# FAQ fixes
html = html.replace("avan\u00e7ar bastante. O programa foi pensado para quem tem uma rotina ocupada e precisa de praticidade.", "As aulas t\u00eam por volta de 5 minutos. D\u00e1 para encaixar no intervalo do almo\u00e7o, no \u00f4nibus ou antes de dormir. Eu pensei cada aula para caber na rotina de quem trabalha, estuda ou cuida da casa.")
html = html.replace("Depende da sua dedica\u00e7\u00e3o, mas muitos alunos relatam que", "Depende da sua dedica\u00e7\u00e3o, mas voc\u00ea come\u00e7a a perceber evolu\u00e7\u00e3o logo nas primeiras semanas. Muitos alunos relatam que")
html = html.replace("se comunicar de verdade , como um nativo fala, n\u00e3o como a gram\u00e1tica manda.", "se comunicar de verdade, do jeito que a gente fala no dia a dia.")
html = html.replace("acompanhamento do seu progresso , tudo no celular, onde e quando quiser.", "acompanhamento do seu progresso. \u00c9 como ter a Ale no seu bolso, dispon\u00edvel 24h.")
html = html.replace("devolvemos <strong>100%", "devolvo <strong>100%")
html = html.replace("vital\u00edcio</strong> , voc\u00ea estuda para sempre, sem pressa.", "vital\u00edcio</strong>, sem prazo de expira\u00e7\u00e3o.")
html = html.replace("mat\u00e9ria de escola , e a\u00ed", "mat\u00e9ria de escola, e a\u00ed")
html = html.replace("espanhol real , express\u00f5es", "espanhol real, express\u00f5es")
html = html.replace("do dia a dia , para que", "do dia a dia, para que")
html = html.replace("Sim! O programa foi criado para quem nunca estudou espanhol ou tem s\u00f3 o b\u00e1sico. Voc\u00ea come\u00e7a do zero, no seu ritmo,", "Sim! O programa foi criado tanto para quem est\u00e1 come\u00e7ando do zero quanto para quem j\u00e1 estudou antes mas ainda trava na hora de falar. Voc\u00ea segue no seu ritmo,")

# M08
html = html.replace("Quem vai te guiar", "Quem vai te acompanhar nessa jornada")
html = html.replace("o que nenhuma escola te ensina", "como o c\u00e9rebro realmente aprende um idioma")
html = html.replace("Cheguei no Brasil sem falar nada e aprendi do zero, sem escola, sem m\u00e9todo tradicional.", "Cheguei no Brasil em 2011 com certificado avan\u00e7ado de portugu\u00eas. Na teoria estava preparada. Mas na hora de falar com o porteiro, no mercado, com a corretora de im\u00f3veis, eu travava.")
html = html.replace("Eu conhe\u00e7o cada erro que o brasileiro comete em espanhol porque j\u00e1 ouvi todos eles. Sei onde voc\u00ea trava, sei por que trava e sei como destravar, porque fiz o caminho inverso.", "")

# Remover travessoes do texto visivel
def fix_emdash(m):
    text = m.group(1)
    if "/*" in text or "{" in text or ":root" in text:
        return ">" + text + "<"
    return ">" + text.replace(" \u2014 ", ", ").replace("\u2014 ", ", ").replace(" \u2014", ",").replace("\u2014", ",") + "<"
html = re.sub(r">([^<]*\u2014[^<]*)<", fix_emdash, html)

# Instagram icons
ig = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:3px"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>'
html = re.sub(r'>(@[a-zA-Z0-9_.]+)<(?!/svg)', lambda m: '>' + ig + m.group(1) + '<', html)

# M07 fundo claro + cards azul
m07s = html.find("<!-- Styles: mod07 -->")
m07e = html.find("<!-- Styles: mod08 -->")
block = html[m07s:m07e]
block = block.replace("background:linear-gradient(165deg,#001e38 0%,#0d3a5c 50%,#001e38 100%);", "background:#e8eef4;")
block = block.replace("background:rgba(255,255,255,.04);", "background:#001e38;")
block = block.replace("color:#fff;", "color:#001e38;")
block = block.replace("color:#fff}", "color:#001e38}")
block = block.replace("border:1px solid rgba(255,255,255,.08)", "border:1px solid rgba(0,30,56,.12)")
html = html[:m07s] + block + html[m07e:]

# M13 fundo branco, cards azul
m13s = html.find("<!-- Styles: mod13 -->")
m13e = html.find("</head>", m13s)
block13 = html[m13s:m13e]
block13 = block13.replace("background: #e8eef4;", "background: #ffffff;")
block13 = block13.replace("background:#e8eef4;", "background:#ffffff;")
block13 = block13.replace("background: rgba(0,30,56, 0.02);", "background: #001e38;")
block13 = re.sub(r"(#mod13 \.faq-item\s*\{[^}]*?)background:[^;]+;", r"\1background: #001e38;", block13)
block13 = block13.replace("border: 1px solid rgba(0,30,56, 0.08);", "border: 1px solid rgba(0,144,190, 0.2);")
block13 = block13.replace("border-left: 3px solid var(--sky);", "border-left: 3px solid #0090be;")
block13 = block13.replace("border-left-color: var(--emerald);", "border-left-color: #36c551;")
block13 = block13.replace("color: var(--navy);", "color: #ffffff;")
block13 = block13.replace("color: #4a5568;", "color: rgba(255,255,255,0.75);")
block13 = block13.replace("border: 1.5px solid rgba(0,30,56, 0.15);", "border: 1.5px solid rgba(255,255,255, 0.2);")
block13 = block13.replace("border: 1.5px solid rgba(10, 22, 40, 0.15);", "border: 1.5px solid rgba(255,255,255, 0.2);")
block13 = block13.replace("color: #94a3b8;", "color: rgba(255,255,255,0.5);")
block13 = block13.replace("#mod13 .faq-item.open .faq-question { color: var(--navy); }", "#mod13 .faq-item.open .faq-question { color: #ffffff; }")
block13 = block13.replace("#mod13 .faq-question:hover { color: var(--sky); }", "#mod13 .faq-question:hover { color: #36c551; }")
block13 = re.sub(r"(#mod13 \.faq-answer-inner strong\s*\{[^}]*?)color:[^;]+;", r"\1color: #ffffff;", block13)
block13 = re.sub(r"(#mod13 \.faq-title\s*\{[^}]*?)color:\s*#ffffff;", r"\1color: #001e38;", block13)
html = html[:m13s] + block13 + html[m13e:]

# M02 CTA
m02s = html.find('id="mod02"')
m02e = html.find('id="mod03"')
if "hotmart" not in html[m02s:m02e]:
    m02_last = html.rfind("</div>", m02s, m02e)
    cta = '<div style="text-align:center;margin-top:32px"><a href="https://pay.hotmart.com/W10136664F?off=4pflcpst&checkoutMode=10&bid=1762018872179&offDiscount=DESC200" style="display:inline-block;background:#36c551;color:#ffffff;font-weight:800;font-size:.95rem;padding:17px 40px;border-radius:50px;text-decoration:none;letter-spacing:.04em;text-transform:uppercase;box-shadow:0 8px 28px rgba(54,197,81,.35)">QUERO DESTRAVAR MEU ESPANHOL AGORA</a></div>'
    html = html[:m02_last] + cta + html[m02_last:]

# Remover escassez do M10
html = re.sub(r'<p[^>]*>Esta \u00e9 a vers\u00e3o mais evolu\u00edda[^<]*encerramento desta turma\.</p>', '', html)

# === NOVAS CORRECOES: PILAR 2 APP ===

# Card 2: Vocabulario
html = html.replace("O vocabul\u00e1rio aparece quando precisa.", "O vocabul\u00e1rio aparece na hora certa.")
html = html.replace("\u2728 Vocabul\u00e1rio que lembra na hora certa", "\u2728 Nunca mais esquece o que aprendeu")

# Card 3: Duvidas
html = html.replace("explica\u00e7\u00f5es claras adaptadas para brasileiros", "explica\u00e7\u00f5es claras, feitas especialmente para brasileiros")
html = html.replace("\u2728 Nunca fica travado no estudo", "\u2728 D\u00favida respondida, aprendizado que avan\u00e7a")

# Card 4: Pratica real
html = html.replace("Conhecimento vira habilidade real.", "Conhecimento vira habilidade de verdade.")
html = html.replace("\u2728 Voc\u00ea usa o espanhol de verdade", "\u2728 Voc\u00ea usa o espanhol, n\u00e3o s\u00f3 estuda")

# Card 5: DELE -> Compreensao leitora
html = html.replace("Prepara\u00e7\u00e3o para DELE e SIELE", "Compreens\u00e3o leitora")
html = html.replace("Simulados no formato real das provas oficiais. Chegue ao exame com seguran\u00e7a e certifica\u00e7\u00e3o internacional.", "Textos reais em espanhol com exerc\u00edcios que treinam sua leitura no ritmo dos nativos. Voc\u00ea entende o que l\u00ea sem precisar de tradutor.")
html = html.replace("\u2728 Certifica\u00e7\u00e3o reconhecida mundialmente", "\u2728 Ler em espanhol vira algo natural")

# Card 6: Adicionar Compreensao auditiva
card5_marker = "Ler em espanhol vira algo natural</span>"
card5_pos = html.find(card5_marker)
if card5_pos > 0:
    close1 = html.find("</div>", card5_pos)
    close2 = html.find("</div>", close1 + 6)
    close3 = html.find("</div>", close2 + 6)
    insert_pos = close3 + 6

    new_card6 = """
        <div class="feature-card fc-6">
          <div class="fc-inner">
            <div class="fc-icon">\U0001f3a7</div>
            <h4 class="fc-title">Compreens\u00e3o auditiva</h4>
            <p class="fc-desc">\u00c1udios com sotaques reais de diferentes pa\u00edses. Seu ouvido aprende a captar tudo, mesmo quando falam r\u00e1pido.</p>
            <span class="fc-chip">\u2728 Voc\u00ea entende de verdade, n\u00e3o s\u00f3 adivinha</span>
          </div>
        </div>
"""
    html = html[:insert_pos] + new_card6 + html[insert_pos:]

with open("D:/EspanholComVoce/site-vendas/index_v3.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"v3 atualizada: {len(html)} bytes")
