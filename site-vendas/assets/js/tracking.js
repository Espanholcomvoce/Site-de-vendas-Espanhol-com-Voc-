/**
 * tracking.js — Espanhol com Você | Programa Imersão Nativa
 *
 * ANTES DE PUBLICAR, substituir:
 *   GTM_ID         → seu ID do Google Tag Manager (ex: GTM-XXXXXXX)
 *   META_PIXEL_ID  → seu ID do Meta Pixel (ex: 1234567890123456)
 */

(function () {
  'use strict';

  var GTM_ID = 'GTM-WZ9KJZDQ';
  var META_PIXEL_ID = '404764304424371';

  // =============================================
  // 1. GOOGLE TAG MANAGER
  // =============================================
  (function (w, d, s, l, i) {
    w[l] = w[l] || [];
    w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var f = d.getElementsByTagName(s)[0],
      j = d.createElement(s),
      dl = l !== 'dataLayer' ? '&l=' + l : '';
    j.async = true;
    j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
    if (f && f.parentNode) f.parentNode.insertBefore(j, f);
  })(window, document, 'script', 'dataLayer', GTM_ID);

  // GTM noscript fallback (append to body when ready)
  function addGtmNoscript() {
    var ns = document.createElement('noscript');
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.googletagmanager.com/ns.html?id=' + GTM_ID;
    iframe.height = '0';
    iframe.width = '0';
    iframe.style.display = 'none';
    iframe.style.visibility = 'hidden';
    ns.appendChild(iframe);
    document.body.insertBefore(ns, document.body.firstChild);
  }

  // =============================================
  // 2. META PIXEL
  // =============================================
  (function (f, b, e, v, n, t, s) {
    if (f.fbq) return;
    n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n;
    n.loaded = true;
    n.version = '2.0';
    n.queue = [];
    t = b.createElement(e);
    t.async = true;
    t.src = v;
    s = b.getElementsByTagName(e)[0];
    if (s && s.parentNode) s.parentNode.insertBefore(t, s);
  })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');

  fbq('init', META_PIXEL_ID);
  fbq('track', 'PageView');

  // =============================================
  // 3. DATALAYER HELPER
  // =============================================
  window.dataLayer = window.dataLayer || [];

  function pushEvent(eventName, params) {
    // GTM
    var data = { event: eventName };
    if (params) {
      for (var key in params) {
        if (params.hasOwnProperty(key)) data[key] = params[key];
      }
    }
    window.dataLayer.push(data);
  }

  // =============================================
  // 4. CTA CLICK — auto-attach
  // Captures: .btn, .cta-btn, .faq-btn, .cta-button, [href*="hotmart"]
  // =============================================
  function attachCTATracking() {
    var selectors = '.btn, .cta-btn, .faq-btn, .cta-button, a[href*="hotmart"]';
    var buttons = document.querySelectorAll(selectors);

    buttons.forEach(function (btn) {
      if (btn.dataset.trackingAttached) return;
      btn.dataset.trackingAttached = 'true';

      btn.addEventListener('click', function () {
        var label = (btn.textContent || '').trim().substring(0, 60);
        var section = getSection(btn);

        // GTM event
        pushEvent('CTAClick', {
          cta_label: label,
          cta_section: section,
          cta_url: btn.href || ''
        });

        // Meta Pixel — InitiateCheckout
        if (typeof fbq === 'function') {
          fbq('track', 'InitiateCheckout', {
            content_name: 'Programa Imersão Nativa',
            content_category: section,
            value: 497.0,
            currency: 'BRL'
          });
        }
      });
    });
  }

  function getSection(el) {
    var parent = el.closest('[id]');
    if (parent) return parent.id;
    var section = el.closest('section');
    if (section) return section.className.split(' ')[0] || 'unknown';
    return 'unknown';
  }

  // =============================================
  // 5. SCROLL DEPTH — 25%, 50%, 75%, 100%
  // =============================================
  var scrollMarks = { 25: false, 50: false, 75: false, 100: false };

  function trackScrollDepth() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    var docHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (docHeight <= 0) return;
    var percent = Math.round((scrollTop / docHeight) * 100);

    [25, 50, 75, 100].forEach(function (mark) {
      if (percent >= mark && !scrollMarks[mark]) {
        scrollMarks[mark] = true;
        pushEvent('ScrollDepth', { scroll_percent: mark });
      }
    });
  }

  var scrollTimer = null;
  window.addEventListener('scroll', function () {
    if (scrollTimer) return;
    scrollTimer = setTimeout(function () {
      scrollTimer = null;
      trackScrollDepth();
    }, 200);
  }, { passive: true });

  // =============================================
  // 6. VIEW CONTENT — seção de preço
  // =============================================
  function trackViewContent() {
    var precoSection = document.getElementById('mod11');
    if (!precoSection) return;

    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          pushEvent('ViewContent', { content_name: 'Preço', content_id: 'mod11' });

          if (typeof fbq === 'function') {
            fbq('track', 'ViewContent', {
              content_name: 'Programa Imersão Nativa — Preço',
              content_type: 'product',
              value: 497.0,
              currency: 'BRL'
            });
          }

          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    obs.observe(precoSection);
  }

  // =============================================
  // 7. TIME ON PAGE — 30s, 60s, 180s
  // =============================================
  var timeMarks = [30, 60, 180];
  timeMarks.forEach(function (seconds) {
    setTimeout(function () {
      pushEvent('TimeOnPage', { time_seconds: seconds });
    }, seconds * 1000);
  });

  // =============================================
  // 8. VIDEO PLAY — detect Vimeo/YouTube plays
  // =============================================
  function trackVideoPlays() {
    var iframes = document.querySelectorAll('iframe[src*="vimeo"], iframe[src*="youtube"]');
    iframes.forEach(function (iframe, index) {
      var wrapper = iframe.closest('[id]');
      var section = wrapper ? wrapper.id : 'unknown';

      // Listen for focus on iframe (basic play detection)
      iframe.addEventListener('load', function () {
        var clicked = false;
        iframe.addEventListener('mouseenter', function () {
          if (!clicked) {
            // Wait for actual click
            window.addEventListener('blur', function onBlur() {
              if (document.activeElement === iframe && !clicked) {
                clicked = true;
                pushEvent('VideoPlay', {
                  video_index: index,
                  video_section: section,
                  video_src: iframe.src.substring(0, 100)
                });
              }
              window.removeEventListener('blur', onBlur);
            });
          }
        });
      });
    });
  }

  // =============================================
  // INIT — wait for DOM
  // =============================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    addGtmNoscript();
    attachCTATracking();
    trackViewContent();
    trackVideoPlays();
  }
})();
