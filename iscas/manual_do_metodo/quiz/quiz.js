/**
 * ============================================================
 * ESPANHOL COM VOCE — Quiz de Nivel Interativo
 * ============================================================
 * Single-page quiz app controlled via .active class on screens.
 * 10 questions across 3 acts: Comprehension, Production, Personal.
 * Vanilla JS, no dependencies.
 * ============================================================
 */

// ─── QUIZ DATA ──────────────────────────────────────────────
const questions = [
  // ── ACT 1 — COMPREHENSION (Q1-Q3) ──
  {
    id: 1,
    act: 1,
    label: "Compreensao auditiva",
    type: "audio",
    audioText: "Mi vecina me pidio que le echara un ojo a su gato. El primer dia el gato se escapo y tuve que buscarlo por todo el barrio.",
    question: "O que aconteceu com o gato?",
    options: [
      "Ficou doente",
      "Fugiu no primeiro dia",
      "Arranhou a vizinha",
      "Nao quis comer"
    ],
    correct: 1,
    feedbackCorrect: {
      title: "Muito bem! \uD83D\uDC4F",
      text: 'Voce entendeu "se escapo" pelo contexto. E aprendeu uma expressao: <span class="feedback-highlight">echar un ojo</span> = ficar de olho em algo. Nao e "jogar um olho" \u2014 e cuidar. Guarda essa. \uD83D\uDC40'
    },
    feedbackWrong: {
      title: "Quase!",
      text: 'A resposta era B. "Se escapo" = fugiu. E <span class="feedback-highlight">echar un ojo</span> significa ficar de olho, cuidar. Expressao que nos, nativos, usamos muito. Guarda essa. \uD83D\uDC40'
    },
    scoreType: "comprehension"
  },
  {
    id: 2,
    act: 1,
    label: "Falso cognato perigoso",
    type: "text",
    question: 'Um brasileiro na Espanha diz:\n"Estoy embarazado porque llegue tarde."\n\nO que os espanhois entenderam?',
    options: [
      "Que ele estava envergonhado",
      "Que ele estava gravido",
      "Que ele estava preocupado",
      "Que ele estava com pressa"
    ],
    correct: 1,
    feedbackCorrect: {
      title: "Exato! \uD83D\uDE02",
      text: '"Embarazado" em espanhol = GRAVIDO. Envergonhado = <span class="feedback-highlight">avergonzado</span>. Esse e um dos falsos cognatos mais perigosos. Imagina falar isso numa reuniao de trabalho. Sao mais de 150 assim.'
    },
    feedbackWrong: {
      title: "Essa pega muita gente! \uD83D\uDE02",
      text: '"Embarazado" em espanhol = GRAVIDO, nao envergonhado! Envergonhado = <span class="feedback-highlight">avergonzado</span>. Imagina falar isso numa reuniao. Sao mais de 150 falsos cognatos perigosos assim.'
    },
    scoreType: "comprehension"
  },
  {
    id: 3,
    act: 1,
    label: "Expressao nativa",
    type: "text",
    question: '"Quedarse de piedra" significa:',
    options: [
      "Ficar duro como pedra (de frio)",
      "Ficar paralisado de surpresa",
      "Ficar com raiva",
      "Ficar parado esperando"
    ],
    correct: 1,
    feedbackCorrect: {
      title: "Perfeito! \u2728",
      text: '"Quedarse de piedra" = ficar chocado, sem reacao. <span class="feedback-highlight">"Cuando me dijo que se iba, me quede de piedra."</span> Essa expressao nao existe em nenhum livro didatico. Mas nos, nativos, usamos toda semana.'
    },
    feedbackWrong: {
      title: "Boa tentativa!",
      text: '"Quedarse de piedra" = ficar paralisado de surpresa/choque. <span class="feedback-highlight">"Cuando me dijo que se iba, me quede de piedra."</span> Essa expressao nao existe em livros didaticos. Nos, nativos, usamos toda semana.'
    },
    scoreType: "comprehension"
  },
  // ── ACT 2 — PRODUCTION (Q4-Q7) ──
  {
    id: 4,
    act: 2,
    label: "PRODUCAO",
    type: "text",
    question: 'Como voce diria em espanhol:\n"Eu estava a toa em casa e resolvi dar uma volta"',
    options: [
      '"Yo estaba en casa sin hacer nada y decidi caminar"',
      '"Estaba al pedo en casa y sali a dar una vuelta"',
      '"Estuve a toa en casa y fui a pasear"',
      '"No tenia nada que hacer y sali a caminar"'
    ],
    correct: 1,
    feedbackCorrect: {
      title: "Impressionante!",
      text: 'Voce conhece a forma nativa! <span class="feedback-highlight">"Estar al pedo"</span> = ficar a toa. <span class="feedback-highlight">"Dar una vuelta"</span> = dar uma volta. Sao <span class="feedback-mechanism">BLOCOS PRONTOS</span> \u2014 padroes que nativos usam automaticamente.'
    },
    feedbackWrong: {
      title: "Isso e o bloqueio em acao",
      text: 'A opcao B e como um nativo falaria. <span class="feedback-highlight">"Estar al pedo"</span> = ficar a toa. <span class="feedback-highlight">"Dar una vuelta"</span> = dar uma volta. Sao <span class="feedback-mechanism">BLOCOS PRONTOS</span>. Seu cerebro nao chegaria nisso traduzindo palavra por palavra. Precisaria ter TREINADO esses padroes antes.'
    },
    scoreType: "production"
  },
  {
    id: 5,
    act: 2,
    label: "SITUACAO REAL",
    type: "text",
    question: 'Restaurante em Montevideu. O garcom pergunta: "\u00bfYa eligieron?"\n\nVoce quer dizer: "Ainda nao. Pode nos dar mais um minutinho?"\n\nQual opcao soa mais natural?',
    options: [
      '"\u00bfTodavia no. Puede darnos un minutito mas?"',
      '"Aun no decidimos. \u00bfNos da un momentito?"',
      '"No elegimos todavia. \u00bfPuede esperar?"',
      '"No sabemos. Un momento, por favor."'
    ],
    correct: 1,
    feedbackCorrect: {
      title: "Olha so! \uD83D\uDC4F",
      text: 'Voce identificou a forma mais natural. Mas aqui esta o ponto: <span class="feedback-mechanism">LENDO, voce consegue identificar a melhor opcao. Mas se estivesse NO restaurante, com o garcom esperando, conseguiria FALAR isso na hora?</span> Essa e a diferenca entre entender e produzir.'
    },
    feedbackWrong: {
      title: "Percebeu o que aconteceu?",
      text: 'A opcao B e a mais natural. <span class="feedback-highlight">"\u00bfNos da un momentito?"</span> e educado e fluido. Mas o ponto real e: <span class="feedback-mechanism">LENDO, talvez voce reconheca a melhor opcao. Mas no restaurante, com o garcom esperando, conseguiria FALAR isso?</span> Seu cerebro foi treinado para entender, nao para produzir.'
    },
    scoreType: "production"
  },
  {
    id: 6,
    act: 2,
    label: "CONFRONTO",
    type: "honesty",
    question: 'Alguem te para na rua e fala rapido:\n"Oye, disculpa, \u00bfsabes si hay alguna farmacia por aqui cerca? Es que me siento un poco mal y necesito comprar algo."\n\nSeja honesta: o que aconteceria AGORA?',
    options: [
      "Responderia na hora, sem problema",
      "Entenderia tudo mas demoraria pra responder",
      "Entenderia e tentaria, mas travaria no meio",
      "Entenderia mas responderia em portugues"
    ],
    correct: null,
    feedback: {
      0: {
        title: "Se for verdade, parabens! \uD83D\uDCAA",
        text: 'Poucos conseguem responder na hora sem hesitar. Mas a maioria das pessoas que diz isso ainda <span class="feedback-mechanism">pensa a resposta em portugues primeiro</span> e depois traduz. Se isso acontece com voce \u2014 mesmo que rapido \u2014 ainda ha um bloqueio ativo.'
      },
      1: {
        title: "Honestidade e o primeiro passo",
        text: 'Voce <span class="feedback-mechanism">entendeu em espanhol, mas processou em portugues</span>. Tentou montar a resposta em portugues e traduzir de volta. Esse processo de traducao mental e exatamente o que causa a demora. E numa conversa real, a pessoa nao espera.'
      },
      2: {
        title: "Isso tem explicacao",
        text: 'Seu cerebro <span class="feedback-mechanism">recebeu em espanhol, processou em portugues, e tentou devolver em espanhol</span>. No meio desse caminho... travou. Isso acontece porque voce foi programada pra TRADUZIR, nao pra FALAR. A escola fez isso. O app fez isso.'
      },
      3: {
        title: "Voce nao esta sozinha",
        text: 'A maioria faz isso. Voce <span class="feedback-mechanism">entende o espanhol mas seu circuito de PRODUCAO nunca foi ativado</span>. Entender e passivo \u2014 voce recebe e processa. Falar e ativo \u2014 voce busca, monta e entrega. Sao circuitos diferentes. E o seu de producao esta desligado.'
      }
    },
    scoreType: "production"
  },
  {
    id: 7,
    act: 2,
    label: "CALIBRACAO",
    type: "diagnostic",
    question: "Quando voce tenta aprender espanhol por conta propria (series, musica, apps), o que acontece?",
    options: [
      "Eu entendo quase tudo \u2192 nao sinto que evoluo",
      "Eu nao entendo quase nada \u2192 fico frustrada e paro",
      "As vezes entendo, as vezes nao \u2192 nao sei se evoluo",
      "Eu nem tento mais \u2192 ja desisti"
    ],
    correct: null,
    feedback: {
      0: {
        title: "Zona de conforto detectada",
        text: 'Se voce entende quase tudo, o conteudo esta <span class="feedback-mechanism">FACIL DEMAIS</span> pro seu nivel. Seu cerebro nao esta sendo desafiado. Existe uma zona ideal \u2014 onde voce entende 70-80% e os outros 20% te fazem crescer. Chama-se <span class="feedback-highlight">Zona de Expansao</span>. Calibrar isso sozinha e quase impossivel.'
      },
      1: {
        title: "Bloqueio por excesso",
        text: 'Se voce nao entende quase nada, o conteudo esta <span class="feedback-mechanism">DIFICIL DEMAIS</span>. Seu cerebro bloqueia. Frustra. Voce desiste. A solucao nao e "se esforcar mais" \u2014 e encontrar a <span class="feedback-highlight">Zona de Expansao</span>: conteudo onde voce entende 70-80% e cresce nos outros 20%.'
      },
      2: {
        title: "Sem bussola",
        text: 'Essa inconsistencia significa que voce esta consumindo conteudo <span class="feedback-mechanism">SEM PROGRESSAO</span>. Um dia facil, outro impossivel. Seu cerebro precisa de <span class="feedback-highlight">calibracao</span>: conteudo na ordem certa, no nivel certo, com progressao controlada.'
      },
      3: {
        title: "Nao e fraqueza",
        text: 'Desistir e o resultado natural de tentar aprender com material que <span class="feedback-mechanism">nao foi calibrado pro seu nivel</span>. Nao e falta de forca de vontade. E falta de <span class="feedback-highlight">Zona de Expansao</span>: conteudo ajustado pra te desafiar sem bloquear.'
      }
    },
    scoreType: "none"
  },
  // ── ACT 3 — PERSONAL CONTEXT (Q8-Q10) ──
  {
    id: 8,
    act: 3,
    label: "me conta sobre voce...",
    type: "personal",
    question: "Qual o principal motivo pra voce querer falar espanhol?",
    options: [
      "\uD83C\uDF0E Viagem \u2014 quero me virar nos paises",
      "\uD83C\uDFE0 Morar fora \u2014 vou me mudar ou ja moro",
      "\uD83D\uDCBC Trabalho \u2014 preciso pra carreira",
      "\uD83C\uDF93 Estudo \u2014 prova ou certificacao"
    ],
    correct: null,
    scoreType: "avatar"
  },
  {
    id: 9,
    act: 3,
    label: "e ha quanto tempo...",
    type: "personal",
    question: "Ha quanto tempo voce tenta aprender espanhol?",
    options: [
      "Nunca estudei formalmente",
      "Menos de 1 ano",
      "1-3 anos",
      "Mais de 3 anos"
    ],
    correct: null,
    scoreType: "context"
  },
  {
    id: 10,
    act: 3,
    label: "ultima pergunta...",
    type: "personal",
    question: "Quanto tempo por dia voce tem disponivel?",
    options: [
      "\u23F1\uFE0F 5 minutos",
      "\u23F1\uFE0F 15 minutos",
      "\u23F1\uFE0F 30 minutos",
      "\u23F1\uFE0F 1 hora ou mais"
    ],
    correct: null,
    scoreType: "context"
  }
];

