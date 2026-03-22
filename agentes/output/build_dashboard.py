"""
Build Dashboard Abril — Parseia roteiros reais e gera HTML interativo
"""
import re
import json
import os
import sys

MD_PATH = r"D:\EspanholComVoce\agentes\output\calendario_abril_roteiros.md"
OUT_PATH = r"D:\EspanholComVoce\agentes\output\dashboard_abril.html"

# ─── Parse the markdown ───

def parse_calendar(md_text):
    """Extract structured data from the 15k-line markdown."""
    days = []
    current_day = None
    current_post = None
    buffer_lines = []

    lines = md_text.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()

        # ── Detect day headers ──
        # Format 1: "# DIA 1 — QUARTA-FEIRA 01/04/2026"
        # Format 2: "# ║           DIA 6 — SEGUNDA-FEIRA 06/04/2026              ║"
        day_match = re.search(r'DIA\s+(\d+)\s*[-–—]+\s*(\S+)\s+(\d{2}/\d{2})', stripped)
        if day_match:
            # Save previous post
            if current_post and current_day:
                current_post['content'] = '\n'.join(buffer_lines)
                current_day['posts'].append(current_post)
                current_post = None
                buffer_lines = []

            # Save previous day
            if current_day:
                days.append(current_day)

            day_num = int(day_match.group(1))
            weekday = day_match.group(2).strip()
            date_str = day_match.group(3).strip()

            current_day = {
                'day': day_num,
                'theme': '',
                'avatar': '',
                'date': date_str,
                'weekday': weekday,
                'posts': [],
            }
            continue

        # Extract theme from header or nearby line
        if current_day and not current_day['theme']:
            # "TEMA: "Dar uma olhadinha"" or in box headers
            theme_match = re.search(r'TEMA[:\s]*["\u201c]?([^"\u201d\n║]+)', stripped)
            if theme_match:
                current_day['theme'] = theme_match.group(1).strip().rstrip('"').strip()

        # Extract avatar
        if current_day and not current_day['avatar'] and current_post is None:
            avatar_match = re.search(r'(?:Avatar|avatar)[:\s]+(.+)', stripped)
            if avatar_match:
                current_day['avatar'] = avatar_match.group(1).strip()

        # ── Detect post headers ──
        # Format 1: "# POST 1/15 — REEL 09:00 — A1 Expressao"
        # Format 2: "# POST 1/21 — DIA 6 — 09:00 — REEL A1"
        post_match = re.match(r'^#\s*(?:[═╔╗]+\s*)?POST\s+\d+/\d+\s*[-–—]+\s*(.*)', stripped)
        if post_match:
            # Save previous post
            if current_post and current_day:
                current_post['content'] = '\n'.join(buffer_lines)
                current_day['posts'].append(current_post)
                buffer_lines = []

            rest = post_match.group(1)

            # Extract time
            time_match = re.search(r'(\d{2}:\d{2})', rest)
            time_str = time_match.group(1) if time_match else '??:??'

            # Extract format
            fmt = 'CARROSSEL'
            if 'REEL' in rest.upper():
                fmt = 'REEL'

            # Extract type code
            type_match = re.search(r'\b(A[123]|C[123]|D[12]|V[12])\b', rest)
            type_code = type_match.group(1) if type_match else ''

            # Extract title (everything after the last —)
            title_parts = re.split(r'[-–—]', rest)
            title = title_parts[-1].strip() if title_parts else ''
            # Clean quotes from title
            title = re.sub(r'^["\u201c]|["\u201d]$', '', title).strip()

            current_post = {
                'time': time_str,
                'format': fmt,
                'title': title,
                'content': '',
                'hook': '',
                'keyword': '',
                'type_code': type_code,
            }
            buffer_lines = []
            continue

        # ── Collect content for current post ──
        if current_post:
            buffer_lines.append(line)

            # Extract hook from "ALE FALA:" or GANCHO section
            if not current_post['hook']:
                # Look for text after "ALE FALA:"
                ale_match = re.search(r'ALE\s+FALA:\s*$', stripped)
                if ale_match:
                    # Next non-empty line is the hook
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip().strip('"').strip('\u201c\u201d')
                        if next_line and not next_line.startswith('#') and not next_line.startswith('='):
                            current_post['hook'] = next_line[:150]
                            break

                # Or inline: "ALE FALA: "texto""
                ale_inline = re.search(r'ALE\s+FALA:\s*["\u201c]?(.+)', stripped)
                if ale_inline and not current_post['hook']:
                    current_post['hook'] = ale_inline.group(1).strip().strip('"').strip('\u201c\u201d')[:150]

                # Or from TEXTO NA TELA
                texto_match = re.search(r'TEXTO NA TELA[^:]*:\s*$', stripped)
                if texto_match:
                    for j in range(i+1, min(i+3, len(lines))):
                        next_line = lines[j].strip().strip('"').strip('\u201c\u201d')
                        if next_line and not next_line.startswith('#'):
                            current_post['hook'] = next_line[:150]
                            break

            # Extract keyword
            kw_match = re.search(r'(?:keyword|palavra.chave|ManyChat)[:\s]*(TRAVA|MANUAL|METODO|AULA|QUERO)', stripped, re.IGNORECASE)
            if kw_match:
                current_post['keyword'] = kw_match.group(1).upper()

    # Save last post and day
    if current_post and current_day:
        current_post['content'] = '\n'.join(buffer_lines)
        current_day['posts'].append(current_post)
    if current_day:
        days.append(current_day)

    return days


