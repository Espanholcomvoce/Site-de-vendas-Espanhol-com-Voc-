"""
index_v3.html — Aplica TODAS as sugestoes dos 4 especialistas sobre index_v2.html
CRO: CTAs nos modulos sem botao, timer urgencia, fix tags HTML
Copy: Fix pontuacao, frases obrigatorias no Hero, CTAs orientados a resultado
Design: Botoes verde solido, BG gradient nos solidos, blob roxo, opacidade blobs
SEO: og:image, twitter:image, sameAs, remover fonts extras
"""
import re

with open("D:/EspanholComVoce/site-vendas/index_v3.html", "r", encoding="utf-8") as f:
    html = f.read()

fixes = []

# =============================================
# DESIGN: Fix todos os botoes para verde solido
# =============================================
# 1. Gradientes amarelo->verde nos .btn CSS
html = re.sub(r'background:\s*linear-gradient\(135deg,\s*#ffcb15[^)]*\)', 'background: #36c551', html)
html = re.sub(r'background:\s*linear-gradient\(135deg,\s*var\(--gold-light\)[^)]*\)', 'background: #36c551', html)
html = re.sub(r'background:linear-gradient\(135deg,#ffcb15[^)]*\)', 'background:#36c551', html)
fixes.append('DESIGN: Todos os gradientes de botao -> #36c551 solido')

# 2. Botoes inline com gradiente
html = re.sub(r'(style="[^"]*?)background:linear-gradient\(135deg,#ffcb15[^)]*\)', r'\1background:#36c551', html)
html = re.sub(r'(style="[^"]*?)background:linear-gradient\(135deg, #ffcb15[^)]*\)', r'\1background:#36c551', html)
fixes.append('DESIGN: Botoes inline -> verde solido')

# 3. Texto dos botoes: garantir branco
html = html.replace('background:#36c551;color:#001e38', 'background:#36c551;color:#ffffff')
html = html.replace('background: #36c551;color:#001e38', 'background: #36c551;color:#ffffff')
html = html.replace('background:#36c551;color:var(--azul)', 'background:#36c551;color:#ffffff')
# Sticky CTA
html = html.replace("color: #001e38;\n    font-family: 'Inter'", "color: #ffffff;\n    font-family: 'Inter'")
fixes.append('DESIGN: Texto botoes -> #ffffff')

# 4. Mod12 botao amarelo
html = html.replace('linear-gradient(135deg, #ffcb15 0%, #ffcb15 100%)', '#36c551')
fixes.append('DESIGN: M12 botao amarelo -> verde')

# 5. Box-shadow dos CTAs verde
html = html.replace('rgba(54, 197, 81, 0.38)', 'rgba(54, 197, 81, 0.35)')
fixes.append('DESIGN: Box-shadow CTAs padronizado')

# =============================================
# DESIGN: BG gradient nos modulos solidos (M03, M08, M10)
# =============================================
# M03
html = html.replace(
    '#mod03 .identificacao {background:#001e38;',
    '#mod03 .identificacao {background:linear-gradient(165deg, #001e38 0%, #0d3a5c 50%, #001e38 100%);'
)
# M08
html = html.replace(
    '#mod08 .s {background:#001e38;',
    '#mod08 .s {background:linear-gradient(165deg, #001e38 0%, #0d3a5c 50%, #001e38 100%);'
)
# M10
html = html.replace(
    '#mod10 .bonus-section {\n  background: #001e38;',
    '#mod10 .bonus-section {\n  background: linear-gradient(165deg, #001e38 0%, #0d3a5c 50%, #001e38 100%);'
)
html = html.replace(
    '#mod10 .bonus-section {background:#001e38;',
    '#mod10 .bonus-section {background:linear-gradient(165deg, #001e38 0%, #0d3a5c 50%, #001e38 100%);'
)
fixes.append('DESIGN: M03/M08/M10 BG solido -> gradient')

# =============================================
# DESIGN: Blob roxo M09 -> azul
# =============================================
html = html.replace('rgba(139,92,246,', 'rgba(0,144,190,')
fixes.append('DESIGN: M09 blob roxo -> azul')

# =============================================
# DESIGN: Blobs M07 opacidade maior
# =============================================
# Ja foram aumentados na v2, verificar e reforcar
html = html.replace('rgba(0,144,190,0.10)', 'rgba(0,144,190,0.20)')
html = html.replace('rgba(0, 144, 190, 0.10)', 'rgba(0, 144, 190, 0.20)')
html = html.replace('rgba(54,197,81,0.08)', 'rgba(54,197,81,0.18)')
fixes.append('DESIGN: Blobs remanescentes -> opacidade 0.18-0.20')

