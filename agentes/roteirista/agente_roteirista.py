"""
Agente Roteirista — @espanholcomvoce
=====================================
Le o calendario gerado pelo Agente Estrategista e produz roteiros
prontos para gravar (reels) e montar (carrosseis).

Entrada: calendario JSON do Estrategista
Saida: JSON com roteiros completos + CSV resumido

Cada roteiro inclui:
  REEL  → hook (3s), fala da Ale, pilulas visuais, CTA, legenda
  CARROSSEL → capa, slides de conteudo, slide CTA, legenda

Tom de voz, formulas e identidade visual sao lidos do briefing_marca.md
e tipos_conteudo.json em runtime.
"""

import json
import csv
import random
from datetime import datetime
from pathlib import Path

# --- Caminhos ---
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def carregar_json(nome):
    with open(CONFIG_DIR / nome, "r", encoding="utf-8") as f:
        return json.load(f)


def carregar_dicionario():
    data = carregar_json("dicionario_linguistico.json")
    return data


# Dicionario global — carregado uma vez
DICIONARIO = carregar_dicionario()


def buscar_expressao(tema):
    """Extrai a chave de busca do tema e procura no dicionario."""
    # Tenta extrair a expressao/palavra do tema
    chave = tema.lower()
    # Remove prefixos comuns
    for prefixo in [
        "como falar '", "como falar ", "como falar'",
    ]:
        if chave.startswith(prefixo):
            chave = chave[len(prefixo):]
    # Remove sufixos comuns
    for sufixo in [
        "' em espanhol", " em espanhol", "' em espanhol",
        " (spoiler: nao tem!)", " (cuidado!)", " (da escola)",
    ]:
        if chave.endswith(sufixo):
            chave = chave[:-len(sufixo)]
    chave = chave.strip().strip("'").strip()

    # Busca em expressoes
    if chave in DICIONARIO["expressoes"]:
        return DICIONARIO["expressoes"][chave], "expressao"
    # Busca em palavras
    if chave in DICIONARIO["palavras"]:
        return DICIONARIO["palavras"][chave], "palavra"
    # Busca parcial (caso a chave contenha algo mais)
    for k, v in DICIONARIO["expressoes"].items():
        if k in chave or chave in k:
            return v, "expressao"
    for k, v in DICIONARIO["palavras"].items():
        if k in chave or chave in k:
            return v, "palavra"
    return None, None


def buscar_pergunta(tema):
    """Busca resposta para pergunta de seguidor no dicionario."""
    chave = tema.lower().replace("seguidor pergunta: ", "").strip().rstrip("?")
    perguntas = DICIONARIO.get("perguntas_seguidores", {})
    # Busca exata
    if chave in perguntas:
        return perguntas[chave]
    # Busca parcial
    for k, v in perguntas.items():
        # Verifica se as palavras-chave da pergunta batem
        palavras_chave_k = set(k.lower().split())
        palavras_chave_tema = set(chave.lower().split())
        # Se compartilham 2+ palavras relevantes (excluindo artigos)
        irrelevantes = {"como", "em", "o", "a", "de", "do", "da", "e", "no", "na", "um", "uma", "que", "por", "para", "se", "vs"}
        comuns = (palavras_chave_k - irrelevantes) & (palavras_chave_tema - irrelevantes)
        if len(comuns) >= 2:
            return v
    return None


def buscar_falso_amigo(tema):
    """Extrai o falso amigo do tema e procura no dicionario."""
    chave = tema.lower()
    # Tenta encontrar a palavra principal do tema
    for k, v in DICIONARIO["falsos_amigos"].items():
        k_lower = k.lower()
        if k_lower in chave:
            return v, k
    return None, None


def carregar_briefing():
    with open(CONFIG_DIR / "briefing_marca.md", "r", encoding="utf-8") as f:
        return f.read()


# ================================================================
# CORES OFICIAIS — rotacionam nas pilulas dos reels
# ================================================================
CORES = [
    {"hex": "#001e38", "nome": "Azul Marinho"},
    {"hex": "#fbbf24", "nome": "Dourado"},
    {"hex": "#ffcb15", "nome": "Amarelo"},
    {"hex": "#10b981", "nome": "Emerald"},
    {"hex": "#0090be", "nome": "Azul Ceu"},
    {"hex": "#79458f", "nome": "Roxo"},
    {"hex": "#4e4b97", "nome": "Indigo"},
]

# ================================================================
# TOM DE VOZ — frases e padroes da Ale
# ================================================================
FRASES_ALE = [
    "No espanhol real...",
    "A gente fala assim...",
    "Nos, nativos, falamos assim...",
    "Isso que ninguem te ensinou na escola...",
    "O problema nao e voce, e o metodo.",
    "Salva esse video pra nao esquecer!",
    "Manda pra quem precisa ouvir isso!",
]

FRASES_PROIBIDAS = [
    "fluente em 30 dias",
    "facil",
    "voce precisa decorar",
    "os nativos falam",
]

# Aberturas de hook por tipo de conteudo (3 primeiros segundos do reel)
HOOKS_POR_TIPO = {
    1: [  # Expressoes Idiomaticas
        "Voce sabe como falar isso em espanhol?",
        "Essa expressao brasileira nao existe em espanhol!",
        "Para! Voce fala isso todo dia mas nao sabe em espanhol.",
        "Eu, como nativa, nunca entendi essa expressao... ate agora.",
    ],
    2: [  # Palavras do Cotidiano
        "Essa palavra simples tem traducao ERRADA na sua cabeca.",
        "Voce usa isso todo dia mas em espanhol e completamente diferente.",
        "Uma palavra. Mil confusoes. Bora resolver.",
        "Se voce falar essa palavra errada, vai passar vergonha.",
    ],
    3: [  # Erros e Falsos Amigos
        "PARA! Nao fala isso em espanhol!",
        "Esse erro pode te colocar numa situacao MUITO constrangedora.",
        "90% dos brasileiros falam isso errado. Voce tambem?",
        "Cuidado! Essa palavra nao significa o que voce pensa.",
    ],
    4: [  # Perguntas de Seguidores
        "Voces me perguntaram isso e eu PRECISO responder.",
        "Essa e a duvida mais comum que eu recebo.",
        "Um seguidor me mandou essa pergunta e a resposta vai te surpreender.",
        "Voce tambem tem essa duvida? Entao presta atencao.",
    ],
    5: [  # Cultura e Diferencas
        "Voce sabia que em espanhol isso muda de pais pra pais?",
        "Isso que voce acha normal no Brasil e MUITO diferente la fora.",
        "A diferenca cultural que ninguem te contou.",
        "Em cada pais hispanico chamam isso de um jeito diferente.",
    ],
    6: [  # Metodo e Bastidor
        "Voce sabe POR QUE voce trava ao falar espanhol?",
        "Eu vou te explicar o que acontece no seu cerebro quando voce tenta falar.",
        "A ciencia explica por que voce entende mas nao fala.",
        "Deixa eu te mostrar como o aprendizado REALMENTE funciona.",
    ],
    7: [  # Dor e Identificacao
        "Se isso e voce, presta atencao ate o final.",
        "Eu sei exatamente o que voce ta sentindo.",
        "Voce se identifica com isso? Entao voce PRECISA ouvir.",
        "Essa frustracao tem nome. E tem solucao.",
    ],
    8: [  # Desejo e Transformacao
        "Fecha os olhos e imagina isso comigo...",
        "E se eu te dissesse que isso e possivel em 6 meses?",
        "Essa pode ser a sua realidade. Eu vou te mostrar como.",
        "A transformacao que meus alunos vivem todo dia.",
    ],
    9: [  # Quebra de Crencas
        "Voce acredita nisso? Entao voce ta errado.",
        "Tudo que te ensinaram sobre aprender espanhol e mentira.",
        "Essa crenca esta DESTRUINDO seu espanhol.",
        "Prepare-se: o que eu vou falar vai contra tudo que voce ouviu.",
    ],
    10: [  # Prova Social
        "Olha o que essa aluna me mandou...",
        "Essa historia me emociona toda vez que eu conto.",
        "De travado a fluente. Olha o resultado.",
        "Isso aqui e a prova de que o metodo funciona.",
    ],
    11: [  # CTA Indireto
        "Se voce chegou ate aqui, essa mensagem e pra voce.",
        "Eu tenho algo especial pra te mostrar.",
        "Voce ja deu o primeiro passo. Agora vem o proximo.",
        "Eu preparei algo que pode mudar sua relacao com o espanhol.",
    ],
    12: [  # Historia e Autoridade Pessoal
        "Eu preciso te contar uma coisa sobre mim.",
        "Quando eu cheguei no Brasil, eu nao falava uma palavra em portugues.",
        "Essa experiencia mudou completamente a forma como eu ensino.",
        "Pouca gente sabe disso sobre mim, mas...",
    ],
}

