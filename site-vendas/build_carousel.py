# -*- coding: utf-8 -*-
"""Adiciona carrossel de 16 depoimentos ao M07 na v3"""

with open("D:/EspanholComVoce/site-vendas/index_v3.html", "r", encoding="utf-8") as f:
    html = f.read()

# Dados dos 16 depoimentos (4 slides de 4)
depoimentos = [
    # Slide 1
    {"nome": "Fernanda De Oliveira", "ig": "@feoliveira.26", "foto": "fernanda-oliveira.png",
     "texto": "Trabalho com projetos na LATAM e o curso tem me ajudado muito. Vale muito a pena e indico de olhos fechados!"},
    {"nome": "Diego Costa", "ig": "@diegodygavira", "foto": "diego-costa.png",
     "texto": "Estou indo morar no Chile. A Alejandra é extremamente atenciosa, incentiva, ajuda e acima de tudo, torce por você!"},
    {"nome": "Cybelle Leal Reis", "ig": "@cybellelealreis", "foto": "cybelle-reis.png",
     "texto": "Em pouco tempo consegui destravar. Abriu portas para compreender uma cultura vibrante e cheia de vida."},
    {"nome": "Fernanda Romero", "ig": "@eufer.romero", "foto": "fernanda-romero.png",
     "texto": "A Alejandra é simplesmente sensacional! Sempre disponível e com uma didática impecável!"},
    # Slide 2
    {"nome": "Ronaldo Sales", "ig": "@ronaldoaraujopsi", "foto": "ronaldo-sales.png",
     "texto": "Metodologia simples de compreender sem deixar o rigor acadêmico. A professora Alejandra é muito acolhedora."},
    {"nome": "Monalisa dos Santos", "ig": "@monalisa.santospereira", "foto": "monalisa-santos.png",
     "texto": "Meu vocabulário evoluiu muito, o que em curso tradicional precisaria de bem mais tempo. O método é intuitivo e leve."},
    {"nome": "Rodrigo Berghahn", "ig": "@rodrigoberghahn", "foto": "rodrigo-berghahn.png",
     "texto": "O método da professora Alejandra nos faz aprender de uma forma descomplicada."},
    {"nome": "Lund De Castro", "ig": "@lundcals", "foto": "lund-castro.png",
     "texto": "Feito especialmente para brasileiros. A gramática é apresentada sem complicações. Estou sentindo progresso real."},
    # Slide 3
    {"nome": "Manuelle Faustino", "ig": "@manuellefaustino_mf", "foto": "manuelle-faustino.png",
     "texto": "Único curso que consegui adaptar na minha rotina com alta qualidade. O valor é baixo para a entrega de alto nível."},
    {"nome": "Gabriel Ramos", "ig": "@G-RAMOSSIL", "foto": "gabriel-ramos.png",
     "texto": "O curso te estimula a praticar e associar à sua realidade pessoal. Ajuda a destravar e acreditar no seu potencial!"},
    {"nome": "Josie dos Santos", "ig": "@josiesanli13", "foto": "josie-santos.png",
     "texto": "A metodologia é dinâmica. O esclarecimento das dúvidas via WhatsApp é excelente! Melhor escolha do ano."},
    {"nome": "Luciane Oliveira", "ig": "@lucianediasdeoliveira", "foto": "luciane-oliveira.png",
     "texto": "Videoaulas curtas e práticas. Ela está sempre disponível no WhatsApp. Isso é um diferencial incrível!"},
    # Slide 4
    {"nome": "Gabriel Erom", "ig": "@gabriel.errm", "foto": "gabriel-erom.png",
     "texto": "Você que quer sair do portunhol e se tornar bilíngue, eu te afirmo com toda certeza que vale a pena. EU TE AVISEI."},
    {"nome": "Gisele Garrido", "ig": "@Gisa05", "foto": "gisele-garrido.png",
     "texto": "Achei que fosse desistir, mas ela com sua segurança e preocupação me fez crer e continuar. Obrigada por não desistir de mim!"},
    {"nome": "Larrissa Marucci", "ig": "@larimarucci_", "foto": "larrissa-marucci.png",
     "texto": "Eu não sabia que tinha essa habilidade para falar espanhol tão rápido. O curso é muito completo!"},
    {"nome": "Jesús Henrique", "ig": "@jesus_henrique_1966", "foto": "jesus-henrique.png",
     "texto": "Eu consigo ver minha evolução. Recomendo a todos que realmente querem aprender espanhol e por um preço justo!"},
]