// ─── STATE ──────────────────────────────────────────────────
let currentQuestionIndex = 0;
let isTransitioning = false; // guards against double-clicks / rapid nav
let scores = {
  comprehension: 0,
  production: 0,
  avatar: null,
  studyTime: null,
  availability: null,
  q7answer: null
};

// UTM parameters for tracking
const utmParams = (() => {
  const params = new URLSearchParams(window.location.search);
  return {
    source: params.get('utm_source') || '',
    medium: params.get('utm_medium') || '',
    campaign: params.get('utm_campaign') || '',
    content: params.get('utm_content') || '',
    term: params.get('utm_term') || ''
  };
})();

// ─── ANALYTICS HELPER ───────────────────────────────────────
const trackEvent = (eventName, data = {}) => {
  console.log(`[ANALYTICS] ${eventName}`, { ...data, utmParams, timestamp: Date.now() });
  // Future: send to analytics service (GA4, Mixpanel, etc.)
};

// ─── DOM READY ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initQuiz();
});

const initQuiz = () => {
  // Bind the start CTA
  const startBtn = document.getElementById('btn-start-quiz');
  if (startBtn) {
    startBtn.addEventListener('click', startQuiz);
  }

  // Bind email form
  const emailForm = document.getElementById('email-form');
  if (emailForm) {
    emailForm.addEventListener('submit', handleEmailSubmit);
  }

  // Bind next button (once, globally)
  const nextBtn = document.getElementById('feedback-next-btn');
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      nextQuestion();
    });
  }

  // Bind transition screen tap-to-skip
  const transitionScreen = document.getElementById('transition-screen');
  if (transitionScreen) {
    transitionScreen.addEventListener('click', () => {
      if (transitionScreen.classList.contains('active')) {
        clearTimeout(transitionScreen._timer);
        proceedToAct2();
      }
    });
  }

  trackEvent('quiz_loaded');
};