# ================================================================
# TEMPLATES DE ROTEIRO — REEL
# ================================================================

def gerar_roteiro_reel(post, tipo_info, avatar_info, cor_pilula):
    """Gera roteiro completo de reel pronto para gravar."""
    tipo_id = post["tipo_conteudo_id"]
    tema = post["tema"]
    avatar_id = post["avatar_id"]
    funil = post["funil"]

    # Hook (3 primeiros segundos)
    hooks = HOOKS_POR_TIPO.get(tipo_id, ["Presta atencao nisso!"])
    hook = random.choice(hooks)

    # Pilulas visuais (overlay no video)
    pilulas = _gerar_pilulas(tipo_id, tema, cor_pilula)

    # Desenvolvimento (fala da Ale)
    desenvolvimento = _gerar_desenvolvimento_reel(tipo_id, tema, avatar_id, avatar_info)

    # CTA falado
    cta_falado = _gerar_cta_falado(tipo_id, post["keyword_manychat"], funil)

    # Legenda
    legenda = _gerar_legenda(post, tipo_info, hook)

    return {
        "formato": "REEL",
        "duracao_estimada": "30-60 segundos",
        "roteiro": {
            "hook_3s": {
                "fala": hook,
                "instrucao_gravacao": "Olhar direto pra camera. Expressao de quem vai revelar algo. Energia alta.",
            },
            "pilulas_visuais": pilulas,
            "desenvolvimento": desenvolvimento,
            "cta_final": {
                "fala": cta_falado,
                "instrucao_gravacao": "Apontar pra baixo (comentarios) ou pra bio. Tom convidativo, nao desesperado.",
            },
        },
        "legenda": legenda,
    }


def _gerar_pilulas(tipo_id, tema, cor):
    """Gera as 3 pilulas visuais do padrao de reels."""
    # Determina textos das pilulas baseado no tipo
    if tipo_id in [1, 2]:  # Expressoes / Palavras
        # Extrai a expressao/palavra do tema
        expressao = tema.replace("Como falar '", "").replace("' em espanhol", "")
        expressao = expressao.replace("Como falar ", "").replace(" em espanhol", "")
        for suffix in [" (spoiler: nao tem!)", " (cuidado!)", " (da escola)"]:
            expressao = expressao.replace(suffix, "")
        # Busca traducao real para a pilula 3
        dados, _ = buscar_expressao(tema)
        traducao_pilula = dados["espanhol"].upper().split("/")[0].strip() if dados else "EM ESPANHOL"
        return {
            "pilula_1": {"texto": "COMO FALAR", "fundo": cor["hex"], "texto_cor": "branco"},
            "pilula_2": {"texto": expressao.upper(), "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": traducao_pilula, "fundo": cor["hex"], "texto_cor": "branco"},
        }
    elif tipo_id == 3:  # Erros
        dados_fa, palavra_fa = buscar_falso_amigo(tema)
        palavra_erro = palavra_fa.upper() if palavra_fa else tema.split(" ")[0].upper()
        significa = dados_fa["significa_realmente"].upper() if dados_fa else "NAO SIGNIFICA ISSO"
        return {
            "pilula_1": {"texto": "CUIDADO", "fundo": "#fbbf24", "texto_cor": "branco"},
            "pilula_2": {"texto": palavra_erro, "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": f"= {significa}", "fundo": "#fbbf24", "texto_cor": "branco"},
        }
    elif tipo_id == 4:  # Perguntas
        return {
            "pilula_1": {"texto": "SEGUIDOR PERGUNTOU", "fundo": cor["hex"], "texto_cor": "branco"},
            "pilula_2": {"texto": "ALE RESPONDE", "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": "ASSISTE ATE O FINAL", "fundo": cor["hex"], "texto_cor": "branco"},
        }
    elif tipo_id == 5:  # Cultura
        return {
            "pilula_1": {"texto": "VOCE SABIA?", "fundo": cor["hex"], "texto_cor": "branco"},
            "pilula_2": {"texto": "DIFERENCA CULTURAL", "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": "ESPANHOL REAL", "fundo": cor["hex"], "texto_cor": "branco"},
        }
    elif tipo_id == 7:  # Dor
        return {
            "pilula_1": {"texto": "VOCE SE IDENTIFICA?", "fundo": "#fbbf24", "texto_cor": "branco"},
            "pilula_2": {"texto": "ISSO TEM SOLUCAO", "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": "ASSISTE ATE O FINAL", "fundo": "#fbbf24", "texto_cor": "branco"},
        }
    elif tipo_id == 9:  # Quebra de Crencas
        return {
            "pilula_1": {"texto": "VOCE ACREDITA NISSO?", "fundo": "#4e4b97", "texto_cor": "branco"},
            "pilula_2": {"texto": "MENTIRA!", "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": "A VERDADE E OUTRA", "fundo": "#4e4b97", "texto_cor": "branco"},
        }
    else:  # Generico
        return {
            "pilula_1": {"texto": "ESPANHOL COM VOCE", "fundo": cor["hex"], "texto_cor": "branco"},
            "pilula_2": {"texto": "ALE EXPLICA", "fundo": "#FFFFFF", "texto_cor": "preto bold"},
            "pilula_3": {"texto": "ASSISTE ATE O FINAL", "fundo": cor["hex"], "texto_cor": "branco"},
        }


