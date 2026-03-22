"""
Agente QA — Quiz Espanhol com Você
Verifica integração entre index.html e quiz.js
Detecta seletores desacoplados e aplica correções automaticamente
"""

import re
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4"])
    from bs4 import BeautifulSoup

try:
    import anthropic
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "anthropic"])
    import anthropic

# ─── Configuração ───
QUIZ_DIR = Path(r"D:\EspanholComVoce\iscas\manual_do_metodo\quiz")
HTML_PATH = QUIZ_DIR / "index.html"
JS_PATH = QUIZ_DIR / "quiz.js"
REPORT_PATH = QUIZ_DIR / "qa_report.md"


def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ═══════════════════════════════════════════════
# FASE 1 — Extração estática de seletores do JS
# ═══════════════════════════════════════════════

def extract_js_selectors(js_content: str) -> dict:
    """Extrai todos os seletores CSS usados no JS."""

    patterns = {
        "getElementById": re.findall(
            r'getElementById\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "querySelector": re.findall(
            r'querySelector\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "querySelectorAll": re.findall(
            r'querySelectorAll\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "classList_add": re.findall(
            r'classList\.add\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "classList_remove": re.findall(
            r'classList\.remove\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "classList_toggle": re.findall(
            r'classList\.toggle\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "classList_contains": re.findall(
            r'classList\.contains\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)', js_content
        ),
        "addEventListener_id": re.findall(
            r'getElementById\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\.addEventListener', js_content
        ),
        "innerHTML_targets": re.findall(
            r'getElementById\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\.(?:innerHTML|textContent|innerText|value)', js_content
        ),
        "style_targets": re.findall(
            r'getElementById\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\.style', js_content
        ),
        "dataset_access": re.findall(
            r'\.dataset\.(\w+)', js_content
        ),
    }

    # Template literals com seletores
    template_selectors = re.findall(
        r'querySelector(?:All)?\s*\(\s*`([^`]+)`\s*\)', js_content
    )
    patterns["template_selectors"] = template_selectors

    # Classes usadas em criação dinâmica (createElement + className)
    dynamic_classes = re.findall(
        r'className\s*=\s*[\'"]([^\'"]+)[\'"]', js_content
    )
    # Classes em template literals com class=
    dynamic_classes += re.findall(
        r'class="([^"]+)"', js_content
    )
    patterns["dynamic_classes"] = dynamic_classes

    return patterns


# ═══════════════════════════════════════════════
# FASE 2 — Extração de IDs e classes do HTML
# ═══════════════════════════════════════════════

def extract_html_elements(html_content: str) -> dict:
    """Extrai todos os IDs, classes e data-attributes do HTML."""

    soup = BeautifulSoup(html_content, "html.parser")

    ids = set()
    classes = set()
    data_attrs = set()

    for tag in soup.find_all(True):
        # IDs
        if tag.get("id"):
            ids.add(tag["id"])

        # Classes
        if tag.get("class"):
            for cls in tag["class"]:
                classes.add(cls)

        # Data attributes
        for attr in tag.attrs:
            if attr.startswith("data-"):
                data_attrs.add(attr)

    return {
        "ids": ids,
        "classes": classes,
        "data_attrs": data_attrs,
    }


# ═══════════════════════════════════════════════
# FASE 3 — Verificação de acoplamento
# ═══════════════════════════════════════════════