// ─── SCREEN MANAGEMENT ─────────────────────────────────────
const showScreen = (screenId) => {
  const allScreens = document.querySelectorAll(
    '#intro-screen, #question-screen, #transition-screen, #loading-screen, #result-screen, #thankyou-screen'
  );
  allScreens.forEach(screen => {
    screen.classList.remove('active');
  });

  const target = document.getElementById(screenId);
  if (target) {
    // Small RAF delay ensures the browser paints the removal before adding .active
    requestAnimationFrame(() => {
      target.classList.add('active');
    });
  }
};

const setAct = (actNumber) => {
  const questionScreen = document.getElementById('question-screen');
  if (questionScreen) {
    questionScreen.setAttribute('data-act', actNumber);
  }
};

// ─── QUIZ START ─────────────────────────────────────────────
const startQuiz = () => {
  trackEvent('quiz_start');
  currentQuestionIndex = 0;
  scores = {
    comprehension: 0,
    production: 0,
    avatar: null,
    studyTime: null,
    availability: null,
    q7answer: null
  };
  setAct(1);
  showScreen('question-screen');
  showQuestion(0);
};

// ─── QUESTION DISPLAY ───────────────────────────────────────
const showQuestion = (index) => {
  if (index < 0 || index >= questions.length) return;

  isTransitioning = false;
  const q = questions[index];
  const container = document.getElementById('question-screen');
  if (!container) return;

  // Update act styling
  setAct(q.act);

  // Build progress indicator
  const progressEl = document.getElementById('progress-counter');
  if (progressEl) {
    progressEl.textContent = `${q.id} / ${questions.length}`;
  }

  // Update progress bar if present
  const progressBar = document.getElementById('progress-fill');
  if (progressBar) {
    progressBar.style.width = `${(q.id / questions.length) * 100}%`;
  }

  // Update label / category tag
  const labelEl = document.getElementById('question-label');
  if (labelEl) {
    labelEl.textContent = q.label;
  }

  // Audio player (Q1 only) — simulated text display since no audio files
  const audioContainer = document.getElementById('audio-player');
  if (audioContainer) {
    if (q.type === 'audio' && q.audioText) {
      audioContainer.style.display = '';
      audioContainer.innerHTML = `
        <div class="audio-simulation">
          <span class="audio-icon">\uD83D\uDD0A Audio da nativa:</span>
          <p class="audio-text"><em>${q.audioText}</em></p>
          <span class="audio-hint">Leia como se estivesse ouvindo</span>
        </div>
      `;
    } else {
      audioContainer.style.display = 'none';
      audioContainer.innerHTML = '';
    }
  }

  // Question text (preserve line breaks)
  const questionEl = document.getElementById('question-text');
  if (questionEl) {
    questionEl.innerHTML = q.question.replace(/\n/g, '<br>');
  }

  // Options
  const optionsContainer = document.getElementById('options-list');
  if (optionsContainer) {
    optionsContainer.innerHTML = '';
    q.options.forEach((text, i) => {
      const btn = document.createElement('button');
      btn.className = 'option-card';
      btn.setAttribute('data-index', i);
      btn.innerHTML = `<span class="option-letter">${String.fromCharCode(65 + i)}</span><span class="option-text">${text}</span>`;
      btn.addEventListener('click', () => selectOption(i));
      optionsContainer.appendChild(btn);
    });
  }

  // Hide any previous feedback
  const feedbackCard = document.getElementById('feedback-card');
  if (feedbackCard) {
    feedbackCard.classList.remove('visible', 'show');
    feedbackCard.style.display = 'none';
    const fbTitle = document.getElementById('feedback-title');
    const fbBody = document.getElementById('feedback-body');
    if (fbTitle) fbTitle.innerHTML = '';
    if (fbBody) fbBody.innerHTML = '';
  }

  // Hide "next" button initially
  const nextBtn = document.getElementById('feedback-next-btn');
  if (nextBtn) {
    nextBtn.style.display = 'none';
  }

  // Enter animation
  const questionContent = document.getElementById('question-content');
  questionContent.classList.remove('enter', 'exit');
  // Force reflow then add enter class
  void questionContent.offsetWidth;
  questionContent.classList.add('enter');
};

