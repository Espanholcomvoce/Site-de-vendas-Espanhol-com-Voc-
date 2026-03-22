# Agente de Tracking
Leia sempre o MASTER_BRIEFING.md antes de qualquer ação.
Missão: implementar rastreamento completo para otimizar tráfego pago.

## Criar: assets/js/tracking.js

### Google Tag Manager
- GTM snippet no <head> — substituir GTM_ID
- Eventos: PageView, CTAClick, ScrollDepth (25/50/75/100%), TimeOnPage (30s/60s/180s), VideoPlay

### Meta Pixel
- Pixel snippet no <head> — substituir META_PIXEL_ID
- Eventos: PageView (automático), ViewContent (ao rolar até seção de preço), InitiateCheckout (ao clicar em comprar)

### Auto-attach
- Todos os elementos com class="cta-button" disparam CTAClick automaticamente
- ScrollDepth detecta automaticamente via IntersectionObserver

## Variáveis para substituir antes de publicar
- GTM_ID = GTM-XXXXXXX
- META_PIXEL_ID = XXXXXXXXXXXXXXXXX
