"""
Cria index_v2.html com a paleta oficial da marca.
Preserva: copy, estrutura, animações, contadores, abas, scripts.
Não altera módulos 06B, 06C, 06D (conteúdo dentro de #mod06b, #mod06c, #mod06d).
"""
import re

with open("D:/EspanholComVoce/site-vendas/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = []

# =============================================
# MAPEAMENTO DE CORES
# =============================================
# Fundos escuros: #0a1628 / #0d2140 / #0d1f4a → #001e38
# Gold/destaques: #fbbf24 / #facc15 / #f59e0b → #ffcb15
# Sky/info: #38bdf8 / #0891b2 → #0090be
# Emerald/check: #10b981 / #4CAF82 / #22c55e → #36c551
# CTA gradient gold→orange → solid #36c551 com texto branco
# Navy text on light: #0a1628 → #001e38
# Rose/urgência: #f43f5e / #f87171 → #ff421c

# =============================================
# 1. FUNDOS ESCUROS
# =============================================
# Manter gradients mas trocar a cor base
for old, new in [
    ('#0a1628', '#001e38'),
    ('#0d2140', '#001e38'),
    ('#0d1f4a', '#001e38'),
    ('#0f1d34', '#001e38'),
    ('#1a2942', '#0a3050'),  # navy-light → versão mais clara do novo navy
]:
    c = html.count(old)
    if c:
        html = html.replace(old, new)
        changes.append(f'{old} → {new}: {c}x')

# =============================================
# 2. GOLD/DESTAQUES → #ffcb15
# =============================================
for old, new in [
    ('#fbbf24', '#ffcb15'),
    ('#facc15', '#ffcb15'),
    ('#f59e0b', '#ffcb15'),
]:
    c = html.count(old)
    if c:
        html = html.replace(old, new)
        changes.append(f'{old} → {new}: {c}x')

# =============================================
# 3. CTA BUTTONS: gold gradient → solid green #36c551
# Replace gradient backgrounds on CTA buttons
# =============================================
# Pattern: linear-gradient(135deg, #ffcb15 0%, #fb923c 100%)
# and variations like linear-gradient(135deg,#ffcb15,#fb923c)
cta_patterns = [
    ('linear-gradient(135deg, #ffcb15 0%, #fb923c 100%)', '#36c551'),
    ('linear-gradient(135deg,#ffcb15,#fb923c)', '#36c551'),
    ('linear-gradient(135deg,#ffcb15, #fb923c)', '#36c551'),
    ('linear-gradient(135deg, #ffcb15, #fb923c)', '#36c551'),
]
for old, new in cta_patterns:
    c = html.count(old)
    if c:
        html = html.replace(old, 'background:' in old and new or new)
        changes.append(f'CTA gradient → {new}: {c}x')

# Also fix the remaining #fb923c (orange in gradients) → #36c551
c = html.count('#fb923c')
if c:
    html = html.replace('#fb923c', '#2ab048')  # slightly darker green for gradient end
    changes.append(f'#fb923c → #2ab048: {c}x')

# =============================================
# 4. CTA TEXT COLOR: navy → white
# The CTA buttons had color:#001e38 (was #0a1628), change to white
# This is tricky because #001e38 is also used for text on light bgs
# We target specifically the CTA button styles
# =============================================
# Replace in CTA button class
html = html.replace(
    'color: #001e38;\n      font-family: \'Inter\', sans-serif;\n      font-size: 14px;\n      font-weight: 900;\n      letter-spacing: 2px;\n      text-transform: uppercase;\n      border: none;\n      border-radius: 50px;',
    'color: #ffffff;\n      font-family: \'Inter\', sans-serif;\n      font-size: 14px;\n      font-weight: 900;\n      letter-spacing: 2px;\n      text-transform: uppercase;\n      border: none;\n      border-radius: 50px;'
)
# Inline CTA buttons with color:#001e38 in style attributes
html = re.sub(
    r'(background:(?:linear-gradient\([^)]+\)|#36c551|#2ab048)[^"]*?)color:#001e38',
    r'\1color:#ffffff',
    html
)
changes.append('CTA text color → #ffffff')

# =============================================
# 5. SKY/INFO → #0090be
# =============================================
for old, new in [
    ('#38bdf8', '#0090be'),
    ('#0891b2', '#0090be'),
    ('#60a5fa', '#0090be'),
]:
    c = html.count(old)
    if c:
        html = html.replace(old, new)
        changes.append(f'{old} → {new}: {c}x')

# =============================================
# 6. EMERALD/CHECK → #36c551
# =============================================
for old, new in [
    ('#10b981', '#36c551'),
    ('#4CAF82', '#36c551'),
    ('#22c55e', '#36c551'),
    ('#34d399', '#36c551'),
    ('#86efac', '#6ee78a'),  # lime → lighter green
    ('#4ade80', '#6ee78a'),
]:
    c = html.count(old)
    if c:
        html = html.replace(old, new)
        changes.append(f'{old} → {new}: {c}x')

# =============================================
# 7. ROSE/URGÊNCIA → #ff421c
# =============================================
for old, new in [
    ('#f43f5e', '#ff421c'),
    ('#f87171', '#ff421c'),
    ('#f44336', '#ff421c'),
]:
    c = html.count(old)
    if c:
        html = html.replace(old, new)
        changes.append(f'{old} → {new}: {c}x')

# =============================================
# 8. PURPLE → keep or map to blue
# =============================================
c = html.count('#8b5cf6')
if c:
    html = html.replace('#8b5cf6', '#0090be')
    changes.append(f'#8b5cf6 → #0090be: {c}x')

# =============================================
# 9. BROWN/BADGE → #001e38 (was #b45309)
# =============================================
c = html.count('#b45309')
if c:
    html = html.replace('#b45309', '#001e38')
    changes.append(f'#b45309 → #001e38: {c}x')

# =============================================
# 10. BOX-SHADOW colors on CTAs: gold → green
# =============================================
html = html.replace('rgba(250,204,21,', 'rgba(54,197,81,')
html = html.replace('rgba(250, 204, 21,', 'rgba(54, 197, 81,')
html = html.replace('rgba(251,191,36,', 'rgba(54,197,81,')
html = html.replace('rgba(251, 191, 36,', 'rgba(54, 197, 81,')
html = html.replace('rgba(245,158,11,', 'rgba(54,197,81,')
html = html.replace('rgba(245, 158, 11,', 'rgba(54, 197, 81,')
changes.append('CTA box-shadow gold → green')

# =============================================
# 11. CSS custom properties
# =============================================
html = html.replace("--gold:       #ffcb15", "--gold:       #ffcb15")  # already done
html = html.replace("--gold-light: #ffcb15", "--gold-light: #ffcb15")  # already done
html = html.replace("--sky:        #0090be", "--sky:        #0090be")  # already done
html = html.replace("--emerald:    #36c551", "--emerald:    #36c551")  # already done
html = html.replace("--navy:       #001e38", "--navy:       #001e38")  # already done

# =============================================
# SAVE
# =============================================
output = "D:/EspanholComVoce/site-vendas/index_v2.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(html)

for c in changes:
    print(c.encode('ascii', 'replace').decode())
print(f"\nDone! {output}: {len(html)} bytes ({round(len(html)/1024/1024, 1)} MB)")