// ─── AUDIO PLAYER (simulated) ───────────────────────────────
const initAudioPlayer = () => {
  // Since we don't have actual audio files, the audio player is simulated.
  // The audioText is displayed as styled text in showQuestion() when type === "audio".
  // If real audio files are added later, this function would initialize
  // an HTMLAudioElement and control play/pause/progress.
};

// ─── OPTION SELECTION ───────────────────────────────────────
const selectOption = (optionIndex) => {
  if (isTransitioning) return;
  isTransitioning = true;

  const q = questions[currentQuestionIndex];
  const container = document.getElementById('question-screen');
  const optionBtns = container.querySelectorAll('.option-card');

  // Disable all options
  optionBtns.forEach(btn => {
    btn.disabled = true;
    btn.classList.add('disabled');
  });

  // Highlight selected
  const selectedBtn = optionBtns[optionIndex];
  if (selectedBtn) {
    selectedBtn.classList.add('selected');
  }

  // Score tracking
  updateScore(q, optionIndex);

  // Log analytics
  trackEvent('question_answered', {
    questionId: q.id,
    act: q.act,
    type: q.type,
    selectedOption: optionIndex,
    correct: q.correct !== null ? optionIndex === q.correct : null
  });

  // For scored questions, show correct/incorrect state
  if (q.correct !== null) {
    optionBtns[q.correct].classList.add('correct');
    if (optionIndex !== q.correct) {
      selectedBtn.classList.add('incorrect');
    }
  }

  // For personal questions (act 3), advance after short delay — no feedback
  if (q.type === 'personal') {
    setTimeout(() => {
      nextQuestion();
    }, 800);
    return;
  }

  // For all other types, show feedback after short delay
  setTimeout(() => {
    showFeedback(q, optionIndex);
  }, 400);
};