def enrich_days(days):
    """Add missing metadata using the theme calendar data."""
    themes = {
        1: {"theme": "Dar uma olhadinha", "weekday": "Quarta", "date": "01/04", "avatar": "Viajante", "week": 1},
        2: {"theme": "A trava invisível", "weekday": "Quinta", "date": "02/04", "avatar": "Profissional", "week": 1},
        3: {"theme": "Cara de pau", "weekday": "Sexta", "date": "03/04", "avatar": "Todos", "week": 1},
        4: {"theme": "5 minutos que mudam tudo", "weekday": "Sábado", "date": "04/04", "avatar": "Sem tempo", "week": 1},
        5: {"theme": "Você entende mas não fala", "weekday": "Domingo", "date": "05/04", "avatar": "Todos", "week": 1},
        6: {"theme": "Tô nem aí", "weekday": "Segunda", "date": "06/04", "avatar": "Viajante", "week": 2},
        7: {"theme": "O mito da gramática", "weekday": "Terça", "date": "07/04", "avatar": "Acadêmico", "week": 2},
        8: {"theme": "Ficar de bobeira", "weekday": "Quarta", "date": "08/04", "avatar": "Todos", "week": 2},
        9: {"theme": "Por que larguei tudo", "weekday": "Quinta", "date": "09/04", "avatar": "Conexão", "week": 2},
        10: {"theme": "Sei lá", "weekday": "Sexta", "date": "10/04", "avatar": "Viajante", "week": 2},
        11: {"theme": "O método por dentro", "weekday": "Sábado", "date": "11/04", "avatar": "Dúvida", "week": 2},
        12: {"theme": "O circuito desligado", "weekday": "Domingo", "date": "12/04", "avatar": "Todos", "week": 2},
        13: {"theme": "Fazer de conta", "weekday": "Segunda", "date": "13/04", "avatar": "Morar fora", "week": 3},
        14: {"theme": "O app te enganou", "weekday": "Terça", "date": "14/04", "avatar": "App users", "week": 3},
        15: {"theme": "Dar um jeitinho", "weekday": "Quarta", "date": "15/04", "avatar": "Profissional", "week": 3},
        16: {"theme": "5.000 alunos me ensinaram", "weekday": "Quinta", "date": "16/04", "avatar": "Todos", "week": 3},
        17: {"theme": "Passar perrengue", "weekday": "Sexta", "date": "17/04", "avatar": "Viajante", "week": 3},
        18: {"theme": "O suporte que faz diferença", "weekday": "Sábado", "date": "18/04", "avatar": "Medo", "week": 3},
        19: {"theme": "Traduzir na cabeça", "weekday": "Domingo", "date": "19/04", "avatar": "Todos", "week": 3},
        20: {"theme": "Chutar o balde", "weekday": "Segunda", "date": "20/04", "avatar": "Todos", "week": 4},
        21: {"theme": "Decorar é o pior caminho", "weekday": "Terça", "date": "21/04", "avatar": "Acadêmico", "week": 4},
        22: {"theme": "Meio-dia e meia", "weekday": "Quarta", "date": "22/04", "avatar": "Todos", "week": 4},
        23: {"theme": "A mensagem que mudou tudo", "weekday": "Quinta", "date": "23/04", "avatar": "Emocional", "week": 4},
        24: {"theme": "Deixa eu ver se entendi", "weekday": "Sexta", "date": "24/04", "avatar": "Profissional", "week": 4},
        25: {"theme": "A zona de expansão", "weekday": "Sábado", "date": "25/04", "avatar": "Autodidata", "week": 4},
        26: {"theme": "O próximo pode ser você", "weekday": "Domingo", "date": "26/04", "avatar": "Todos", "week": 4},
        27: {"theme": "Por supuesto", "weekday": "Segunda", "date": "27/04", "avatar": "Viajante", "week": 5},
        28: {"theme": "Padrões prontos", "weekday": "Terça", "date": "28/04", "avatar": "Todos", "week": 5},
        29: {"theme": "Dando uma volta", "weekday": "Quarta", "date": "29/04", "avatar": "Morar fora", "week": 5},
        30: {"theme": "O mês que tudo mudou", "weekday": "Quinta", "date": "30/04", "avatar": "Todos", "week": 5},
    }

    for day in days:
        d = day['day']
        if d in themes:
            t = themes[d]
            if not day['theme']:
                day['theme'] = t['theme']
            if not day['weekday']:
                day['weekday'] = t['weekday']
            if not day['date']:
                day['date'] = t['date']
            if not day['avatar']:
                day['avatar'] = t['avatar']
            day['week'] = t['week']

    return days