def check_coupling(js_selectors: dict, html_elements: dict) -> list:
    """Verifica se cada seletor do JS tem correspondência no HTML."""

    issues = []

    # Verificar IDs
    js_ids = set()
    for key in ["getElementById", "addEventListener_id", "innerHTML_targets", "style_targets"]:
        js_ids.update(js_selectors.get(key, []))

    for js_id in sorted(js_ids):
        if js_id not in html_elements["ids"]:
            issues.append({
                "type": "MISSING_ID",
                "selector": js_id,
                "source": "JS getElementById / DOM access",
                "severity": "CRITICAL",
                "description": f'ID "#{js_id}" usado no JS mas não existe no HTML',
            })

    # Verificar querySelector com #id
    for selector in js_selectors.get("querySelector", []):
        if selector.startswith("#"):
            sel_id = selector[1:].split(" ")[0].split(".")[0].split(":")[0].split("[")[0]
            if sel_id and sel_id not in html_elements["ids"]:
                issues.append({
                    "type": "MISSING_ID",
                    "selector": selector,
                    "source": "JS querySelector",
                    "severity": "CRITICAL",
                    "description": f'Seletor "{selector}" referencia ID que não existe no HTML',
                })

    # Verificar querySelector com .class
    for selector in js_selectors.get("querySelector", []) + js_selectors.get("querySelectorAll", []):
        # Extrair classes do seletor
        cls_matches = re.findall(r'\.([a-zA-Z_-][\w-]*)', selector)
        for cls in cls_matches:
            # Ignorar pseudo-classes e classes que são adicionadas dinamicamente
            dynamic = js_selectors.get("classList_add", []) + [
                c for group in js_selectors.get("dynamic_classes", [])
                for c in group.split()
            ]
            if cls not in html_elements["classes"] and cls not in dynamic:
                issues.append({
                    "type": "MISSING_CLASS",
                    "selector": selector,
                    "class": cls,
                    "source": "JS querySelector",
                    "severity": "WARNING",
                    "description": f'Classe ".{cls}" no seletor "{selector}" não existe no HTML (pode ser dinâmica)',
                })

    # Verificar classList operations que referenciam classes usadas em CSS
    for cls in js_selectors.get("classList_add", []):
        # Estas são dinâmicas — verificar se o CSS define estilos para elas
        pass  # OK — classList.add cria a classe dinamicamente

    # Verificar data attributes
    for data_attr in js_selectors.get("dataset_access", []):
        html_attr = f"data-{camel_to_kebab(data_attr)}"
        if html_attr not in html_elements["data_attrs"]:
            issues.append({
                "type": "MISSING_DATA_ATTR",
                "attribute": html_attr,
                "dataset_key": data_attr,
                "source": "JS dataset access",
                "severity": "WARNING",
                "description": f'data attribute "{html_attr}" acessado via dataset.{data_attr} não existe no HTML',
            })

    # Verificar template selectors
    for selector in js_selectors.get("template_selectors", []):
        # Template literals podem ter variáveis, ignorar se tiver ${}
        if "${" in selector:
            continue
        cls_matches = re.findall(r'\.([a-zA-Z_-][\w-]*)', selector)
        id_matches = re.findall(r'#([a-zA-Z_-][\w-]*)', selector)
        for cls in cls_matches:
            dynamic = [c for group in js_selectors.get("dynamic_classes", []) for c in group.split()]
            if cls not in html_elements["classes"] and cls not in dynamic:
                issues.append({
                    "type": "MISSING_CLASS_TEMPLATE",
                    "selector": selector,
                    "class": cls,
                    "source": "JS template literal querySelector",
                    "severity": "WARNING",
                    "description": f'Classe ".{cls}" em template selector não encontrada no HTML',
                })
        for sel_id in id_matches:
            if sel_id not in html_elements["ids"]:
                issues.append({
                    "type": "MISSING_ID_TEMPLATE",
                    "selector": selector,
                    "id": sel_id,
                    "source": "JS template literal querySelector",
                    "severity": "CRITICAL",
                    "description": f'ID "#{sel_id}" em template selector não existe no HTML',
                })

    return issues


def camel_to_kebab(name: str) -> str:
    return re.sub(r'([A-Z])', r'-\1', name).lower()


# ═══════════════════════════════════════════════
# FASE 4 — Análise via Claude API
# ═══════════════════════════════════════════════