// ─── SCORE UPDATE ───────────────────────────────────────────
const updateScore = (q, selectedIndex) => {
  switch (q.scoreType) {
    case 'comprehension':
      if (selectedIndex === q.correct) {
        scores.comprehension++;
      }
      break;

    case 'production':
      if (q.type === 'honesty') {
        // Q6: self-assessment scoring — a=3, b=2, c=1, d=0
        const honestyScores = [3, 2, 1, 0];
        scores.production += honestyScores[selectedIndex];
      } else if (selectedIndex === q.correct) {
        scores.production++;
      }
      break;

    case 'avatar':
      // Q8: maps to avatar type
      const avatarTypes = ['viajante', 'morar_fora', 'profissional', 'academico'];
      scores.avatar = avatarTypes[selectedIndex];
      break;

    case 'context':
      if (q.id === 9) {
        scores.studyTime = selectedIndex;
      } else if (q.id === 10) {
        scores.availability = selectedIndex;
      }
      break;

    case 'none':
      // Q7: store answer for personalization
      scores.q7answer = selectedIndex;
      break;
  }
};

// ─── FEEDBACK DISPLAY ───────────────────────────────────────
const showFeedback = (q, selectedIndex) => {
  const container = document.getElementById('question-screen');
  const feedbackCard = document.getElementById('feedback-card');
  if (!feedbackCard) return;

  let title, text;

  if (q.type === 'honesty' || q.type === 'diagnostic') {
    // Q6, Q7 — feedback per answer
    const fb = q.feedback[selectedIndex];
    title = fb.title;
    text = fb.text;
  } else {
    // Standard scored questions
    if (selectedIndex === q.correct) {
      title = q.feedbackCorrect.title;
      text = q.feedbackCorrect.text;
    } else {
      title = q.feedbackWrong.title;
      text = q.feedbackWrong.text;
    }
  }

  // Fill existing feedback elements (don't destroy DOM with innerHTML)
  const fbTitle = document.getElementById('feedback-title');
  const fbBody = document.getElementById('feedback-body');
  if (fbTitle) fbTitle.innerHTML = title;
  if (fbBody) fbBody.innerHTML = text;

  // Show the "next" button
  const nextBtn = document.getElementById('feedback-next-btn');
  if (nextBtn) {
    nextBtn.style.display = '';
    nextBtn.textContent = currentQuestionIndex < questions.length - 1 ? 'Proxima \u2192' : 'Ver resultado \u2192';
  }

  // Show and animate feedback card
  feedbackCard.style.display = '';
  requestAnimationFrame(() => {
    feedbackCard.classList.add('visible', 'show');
  });
};