def extract_post_summary(post):
    """Extract a clean summary from raw post content."""
    content = post.get('content', '')
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]

    # Clean up common markers
    clean_lines = []
    for line in lines:
        # Skip meta lines
        if any(skip in line.lower() for skip in ['hashtag', '---', '===', '```', 'formato:', 'tipo de slide']):
            continue
        # Remove markdown bold markers for display
        line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
        clean_lines.append(line)

    # Get first meaningful chunk (up to ~500 chars)
    summary = '\n'.join(clean_lines[:20])
    if len(summary) > 600:
        summary = summary[:600] + '...'

    return summary


def build_html(days):
    """Generate the complete dashboard HTML."""

    # Prepare JSON data for JS
    js_days = []
    for day in days:
        posts_data = []
        for i, post in enumerate(day.get('posts', [])):
            summary = extract_post_summary(post)
            # Escape for JSON
            summary = summary.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            hook = (post.get('hook', '') or '').replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
            title = (post.get('title', '') or '').replace('\\', '\\\\').replace('"', '\\"')

            fmt = post.get('format', 'CARROSSEL')
            if i == 0:
                fmt = 'REEL'
            elif fmt not in ('REEL', 'CARROSSEL'):
                fmt = 'CARROSSEL'

            posts_data.append({
                'time': post.get('time', ['09:00', '12:00', '19:00'][min(i, 2)]),
                'format': fmt,
                'type_code': post.get('type_code', ''),
                'keyword': post.get('keyword', ''),
                'hook': hook[:150],
                'title': title[:120],
                'summary': summary
            })

        # Ensure 3 posts per day
        while len(posts_data) < 3:
            idx = len(posts_data)
            posts_data.append({
                'time': ['09:00', '12:00', '19:00'][min(idx, 2)],
                'format': 'REEL' if idx == 0 else 'CARROSSEL',
                'type_code': '',
                'keyword': '',
                'hook': '',
                'title': '(conteúdo pendente)',
                'summary': ''
            })

        js_days.append({
            'day': day['day'],
            'date': day.get('date', f"{day['day']:02d}/04"),
            'weekday': day.get('weekday', ''),
            'theme': day.get('theme', ''),
            'avatar': day.get('avatar', ''),
            'week': day.get('week', 1),
            'posts': posts_data[:3]
        })

    data_json = json.dumps(js_days, ensure_ascii=False, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Abril 2026 — Espanhol com Você</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#0a1628; color:#fff; font-family:system-ui,-apple-system,sans-serif; line-height:1.5; }}

/* ── Header ── */
.header {{ background:linear-gradient(180deg,#0f1d35 0%,#0a1628 100%); padding:24px 16px 16px; border-bottom:1px solid rgba(251,191,36,0.15); position:sticky; top:0; z-index:100; }}
.header h1 {{ font-size:22px; font-weight:900; text-align:center; }}
.header h1 span {{ color:#fbbf24; }}
.header-sub {{ text-align:center; color:#94a3b8; font-size:13px; margin-top:2px; }}

/* Stats */
.stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin:16px 0 12px; max-width:600px; margin-left:auto; margin-right:auto; }}
.stat {{ background:#1a2f5a; border-radius:10px; padding:10px 8px; text-align:center; }}
.stat-num {{ font-size:20px; font-weight:800; color:#fbbf24; }}
.stat-label {{ font-size:11px; color:#94a3b8; }}

/* Progress */
.progress-wrap {{ max-width:600px; margin:0 auto 12px; }}
.progress-label {{ font-size:12px; color:#94a3b8; margin-bottom:4px; display:flex; justify-content:space-between; }}
.progress-track {{ height:6px; background:rgba(255,255,255,0.08); border-radius:3px; overflow:hidden; }}
.progress-fill {{ height:100%; background:linear-gradient(90deg,#fbbf24,#f59e0b); border-radius:3px; transition:width 0.5s; }}

/* ── Week nav ── */
.week-nav {{ display:flex; gap:6px; padding:12px 16px; overflow-x:auto; -webkit-overflow-scrolling:touch; position:sticky; top:120px; z-index:90; background:#0a1628; border-bottom:1px solid rgba(255,255,255,0.06); }}
.week-btn {{ flex-shrink:0; padding:8px 16px; border-radius:10px; border:1px solid rgba(255,255,255,0.1); background:transparent; color:#94a3b8; font-size:13px; font-weight:600; cursor:pointer; transition:all 0.2s; white-space:nowrap; }}
.week-btn:hover {{ border-color:rgba(251,191,36,0.3); color:#fff; }}
.week-btn.active {{ background:#fbbf24; color:#0a1628; border-color:#fbbf24; }}

/* ── Week section ── */
.week-section {{ display:none; padding:16px; }}
.week-section.active {{ display:block; }}
.week-title {{ font-size:16px; font-weight:700; color:#94a3b8; margin-bottom:16px; padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.06); }}

/* ── Day card ── */
.day-card {{ background:#1a2f5a; border-radius:14px; margin-bottom:16px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); }}
.day-header {{ padding:14px 16px; cursor:pointer; display:flex; align-items:center; justify-content:space-between; transition:background 0.2s; }}
.day-header:hover {{ background:rgba(251,191,36,0.05); }}
.day-date {{ font-size:14px; font-weight:700; color:#fff; }}
.day-date span {{ color:#94a3b8; font-weight:400; }}
.day-theme {{ font-size:15px; font-weight:700; color:#fbbf24; margin-top:2px; }}
.day-avatar {{ font-size:12px; color:#94a3b8; }}
.day-arrow {{ color:#94a3b8; font-size:18px; transition:transform 0.3s; flex-shrink:0; margin-left:12px; }}
.day-card.expanded .day-arrow {{ transform:rotate(180deg); }}
.day-header-left {{ flex:1; }}

/* Keyword badges on day header */
.day-keywords {{ display:flex; gap:4px; margin-top:6px; flex-wrap:wrap; }}
.kw-badge {{ font-size:10px; font-weight:700; padding:2px 8px; border-radius:6px; text-transform:uppercase; letter-spacing:0.5px; }}
.kw-TRAVA {{ background:rgba(239,68,68,0.15); color:#ef4444; }}
.kw-MANUAL {{ background:rgba(251,191,36,0.15); color:#fbbf24; }}
.kw-METODO {{ background:rgba(56,189,248,0.15); color:#38bdf8; }}
.kw-AULA {{ background:rgba(16,185,129,0.15); color:#10b981; }}
.kw-QUERO {{ background:rgba(168,85,247,0.15); color:#a855f7; }}

/* Day content (expandable) */
.day-content {{ display:none; padding:0 16px 16px; }}
.day-card.expanded .day-content {{ display:block; }}

/* Post card */
.post-card {{ background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:14px; margin-bottom:12px; }}
.post-header {{ display:flex; align-items:center; gap:8px; margin-bottom:8px; }}
.post-icon {{ font-size:18px; }}
.post-time {{ font-size:12px; color:#94a3b8; font-weight:600; }}
.post-format {{ font-size:11px; font-weight:700; padding:2px 8px; border-radius:6px; text-transform:uppercase; }}
.post-format.reel {{ background:rgba(251,191,36,0.15); color:#fbbf24; }}
.post-format.carousel {{ background:rgba(56,189,248,0.15); color:#38bdf8; }}
.post-type {{ font-size:11px; color:#94a3b8; background:rgba(255,255,255,0.06); padding:2px 8px; border-radius:6px; }}

.post-title {{ font-size:14px; font-weight:700; color:#fff; margin-bottom:4px; line-height:1.4; }}
.post-hook {{ font-size:13px; color:#fbbf24; font-style:italic; margin-bottom:8px; line-height:1.4; }}
.post-hook::before {{ content:'"'; }}
.post-hook::after {{ content:'"'; }}

.post-summary {{ font-size:12px; color:#c8d6e5; line-height:1.6; max-height:200px; overflow-y:auto; white-space:pre-line; padding:10px; background:rgba(0,0,0,0.2); border-radius:8px; margin-top:8px; }}

.post-meta {{ display:flex; align-items:center; gap:8px; margin-top:10px; flex-wrap:wrap; }}

/* Status button */
.status-btn {{ font-size:11px; font-weight:600; padding:4px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); background:transparent; color:#94a3b8; cursor:pointer; transition:all 0.2s; }}
.status-btn.gravado {{ background:rgba(251,191,36,0.15); color:#fbbf24; border-color:rgba(251,191,36,0.3); }}
.status-btn.publicado {{ background:rgba(16,185,129,0.15); color:#10b981; border-color:rgba(16,185,129,0.3); }}

/* Toggle full content */
.toggle-content {{ font-size:12px; color:#38bdf8; cursor:pointer; border:none; background:none; padding:4px 0; margin-top:6px; }}
.toggle-content:hover {{ text-decoration:underline; }}

/* ── Responsive ── */
@media(min-width:768px) {{
  .week-section {{ max-width:800px; margin:0 auto; }}
  .header {{ padding:24px 24px 16px; }}
  .stats {{ grid-template-columns:repeat(4,1fr); }}
}}
@media(max-width:400px) {{
  .stats {{ grid-template-columns:repeat(2,1fr); }}
  .stat-num {{ font-size:18px; }}
}}
</style>
</head>
<body>

<div class="header">
  <h1><span>Calendário</span> Abril 2026</h1>
  <div class="header-sub">@espanholcomvoce — 90 roteiros completos</div>

  <div class="stats">
    <div class="stat"><div class="stat-num">90</div><div class="stat-label">posts</div></div>
    <div class="stat"><div class="stat-num">30</div><div class="stat-label">dias</div></div>
    <div class="stat"><div class="stat-num" id="reels-gravados">0</div><div class="stat-label">Reels gravados</div></div>
    <div class="stat"><div class="stat-num" id="publicados">0</div><div class="stat-label">publicados</div></div>
  </div>

  <div class="progress-wrap">
    <div class="progress-label">
      <span>Progresso</span>
      <span id="progress-text">0/90 publicados</span>
    </div>
    <div class="progress-track">
      <div class="progress-fill" id="progress-fill" style="width:0%"></div>
    </div>
  </div>
</div>

<nav class="week-nav" id="week-nav"></nav>
<main id="main-content"></main>

<script>
// ── Data ──
const calendarData = {data_json};

// ── State (localStorage) ──
const STORAGE_KEY = 'ecv_dashboard_abril';
let state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
// state[dayNum_postIdx] = 'gravar' | 'gravado' | 'publicado'

function saveState() {{
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  updateStats();
}}

function getStatus(dayNum, postIdx) {{
  return state[dayNum + '_' + postIdx] || 'gravar';
}}

function cycleStatus(dayNum, postIdx) {{
  const current = getStatus(dayNum, postIdx);
  const next = current === 'gravar' ? 'gravado' : current === 'gravado' ? 'publicado' : 'gravar';
  state[dayNum + '_' + postIdx] = next;
  saveState();
  return next;
}}

// ── Build UI ──
function init() {{
  buildWeekNav();
  buildWeeks();
  showWeek(1);
  updateStats();
}}

function buildWeekNav() {{
  const nav = document.getElementById('week-nav');
  const weeks = [
    {{ num: 1, label: 'Sem 1 (01-05)' }},
    {{ num: 2, label: 'Sem 2 (06-12)' }},
    {{ num: 3, label: 'Sem 3 (13-19)' }},
    {{ num: 4, label: 'Sem 4 (20-26)' }},
    {{ num: 5, label: 'Sem 5 (27-30)' }}
  ];
  weeks.forEach(w => {{
    const btn = document.createElement('button');
    btn.className = 'week-btn';
    btn.dataset.week = w.num;
    btn.textContent = w.label;
    btn.addEventListener('click', () => showWeek(w.num));
    nav.appendChild(btn);
  }});
}}

function showWeek(num) {{
  document.querySelectorAll('.week-btn').forEach(b => b.classList.toggle('active', b.dataset.week == num));
  document.querySelectorAll('.week-section').forEach(s => s.classList.toggle('active', s.dataset.week == num));
}}

function buildWeeks() {{
  const main = document.getElementById('main-content');
  const weeks = {{}};
  calendarData.forEach(day => {{
    const w = day.week || 1;
    if (!weeks[w]) weeks[w] = [];
    weeks[w].push(day);
  }});

  for (const [weekNum, days] of Object.entries(weeks)) {{
    const section = document.createElement('div');
    section.className = 'week-section';
    section.dataset.week = weekNum;

    const weekLabels = {{
      1: 'Semana 1 — 01 a 05 de Abril',
      2: 'Semana 2 — 06 a 12 de Abril',
      3: 'Semana 3 — 13 a 19 de Abril',
      4: 'Semana 4 — 20 a 26 de Abril',
      5: 'Semana 5 — 27 a 30 de Abril'
    }};

    section.innerHTML = '<div class="week-title">' + (weekLabels[weekNum] || 'Semana ' + weekNum) + ' (' + days.length + ' dias, ' + (days.length * 3) + ' posts)</div>';

    days.forEach(day => {{
      section.appendChild(buildDayCard(day));
    }});

    main.appendChild(section);
  }}
}}

function buildDayCard(day) {{
  const card = document.createElement('div');
  card.className = 'day-card';
  card.id = 'day-' + day.day;

  // Collect keywords for this day
  const keywords = [...new Set(day.posts.map(p => p.keyword).filter(k => k))];

  const kwHtml = keywords.map(k => '<span class="kw-badge kw-' + k + '">' + k + '</span>').join('');

  card.innerHTML = `
    <div class="day-header" onclick="toggleDay(${{day.day}})">
      <div class="day-header-left">
        <div class="day-date">${{day.weekday}} <span>${{day.date}}</span></div>
        <div class="day-theme">${{day.theme}}</div>
        <div class="day-avatar">${{day.avatar}}</div>
        <div class="day-keywords">${{kwHtml}}</div>
      </div>
      <div class="day-arrow">▼</div>
    </div>
    <div class="day-content" id="day-content-${{day.day}}">
      ${{day.posts.map((p, i) => buildPostCard(day.day, p, i)).join('')}}
    </div>
  `;

  return card;
}}

function buildPostCard(dayNum, post, idx) {{
  const isReel = post.format === 'REEL';
  const icon = isReel ? '🎬' : '🃏';
  const formatClass = isReel ? 'reel' : 'carousel';
  const formatLabel = isReel ? 'REEL' : 'CARROSSEL';
  const status = getStatus(dayNum, idx);

  const statusLabel = {{
    'gravar': '○ A gravar',
    'gravado': '◐ Gravado',
    'publicado': '● Publicado'
  }}[status];

  const statusClass = status;

  let hookHtml = '';
  if (post.hook) {{
    hookHtml = '<div class="post-hook">' + escapeHtml(post.hook) + '</div>';
  }}

  let summaryHtml = '';
  if (post.summary) {{
    const id = 'summary-' + dayNum + '-' + idx;
    summaryHtml = `
      <button class="toggle-content" onclick="toggleSummary('${{id}}')">▸ Ver roteiro completo</button>
      <div class="post-summary" id="${{id}}" style="display:none">${{escapeHtml(post.summary)}}</div>
    `;
  }}

  const kwHtml = post.keyword ? '<span class="kw-badge kw-' + post.keyword + '">' + post.keyword + '</span>' : '';

  return `
    <div class="post-card">
      <div class="post-header">
        <span class="post-icon">${{icon}}</span>
        <span class="post-time">${{post.time}}</span>
        <span class="post-format ${{formatClass}}">${{formatLabel}}</span>
        ${{post.type_code ? '<span class="post-type">' + post.type_code + '</span>' : ''}}
        ${{kwHtml}}
      </div>
      <div class="post-title">${{escapeHtml(post.title || '(sem título)')}}</div>
      ${{hookHtml}}
      ${{summaryHtml}}
      <div class="post-meta">
        <button class="status-btn ${{statusClass}}" onclick="onStatusClick(${{dayNum}},${{idx}},this)">
          ${{statusLabel}}
        </button>
      </div>
    </div>
  `;
}}

// ── Interactions ──
function toggleDay(dayNum) {{
  const card = document.getElementById('day-' + dayNum);
  card.classList.toggle('expanded');
}}

function toggleSummary(id) {{
  const el = document.getElementById(id);
  const btn = el.previousElementSibling;
  if (el.style.display === 'none') {{
    el.style.display = 'block';
    btn.textContent = '▾ Ocultar roteiro';
  }} else {{
    el.style.display = 'none';
    btn.textContent = '▸ Ver roteiro completo';
  }}
}}

function onStatusClick(dayNum, idx, btn) {{
  const newStatus = cycleStatus(dayNum, idx);
  const labels = {{
    'gravar': '○ A gravar',
    'gravado': '◐ Gravado',
    'publicado': '● Publicado'
  }};
  btn.textContent = labels[newStatus];
  btn.className = 'status-btn ' + newStatus;
}}

function updateStats() {{
  let gravados = 0;
  let publicados = 0;
  const total = calendarData.length * 3;

  calendarData.forEach(day => {{
    day.posts.forEach((_, idx) => {{
      const s = getStatus(day.day, idx);
      if (s === 'gravado') gravados++;
      if (s === 'publicado') publicados++;
    }});
  }});

  // Count Reels gravados (idx 0 = reel)
  let reelsGravados = 0;
  calendarData.forEach(day => {{
    const s = getStatus(day.day, 0);
    if (s === 'gravado' || s === 'publicado') reelsGravados++;
  }});

  document.getElementById('reels-gravados').textContent = reelsGravados;
  document.getElementById('publicados').textContent = publicados;
  document.getElementById('progress-text').textContent = publicados + '/' + total + ' publicados';
  document.getElementById('progress-fill').style.width = (publicados / total * 100) + '%';
}}

function escapeHtml(text) {{
  if (!text) return '';
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

// ── Init ──
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>'''

    return html


# ─── Main ───
def main():
    print("[1/4] Lendo calendario_abril_roteiros.md...")
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_text = f.read()
    print(f"  {len(md_text):,} chars lidos")

    print("[2/4] Parseando 30 dias...")
    days = parse_calendar(md_text)
    print(f"  {len(days)} dias encontrados")

    days = enrich_days(days)

    # Stats
    total_posts = sum(len(d['posts']) for d in days)
    posts_with_hook = sum(1 for d in days for p in d['posts'] if p.get('hook'))
    posts_with_kw = sum(1 for d in days for p in d['posts'] if p.get('keyword'))
    print(f"  {total_posts} posts extraídos")
    print(f"  {posts_with_hook} posts com hook")
    print(f"  {posts_with_kw} posts com keyword")

    print("[3/4] Gerando HTML...")
    html = build_html(days)

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    size = os.path.getsize(OUT_PATH)
    print(f"  Salvo: {OUT_PATH} ({size/1024:.0f} KB)")

    print("[4/4] Abrindo no navegador...")
    if sys.platform == 'win32':
        os.startfile(OUT_PATH)

    print("\nConcluído!")


if __name__ == '__main__':
    main()
