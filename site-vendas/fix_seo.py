import re

with open("D:/EspanholComVoce/site-vendas/index.html", "r", encoding="utf-8") as f:
    html = f.read()

changes = []

# =============================================
# 1. META TITLE + DESCRIPTION + OG TAGS
# =============================================
old_head = """<title>Programa Imersao Nativa - Espanhol com Voce</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@400;600;700;900&display=swap" rel="stylesheet">"""

new_head = """<title>Aprenda Espanhol Online para Brasileiros | Imersão Nativa</title>
<meta name="description" content="Destravar o espanhol em até 6 meses com o método Imersão Nativa. Aulas curtas, app exclusivo e suporte 24h. Mais de 5.000 alunos. Garantia de 7 dias.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://espanholcomvoce.com/">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:title" content="Programa Imersão Nativa | Espanhol para Brasileiros">
<meta property="og:description" content="Fale espanhol com confiança em até 6 meses. Método criado por nativa colombiana, com app exclusivo e suporte 24h. 5.000+ alunos.">
<meta property="og:url" content="https://espanholcomvoce.com/">
<meta property="og:site_name" content="Espanhol com Você">
<meta property="og:locale" content="pt_BR">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Programa Imersão Nativa | Espanhol para Brasileiros">
<meta name="twitter:description" content="Fale espanhol com confiança em até 6 meses. Método criado por nativa colombiana, com app exclusivo e suporte 24h.">

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Lato:wght@400;600;700;900&display=swap" rel="stylesheet">"""

if old_head in html:
    html = html.replace(old_head, new_head)
    changes.append("1. Meta title + description + OG tags: OK")
else:
    changes.append("1. Meta title: NOT FOUND")

# =============================================
# 2. HIERARQUIA H1 H2 H3
# Only 1 H1 (already in Hero). Convert sub-section H2s to H3 where appropriate.
# Keep main section H2s, demote internal H2s within pilares to H3.
# =============================================

# Pilar 1 internal H2 -> H3
html = html.replace(
    '<h2 class="journey-h2">Do zero à <em>fluência</em> em 24 semanas</h2>',
    '<h3 class="journey-h2">Do zero à <em>fluência</em> em 24 semanas</h3>'
)

# Pilar 2 internal H2 -> H3
html = html.replace(
    '<h2 class="main-h2">Não é apenas um <em>App de espanhol</em></h2>',
    '<h3 class="main-h2">Não é apenas um <em>App de espanhol</em></h3>'
)

# Pilar 3 internal H2 -> H3
html = html.replace(
    '<h2 class="main-h2">Você <em>nunca</em> estuda sozinho</h2>',
    '<h3 class="main-h2">Você <em>nunca</em> estuda sozinho</h3>'
)

changes.append("2. H1/H2/H3 hierarchy: fixed (3 internal H2s demoted to H3)")

# =============================================
# 3. LAZY LOADING on images
# Add loading="lazy" to all <img> that don't have it
# =============================================
count_lazy = 0
def add_lazy(match):
    global count_lazy
    tag = match.group(0)
    if 'loading=' not in tag:
        count_lazy += 1
        return tag.replace('<img ', '<img loading="lazy" ')
    return tag

html = re.sub(r'<img [^>]+>', add_lazy, html)
changes.append(f"3. Lazy loading: added to {count_lazy} images")

# =============================================
# 4. IFRAME lazy loading
# =============================================
count_iframe = 0
def add_iframe_lazy(match):
    global count_iframe
    tag = match.group(0)
    if 'loading=' not in tag:
        count_iframe += 1
        return tag.replace('<iframe ', '<iframe loading="lazy" ')
    return tag

html = re.sub(r'<iframe [^>]+>', add_iframe_lazy, html)
changes.append(f"4. Iframe lazy loading: added to {count_iframe} iframes")