// ─── NEXT QUESTION ──────────────────────────────────────────
const nextQuestion = () => {
  if (isTransitioning && questions[currentQuestionIndex].type !== 'personal') {
    // For personal questions isTransitioning is set but we still want to advance
    // For others, only advance if we're in the right state
  }

  const container = document.getElementById('question-screen');
  const questionContent = document.getElementById('question-content');

  // Exit animation
  questionContent.classList.remove('enter');
  questionContent.classList.add('exit');

  const currentQ = questions[currentQuestionIndex];
  const nextIndex = currentQuestionIndex + 1;

  setTimeout(() => {
    questionContent.classList.remove('exit');

    // After Q3 (index 2): show transition screen
    if (currentQ.id === 3) {
      showTransitionScreen();
      return;
    }

    // After Q10 (last question): show loading
    if (nextIndex >= questions.length) {
      startLoading();
      return;
    }

    // After Q7 (index 6): entering act 3
    if (currentQ.id === 7) {
      setAct(3);
    }

    currentQuestionIndex = nextIndex;
    showQuestion(currentQuestionIndex);
  }, 300); // match CSS exit animation duration
};

// ─── TRANSITION SCREEN (between Act 1 and Act 2) ───────────
const showTransitionScreen = () => {
  showScreen('transition-screen');

  const transitionScreen = document.getElementById('transition-screen');
  // Auto-advance after 3.5s (or tap to skip, bound in initQuiz)
  transitionScreen._timer = setTimeout(() => {
    proceedToAct2();
  }, 3500);
};

const proceedToAct2 = () => {
  currentQuestionIndex = 3; // Q4 is index 3
  setAct(2);
  showScreen('question-screen');
  showQuestion(currentQuestionIndex);
};

// ─── LOADING SCREEN ─────────────────────────────────────────
const loadingTexts = [
  "Analisando suas respostas...",
  "Mapeando seu nivel de compreensao...",
  "Calculando seu gap de producao...",
  "Identificando seus bloqueios...",
  "Montando seu perfil personalizado..."
];

const startLoading = () => {
  trackEvent('quiz_complete', { scores: { ...scores } });

  showScreen('loading-screen');

  const loadingScreen = document.getElementById('loading-screen');
  const textEl = document.getElementById('loading-text');

  let textIndex = 0;

  if (textEl) {
    textEl.textContent = loadingTexts[0];
  }

  const rotateInterval = setInterval(() => {
    textIndex++;
    if (textIndex >= loadingTexts.length) {
      clearInterval(rotateInterval);
      return;
    }
    if (textEl) {
      textEl.style.opacity = '0';
      setTimeout(() => {
        textEl.textContent = loadingTexts[textIndex];
        textEl.style.opacity = '1';
      }, 200);
    }
  }, 1500);

  // After 4.5s, show results
  setTimeout(() => {
    clearInterval(rotateInterval);
    showResult();
  }, 4500);
};

// ─── CALCULATE LEVELS ───────────────────────────────────────
const calculateLevels = () => {
  // Comprehension: 3=B2, 2=B1, 1=A2, 0=A1
  const compLevels = ['A1', 'A2', 'B1', 'B2'];
  const compLevel = compLevels[scores.comprehension];
  const compPercent = Math.round((scores.comprehension / 3) * 100);

  // Production: 5-6=B1, 3-4=A2, 1-2=A1, 0=A0
  let prodLevel, prodPercent;
  if (scores.production >= 5) {
    prodLevel = 'B1';
    prodPercent = 75;
  } else if (scores.production >= 3) {
    prodLevel = 'A2';
    prodPercent = 50;
  } else if (scores.production >= 1) {
    prodLevel = 'A1';
    prodPercent = 28;
  } else {
    prodLevel = 'A0';
    prodPercent = 10;
  }

  const gap = compPercent - prodPercent;

  return { compLevel, compPercent, prodLevel, prodPercent, gap };
};

// ─── AVATAR DATA ────────────────────────────────────────────
const getAvatarData = (avatarType) => {
  const avatars = {
    viajante: {
      name: "A Viajante",
      color: "#F59E0B",
      text: "Voce quer viajar e se virar sozinha. Entender placas e cardapios nao e o problema \u2014 o problema e RESPONDER quando alguem fala com voce. Isso muda quando voce treina os padroes certos."
    },
    morar_fora: {
      name: "A Expatriada",
      color: "#3B82F6",
      text: "Voce vai morar (ou ja mora) fora. Sobreviver entendendo nao e suficiente. Voce precisa PERTENCER. E pertencer exige FALAR. Isso muda quando voce ativa o circuito de producao."
    },
    profissional: {
      name: "A Profissional",
      color: "#8B5CF6",
      text: 'No trabalho, travar nao e opcao. Voce nao pode pedir "um minutinho" numa reuniao pra traduzir na cabeca. Precisa ser automatico. Isso muda com padroes prontos e imersao calibrada.'
    },
    academico: {
      name: "A Estudante",
      color: "#10B981",
      text: "Provas de proficiencia testam producao, nao so compreensao. Se seu circuito de producao esta fraco, voce pode reprovar mesmo entendendo tudo. Isso muda com treino especifico e calibrado."
    }
  };

  return avatars[avatarType] || avatars.viajante;
};

