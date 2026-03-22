# Espanhol Com Voce - Briefing do Projeto

## Visao Geral

**Espanhol Com Voce** e uma plataforma web educacional para ensino de espanhol voltada ao publico brasileiro. O objetivo e oferecer uma experiencia de aprendizado acessivel, interativa e progressiva, permitindo que qualquer pessoa aprenda espanhol do zero ao avancado.

## Publico-Alvo

- Brasileiros que desejam aprender espanhol
- Estudantes preparando-se para vestibulares e provas de proficiencia
- Profissionais que precisam do espanhol no trabalho
- Viajantes que querem se comunicar em paises hispanicos

## Objetivos do Projeto

1. Oferecer licoes estruturadas por nivel (basico, intermediario, avancado)
2. Proporcionar pratica interativa com exercicios e quizzes
3. Disponibilizar conteudo de vocabulario com flashcards
4. Incluir recursos de audio para pratica de pronuncia
5. Acompanhar o progresso do usuario ao longo do aprendizado

## Funcionalidades Principais

### Licoes e Modulos
- Conteudo organizado em modulos tematicos (saudacoes, numeros, familia, viagens, etc.)
- Cada modulo contem explicacoes, exemplos e exercicios
- Progressao gradual de dificuldade

### Quizzes e Exercicios
- Questoes de multipla escolha
- Completar frases
- Traducao (portugues <-> espanhol)
- Exercicios de escuta

### Flashcards de Vocabulario
- Sistema de cartoes com palavra em espanhol e traducao em portugues
- Organizados por categoria tematica
- Repeticao espacada para melhor memorizacao

### Audio e Pronuncia
- Reproducao de audio com pronuncia nativa
- Comparacao entre portugues e espanhol
- Dicas de fonetica

### Acompanhamento de Progresso
- Dashboard do usuario com estatisticas
- Registro de licoes completadas
- Pontuacao e conquistas

## Stack Tecnologica

- **Frontend:** HTML5, CSS3, JavaScript (vanilla)
- **Estilizacao:** CSS customizado com design responsivo (mobile-first)
- **Conteudo:** Arquivos JSON para dados de licoes, vocabulario e quizzes
- **Audio:** Arquivos de audio em formato MP3/OGG
- **Hospedagem:** GitHub Pages (site estatico)

## Estrutura de Pastas Planejada

```
EspanholComVoce/
├── index.html              # Pagina inicial
├── pages/                  # Paginas HTML
│   ├── licoes.html         # Lista de licoes
│   ├── licao.html          # Pagina de licao individual
│   ├── quiz.html           # Pagina de quiz
│   ├── flashcards.html     # Pagina de flashcards
│   ├── progresso.html      # Pagina de progresso
│   └── sobre.html          # Sobre o projeto
├── css/                    # Estilos
│   ├── style.css           # Estilos globais
│   └── components.css      # Estilos de componentes
├── js/                     # Scripts
│   ├── app.js              # Logica principal
│   ├── licoes.js           # Logica das licoes
│   ├── quiz.js             # Logica dos quizzes
│   ├── flashcards.js       # Logica dos flashcards
│   └── progresso.js        # Logica de progresso
├── data/                   # Dados em JSON
│   ├── licoes/             # Dados das licoes por modulo
│   ├── vocabulario/        # Dados de vocabulario por tema
│   └── quizzes/            # Dados dos quizzes
├── assets/                 # Recursos estaticos
│   ├── images/             # Imagens
│   ├── audio/              # Arquivos de audio
│   └── icons/              # Icones
├── BRIEFING.md             # Este arquivo
└── README.md               # Documentacao do projeto
```

## Design e Identidade Visual

- **Cores principais:** Tons de vermelho e amarelo (referencia a bandeira espanhola) com detalhes em branco
- **Tipografia:** Fontes limpas e legiveis (sans-serif)
- **Estilo:** Moderno, amigavel e convidativo
- **Responsividade:** Funcional em desktop, tablet e celular

## Proximos Passos

1. Criar a estrutura de pastas e arquivos base
2. Desenvolver a pagina inicial (index.html)
3. Implementar o sistema de licoes
4. Criar os quizzes interativos
5. Desenvolver o sistema de flashcards
6. Adicionar recursos de audio
7. Implementar o acompanhamento de progresso
8. Testes e ajustes de responsividade
9. Deploy no GitHub Pages
