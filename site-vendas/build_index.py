import re
import os

MODULOS_DIR = "D:/EspanholComVoce/site-vendas/modulos"
OUTPUT = "D:/EspanholComVoce/site-vendas/index.html"

FILES_AND_IDS = [
    ("MÓDULO 1 - Hero.html",                          "mod01"),
    ("MÓDULO 2 - Depoimentos Parte 1.html",            "mod02"),
    ("MÓDULO 3 - Dores  identificaçao.html",           "mod03"),
    ("MÓDULO 4 - Objeções.html",                       "mod04"),
    ("MÓDULO 5 - Comparativo.html",                    "mod05"),
    ("MÓDULO 6- 3 pilares (mecanismo).html",           "mod06"),
    ("MÓDULO 6B - Pilar 1 Jornada.html",               "mod06b"),
    ("MÓDULO 6C - Pilar 2 App.html",                   "mod06c"),
    ("MÓDULO 6D - Pilar 3 Suporte.html",               "mod06d"),
    ("MÓDULO 7 - Depoimentos de transformação.html",   "mod07"),
    ("MÓDULO 8 - Quem sou eu.html",                    "mod08"),
    ("MÓDULO 9 - Depoimentos finais.html",             "mod09"),
    ("MÓDULO 10 BONUS.html",                           "mod10"),
    ("MÓDULO 11 - Preço.html",                         "mod11"),
    ("MÓDULO 12 - Garantia.html",                      "mod12"),
    ("MÓDULO 13 - FAQ.html",                           "mod13"),
]

def extract_styles(html):
    return re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)

def extract_body(html):
    m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""

def extract_scripts_from_body(body):
    scripts = re.findall(r'<script[^>]*>.*?</script>', body, re.DOTALL | re.IGNORECASE)
    body_clean = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
    return body_clean.strip(), scripts

def scope_selector(selector, scope_id):
    parts = [s.strip() for s in selector.split(',')]
    scoped = []
    for part in parts:
        if not part:
            continue
        if part in (':root', 'html', '*'):
            scoped.append(part)
        elif part == 'body' or part.startswith('body ') or part.startswith('body.'):
            scoped.append(part.replace('body', '#' + scope_id, 1))
        else:
            scoped.append('#' + scope_id + ' ' + part)
    return ', '.join(scoped)

def scope_rules(css, scope_id):
    output = []
    i = 0
    length = len(css)
    while i < length:
        while i < length and css[i] in ' \t\n\r':
            output.append(css[i])
            i += 1
        if i >= length:
            break
        if css[i:i+2] == '/*':
            end = css.find('*/', i+2)
            if end == -1:
                output.append(css[i:])
                break
            output.append(css[i:end+2])
            i = end + 2
            continue
        brace_pos = css.find('{', i)
        if brace_pos == -1:
            output.append(css[i:])
            break
        selector = css[i:brace_pos].strip()
        j = brace_pos + 1
        depth = 1
        while j < length and depth > 0:
            if css[j] == '{': depth += 1
            elif css[j] == '}': depth -= 1
            j += 1
        body_block = css[brace_pos:j]
        if selector and not selector.startswith('@'):
            scoped = scope_selector(selector, scope_id)
            output.append(scoped + ' ' + body_block)
        else:
            output.append(selector + ' ' + body_block)
        i = j
    return ''.join(output)