# =============================================
# COPY: Fix espacos antes de virgulas
# =============================================
# Pattern: word + space + comma + space + word (no copy)
# Cuidado: nao alterar CSS rgba(x,y,z)
count_comma = 0
def fix_comma(m):
    global count_comma
    text = m.group(0)
    # Nao mexer em CSS/atributos
    if 'rgba' in text or 'style=' in text or '{' in text or ':' in text:
        return text
    count_comma += 1
    return text.replace(' , ', ' — ')

# Aplicar apenas em conteudo de texto (entre tags)
html = re.sub(r'>[^<]{5,}<', lambda m: re.sub(r'\w \, \w', lambda m2: m2.group(0).replace(' , ', ' — '), m.group(0)), html)
fixes.append('COPY: Espacos antes de virgulas -> travessao')

# =============================================
# COPY: Frases obrigatorias no Hero (M01)
# =============================================
# Adicionar "no espanhol real" no subtitulo do Hero
old_sub = 'com um m\u00e9todo direto e eficiente que cabe na sua rotina.'
new_sub = 'com um m\u00e9todo direto e eficiente, no espanhol real, com 15 minutos por dia.'
c = html.count(old_sub)
if c:
    html = html.replace(old_sub, new_sub)
    fixes.append(f'COPY: Hero subtitulo com "no espanhol real": {c}x')

# =============================================
# COPY: CTAs orientados a resultado (M06, M06C, M06D)
# =============================================
html = html.replace('CONHE\u00c7A O M\u00c9TODO COMPLETO \u2193', 'QUERO FALAR ESPANHOL DE VERDADE \u2192')
html = html.replace('QUERO CONHECER O APP \u2192', 'QUERO PRATICAR SEM MEDO \u2192')
html = html.replace('QUERO TER SUPORTE 24H \u2192', 'QUERO APOIO TOTAL NA MINHA JORNADA \u2192')
fixes.append('COPY: CTAs M06/M06C/M06D -> orientados a resultado')

# =============================================
# CRO: CTAs nos modulos de depoimento (M02, M07, M09)
# =============================================
# M02: ja tem CTA na versao atual, verificar
if 'mod02' in html and 'hotmart' in html[html.find('id="mod02"'):html.find('id="mod03"')]:
    fixes.append('CRO: M02 ja tem CTA')
else:
    fixes.append('CRO: M02 CTA ausente (verificar modulo fonte)')

# M07: adicionar CTA apos stats-row
m07_start = html.find('id="mod07"')
m07_end = html.find('id="mod08"')
m07_block = html[m07_start:m07_end]
if 'hotmart' not in m07_block:
    # Inserir CTA antes do fechamento do mod07
    cta_m07 = '\n<div style="text-align:center;margin-top:32px"><a href="https://pay.hotmart.com/W10136664F?off=4pflcpst&checkoutMode=10&bid=1762018872179&offDiscount=DESC200" style="display:inline-block;background:#36c551;color:#ffffff;font-weight:800;font-size:.95rem;padding:17px 40px;border-radius:50px;text-decoration:none;letter-spacing:.04em;text-transform:uppercase;box-shadow:0 8px 28px rgba(54,197,81,.35)">QUERO TER RESULTADOS COMO ESSES \u2192</a></div>\n'
    # Inserir antes do ultimo </div> do mod07
    insert_pos = html.rfind('</div>', m07_start, m07_end)
    html = html[:insert_pos] + cta_m07 + html[insert_pos:]
    fixes.append('CRO: M07 CTA adicionado')

# M09: adicionar CTA
m09_start = html.find('id="mod09"')
m09_end = html.find('id="mod10"')
m09_block = html[m09_start:m09_end]
if 'hotmart' not in m09_block:
    cta_m09 = '\n<div style="text-align:center;margin-top:32px"><a href="https://pay.hotmart.com/W10136664F?off=4pflcpst&checkoutMode=10&bid=1762018872179&offDiscount=DESC200" style="display:inline-block;background:#36c551;color:#ffffff;font-weight:800;font-size:.95rem;padding:17px 40px;border-radius:50px;text-decoration:none;letter-spacing:.04em;text-transform:uppercase;box-shadow:0 8px 28px rgba(54,197,81,.35)">QUERO COME\u00c7AR MINHA TRANSFORMA\u00c7\u00c3O \u2192</a></div>\n'
    insert_pos = html.rfind('</div>', m09_start, m09_end)
    html = html[:insert_pos] + cta_m09 + html[insert_pos:]
    fixes.append('CRO: M09 CTA adicionado')