// ─── ERROR CARDS ────────────────────────────────────────────
const getErrorCards = () => {
  // Error 1 — Always the same
  const error1 = {
    number: 1,
    title: "Seu cerebro nao tem blocos prontos",
    text: "Nas perguntas de producao, quando voce precisou FALAR em vez de entender, a dificuldade aumentou. Isso acontece porque seu cerebro busca padroes prontos de espanhol \u2014 e nao encontra o suficiente. A solucao: treinar blocos reais que nativos usam. Nao palavras soltas \u2014 frases inteiras, em contexto."
  };

  // Error 2 — Always the same
  const error2 = {
    number: 2,
    title: "A ordem foi invertida",
    text: "Voce provavelmente entendeu mais do que conseguiu produzir. Compreensao e producao sao circuitos separados no cerebro. O seu circuito de producao foi pouco treinado porque te ensinaram a ENTENDER primeiro (gramatica, vocabulario, leitura) em vez de FALAR (ouvir, repetir, praticar)."
  };

  // Error 3 — Personalized based on Q7 answer
  const q7Texts = {
    0: 'Na pergunta sobre como voce aprende sozinha, voce disse que entende quase tudo e nao sente evolucao. Isso acontece porque o conteudo esta facil demais pro seu nivel \u2014 seu cerebro nao esta sendo desafiado.',
    1: 'Na pergunta sobre como voce aprende sozinha, voce disse que nao entende quase nada e desiste. Isso acontece porque o conteudo esta dificil demais \u2014 seu cerebro bloqueia antes de aprender.',
    2: 'Na pergunta sobre como voce aprende sozinha, voce disse que as vezes entende e as vezes nao. Isso acontece porque o conteudo nao tem progressao \u2014 um dia facil, outro impossivel.',
    3: 'Na pergunta sobre como voce aprende sozinha, voce disse que ja desistiu. Isso acontece porque voce tentou com material que nao foi calibrado pro seu nivel \u2014 nao e falta de forca de vontade.'
  };

  const q7Text = q7Texts[scores.q7answer] || q7Texts[2]; // fallback

  const error3 = {
    number: 3,
    title: "Sem calibracao, nao ha progresso",
    text: `${q7Text} A solucao e conteudo na sua Zona de Expansao: onde voce entende 70-80% e os outros 20% te fazem crescer.`
  };

  return [error1, error2, error3];
};