# =============================================
# 5. SCHEMA MARKUP (Course + FAQPage + Person)
# Insert before </body>
# =============================================
schema = """
<!-- Schema Markup: Course -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Course",
  "name": "Programa Imersão Nativa",
  "description": "Curso de espanhol online para brasileiros. Do zero à fluência em 24 semanas com método de imersão, app exclusivo e suporte 24h.",
  "provider": {
    "@type": "Organization",
    "name": "Espanhol com Você",
    "url": "https://espanholcomvoce.com"
  },
  "instructor": {
    "@type": "Person",
    "name": "Alejandra Fajardo",
    "jobTitle": "Professora de Espanhol e Criadora do Programa Imersão Nativa",
    "nationality": "Colombiana"
  },
  "inLanguage": "pt-BR",
  "teaches": "Espanhol",
  "educationalLevel": "Beginner to Advanced (A1-C1)",
  "timeRequired": "P24W",
  "offers": {
    "@type": "Offer",
    "price": "497.00",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock",
    "url": "https://pay.hotmart.com/W10136664F?off=4pflcpst&checkoutMode=10&bid=1762018872179&offDiscount=DESC200"
  },
  "hasCourseInstance": {
    "@type": "CourseInstance",
    "courseMode": "Online",
    "courseWorkload": "PT20M"
  }
}
</script>

<!-- Schema Markup: Person -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Alejandra Fajardo",
  "jobTitle": "Professora de Espanhol",
  "worksFor": {
    "@type": "Organization",
    "name": "Espanhol com Você"
  },
  "knowsLanguage": ["es", "pt"],
  "nationality": {
    "@type": "Country",
    "name": "Colômbia"
  },
  "description": "Nativa colombiana, mora no Brasil há mais de 15 anos. Criadora do Programa Imersão Nativa com mais de 5.000 alunos."
}
</script>

<!-- Schema Markup: FAQPage -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "O curso é para quem está começando do zero?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim! O programa foi criado para quem nunca estudou espanhol ou tem só o básico. Você começa do zero, no seu ritmo, com um método que te coloca em contato com o espanhol real desde a primeira aula."
      }
    },
    {
      "@type": "Question",
      "name": "Preciso ter muito tempo disponível para estudar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Não! Com apenas 15 a 20 minutos por dia você já consegue avançar bastante. O programa foi pensado para quem tem uma rotina ocupada e precisa de praticidade."
      }
    },
    {
      "@type": "Question",
      "name": "Em quanto tempo vou conseguir falar espanhol?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Depende da sua dedicação, mas muitos alunos relatam que em 3 meses já conseguem manter conversas reais em espanhol. O método te prepara para se comunicar de verdade, como um nativo fala."
      }
    },
    {
      "@type": "Question",
      "name": "Como funciona o App exclusivo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ao adquirir o programa, você recebe acesso ao aplicativo exclusivo por 1 ano. Nele você encontra exercícios interativos, áudios nativos, flashcards e acompanhamento do seu progresso."
      }
    },
    {
      "@type": "Question",
      "name": "Tenho garantia caso não me adapte?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim! Você tem 7 dias de garantia incondicional. Se por qualquer motivo não gostar do programa, basta solicitar o reembolso e devolvemos 100% do seu investimento, sem perguntas."
      }
    },
    {
      "@type": "Question",
      "name": "Por quanto tempo tenho acesso?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O acesso ao programa (curso) é vitalício. Já o acesso ao aplicativo exclusivo é por 1 ano a partir da data da sua compra."
      }
    },
    {
      "@type": "Question",
      "name": "Não tenho talento para idiomas. Funciona mesmo assim?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "O problema não é você, é o método. Aqui você aprende como um nativo aprende: ouvindo, repetindo e praticando em contexto real. Talento não é pré-requisito."
      }
    },
    {
      "@type": "Question",
      "name": "Já tentei outros cursos e não funcionou. Por que esse seria diferente?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Porque a maioria dos cursos te ensina a traduzir, não a pensar em espanhol. A Imersão Nativa trabalha com o espanhol real, expressões, pronúncia e situações do dia a dia, para que você pare de traduzir e comece a falar."
      }
    }
  ]
}
</script>
"""

html = html.replace('</body>', schema + '</body>')
changes.append("5. Schema markup (Course + Person + FAQPage): OK")

# =============================================
# SAVE
# =============================================
with open("D:/EspanholComVoce/site-vendas/index.html", "w", encoding="utf-8") as f:
    f.write(html)

for c in changes:
    print(c)
print(f"\nDone! File size: {len(html)} bytes ({round(len(html)/1024/1024, 1)} MB)")