def scope_css(css, scope_id):
    # Separate @keyframes
    kf_blocks = []
    def save_kf(m):
        kf_blocks.append(m.group(0))
        return "/* __KF_" + str(len(kf_blocks)-1) + "__ */"
    css = re.sub(r'@keyframes\s+[\w-]+\s*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', save_kf, css, flags=re.DOTALL)

    output = []
    i = 0
    length = len(css)

    while i < length:
        while i < length and css[i] in ' \t\n\r':
            output.append(css[i])
            i += 1
        if i >= length:
            break
        if css[i:i+2] == '/*':
            end = css.find('*/', i+2)
            if end == -1:
                output.append(css[i:])
                break
            output.append(css[i:end+2])
            i = end + 2
            continue
        # @media
        if css[i] == '@' and css[i:i+6] == '@media':
            brace_pos = css.find('{', i)
            if brace_pos == -1:
                output.append(css[i:])
                break
            output.append(css[i:brace_pos+1])
            i = brace_pos + 1
            depth = 1
            start = i
            while i < length and depth > 0:
                if css[i] == '{': depth += 1
                elif css[i] == '}': depth -= 1
                i += 1
            media_content = css[start:i-1]
            output.append(scope_rules(media_content, scope_id))
            output.append('}')
            continue
        # Regular rule
        brace_pos = css.find('{', i)
        if brace_pos == -1:
            output.append(css[i:])
            break
        selector = css[i:brace_pos].strip()
        j = brace_pos + 1
        depth = 1
        while j < length and depth > 0:
            if css[j] == '{': depth += 1
            elif css[j] == '}': depth -= 1
            j += 1
        body_block = css[brace_pos:j]
        if selector and not selector.startswith('@') and not selector.startswith('/*'):
            scoped = scope_selector(selector, scope_id)
            output.append(scoped + ' ' + body_block)
        else:
            output.append(selector + ' ' + body_block)
        i = j

    result_css = ''.join(output)
    for idx, kf in enumerate(kf_blocks):
        result_css = result_css.replace("/* __KF_" + str(idx) + "__ */", kf)
    return result_css

# Read all modules
modules_data = []
for fname, mid in FILES_AND_IDS:
    fpath = os.path.join(MODULOS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    modules_data.append((fname, mid, html))
    print("Read: " + mid + " (" + str(len(html)) + " bytes)")

# Build combined HTML
parts = []
parts.append('<!DOCTYPE html>')
parts.append('<html lang="pt-BR">')
parts.append('<head>')
parts.append('<meta charset="UTF-8">')
parts.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
parts.append('<title>Programa Imersao Nativa - Espanhol com Voce</title>')
parts.append('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')
parts.append('<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@400;600;700;900&display=swap" rel="stylesheet">')

parts.append('<style>')
parts.append('*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }')
parts.append('html { scroll-behavior: smooth; }')
parts.append('body { font-family: "Inter", sans-serif; background: #0a1628; color: #fff; }')
parts.append('</style>')

for fname, mid, html in modules_data:
    styles = extract_styles(html)
    if styles:
        parts.append('\n<!-- Styles: ' + mid + ' -->')
        parts.append('<style>')
        for s in styles:
            s = re.sub(r'\*\s*,\s*\*::before\s*,\s*\*::after\s*\{[^}]*\}', '', s)
            s = re.sub(r'(?<![.\w#-])\*\s*\{[^}]*\}', '', s)
            s = re.sub(r'body\s*\{[^}]*\}', '', s)
            s = s.strip()
            if s:
                parts.append(scope_css(s, mid))
        parts.append('</style>')

parts.append('</head>')
parts.append('<body>')

all_scripts = []
for fname, mid, html in modules_data:
    body = extract_body(html)
    if body:
        body_clean, scripts = extract_scripts_from_body(body)
        all_scripts.extend(scripts)
        parts.append('\n<!-- ======== ' + mid + ' ======== -->')
        parts.append('<div id="' + mid + '">')
        parts.append(body_clean)
        parts.append('</div>')

if all_scripts:
    parts.append('\n<!-- Scripts -->')
    for s in all_scripts:
        parts.append(s)

parts.append('</body>')
parts.append('</html>')

final = '\n'.join(parts)

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(final)

size = len(final)
print("Done! index.html: " + str(size) + " bytes (" + str(round(size/1024/1024, 1)) + " MB)")
print("Modules combined: " + str(len(modules_data)))