// ─── RESULT SCREEN ──────────────────────────────────────────
const showResult = () => {
  isTransitioning = false; // Reset for email form interaction
  showScreen('result-screen');

  const result = document.getElementById('result-screen');
  if (!result) return;

  const { compLevel, compPercent, prodLevel, prodPercent, gap } = calculateLevels();
  const avatar = getAvatarData(scores.avatar);
  const errorCards = getErrorCards();

  // ── Populate level bars ──
  const compLevelEl = document.getElementById('comp-value');
  const prodLevelEl = document.getElementById('prod-value');
  const compBar = document.getElementById('comp-bar');
  const prodBar = document.getElementById('prod-bar');
  const gapEl = document.getElementById('gap-number');

  if (compLevelEl) compLevelEl.textContent = compLevel;
  if (prodLevelEl) prodLevelEl.textContent = prodLevel;
  if (gapEl) gapEl.textContent = `${gap}%`;

  // Animate bars with staggered delays
  requestAnimationFrame(() => {
    setTimeout(() => {
      if (compBar) {
        compBar.style.width = `${compPercent}%`;
        compBar.setAttribute('data-percent', `${compPercent}%`);
      }
    }, 300);

    setTimeout(() => {
      if (prodBar) {
        prodBar.style.width = `${prodPercent}%`;
        prodBar.setAttribute('data-percent', `${prodPercent}%`);
      }
    }, 700);

    setTimeout(() => {
      if (gapEl) {
        gapEl.classList.add('visible', 'show');
      }
    }, 1100);
  });

  // ── Avatar section ──
  const avatarNameEl = document.getElementById('avatar-badge-text');
  const avatarTextEl = document.getElementById('impact-phrase');
  const avatarBadge = document.getElementById('avatar-badge');

  if (avatarNameEl) avatarNameEl.textContent = avatar.name;
  if (avatarTextEl) avatarTextEl.innerHTML = avatar.text;
  if (avatarBadge) avatarBadge.style.backgroundColor = avatar.color;

  // ── Error cards ──
  // Populate the 3 existing error cards in HTML
  errorCards.forEach(card => {
    const cardEl = document.getElementById(`error-card-${card.number}`);
    if (cardEl) {
      const titleEl = cardEl.querySelector('.error-card-title, [data-error-title]');
      const descEl = cardEl.querySelector('.error-card-desc, [data-error-desc]');
      if (titleEl) titleEl.textContent = card.title;
      if (descEl) descEl.innerHTML = card.text;
    }
  });

  // ── Gap diagnosis text ──
  const diagnosisEl = document.getElementById('impact-phrase');
  if (diagnosisEl) {
    if (gap >= 40) {
      diagnosisEl.innerHTML = `Seu gap e de <strong>${gap}%</strong>. Isso significa que sua compreensao esta muito a frente da sua producao. Voce entende <strong>${compLevel}</strong>, mas fala no nivel <strong>${prodLevel}</strong>. A boa noticia: o caminho pra fechar esse gap e mais curto do que parece.`;
    } else if (gap >= 20) {
      diagnosisEl.innerHTML = `Seu gap e de <strong>${gap}%</strong>. Ha uma diferenca entre o que voce entende (<strong>${compLevel}</strong>) e o que consegue produzir (<strong>${prodLevel}</strong>). Isso e corrigivel com o treino certo.`;
    } else {
      diagnosisEl.innerHTML = `Seu gap e de <strong>${gap}%</strong>. Sua compreensao e producao estao proximas. O proximo passo e elevar os dois juntos, com conteudo calibrado.`;
    }
  }

  // Setup scroll reveal for error cards
  setupScrollReveal();
};

// ─── SCROLL REVEAL ──────────────────────────────────────────
const setupScrollReveal = () => {
  const cards = document.querySelectorAll('.error-card');
  if (!cards.length) return;

  // If IntersectionObserver is not supported, show all immediately
  if (!('IntersectionObserver' in window)) {
    cards.forEach(card => card.classList.add('revealed'));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
  });

  cards.forEach(card => observer.observe(card));
};

// ─── EMAIL HANDLING ─────────────────────────────────────────
const handleEmailSubmit = (event) => {
  event.preventDefault();

  const form = event.target;
  const emailInput = form.querySelector('input[type="email"], input[name="email"]');

  if (!emailInput) return;

  const email = emailInput.value.trim();

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    // Show validation error
    const errorEl = form.querySelector('.email-error');
    if (errorEl) {
      errorEl.textContent = 'Por favor, insira um email valido.';
      errorEl.style.display = '';
    } else {
      // Create error element if not present
      const err = document.createElement('span');
      err.className = 'email-error';
      err.textContent = 'Por favor, insira um email valido.';
      err.style.color = '#EF4444';
      err.style.fontSize = '0.875rem';
      err.style.marginTop = '0.5rem';
      err.style.display = 'block';
      emailInput.parentNode.appendChild(err);
    }
    isTransitioning = false;
    return;
  }

  // Prevent double submission
  if (isTransitioning) return;
  isTransitioning = true;

  // Disable button
  const submitBtn = form.querySelector('button[type="submit"], .submit-btn');
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';
  }

  trackEvent('email_submitted', {
    email,
    scores: { ...scores },
    levels: calculateLevels(),
    avatar: scores.avatar,
    utmParams
  });

  // ──────────────────────────────────────────────────────────
  // TODO: ManyChat / Mailchimp API integration
  // Replace the setTimeout below with an actual API call, e.g.:
  //
  // fetch('https://api.mailchimp.com/...', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({
  //     email,
  //     tags: [scores.avatar, calculateLevels().compLevel],
  //     merge_fields: {
  //       COMP_LEVEL: calculateLevels().compLevel,
  //       PROD_LEVEL: calculateLevels().prodLevel,
  //       GAP: calculateLevels().gap,
  //       AVATAR: scores.avatar,
  //       UTM_SOURCE: utmParams.source,
  //       UTM_MEDIUM: utmParams.medium,
  //       UTM_CAMPAIGN: utmParams.campaign
  //     }
  //   })
  // })
  // .then(res => res.json())
  // .then(data => { showScreen('thankyou-screen'); })
  // .catch(err => { console.error('Email submission failed:', err); });
  // ──────────────────────────────────────────────────────────

  // Simulated submission — show thank you after brief delay
  setTimeout(() => {
    showScreen('thankyou-screen');
    isTransitioning = false;
  }, 600);
};