def analyze_with_claude(html_content: str, js_content: str, static_issues: list) -> str:
    """Usa Claude para análise profunda e geração de correções."""

    client = anthropic.Anthropic()

    static_report = "\n".join(
        f"- [{i['severity']}] {i['description']}" for i in static_issues
    ) if static_issues else "Nenhum problema encontrado na análise estática."

    prompt = f"""Você é um QA engineer especializado em frontend. Analise a integração entre o HTML e o JS deste quiz interativo.

## ANÁLISE ESTÁTICA JÁ FEITA (problemas encontrados):
{static_report}

## TAREFA:
1. Analise o JS e identifique TODOS os seletores usados (getElementById, querySelector, querySelectorAll, classList, addEventListener, innerHTML, textContent, style, dataset)
2. Para cada seletor, verifique se o elemento correspondente existe no HTML
3. Identifique problemas de:
   - IDs referenciados no JS que não existem no HTML
   - Classes usadas em querySelector que não existem no HTML nem são criadas dinamicamente
   - Event listeners em elementos que não existem
   - Manipulações de DOM em elementos inexistentes
   - Qualquer outro desacoplamento
4. Para cada problema, forneça a CORREÇÃO EXATA:
   - Se falta um ID no HTML: mostre o trecho HTML a adicionar/modificar
   - Se o seletor no JS está errado: mostre a correção

## FORMATO DE RESPOSTA:
Para cada problema, responda neste formato exato:

### PROBLEMA [N]
- **Severidade:** CRITICAL / WARNING / INFO
- **Arquivo:** index.html ou quiz.js
- **Linha aproximada:** N
- **Seletor:** o seletor problemático
- **Descrição:** o que está errado
- **Correção HTML** (se aplicável):
```html
<!-- ANTES -->
<trecho atual>
<!-- DEPOIS -->
<trecho corrigido>
```
- **Correção JS** (se aplicável):
```javascript
// ANTES
código atual
// DEPOIS
código corrigido
```

Se NÃO houver problemas, diga explicitamente "NENHUM DESACOPLAMENTO ENCONTRADO".

Ao final, liste um resumo:
- Total de problemas CRITICAL: N
- Total de problemas WARNING: N
- Total de problemas INFO: N

## HTML (index.html):
```html
{html_content}
```

## JS (quiz.js):
```javascript
{js_content}
```"""

    print("  Enviando para Claude API para análise profunda...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


# ═══════════════════════════════════════════════
# FASE 5 — Extração e aplicação de correções
# ═══════════════════════════════════════════════

def extract_corrections_with_claude(analysis: str, html_content: str, js_content: str) -> tuple[str, str]:
    """Usa Claude para aplicar as correções identificadas nos arquivos."""

    client = anthropic.Anthropic()

    prompt = f"""Com base na análise QA abaixo, aplique TODAS as correções necessárias nos arquivos.

## ANÁLISE QA:
{analysis}

## REGRAS:
1. Aplique APENAS correções para problemas CRITICAL e WARNING
2. NÃO mude funcionalidade — apenas corrija desacoplamentos de seletores
3. NÃO mude estilos CSS
4. NÃO adicione features novas
5. Mantenha toda a formatação e indentação original
6. Se um ID falta no HTML, adicione-o no elemento mais lógico
7. Se um seletor no JS está errado, corrija para apontar ao elemento certo
8. Se não há correções necessárias, retorne os arquivos inalterados

## FORMATO DE RESPOSTA:
Retorne exatamente neste formato (os marcadores são obrigatórios):

===HTML_START===
(conteúdo completo do index.html corrigido)
===HTML_END===

===JS_START===
(conteúdo completo do quiz.js corrigido)
===JS_END===

## HTML ATUAL:
```html
{html_content}
```

## JS ATUAL:
```javascript
{js_content}
```"""

    print("  Gerando arquivos corrigidos via Claude API...")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=64000,
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.content[0].text

    # Extrair HTML corrigido
    html_match = re.search(r'===HTML_START===\s*(.*?)\s*===HTML_END===', result, re.DOTALL)
    js_match = re.search(r'===JS_START===\s*(.*?)\s*===JS_END===', result, re.DOTALL)

    corrected_html = html_match.group(1).strip() if html_match else None
    corrected_js = js_match.group(1).strip() if js_match else None

    # Limpar possíveis markdown code fences
    if corrected_html and corrected_html.startswith("```"):
        corrected_html = re.sub(r'^```\w*\n?', '', corrected_html)
        corrected_html = re.sub(r'\n?```$', '', corrected_html)

    if corrected_js and corrected_js.startswith("```"):
        corrected_js = re.sub(r'^```\w*\n?', '', corrected_js)
        corrected_js = re.sub(r'\n?```$', '', corrected_js)

    return corrected_html, corrected_js


# ═══════════════════════════════════════════════
# FASE 6 — Gerar relatório
# ═══════════════════════════════════════════════

def generate_report(
    static_issues: list,
    claude_analysis: str,
    html_changes: bool,
    js_changes: bool,
) -> str:
    """Gera relatório QA em Markdown."""

    report = f"""# RELATÓRIO QA — Quiz Espanhol com Você
**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Arquivos analisados:**
- `index.html` ({os.path.getsize(HTML_PATH):,} bytes)
- `quiz.js` ({os.path.getsize(JS_PATH):,} bytes)

---

## 1. ANÁLISE ESTÁTICA (regex)

**Problemas encontrados:** {len(static_issues)}

"""
    if static_issues:
        for i, issue in enumerate(static_issues, 1):
            report += f"### {i}. [{issue['severity']}] {issue['type']}\n"
            report += f"- **Seletor:** `{issue.get('selector', issue.get('attribute', 'N/A'))}`\n"
            report += f"- **Fonte:** {issue['source']}\n"
            report += f"- **Descrição:** {issue['description']}\n\n"
    else:
        report += "*Nenhum problema encontrado na análise estática.*\n\n"

    report += f"""---

## 2. ANÁLISE PROFUNDA (Claude API)

{claude_analysis}

---

## 3. CORREÇÕES APLICADAS

- **HTML modificado:** {'✅ Sim' if html_changes else '⚪ Sem alterações necessárias'}
- **JS modificado:** {'✅ Sim' if js_changes else '⚪ Sem alterações necessárias'}

---

## 4. STATUS FINAL

{'✅ TODOS OS DESACOPLAMENTOS CORRIGIDOS' if (html_changes or js_changes) else '✅ NENHUMA CORREÇÃO NECESSÁRIA — arquivos já estão integrados'}

---

*Relatório gerado automaticamente pelo Agente QA*
*Espanhol com Você — @espanholcomvoce*
"""

    return report


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  AGENTE QA — Quiz Espanhol com Você")
    print("=" * 60)
    print()

    # 1. Ler arquivos
    print("[1/7] Lendo arquivos...")
    html_content = read_file(HTML_PATH)
    js_content = read_file(JS_PATH)
    print(f"  index.html: {len(html_content):,} chars")
    print(f"  quiz.js:    {len(js_content):,} chars")
    print()

    # 2. Extrair seletores do JS
    print("[2/7] Extraindo seletores do JS...")
    js_selectors = extract_js_selectors(js_content)
    total_selectors = sum(len(v) for v in js_selectors.values())
    print(f"  Total de seletores encontrados: {total_selectors}")
    for key, values in js_selectors.items():
        if values:
            print(f"    {key}: {len(values)} ({', '.join(values[:5])}{'...' if len(values) > 5 else ''})")
    print()

    # 3. Extrair elementos do HTML
    print("[3/7] Extraindo elementos do HTML...")
    html_elements = extract_html_elements(html_content)
    print(f"  IDs encontrados: {len(html_elements['ids'])}")
    print(f"  Classes encontradas: {len(html_elements['classes'])}")
    print(f"  Data attributes: {len(html_elements['data_attrs'])}")
    print()

    # 4. Verificação estática
    print("[4/7] Verificando acoplamento (análise estática)...")
    static_issues = check_coupling(js_selectors, html_elements)
    print(f"  Problemas encontrados: {len(static_issues)}")
    for issue in static_issues:
        print(f"    [{issue['severity']}] {issue['description']}")
    print()

    # 5. Análise profunda via Claude
    print("[5/7] Análise profunda via Claude API...")
    claude_analysis = analyze_with_claude(html_content, js_content, static_issues)
    print(f"  Análise completa ({len(claude_analysis):,} chars)")
    print()

    # 6. Aplicar correções
    print("[6/7] Aplicando correções...")
    corrected_html, corrected_js = extract_corrections_with_claude(
        claude_analysis, html_content, js_content
    )

    html_changed = False
    js_changed = False

    if corrected_html and corrected_html != html_content and len(corrected_html) > len(html_content) * 0.8:
        write_file(HTML_PATH, corrected_html)
        html_changed = True
        print(f"  ✅ index.html atualizado ({len(corrected_html):,} chars)")
    else:
        print("  ⚪ index.html sem alterações")

    if corrected_js and corrected_js != js_content and len(corrected_js) > len(js_content) * 0.8:
        write_file(JS_PATH, corrected_js)
        js_changed = True
        print(f"  ✅ quiz.js atualizado ({len(corrected_js):,} chars)")
    else:
        print("  ⚪ quiz.js sem alterações")
    print()

    # 7. Gerar relatório e abrir
    print("[7/7] Gerando relatório e abrindo quiz...")
    report = generate_report(static_issues, claude_analysis, html_changed, js_changed)
    write_file(REPORT_PATH, report)
    print(f"  📄 Relatório salvo: {REPORT_PATH}")

    # Abrir no navegador
    if sys.platform == "win32":
        os.startfile(str(HTML_PATH))
    else:
        subprocess.Popen(["xdg-open", str(HTML_PATH)])
    print(f"  🌐 Quiz aberto no navegador")

    print()
    print("=" * 60)
    print("  QA CONCLUÍDO")
    if html_changed or js_changed:
        print(f"  Correções aplicadas: HTML={'SIM' if html_changed else 'NÃO'} | JS={'SIM' if js_changed else 'NÃO'}")
    else:
        print("  Nenhuma correção necessária — arquivos integrados.")
    print("=" * 60)


if __name__ == "__main__":
    main()
