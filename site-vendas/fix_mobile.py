with open("D:/EspanholComVoce/site-vendas/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = []

# =============================================
# 1. GLOBAL MOBILE CSS — insert after first </style>
# =============================================

mobile_css = """
<!-- Mobile & Tablet Optimization -->
<style>
/* ── Global responsive base ── */
body { font-size: 16px; -webkit-text-size-adjust: 100%; }
img { max-width: 100%; height: auto; }
iframe { max-width: 100%; }

/* ── Tablet (768px) ── */
@media (max-width: 768px) {
  /* Padding lateral */
  [class*="section"], section, .c, .bonus-container, .faq-inner, .block-inner {
    padding-left: 20px !important;
    padding-right: 20px !important;
  }

  /* CTAs full width */
  .btn, .cta-btn, .faq-btn, a[href*="hotmart"] {
    display: block !important;
    width: 100% !important;
    max-width: 400px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    text-align: center !important;
  }

  /* Grids to single column */
  .obj-grid, .cg, .dores, .vg, .tgrid, .stats-row, .gg {
    grid-template-columns: 1fr !important;
  }

  /* Headings scale */
  h1, .sec-h2, .comp-h2, .main-title, .section-title, .bonus-title, .faq-title, .gh, .journey-h2, .main-h2, .intro-h2 {
    font-size: clamp(1.3rem, 5vw, 2rem) !important;
    line-height: 1.2 !important;
  }

  /* Cards padding */
  .card, .obj-card, .cc, .dor, .bonus-card, .faq-item {
    padding: 20px !important;
  }

  /* Module 06B tabs — horizontal scroll on tablet */
  #mod06b .tabs {
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    scroll-snap-type: x mandatory;
    justify-content: flex-start !important;
    gap: 8px !important;
    padding-bottom: 8px !important;
  }
  #mod06b .tab {
    flex-shrink: 0 !important;
    scroll-snap-align: start;
    min-width: 120px !important;
    padding: 14px 18px 16px !important;
  }

  /* Module 08 Quem sou eu — stack */
  #mod08 .ag {
    grid-template-columns: 1fr !important;
    gap: 32px !important;
    text-align: center !important;
  }

  /* Module 09 video grid */
  #mod09 .vgrid {
    grid-template-columns: 1fr !important;
  }

  /* Module 10 bonus grid */
  #mod10 .bonus-grid {
    grid-template-columns: 1fr !important;
  }
}

/* ── Mobile (480px) ── */
@media (max-width: 480px) {
  /* Tighter padding */
  [class*="section"], section, .c, .bonus-container, .faq-inner, .block-inner {
    padding-left: 16px !important;
    padding-right: 16px !important;
  }

  /* Smaller headings */
  h1 {
    font-size: 1.25rem !important;
  }
  .sec-h2, .comp-h2, .main-title, .section-title, .bonus-title, .faq-title, .gh, .journey-h2, .main-h2, .intro-h2 {
    font-size: 1.15rem !important;
  }

  /* Body text min size */
  p, span, .item-text, .obj-a, .gp, .faq-answer-inner, .ci, .dor p {
    font-size: 15px !important;
    line-height: 1.6 !important;
  }

  /* CTA buttons — full width */
  .btn, .cta-btn, .faq-btn, a[href*="hotmart"] {
    max-width: 100% !important;
    padding: 16px 24px !important;
    font-size: 13px !important;
  }

  /* Hero section */
  #mod01 .hero {
    padding: 20px 16px 28px !important;
    min-height: auto !important;
  }

  /* Price card */
  #mod11 .card {
    padding: 24px 16px !important;
  }
  #mod11 .price-big {
    font-size: 44px !important;
  }

  /* FAQ question */
  .faq-question {
    font-size: 13px !important;
    padding: 14px 16px !important;
  }

  /* Module 06B tabs — smaller on mobile */
  #mod06b .tab {
    min-width: 100px !important;
    padding: 10px 14px 12px !important;
    font-size: .65rem !important;
  }

  /* Stats row items */
  .stat-num {
    font-size: 1.8rem !important;
  }

  /* Guarantee layout */
  #mod12 .gg {
    grid-template-columns: 1fr !important;
    text-align: center !important;
  }
  #mod12 .selo-wrap {
    display: flex !important;
    justify-content: center !important;
  }
  #mod12 .selo-wrap img {
    width: 140px !important;
  }
}

/* ── Sticky CTA — mobile only ── */
@media (max-width: 768px) {
  .sticky-cta {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: rgba(255, 255, 255, 0.97);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 12px 16px;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    transform: translateY(100%);
    transition: transform 0.3s ease;
  }
  .sticky-cta.visible {
    transform: translateY(0);
  }
  .sticky-cta a {
    display: block;
    width: 100%;
    max-width: 400px;
    background: linear-gradient(135deg, #fbbf24 0%, #fb923c 100%);
    color: #0a1628;
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-decoration: none;
    text-align: center;
    padding: 16px 24px;
    border-radius: 50px;
    box-shadow: 0 4px 16px rgba(251, 191, 36, 0.4);
  }

  /* Add bottom padding to body so sticky doesn't cover content */
  body { padding-bottom: 72px !important; }
}

/* ── Hide sticky CTA on desktop ── */
@media (min-width: 769px) {
  .sticky-cta { display: none !important; }
}
</style>
"""

# Insert after the closing of first <style> block
first_style_end = html.find('</style>')
if first_style_end != -1:
    insert_pos = first_style_end + len('</style>')
    html = html[:insert_pos] + mobile_css + html[insert_pos:]
    changes.append("1. Global mobile CSS: inserted")
else:
    changes.append("1. Global mobile CSS: FAILED - no </style> found")

# =============================================
# 2. STICKY CTA HTML + JS — insert before </body>
# =============================================

sticky_html = """
<!-- Sticky CTA Mobile -->
<div class="sticky-cta" id="stickyCta">
  <a href="https://pay.hotmart.com/W10136664F?off=4pflcpst&checkoutMode=10&bid=1762018872179&offDiscount=DESC200">
    Quero Destravar Meu Espanhol &rarr;
  </a>
</div>

<script>
(function(){
  var sticky = document.getElementById('stickyCta');
  if (!sticky) return;

  // Show sticky after scrolling past hero (mod01)
  var hero = document.getElementById('mod01');
  if (!hero) return;

  var heroBottom = hero.offsetTop + hero.offsetHeight;
  var shown = false;

  function checkSticky() {
    var scrollY = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollY > heroBottom && !shown) {
      sticky.classList.add('visible');
      shown = true;
    } else if (scrollY <= heroBottom && shown) {
      sticky.classList.remove('visible');
      shown = false;
    }
  }

  var timer = null;
  window.addEventListener('scroll', function() {
    if (timer) return;
    timer = setTimeout(function() {
      timer = null;
      checkSticky();
    }, 100);
  }, { passive: true });

  // Initial check
  checkSticky();
})();
</script>
"""

# Find the schema markup section to insert before it
schema_marker = '\n<!-- Schema Markup: Course -->'
if schema_marker in html:
    html = html.replace(schema_marker, sticky_html + schema_marker)
    changes.append("2. Sticky CTA HTML + JS: inserted")
else:
    # Fallback: insert before </body>
    html = html.replace('</body>', sticky_html + '</body>')
    changes.append("2. Sticky CTA HTML + JS: inserted before </body>")

# =============================================
# 3. Add touch-action to tabs for better mobile UX
# =============================================
old_tabs = '#mod06b .tabs {\n    flex-wrap: wrap;'
new_tabs = '#mod06b .tabs {\n    flex-wrap: wrap;\n    touch-action: pan-x;'

# Try scoped version
if '#mod06b .tabs {' in html:
    # Check if touch-action already exists
    if 'touch-action' not in html.split('#mod06b .tabs')[1][:200]:
        html = html.replace(
            '#mod06b .tabs {\n    display: flex;',
            '#mod06b .tabs {\n    display: flex;\n    touch-action: pan-x;'
        )
        changes.append("3. Touch-action on tabs: added")
    else:
        changes.append("3. Touch-action on tabs: already exists")
else:
    changes.append("3. Touch-action on tabs: selector not found (handled via media query)")

# =============================================
# SAVE
# =============================================
with open("D:/EspanholComVoce/site-vendas/index.html", "w", encoding="utf-8") as f:
    f.write(html)

for c in changes:
    print(c)
print(f"\nDone! File size: {len(html)} bytes ({round(len(html)/1024/1024, 1)} MB)")