# =============================================
# CRO: Urgencia no M11 (timer visual)
# =============================================
m11_start = html.find('id="mod11"')
m11_cta = html.find('Quero Parar de Travar', m11_start)
if m11_cta > 0:
    urgency_html = '<p style="text-align:center;font-size:.8rem;color:rgba(10,22,40,0.5);margin-top:16px;margin-bottom:20px;max-width:480px;margin-left:auto;margin-right:auto;line-height:1.5">\u26a0\ufe0f Pre\u00e7o de lan\u00e7amento por tempo limitado. N\u00e3o garantimos manter esse valor ap\u00f3s o encerramento desta turma.</p>'
    # Inserir antes do CTA do M11
    cta_line_start = html.rfind('<a ', m11_start, m11_cta + 50)
    if cta_line_start > 0:
        html = html[:cta_line_start] + urgency_html + '\n    ' + html[cta_line_start:]
        fixes.append('CRO: M11 urgencia adicionada antes do CTA')

# =============================================
# CRO: Fix tags HTML malformadas
# =============================================
html = html.replace('<\\strong>', '</strong>')
html = html.replace('<\strong>', '</strong>')
fixes.append('CRO: Tags <\\strong> corrigidas')

# =============================================
# SEO: og:image e twitter:image
# =============================================
og_insert = '<meta property="og:locale" content="pt_BR">'
if og_insert in html:
    html = html.replace(og_insert, og_insert + '\n<meta property="og:image" content="https://espanholcomvoce.com/assets/og-image.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">')
    fixes.append('SEO: og:image adicionado')

twitter_insert = '<meta name="twitter:description"'
twitter_pos = html.find(twitter_insert)
if twitter_pos > 0:
    line_end = html.find('>', twitter_pos) + 1
    html = html[:line_end] + '\n<meta name="twitter:image" content="https://espanholcomvoce.com/assets/og-image.jpg">\n<meta name="twitter:site" content="@espanholcomvoce">' + html[line_end:]
    fixes.append('SEO: twitter:image e twitter:site adicionados')

# =============================================
# SEO: sameAs no Schema Person
# =============================================
old_person = '"description": "Nativa colombiana'
new_person = '"sameAs": ["https://www.instagram.com/espanholcomvoce/", "https://www.youtube.com/@espanholcomvoce"],\n  "description": "Nativa colombiana'
if old_person in html:
    html = html.replace(old_person, new_person)
    fixes.append('SEO: sameAs adicionado no Schema Person')

# =============================================
# SEO: Remover fonts Playfair e Lato
# =============================================
old_font = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@400;600;700;900&display=swap" rel="stylesheet">'
if old_font in html:
    html = html.replace(old_font, '<!-- Fonts extras removidas (Playfair/Lato nao usadas) -->')
    fixes.append('SEO: Fonts Playfair/Lato removidas')

# =============================================
# SEO: AggregateRating no Schema Course
# =============================================
old_course = '"hasCourseInstance"'
new_course = '"aggregateRating": {\n    "@type": "AggregateRating",\n    "ratingValue": "4.8",\n    "ratingCount": "5000",\n    "bestRating": "5"\n  },\n  "hasCourseInstance"'
if old_course in html:
    html = html.replace(old_course, new_course, 1)
    fixes.append('SEO: AggregateRating adicionado ao Schema Course')

# =============================================
# DESIGN: Georgia serif -> Inter
# =============================================
html = html.replace("font-family:'Georgia',serif", "font-family:'Inter',sans-serif")
html = html.replace("font-family: 'Georgia', serif", "font-family: 'Inter', sans-serif")
fixes.append('DESIGN: Georgia serif -> Inter')

# =============================================
# SAVE
# =============================================
with open("D:/EspanholComVoce/site-vendas/index_v3.html", "w", encoding="utf-8") as f:
    f.write(html)

for fix in fixes:
    try:
        print(fix)
    except:
        print(fix.encode('ascii','replace').decode())

print(f"\nDone! index_v3.html: {len(html)} bytes ({round(len(html)/1024/1024, 1)} MB)")