# CSS do carrossel
carousel_css = """
/* Carousel de depoimentos */
#mod07 .carousel-wrap {
  position: relative;
  margin-top: 32px;
  overflow: hidden;
}
#mod07 .carousel-track {
  display: flex;
  transition: transform 0.4s ease;
}
#mod07 .carousel-slide {
  min-width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 0 4px;
}
@media (max-width: 768px) {
  #mod07 .carousel-slide {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
}
@media (max-width: 480px) {
  #mod07 .carousel-slide {
    grid-template-columns: 1fr;
  }
}
#mod07 .c-card {
  background: #ffffff;
  border: 1px solid rgba(10,22,40,.08);
  border-left: 3px solid #0090be;
  border-radius: 10px;
  padding: 14px;
  transition: transform .25s, box-shadow .25s;
}
#mod07 .c-card:nth-child(2) { border-left-color: #36c551; }
#mod07 .c-card:nth-child(3) { border-left-color: #ffcb15; }
#mod07 .c-card:nth-child(4) { border-left-color: #0090be; }
#mod07 .c-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(10,22,40,.08);
}
#mod07 .c-card-text {
  font-size: .8rem;
  line-height: 1.5;
  color: #475569;
  font-style: italic;
  margin-bottom: 12px;
}
#mod07 .c-card-author {
  display: flex;
  align-items: center;
  gap: 8px;
  border-top: 1px solid rgba(10,22,40,.06);
  padding-top: 10px;
}
#mod07 .c-card-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: #fff;
  border: 2px solid #fff;
  box-shadow: 0 0 0 1px #0090be;
  flex-shrink: 0;
}
#mod07 .c-card-avatar img {
  width: 100%; height: 100%;
  object-fit: cover; display: block;
}
#mod07 .c-card-name {
  font-size: .75rem;
  font-weight: 700;
  color: #001e38;
}
#mod07 .c-card-ig {
  font-size: .7rem;
  color: #0090be;
}
#mod07 .c-card-stars {
  font-size: .7rem;
  color: #ffcb15;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
/* Navigation */
#mod07 .carousel-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
}
#mod07 .carousel-btn {
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(0,144,190,.3);
  background: #fff;
  color: #0090be;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .2s;
}
#mod07 .carousel-btn:hover {
  background: #0090be;
  color: #fff;
}
#mod07 .carousel-dots {
  display: flex;
  gap: 6px;
}
#mod07 .carousel-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: rgba(0,144,190,.2);
  cursor: pointer;
  transition: all .2s;
}
#mod07 .carousel-dot.active {
  background: #0090be;
  width: 24px;
  border-radius: 4px;
}
"""

# Gerar HTML dos cards
def make_card(d):
    return f'''<div class="c-card">
          <div class="c-card-stars">\u2605\u2605\u2605\u2605\u2605</div>
          <p class="c-card-text">"{d['texto']}"</p>
          <div class="c-card-author">
            <div class="c-card-avatar"><img src="assets/depoimentos/{d['foto']}" alt="{d['nome']}"></div>
            <div>
              <div class="c-card-name">{d['nome']}</div>
              <div class="c-card-ig">{d['ig']}</div>
            </div>
          </div>
        </div>'''

# Gerar slides
slides_html = ""
for i in range(4):
    cards = "\n        ".join([make_card(depoimentos[i*4+j]) for j in range(4)])
    slides_html += f'''
      <div class="carousel-slide">
        {cards}
      </div>'''

carousel_html = f"""
    <!-- Carrossel de depoimentos -->
    <div class="carousel-wrap">
      <div class="carousel-track" id="carouselTrack">
{slides_html}
      </div>
      <div class="carousel-nav">
        <button class="carousel-btn" onclick="moveCarousel(-1)">\u2039</button>
        <div class="carousel-dots">
          <div class="carousel-dot active" onclick="goToSlide(0)"></div>
          <div class="carousel-dot" onclick="goToSlide(1)"></div>
          <div class="carousel-dot" onclick="goToSlide(2)"></div>
          <div class="carousel-dot" onclick="goToSlide(3)"></div>
        </div>
        <button class="carousel-btn" onclick="moveCarousel(1)">\u203a</button>
      </div>
    </div>
"""

carousel_script = """
<script>
(function(){
  var currentSlide = 0;
  var totalSlides = 4;
  var track = document.getElementById('carouselTrack');
  if(!track) return;

  window.moveCarousel = function(dir) {
    currentSlide = (currentSlide + dir + totalSlides) % totalSlides;
    updateCarousel();
  };
  window.goToSlide = function(idx) {
    currentSlide = idx;
    updateCarousel();
  };
  function updateCarousel() {
    track.style.transform = 'translateX(-' + (currentSlide * 100) + '%)';
    var dots = document.querySelectorAll('#mod07 .carousel-dot');
    dots.forEach(function(d, i) {
      d.classList.toggle('active', i === currentSlide);
    });
  }

  // Touch/swipe support
  var startX = 0;
  track.addEventListener('touchstart', function(e) { startX = e.touches[0].clientX; }, {passive:true});
  track.addEventListener('touchend', function(e) {
    var diff = startX - e.changedTouches[0].clientX;
    if(Math.abs(diff) > 50) moveCarousel(diff > 0 ? 1 : -1);
  }, {passive:true});
})();
</script>
"""

# Inserir CSS antes do </style> do mod07
style_end = html.find('</style>', html.find('<!-- Styles: mod07 -->'))
html = html[:style_end] + carousel_css + html[style_end:]

# Inserir HTML antes do CTA do mod07
cta_marker = html.find('QUERO TER RESULTADOS', html.find('id="mod07"'))
if cta_marker > 0:
    cta_div = html.rfind('<div style="text-align:center', html.find('id="mod07"'), cta_marker)
    html = html[:cta_div] + carousel_html + "\n    " + html[cta_div:]
else:
    # Inserir antes do fechamento do mod07
    m07_end = html.find('</div>\n</div>', html.find('id="mod07"'))
    html = html[:m07_end] + carousel_html + html[m07_end:]

# Inserir script antes do </body> ou antes dos schemas
schema_pos = html.find('<!-- Schema')
if schema_pos > 0:
    html = html[:schema_pos] + carousel_script + "\n" + html[schema_pos:]
else:
    html = html.replace('</body>', carousel_script + '</body>')

with open("D:/EspanholComVoce/site-vendas/index_v3.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Carrossel 16 depoimentos adicionado. Size: {len(html)} bytes")