def _gerar_desenvolvimento_reel(tipo_id, tema, avatar_id, avatar_info):
    """Gera o corpo do roteiro — a fala da Ale no reel."""
    dor = avatar_info.get("dor", "")
    desejo = avatar_info.get("desejo", "")
    gatilho = avatar_info.get("gatilho", "")

    # Frase assinatura aleatorio
    assinatura = random.choice(FRASES_ALE[:5])  # Pega das frases didaticas

    blocos = []

    if tipo_id in [1, 2]:  # Expressoes / Palavras
        expressao = tema.replace("Como falar '", "").replace("' em espanhol", "")
        expressao = expressao.replace("Como falar ", "").replace(" em espanhol", "")
        for suffix in [" (spoiler: nao tem!)", " (cuidado!)", " (da escola)"]:
            expressao = expressao.replace(suffix, "")
        dados, _ = buscar_expressao(tema)
        if dados:
            esp = dados["espanhol"]
            alt = dados.get("alternativa", "")
            pron = dados["pronuncia"]
            ex_es = dados["exemplo_es"]
            ex_pt = dados["exemplo_pt"]
            dica = dados.get("dica", "")
            blocos = [
                f"Voce fala '{expressao}' todo dia, ne? Mas em espanhol... e bem diferente.",
                f"Nos, nativos, falamos assim: {esp}.",
                f"Repete comigo: {pron}.",
                f"Olha o exemplo: {ex_es} — que significa: {ex_pt}.",
                f"{dica}" if dica else "Isso que ninguem te ensinou na escola.",
                f"Agora voce ja sabe. Nao vai mais travar nessa.",
            ]
        else:
            blocos = [
                f"Voce fala '{expressao}' todo dia, ne? Mas em espanhol... e bem diferente.",
                f"Nos, nativos, falamos assim: [TRADUÇÃO — verificar no dicionario].",
                f"Isso que ninguem te ensinou na escola.",
                f"Agora voce ja sabe. Nao vai mais travar nessa.",
            ]
    elif tipo_id == 3:  # Erros e Falsos Amigos
        dados, palavra_chave = buscar_falso_amigo(tema)
        if dados:
            parece = dados["parece_significar"]
            real = dados["significa_realmente"]
            correto = dados["correto_pt"]
            ex_certo_es = dados["exemplo_certo_es"]
            ex_certo_pt = dados["exemplo_certo_pt"]
            blocos = [
                f"Muita gente acha que '{palavra_chave}' em espanhol significa {parece}. Mas ta ERRADO.",
                f"Nos, nativos, NUNCA falamos isso com esse significado. Na verdade significa: {real}.",
                f"{correto}.",
                f"O certo e: {ex_certo_es} — que significa: {ex_certo_pt}.",
                f"Entao cuidado! Salva esse video pra nao esquecer nunca mais.",
            ]
        else:
            blocos = [
                f"Muita gente fala isso achando que ta certo. Mas ta errado.",
                f"Nos, nativos, NUNCA falamos isso com esse significado.",
                f"No espanhol real, essa palavra significa outra coisa.",
                f"Entao cuidado! Salva esse video pra nao esquecer nunca mais.",
            ]
    elif tipo_id == 4:  # Perguntas
        pergunta = tema.replace("Seguidor pergunta: ", "")
        dados_perg = buscar_pergunta(tema)
        if dados_perg:
            resp = dados_perg["resposta"]
            ex_es = dados_perg["exemplo_es"]
            ex_pt = dados_perg["exemplo_pt"]
            dica = dados_perg.get("dica", "")
            blocos = [
                f"Um seguidor me perguntou: '{pergunta}'",
                f"Essa e uma duvida MUITO comum. {resp}",
                f"Olha o exemplo: {ex_es}",
                f"Que significa: {ex_pt}",
                f"{dica}" if dica else "Isso que ninguem te ensinou na escola.",
                f"Entendeu? Agora manda a SUA duvida nos comentarios.",
            ]
        else:
            blocos = [
                f"Um seguidor me perguntou: '{pergunta}'",
                f"Essa e uma duvida MUITO comum, e a resposta e mais simples do que voce imagina.",
                f"Nos, nativos, falamos assim: [VERIFICAR — pergunta nao encontrada no dicionario].",
                f"Entendeu? Agora manda a SUA duvida nos comentarios.",
            ]
    elif tipo_id == 5:  # Cultura
        blocos = [
            f"Isso que voce acha normal no Brasil funciona MUITO diferente no mundo hispanico.",
            f"Hoje eu vou te contar sobre: {tema}.",
            f"Nos, nativos, vemos isso de um jeito completamente diferente de voces brasileiros.",
            f"E o mais curioso: isso muda de pais pra pais dentro do mundo hispanico tambem!",
            f"Comenta qual pais hispanico voce mais quer conhecer.",
        ]
    elif tipo_id == 6:  # Metodo
        blocos = [
            f"Voce quer saber por que voce trava? Eu vou te explicar.",
            f"O cerebro nao aprende idioma por decoreba. Ele aprende por CONEXAO.",
            f"Por isso eu criei o Metodo Imersao Nativa com 3 pilares:",
            f"Nucleo del Conocimiento, Imersao Ativa e Acompanhamento Inteligente.",
            f"E assim que mais de 5.000 alunos destravaram o espanhol de verdade.",
        ]
    elif tipo_id == 7:  # Dor e Identificacao
        blocos = [
            f"{tema}",
            f"Eu sei como e. {dor}",
            f"O problema nao e voce. E o metodo que voce usou ate agora.",
            f"Voce nao precisa de mais vocabulario. Precisa de um caminho certo.",
            f"Se voce se identificou, comenta TRAVA que eu te mostro o proximo passo.",
        ]
    elif tipo_id == 8:  # Desejo e Transformacao
        blocos = [
            f"{tema}",
            f"Isso nao e um sonho. Isso e o que meus alunos vivem toda semana.",
            f"{desejo}",
            f"Em 6 meses voce pode estar vivendo isso. Sem exagero.",
            f"O primeiro passo? Parar de tentar sozinho.",
        ]
    elif tipo_id == 9:  # Quebra de Crencas
        blocos = [
            f"{tema}",
            f"Eu sei que parece loucura, mas e a verdade.",
            f"O metodo tradicional te ensina a ESTUDAR espanhol. Nao a FALAR espanhol.",
            f"A diferenca? Uma te enche de regra. A outra te dá fluencia.",
            f"Se voce acreditava nisso, comenta ai. Voce nao e o unico.",
        ]
    elif tipo_id == 10:  # Prova Social
        # Tema ja contem a historia (ex: "Ela travava... hoje conversa com nativos")
        blocos = [
            f"Eu quero compartilhar uma historia com voce.",
            f"Uma aluna minha veio ate mim assim: {dor}",
            f"Depois de comecar com o Metodo Imersao Nativa, tudo mudou.",
            f"O resultado? {tema}.",
            f"Se voce quer o mesmo resultado, comenta QUERO.",
        ]
    elif tipo_id == 11:  # CTA Indireto
        blocos = [
            f"{tema}",
            f"Eu preparei uma aula demonstrativa gratuita pra voce.",
            f"Nessa aula eu te mostro exatamente como destravar seu espanhol.",
            f"Sem enrolacao. Sem promessa vazia. So o caminho real.",
            f"Comenta AULA que eu te mando o link.",
        ]
    elif tipo_id == 12:  # Historia
        blocos = [
            f"{tema}",
            f"Quando eu cheguei no Brasil, eu nao falava UMA palavra em portugues.",
            f"Eu aprendi por imersao, por necessidade, por viver o idioma no dia a dia.",
            f"Foi essa experiencia que me mostrou COMO o cerebro realmente aprende.",
            f"E por isso que eu ensino diferente. Porque eu VIVI o processo.",
        ]
    else:
        blocos = [
            f"{tema}",
            f"{assinatura}",
            f"[CONTEUDO PRINCIPAL].",
            f"Salva esse video e manda pra quem precisa!",
        ]

    # Monta lista de palavras em espanhol presentes nos blocos
    palavras_es = ""
    if tipo_id in [1, 2]:
        dados, _ = buscar_expressao(tema)
        if dados:
            palavras_es = f"{dados['espanhol']} | Pronuncia: {dados['pronuncia']}"
            if dados.get("alternativa"):
                palavras_es += f" | Alternativas: {dados['alternativa']}"
    elif tipo_id == 3:
        dados, _ = buscar_falso_amigo(tema)
        if dados:
            palavras_es = f"Significa: {dados['significa_realmente']} | Pronuncia: {dados['pronuncia']}"
    elif tipo_id == 4:
        dados_perg = buscar_pergunta(tema)
        if dados_perg:
            palavras_es = f"{dados_perg.get('espanhol', '')} | Pronuncia: {dados_perg.get('pronuncia', '')}"

    return {
        "blocos_fala": blocos,
        "instrucoes_gravacao": [
            "Falar olhando pra camera, tom conversacional, como se tivesse falando com uma amiga",
            "Gesticular naturalmente — Ale e expressiva",
            "Nos momentos de espanhol, falar com pronuncia nativa clara",
            "Energia alta no hook, tom mais intimo no desenvolvimento, confiante no CTA",
        ],
        "palavras_em_espanhol": palavras_es if palavras_es else "[Verificar: expressao nao encontrada no dicionario]",
    }


def _gerar_cta_falado(tipo_id, keyword, funil):
    """Gera CTA que Ale fala no final do reel."""
    if funil == "FUNDO":
        return (
            f"Se voce quer destravar seu espanhol de verdade, "
            f"comenta {keyword} aqui embaixo que eu te mando o proximo passo. "
            f"E salva esse video pra assistir de novo!"
        )
    elif funil == "MEIO":
        return (
            f"Se voce se identificou, comenta {keyword}. "
            f"E manda esse video pra alguem que precisa ouvir isso."
        )
    else:  # TOPO
        return (
            f"Gostou? Salva pra nao esquecer e segue o @espanholcomvoce "
            f"pra aprender espanhol de verdade todo dia. "
            f"Comenta {keyword} que eu te mando um material gratis!"
        )


# ================================================================
# TEMPLATES DE ROTEIRO — CARROSSEL
# ================================================================

def gerar_roteiro_carrossel(post, tipo_info, avatar_info, cor_fundo):
    """Gera roteiro completo de carrossel slide a slide."""
    tipo_id = post["tipo_conteudo_id"]
    tema = post["tema"]
    avatar_id = post["avatar_id"]
    funil = post["funil"]

    keyword = post.get("keyword_manychat", "ESPANHOL")
    slides = _gerar_slides(tipo_id, tema, avatar_id, avatar_info, cor_fundo, keyword)
    legenda = _gerar_legenda(post, tipo_info, slides[0]["texto_principal"])

    return {
        "formato": "CARROSSEL",
        "total_slides": len(slides),
        "roteiro": {
            "slides": slides,
            "identidade_visual": {
                "cor_fundo": cor_fundo["hex"],
                "cor_nome": cor_fundo["nome"],
                "fonte_titulo": "Bold, grande, impactante",
                "fonte_corpo": "Regular, legivel",
                "logo": "Espanhol com Voce — canto inferior",
                "icone_mao": "Maozinha apontando — canto",
            },
        },
        "legenda": legenda,
    }


def _gerar_slides(tipo_id, tema, avatar_id, avatar_info, cor, keyword="ESPANHOL"):
    """Gera lista de slides do carrossel."""
    dor = avatar_info.get("dor", "")
    desejo = avatar_info.get("desejo", "")

    slides = []

    if tipo_id in [1, 2]:  # Expressoes / Palavras
        expressao = tema.replace("Como falar '", "").replace("' em espanhol", "")
        expressao = expressao.replace("Como falar ", "").replace(" em espanhol", "")
        for suffix in [" (spoiler: nao tem!)", " (cuidado!)", " (da escola)"]:
            expressao = expressao.replace(suffix, "")
        dados, _ = buscar_expressao(tema)
        if dados:
            esp = dados["espanhol"]
            pron = dados["pronuncia"]
            ex_es = dados["exemplo_es"]
            ex_pt = dados["exemplo_pt"]
            alt = dados.get("alternativa", "")
            dica = dados.get("dica", "Nos, nativos, falamos assim no dia a dia")
        else:
            esp, pron, ex_es, ex_pt, alt, dica = "---", "---", "---", "---", "", "Consultar dicionario"
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": f"COMO FALAR\n{expressao.upper()}\nEM ESPANHOL?", "texto_secundario": "Desliza pra aprender →", "cor_fundo": cor["hex"]},
            {"slide": 2, "tipo_slide": "CONTEXTO", "texto_principal": f"Voce usa '{expressao}' todo dia em portugues...", "texto_secundario": "Mas em espanhol e bem diferente!", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "RESPOSTA", "texto_principal": esp.upper(), "texto_secundario": f"Nos, nativos, falamos assim\nPronuncia: {pron}", "cor_fundo": "#FFFFFF"},
            {"slide": 4, "tipo_slide": "EXEMPLO", "texto_principal": ex_es, "texto_secundario": ex_pt, "cor_fundo": cor["hex"]},
            {"slide": 5, "tipo_slide": "ALTERNATIVA", "texto_principal": f"Tambem pode dizer:\n{alt}" if alt else f"Repete comigo:\n{pron}", "texto_secundario": "Depende do pais e do contexto" if alt else "Pratica em voz alta!", "cor_fundo": "#FFFFFF"},
            {"slide": 6, "tipo_slide": "DICA", "texto_principal": "DICA DA ALE:", "texto_secundario": dica, "cor_fundo": cor["hex"]},
            {"slide": 7, "tipo_slide": "CTA", "texto_principal": "SALVA esse post!\nManda pra quem precisa!", "texto_secundario": f"Comenta {keyword} e receba um material gratis", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id == 3:  # Erros / Falsos Amigos
        dados_fa, palavra_fa = buscar_falso_amigo(tema)
        if dados_fa:
            parece = dados_fa["parece_significar"]
            real = dados_fa["significa_realmente"]
            correto = dados_fa["correto_pt"]
            ex_err_es = dados_fa["exemplo_errado_es"]
            ex_err_pt = dados_fa["exemplo_errado_pt"]
            ex_ok_es = dados_fa["exemplo_certo_es"]
            ex_ok_pt = dados_fa["exemplo_certo_pt"]
        else:
            palavra_fa = tema.split(" ")[0]
            parece, real, correto = "---", "---", "---"
            ex_err_es, ex_err_pt, ex_ok_es, ex_ok_pt = "---", "---", "---", "---"
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": f"CUIDADO!\n{palavra_fa.upper() if palavra_fa else tema.upper()[:30]}", "texto_secundario": "Esse erro e mais comum do que voce imagina →", "cor_fundo": "#fbbf24"},
            {"slide": 2, "tipo_slide": "ERRO", "texto_principal": "O QUE VOCE ACHA\nQUE SIGNIFICA:", "texto_secundario": parece.capitalize(), "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "CORRETO", "texto_principal": "O QUE REALMENTE\nSIGNIFICA:", "texto_secundario": real.capitalize(), "cor_fundo": "#10b981"},
            {"slide": 4, "tipo_slide": "EXEMPLO ERRADO", "texto_principal": f"❌ {ex_err_es}", "texto_secundario": ex_err_pt, "cor_fundo": cor["hex"]},
            {"slide": 5, "tipo_slide": "EXEMPLO CERTO", "texto_principal": f"✅ {ex_ok_es}", "texto_secundario": f"{ex_ok_pt}\nAssim que nos, nativos, falamos", "cor_fundo": "#10b981"},
            {"slide": 6, "tipo_slide": "RESUMO", "texto_principal": "RESUMINDO:", "texto_secundario": f"{correto}", "cor_fundo": cor["hex"]},
            {"slide": 7, "tipo_slide": "CTA", "texto_principal": "Voce ja cometeu\nesse erro?", "texto_secundario": f"Comenta {keyword} e receba o PDF de Falsos Cognatos", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id in [7, 8]:  # Dor / Desejo (meio de funil)
        if tipo_id == 7:
            slides = [
                {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper().replace("?", "?\n").strip(), "texto_secundario": "Se sim, desliza... →", "cor_fundo": cor["hex"]},
                {"slide": 2, "tipo_slide": "IDENTIFICACAO", "texto_principal": "Voce entende\nmas nao fala.", "texto_secundario": "Voce traduz tudo na cabeca. Voce trava.", "cor_fundo": cor["hex"]},
                {"slide": 3, "tipo_slide": "VALIDACAO", "texto_principal": "Isso nao e\nfalta de talento.", "texto_secundario": "E falta de METODO.", "cor_fundo": "#FFFFFF"},
                {"slide": 4, "tipo_slide": "EXPLICACAO", "texto_principal": "O problema:", "texto_secundario": "Voce aprendeu a ESTUDAR espanhol.\nNao a FALAR espanhol.", "cor_fundo": cor["hex"]},
                {"slide": 5, "tipo_slide": "SOLUCAO", "texto_principal": "A solucao:", "texto_secundario": "Um metodo que ativa a fala,\nnao que enche de regra.", "cor_fundo": "#10b981"},
                {"slide": 6, "tipo_slide": "CTA", "texto_principal": "Quer destravar?", "texto_secundario": f"Comenta {keyword} que eu te mando o proximo passo", "cor_fundo": "#fbbf24"},
            ]
        else:  # tipo 8 - Desejo
            slides = [
                {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper().rstrip(".").strip(), "texto_secundario": "Desliza e sente isso →", "cor_fundo": cor["hex"]},
                {"slide": 2, "tipo_slide": "VISAO", "texto_principal": f"{desejo}", "texto_secundario": "Isso pode ser a sua realidade.", "cor_fundo": cor["hex"]},
                {"slide": 3, "tipo_slide": "PROVA", "texto_principal": "Meus alunos vivem\nisso TODA semana.", "texto_secundario": "Mais de 5.000 ja destravaram.", "cor_fundo": "#FFFFFF"},
                {"slide": 4, "tipo_slide": "CAMINHO", "texto_principal": "O caminho:", "texto_secundario": "Metodo Imersao Nativa\n3 pilares. Resultado real.", "cor_fundo": cor["hex"]},
                {"slide": 5, "tipo_slide": "CTA", "texto_principal": "Quer comecar?", "texto_secundario": f"Comenta {keyword} que eu te mando uma aula gratuita", "cor_fundo": "#fbbf24"},
            ]
    elif tipo_id == 6:  # Metodo e Bastidor
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper(), "texto_secundario": "A ciencia explica →", "cor_fundo": "#4e4b97"},
            {"slide": 2, "tipo_slide": "PROBLEMA", "texto_principal": "O metodo tradicional:", "texto_secundario": "Decorar regras → esquecer → frustrar → desistir", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "PILAR 1", "texto_principal": "Pilar 1:\nNucleo del Conocimiento", "texto_secundario": "Vocabulario estrategico que voce usa de verdade", "cor_fundo": cor["hex"]},
            {"slide": 4, "tipo_slide": "PILAR 2", "texto_principal": "Pilar 2:\nImersao Ativa", "texto_secundario": "Exposicao ao espanhol real — sem depender de traducao", "cor_fundo": "#FFFFFF"},
            {"slide": 5, "tipo_slide": "PILAR 3", "texto_principal": "Pilar 3:\nAcompanhamento Inteligente", "texto_secundario": "Repeticao espacada + conversacao guiada + feedback", "cor_fundo": cor["hex"]},
            {"slide": 6, "tipo_slide": "RESULTADO", "texto_principal": "+5.000 alunos\nja destravaram", "texto_secundario": "Acesso vitalicio. Garantia de 7 dias.", "cor_fundo": "#10b981"},
            {"slide": 7, "tipo_slide": "CTA", "texto_principal": "Quer conhecer\no metodo?", "texto_secundario": f"Comenta METODO que eu te explico tudo", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id == 10:  # Prova Social — tema ja contem a historia
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper(), "texto_secundario": "Historia real de aluno →", "cor_fundo": cor["hex"]},
            {"slide": 2, "tipo_slide": "ANTES", "texto_principal": "ANTES:", "texto_secundario": f"Chegou travado. {dor}\nFrustrado. Quase desistindo.", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "VIRADA", "texto_principal": "Entao comecou com o\nMetodo Imersao Nativa", "texto_secundario": "Sem decorar. Sem sofrer. Com metodo.", "cor_fundo": "#FFFFFF"},
            {"slide": 4, "tipo_slide": "DEPOIS", "texto_principal": "DEPOIS:", "texto_secundario": tema, "cor_fundo": "#10b981"},
            {"slide": 5, "tipo_slide": "PROVA", "texto_principal": "Inserir print/depoimento\nreal do aluno aqui", "texto_secundario": "Use screenshot de mensagem do WhatsApp ou Instagram", "cor_fundo": "#FFFFFF"},
            {"slide": 6, "tipo_slide": "CTA", "texto_principal": "Quer o mesmo\nresultado?", "texto_secundario": f"Comenta AULA que eu te mando a aula demonstrativa gratuita", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id == 11:  # CTA Indireto
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": "VOCE QUER DESTRAVAR\nSEU ESPANHOL?", "texto_secundario": "Desliza →", "cor_fundo": cor["hex"]},
            {"slide": 2, "tipo_slide": "VERDADE", "texto_principal": "Eu vou ser sincera\ncom voce:", "texto_secundario": "Sozinho e possivel.\nMas demora MUITO mais.", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "CONVITE", "texto_principal": "Eu preparei uma\naula gratuita", "texto_secundario": "Onde eu te mostro o caminho\npra destravar de verdade.", "cor_fundo": "#FFFFFF"},
            {"slide": 4, "tipo_slide": "PROVA", "texto_principal": "+5.000 alunos\nja fizeram esse caminho", "texto_secundario": "R$397 com acesso vitalicio\nGarantia de 7 dias", "cor_fundo": cor["hex"]},
            {"slide": 5, "tipo_slide": "CTA", "texto_principal": "Comenta AULA", "texto_secundario": "Que eu te mando o link\nda aula demonstrativa gratuita", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id == 9:  # Quebra de Crencas — tema ja e a crenca
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper(), "texto_secundario": "Voce acredita nisso? →", "cor_fundo": "#4e4b97"},
            {"slide": 2, "tipo_slide": "CRENCA", "texto_principal": "O que te ensinaram:", "texto_secundario": f"Que {tema.lower().rstrip('.')}.", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "VERDADE", "texto_principal": "A verdade:", "texto_secundario": "Isso nao funciona porque o cerebro\nnao aprende idioma por decoreba.\nEle aprende por CONEXAO e uso real.", "cor_fundo": "#FFFFFF"},
            {"slide": 4, "tipo_slide": "CIENCIA", "texto_principal": "O Metodo Imersao Nativa\nfunciona porque:", "texto_secundario": "1. Vocabulario estrategico (nao listas)\n2. Exposicao ao espanhol real\n3. Pratica guiada com feedback", "cor_fundo": cor["hex"]},
            {"slide": 5, "tipo_slide": "SOLUCAO", "texto_principal": "O que funciona\nDE VERDADE:", "texto_secundario": "Imersao + pratica + acompanhamento\n+5.000 alunos ja comprovaram", "cor_fundo": "#10b981"},
            {"slide": 6, "tipo_slide": "CTA", "texto_principal": "Voce acreditava nisso?", "texto_secundario": f"Comenta {keyword} se voce quer saber mais", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id == 12:  # Historia Pessoal — tema ja e o aprendizado
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper(), "texto_secundario": "Minha historia →", "cor_fundo": cor["hex"]},
            {"slide": 2, "tipo_slide": "HISTORIA 1", "texto_principal": "Quando eu cheguei\nno Brasil...", "texto_secundario": "Eu nao falava UMA palavra em portugues.", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "HISTORIA 2", "texto_principal": "Eu aprendi por\nimersao e necessidade.", "texto_secundario": "Sem escola. Sem metodo tradicional.", "cor_fundo": "#FFFFFF"},
            {"slide": 4, "tipo_slide": "APRENDIZADO", "texto_principal": "Foi isso que me ensinou:", "texto_secundario": f"Que o cerebro aprende por conexao,\nnao por decoreba. E por isso que\no Metodo Imersao Nativa funciona.", "cor_fundo": cor["hex"]},
            {"slide": 5, "tipo_slide": "RESULTADO", "texto_principal": "Hoje ja ajudei\n+5.000 alunos", "texto_secundario": "Com o Metodo Imersao Nativa", "cor_fundo": "#10b981"},
            {"slide": 6, "tipo_slide": "CTA", "texto_principal": "Me conta SUA historia\nnos comentarios", "texto_secundario": f"E comenta {keyword} pra saber mais sobre o metodo", "cor_fundo": "#fbbf24"},
        ]
    elif tipo_id == 5:  # Cultura e Diferencas — tema descreve o assunto
        slides = [
            {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper(), "texto_secundario": "Voce sabia? Desliza →", "cor_fundo": cor["hex"]},
            {"slide": 2, "tipo_slide": "BRASIL", "texto_principal": "No Brasil:", "texto_secundario": "Voce esta acostumado com um jeito.\nMas no mundo hispanico e BEM diferente.", "cor_fundo": cor["hex"]},
            {"slide": 3, "tipo_slide": "HISPANICO", "texto_principal": "No mundo hispanico:", "texto_secundario": f"Sobre '{tema.lower()}':\nCada pais tem seu proprio costume e forma de lidar.", "cor_fundo": "#FFFFFF"},
            {"slide": 4, "tipo_slide": "DIFERENCA", "texto_principal": "A grande diferenca:", "texto_secundario": "O que parece normal pra voce\npode ser estranho (ou ate ofensivo) la fora.", "cor_fundo": cor["hex"]},
            {"slide": 5, "tipo_slide": "CURIOSIDADE", "texto_principal": "Curiosidade:", "texto_secundario": "Nos, nativos, achamos isso completamente normal!\nE voces brasileiros estranham muito.", "cor_fundo": "#FFFFFF"},
            {"slide": 6, "tipo_slide": "DICA", "texto_principal": "DICA DA ALE:", "texto_secundario": "Pesquise sobre o pais ESPECIFICO\nque voce vai visitar ou morar.\nO espanhol e diverso!", "cor_fundo": cor["hex"]},
            {"slide": 7, "tipo_slide": "CTA", "texto_principal": "Qual pais hispanico\nvoce mais quer conhecer?", "texto_secundario": f"Comenta! E salva esse post pra consultar depois.", "cor_fundo": "#fbbf24"},
        ]
    else:  # Tipo 4 (perguntas em carrossel) e outros
        dados_perg = buscar_pergunta(tema) if tipo_id == 4 else None
        if dados_perg:
            slides = [
                {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper().replace("SEGUIDOR PERGUNTA: ", ""), "texto_secundario": "Seguidor perguntou — Ale responde →", "cor_fundo": cor["hex"]},
                {"slide": 2, "tipo_slide": "PERGUNTA", "texto_principal": "A duvida:", "texto_secundario": tema.replace("Seguidor pergunta: ", ""), "cor_fundo": cor["hex"]},
                {"slide": 3, "tipo_slide": "RESPOSTA", "texto_principal": "A resposta:", "texto_secundario": dados_perg["resposta"], "cor_fundo": "#FFFFFF"},
                {"slide": 4, "tipo_slide": "EXEMPLO", "texto_principal": dados_perg["exemplo_es"], "texto_secundario": dados_perg["exemplo_pt"], "cor_fundo": cor["hex"]},
                {"slide": 5, "tipo_slide": "DICA", "texto_principal": "DICA DA ALE:", "texto_secundario": dados_perg.get("dica", "Nos, nativos, falamos assim no dia a dia"), "cor_fundo": "#FFFFFF"},
                {"slide": 6, "tipo_slide": "CTA", "texto_principal": "Manda SUA duvida\nnos comentarios!", "texto_secundario": f"Comenta {keyword} e receba um material gratis", "cor_fundo": "#fbbf24"},
            ]
        else:
            slides = [
                {"slide": 1, "tipo_slide": "CAPA", "texto_principal": tema.upper(), "texto_secundario": "Desliza →", "cor_fundo": cor["hex"]},
                {"slide": 2, "tipo_slide": "CONTEUDO", "texto_principal": tema, "texto_secundario": "Nos, nativos, falamos assim no dia a dia.", "cor_fundo": cor["hex"]},
                {"slide": 3, "tipo_slide": "DICA", "texto_principal": "DICA DA ALE:", "texto_secundario": "Pratique em voz alta!\nRepetir e o segredo da fluencia.", "cor_fundo": "#FFFFFF"},
                {"slide": 4, "tipo_slide": "CTA", "texto_principal": "Salva esse post!", "texto_secundario": f"Comenta {keyword} e receba um material gratis", "cor_fundo": "#fbbf24"},
            ]

    return slides


# ================================================================
# LEGENDA (serve pra reel e carrossel)
# ================================================================

def _gerar_legenda(post, tipo_info, hook_ou_titulo):
    """Gera legenda completa para o post."""
    tipo_id = post["tipo_conteudo_id"]
    tema = post["tema"]
    keyword = post["keyword_manychat"]
    hashtags = post["hashtags"]
    funil = post["funil"]
    avatar = post["avatar"]

    # Linha de abertura (primeiras palavras visiveis antes do "mais")
    abertura = _abertura_legenda(tipo_id, tema)

    # Corpo da legenda
    corpo = _corpo_legenda(tipo_id, tema, funil, avatar)

    # CTA na legenda
    cta_legenda = _cta_legenda(tipo_id, keyword, funil)

    # Monta legenda completa
    legenda = f"""{abertura}

{corpo}

{cta_legenda}

{hashtags}"""

    return legenda.strip()


def _abertura_legenda(tipo_id, tema):
    """Primeiras palavras da legenda — precisam gerar clique no 'mais'."""
    aberturas = {
        1: f"Voce fala isso todo dia mas nao sabe em espanhol 👇",
        2: f"Essa palavra simples vai te surpreender 👇",
        3: f"⚠️ CUIDADO! Esse erro e mais perigoso do que voce imagina.",
        4: f"Voces pediram, eu respondi 👇",
        5: f"Sabia que isso muda de pais pra pais? 🌎",
        6: f"Voce sabe POR QUE voce trava? A ciencia explica 👇",
        7: f"Se voce se identifica... esse post e pra voce. 👇",
        8: f"Fecha os olhos e imagina isso... ✨",
        9: f"Tudo que te ensinaram sobre espanhol e MENTIRA. 👇",
        10: f"Olha o resultado que esse aluno teve 👇",
        11: f"Eu tenho algo especial pra voce. Le ate o final. 👇",
        12: f"Eu preciso te contar uma coisa sobre mim... 👇",
    }
    return aberturas.get(tipo_id, f"{tema} 👇")


def _corpo_legenda(tipo_id, tema, funil, avatar):
    """Corpo da legenda."""
    if tipo_id in [1, 2]:
        return (
            f"{tema}\n\n"
            f"Nos, nativos, falamos isso de um jeito que voce provavelmente nunca aprendeu na escola.\n\n"
            f"Assiste/desliza pra aprender a forma CERTA de falar isso em espanhol."
        )
    elif tipo_id == 3:
        return (
            f"{tema}\n\n"
            f"Esse e um dos erros mais classicos que brasileiros cometem.\n"
            f"E dependendo da situacao, pode ser BEM constrangedor.\n\n"
            f"Assiste/desliza pra nunca mais errar isso."
        )
    elif tipo_id == 4:
        return (
            f"{tema}\n\n"
            f"Recebi essa pergunta e achei que MUITA gente tem a mesma duvida.\n\n"
            f"A resposta e mais simples do que voce imagina."
        )
    elif tipo_id == 5:
        return (
            f"{tema}\n\n"
            f"O mundo hispanico e muito mais diverso do que voce imagina.\n"
            f"Cada pais tem seus costumes, expressoes e formas de falar.\n\n"
            f"Desliza/assiste pra descobrir."
        )
    elif tipo_id == 6:
        return (
            f"{tema}\n\n"
            f"O Metodo Imersao Nativa tem 3 pilares:\n"
            f"1️⃣ Nucleo del Conocimiento\n"
            f"2️⃣ Imersao Ativa\n"
            f"3️⃣ Acompanhamento Inteligente\n\n"
            f"E assim que +5.000 alunos destravaram o espanhol."
        )
    elif tipo_id == 7:
        return (
            f"{tema}\n\n"
            f"Eu sei como e essa frustracao.\n"
            f"Voce estuda, se esforça, entende tudo...\n"
            f"Mas na hora de FALAR, trava.\n\n"
            f"O problema nao e voce. E o metodo."
        )
    elif tipo_id == 8:
        return (
            f"{tema}\n\n"
            f"Isso nao e um sonho distante.\n"
            f"E o que meus alunos vivem toda semana.\n\n"
            f"Em 6 meses voce pode estar vivendo isso tambem."
        )
    elif tipo_id == 9:
        return (
            f"{tema}\n\n"
            f"Eu sei que parece contra-intuitivo.\n"
            f"Mas o metodo tradicional te ensina a ESTUDAR espanhol.\n"
            f"Nao a FALAR espanhol.\n\n"
            f"A diferenca muda tudo."
        )
    elif tipo_id == 10:
        return (
            f"{tema}\n\n"
            f"Essa e uma historia real de um aluno do Imersao Nativa.\n"
            f"Ele/ela comecou travado, frustrado.\n"
            f"Hoje, fala espanhol com naturalidade.\n\n"
            f"Se ele/ela conseguiu, voce tambem consegue."
        )
    elif tipo_id == 11:
        return (
            f"{tema}\n\n"
            f"Eu preparei uma aula demonstrativa gratuita.\n"
            f"Nessa aula, eu te mostro o caminho real pra destravar.\n\n"
            f"Sem promessa vazia. Sem enrolacao.\n"
            f"So o metodo que ja ajudou +5.000 alunos."
        )
    elif tipo_id == 12:
        return (
            f"{tema}\n\n"
            f"Quando eu cheguei no Brasil, eu nao falava portugues.\n"
            f"Aprendi por imersao, por necessidade.\n"
            f"Essa experiencia me ensinou COMO o cerebro realmente aprende.\n\n"
            f"E por isso que eu ensino diferente."
        )
    return tema


def _cta_legenda(tipo_id, keyword, funil):
    """CTA escrito na legenda."""
    if funil == "FUNDO":
        return (
            f"👉 Comenta {keyword} que eu te mando o proximo passo!\n"
            f"📌 Salva esse post pra consultar depois.\n"
            f"📲 Link na bio!"
        )
    elif funil == "MEIO":
        return (
            f"💬 Se voce se identificou, comenta {keyword}!\n"
            f"📌 Salva e manda pra quem precisa.\n"
            f"👉 Segue @espanholcomvoce pra mais conteudo assim."
        )
    else:  # TOPO
        return (
            f"📌 Salva esse post!\n"
            f"📤 Manda pra quem precisa aprender isso.\n"
            f"💬 Comenta {keyword} pra receber um material gratis!"
        )


# ================================================================
# CLASSE PRINCIPAL
# ================================================================

class AgenteRoteirista:
    """Le o calendario e gera roteiros completos."""

    def __init__(self, arquivo_calendario):
        self.arquivo_calendario = Path(arquivo_calendario)
        self.tipos_config = carregar_json("tipos_conteudo.json")
        self.briefing = carregar_briefing()
        self.objetivos = carregar_json("objetivos.json")

        # Index de tipos
        self.tipos_info = {}
        for nivel in ["topo", "meio", "fundo"]:
            for t in self.tipos_config["tipos_conteudo"][nivel]["tipos"]:
                self.tipos_info[t["id"]] = {**t, "funil": nivel}

        # Avatares com dores/desejos do briefing
        self.avatares_info = {
            "viajante": {
                "dor": "Entende mas nao fala. Trava na hora de se comunicar.",
                "desejo": "Pedir comida, conversar com locais, viver a experiencia completa.",
                "gatilho": "Voce entende mas nao fala? Esse e o motivo...",
            },
            "vai_morar_fora": {
                "dor": "Inseguranca de nao conseguir se adaptar no novo pais.",
                "desejo": "Autonomia, pertencer, comecar bem a nova vida.",
                "gatilho": "Voce nao pode chegar la sem falar...",
            },
            "academico": {
                "dor": "Pode perder a oportunidade da carreira pelo idioma.",
                "desejo": "Cumprir o requisito, passar na prova, nao falhar.",
                "gatilho": "Requisito: certificacao de espanhol. E agora?",
            },
            "profissional": {
                "dor": "Nao consegue se expressar como realmente e no trabalho.",
                "desejo": "Posicionamento, respeito, crescimento de carreira.",
                "gatilho": "Voce e competente na sua area mas trava em espanhol...",
            },
        }

        # Indice de cor (rotaciona)
        self.cor_index = 0

    def _proxima_cor(self):
        """Rotaciona cores oficiais entre posts."""
        cor = CORES[self.cor_index % len(CORES)]
        self.cor_index += 1
        return cor

    def gerar_roteiros(self):
        """Le calendario e gera roteiro para cada post."""
        with open(self.arquivo_calendario, "r", encoding="utf-8") as f:
            calendario = json.load(f)

        roteiros = []
        for post in calendario:
            tipo_id = post["tipo_conteudo_id"]
            tipo_info = self.tipos_info.get(tipo_id, {})
            avatar_info = self.avatares_info.get(post["avatar_id"], {})
            cor = self._proxima_cor()

            if post["formato"] == "REEL":
                roteiro = gerar_roteiro_reel(post, tipo_info, avatar_info, cor)
            else:
                roteiro = gerar_roteiro_carrossel(post, tipo_info, avatar_info, cor)

            # Combina info do calendario + roteiro
            roteiro_completo = {
                "post_id": f"{post['data']}_{post['horario'].replace(':', '')}",
                "data": post["data"],
                "dia_semana": post["dia_semana"],
                "horario": post["horario"],
                "formato": post["formato"],
                "funil": post["funil"],
                "tipo_conteudo_id": tipo_id,
                "tipo_conteudo": post["tipo_conteudo"],
                "avatar": post["avatar"],
                "tema": post["tema"],
                "keyword_manychat": post["keyword_manychat"],
                **roteiro,
            }
            roteiros.append(roteiro_completo)

        return roteiros

    def salvar_json(self, roteiros):
        nome_base = self.arquivo_calendario.stem.replace("calendario_", "roteiros_")
        caminho = OUTPUT_DIR / f"{nome_base}.json"
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(roteiros, f, ensure_ascii=False, indent=2)
        print(f"  [OK] JSON: {caminho}")
        return caminho

    def salvar_csv_resumido(self, roteiros):
        """CSV com visao resumida para equipe de producao."""
        nome_base = self.arquivo_calendario.stem.replace("calendario_", "roteiros_resumo_")
        caminho = OUTPUT_DIR / f"{nome_base}.csv"

        campos = [
            "post_id", "data", "dia_semana", "horario", "formato", "funil",
            "tipo_conteudo", "avatar", "tema", "keyword_manychat",
            "hook_ou_capa", "total_slides_ou_duracao", "legenda_preview",
        ]

        with open(caminho, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writeheader()

            for r in roteiros:
                if r["formato"] == "REEL":
                    hook = r["roteiro"]["hook_3s"]["fala"]
                    duracao = r.get("duracao_estimada", "30-60s")
                else:
                    hook = r["roteiro"]["slides"][0]["texto_principal"].replace("\n", " ")
                    duracao = f"{r['total_slides']} slides"

                legenda_preview = r["legenda"][:100] + "..." if len(r["legenda"]) > 100 else r["legenda"]

                writer.writerow({
                    "post_id": r["post_id"],
                    "data": r["data"],
                    "dia_semana": r["dia_semana"],
                    "horario": r["horario"],
                    "formato": r["formato"],
                    "funil": r["funil"],
                    "tipo_conteudo": r["tipo_conteudo"],
                    "avatar": r["avatar"],
                    "tema": r["tema"],
                    "keyword_manychat": r["keyword_manychat"],
                    "hook_ou_capa": hook,
                    "total_slides_ou_duracao": duracao,
                    "legenda_preview": legenda_preview.replace("\n", " "),
                })

        print(f"  [OK] CSV resumido: {caminho}")
        return caminho

    def gerar_resumo(self, roteiros):
        total = len(roteiros)
        reels = sum(1 for r in roteiros if r["formato"] == "REEL")
        carrosseis = total - reels

        print(f"\n  {'=' * 60}")
        print(f"  ROTEIROS @espanholcomvoce")
        print(f"  Gerados a partir de: {self.arquivo_calendario.name}")
        print(f"  {'=' * 60}")
        print(f"  Total: {total} roteiros ({reels} reels + {carrosseis} carrosseis)")
        print(f"  Cada reel: hook 3s + fala + pilulas visuais + CTA + legenda")
        print(f"  Cada carrossel: {5}-{7} slides + legenda completa")
        print(f"  Tom de voz: Ale (nativa, direta, proxima, motivadora)")
        print(f"  Identidade visual: pilulas coloridas (reels) / cor solida (carrosseis)")
        print(f"  {'=' * 60}")

    def executar(self):
        print(f"\n  Agente Roteirista — @espanholcomvoce")
        print(f"  Lendo calendario: {self.arquivo_calendario.name}\n")

        roteiros = self.gerar_roteiros()
        self.salvar_json(roteiros)
        self.salvar_csv_resumido(roteiros)
        self.gerar_resumo(roteiros)

        return roteiros


# --- CLI ---
# Uso: python agente_roteirista.py <caminho_calendario.json>
# Se nenhum arquivo for passado, usa o mais recente na pasta output/
if __name__ == "__main__":
    import sys
    import glob

    if len(sys.argv) >= 2:
        arquivo = sys.argv[1]
    else:
        # Busca o calendario mais recente
        padrao = str(OUTPUT_DIR / "calendario_*.json")
        arquivos = sorted(glob.glob(padrao))
        if not arquivos:
            print("  [ERRO] Nenhum calendario encontrado em agentes/output/")
            print("  Execute primeiro o Agente Estrategista.")
            sys.exit(1)
        arquivo = arquivos[-1]
        print(f"  Usando calendario mais recente: {arquivo}")

    agente = AgenteRoteirista(arquivo)
    agente.executar()
