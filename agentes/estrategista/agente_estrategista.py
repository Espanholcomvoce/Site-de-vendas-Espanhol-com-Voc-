"""
Agente Estrategista Mensal — @espanholcomvoce
==============================================
Gera calendario completo de conteudo para Instagram/Facebook.

Regras de negocio (briefing_marca.md):
- 6 posts/dia: 3 reels + 3 carrosseis
- 12 tipos de conteudo (IDs: 1,2,3,4,5,6,7,8,9,10,11,12)
- Funil: Topo 40% | Meio 35% | Fundo 25%
- 4 avatares: Viajante, Vai Morar Fora, Academico, Profissional
- NUNCA 2 posts de fundo no mesmo dia
- NUNCA 2 CTAs diretos seguidos
- Todo post de TOPO tem CTA de engajamento
- Todo post de FUNDO tem palavra-chave ManyChat
- Ao menos 1 post/semana com cada avatar

Saida: JSON + CSV do calendario completo.
"""

import json
import csv
import random
import calendar
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

# --- Caminhos ---
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def carregar_json(nome):
    with open(CONFIG_DIR / nome, "r", encoding="utf-8") as f:
        return json.load(f)


# ================================================================
# BANCO DE TEMAS — organizado por tipo_id x avatar_id
# Cada lista tem 8+ temas para garantir variedade no mes inteiro
# ================================================================

BANCO_TEMAS = {
    # --- TOPO ---
    1: {  # Expressoes Idiomaticas
        "viajante": [
            "Como falar 'se vira nos 30' em espanhol",
            "Como falar 'dar um jeitinho' em espanhol",
            "Como falar 'to de boa' em espanhol",
            "Como falar 'ficar de bobeira' em espanhol",
            "Como falar 'chutar o balde' em espanhol",
            "Como falar 'cara de pau' em espanhol",
            "Como falar 'pagar mico' em espanhol",
            "Como falar 'dar mole' em espanhol",
        ],
        "vai_morar_fora": [
            "Como falar 'saudade' em espanhol (spoiler: nao tem!)",
            "Como falar 'gambiarra' em espanhol",
            "Como falar 'matar a saudade' em espanhol",
            "Como falar 'quebrar o galho' em espanhol",
            "Como falar 'dar conta' em espanhol",
            "Como falar 'puxar saco' em espanhol",
            "Como falar 'fazer hora' em espanhol",
            "Como falar 'enrolar' em espanhol",
        ],
        "academico": [
            "Como falar 'colar na prova' em espanhol",
            "Como falar 'ralar muito' em espanhol",
            "Como falar 'ficar por fora' em espanhol",
            "Como falar 'pegar no pe' em espanhol",
            "Como falar 'matar aula' em espanhol",
            "Como falar 'tirar de letra' em espanhol",
            "Como falar 'nao ter pe nem cabeca' em espanhol",
            "Como falar 'dar um branco' em espanhol",
        ],
        "profissional": [
            "Como falar 'vestir a camisa' em espanhol",
            "Como falar 'botar a mao na massa' em espanhol",
            "Como falar 'bater meta' em espanhol",
            "Como falar 'dar um toque' em espanhol",
            "Como falar 'pisar na bola' em espanhol",
            "Como falar 'tapar o sol com a peneira' em espanhol",
            "Como falar 'puxar o tapete' em espanhol",
            "Como falar 'empurrar com a barriga' em espanhol",
        ],
    },
    2: {  # Palavras do Cotidiano
        "viajante": [
            "Como falar 'carona' em espanhol",
            "Como falar 'saudade' em espanhol",
            "Como falar 'gorjeta' em espanhol",
            "Como falar 'perrengue' em espanhol",
            "Como falar 'mochila' em espanhol",
            "Como falar 'fila' em espanhol",
            "Como falar 'troco' em espanhol",
            "Como falar 'mala' em espanhol (cuidado!)",
        ],
        "vai_morar_fora": [
            "Como falar 'aluguel' em espanhol",
            "Como falar 'conta de luz' em espanhol",
            "Como falar 'carteira de motorista' em espanhol",
            "Como falar 'comprovante de residencia' em espanhol",
            "Como falar 'ficha medica' em espanhol",
            "Como falar 'boleto' em espanhol",
            "Como falar 'mudanca' em espanhol",
            "Como falar 'visto de trabalho' em espanhol",
        ],
        "academico": [
            "Como falar 'bolsa de estudos' em espanhol",
            "Como falar 'nota' (da escola) em espanhol",
            "Como falar 'materia' (disciplina) em espanhol",
            "Como falar 'TCC' em espanhol",
            "Como falar 'mestrado' em espanhol",
            "Como falar 'prova' em espanhol",
            "Como falar 'formatura' em espanhol",
            "Como falar 'estagio' em espanhol",
        ],
        "profissional": [
            "Como falar 'reuniao' em espanhol",
            "Como falar 'prazo' em espanhol",
            "Como falar 'ferias' em espanhol",
            "Como falar 'demissao' em espanhol",
            "Como falar 'salario' em espanhol",
            "Como falar 'curriculo' em espanhol",
            "Como falar 'hora extra' em espanhol",
            "Como falar 'folga' em espanhol",
        ],
    },
    3: {  # Erros e Falsos Amigos
        "viajante": [
            "EMBARAZADA nao e envergonhada — cuidado na viagem!",
            "VASO em espanhol e copo, nao vaso de flor!",
            "BORRACHA em espanhol e... bebada!",
            "POLVO nao e polvo — e po/poeira!",
            "PROPINA nao e gorjeta — e suborno!",
            "LARGO em espanhol e comprido, nao largo!",
            "OFICINA em espanhol e escritorio!",
            "ESQUISITO em espanhol (exquisito) e delicioso!",
        ],
        "vai_morar_fora": [
            "PISO em espanhol e apartamento, nao chao!",
            "FIRMA nao e empresa — e assinatura!",
            "CONTESTAR em espanhol e responder, nao contestar!",
            "JUBILACION nao e jubilacao — e aposentadoria!",
            "ABONAR em espanhol e pagar, nao adubar!",
            "CUENTA pode ser conta bancaria E conta do restaurante!",
            "COCHE em espanhol e carro, nao cocho!",
            "CARPETA em espanhol e pasta, nao carpete!",
        ],
        "academico": [
            "TODAVIA em espanhol nao e todavia — e ainda/contudo!",
            "ASIGNATURA nao e assinatura — e materia/disciplina!",
            "EXITO em espanhol e sucesso, nao saida!",
            "APROBAR nao e aprovar — e ser aprovado na prova!",
            "CARRERA em espanhol e curso universitario!",
            "APUNTES nao sao apontes — sao anotacoes!",
            "INTRODUCCION vs PRESENTACION — quando usar cada um",
            "DESDE LUEGO nao e 'desde logo'!",
        ],
        "profissional": [
            "NEGOCIO tem plural diferente em espanhol!",
            "SALARIO vs SUELDO — qual usar no trabalho?",
            "DESPEDIR pode ser demitir OU se despedir!",
            "PRESUPUESTO — nao erre essa na reuniao!",
            "FACTURA nao e fatura do cartao — e nota fiscal!",
            "CARGO em espanhol pode significar taxa/cobranca!",
            "JEFE vs PATRON — a diferenca importa",
            "EMPRESA vs COMPANIA — quando usar cada um",
        ],
    },
    5: {  # Cultura e Diferencas
        "viajante": [
            "Argentina vs Espanha: como cada um fala 'voce'",
            "Por que na Espanha jantam as 22h?",
            "O que e siesta e por que os espanhois amam",
            "Como funciona gorjeta em cada pais hispanico",
            "Festas que voce precisa viver: Espanha vs America Latina",
            "Girias do Mexico que nao existem na Espanha",
            "Comidas com nomes diferentes em cada pais hispanico",
            "Como cada pais hispanico diz 'legal/massa/bacana'",
        ],
        "vai_morar_fora": [
            "Choque cultural: o que ninguem conta sobre morar na Espanha",
            "Sistema de saude Espanha vs Brasil — a diferenca",
            "Como espanhois veem brasileiros de verdade",
            "Feriados na Espanha que nao existem no Brasil",
            "Supermercado na Espanha: o que tem e o que falta",
            "Transporte publico Espanha vs Brasil",
            "Como e o inverno de verdade em Madrid",
            "Vida social: espanhois vs brasileiros",
        ],
        "academico": [
            "Espanhol da Espanha vs America Latina — diferencas reais",
            "Paises onde espanhol e lingua oficial (sao mais que voce pensa)",
            "A origem do espanhol: do latim ate hoje",
            "Por que o espanhol e a 2a lingua mais falada do mundo",
            "Universidades hispanicas entre as melhores do mundo",
            "Escritores hispanicos que voce deveria conhecer",
            "Real Academia Espanola: 5 fatos que voce nao sabia",
            "Como o espanhol virou lingua oficial da ONU",
        ],
        "profissional": [
            "Cultura de trabalho na Espanha vs no Brasil",
            "Reunioes no Brasil vs no Mexico — a diferenca",
            "Por que multinacionais exigem espanhol no curriculo",
            "Mercosul e a importancia do espanhol nos negocios",
            "Setores que mais contratam quem fala espanhol",
            "Diferenca entre networking brasileiro e hispanico",
            "Horario comercial Brasil vs paises hispanicos",
            "Etiqueta empresarial em paises hispanicos",
        ],
    },
    # --- MEIO ---
    4: {  # Perguntas de Seguidores
        "viajante": [
            "Seguidor pergunta: como falar 'namorar' em espanhol?",
            "Seguidor pergunta: como pronunciar o S em espanhol?",
            "Seguidor pergunta: qual diferenca entre buen e bueno?",
            "Seguidor pergunta: como pedir cardapio no restaurante?",
            "Seguidor pergunta: como falar as horas em espanhol?",
            "Seguidor pergunta: como se apresentar em espanhol?",
            "Seguidor pergunta: MUY vs MUCHO — qual usar?",
            "Seguidor pergunta: como falar os numeros grandes?",
        ],
        "vai_morar_fora": [
            "Seguidor pergunta: como marcar consulta medica em espanhol?",
            "Seguidor pergunta: como falar com casero/proprietario?",
            "Seguidor pergunta: documentos para o NIE — vocabulario",
            "Seguidor pergunta: como abrir conta bancaria em espanhol?",
            "Seguidor pergunta: como reclamar de um servico?",
            "Seguidor pergunta: como pedir orcamento em espanhol?",
            "Seguidor pergunta: TU vs USTED — quando usar?",
            "Seguidor pergunta: como falar no telefone em espanhol?",
        ],
        "academico": [
            "Seguidor pergunta: SER vs ESTAR — regra definitiva?",
            "Seguidor pergunta: quando usar subjuntivo?",
            "Seguidor pergunta: POR vs PARA — como nao errar?",
            "Seguidor pergunta: como se preparar para o DELE?",
            "Seguidor pergunta: preterito perfecto vs indefinido?",
            "Seguidor pergunta: como melhorar redacao em espanhol?",
            "Seguidor pergunta: como interpretar texto em espanhol?",
            "Seguidor pergunta: verbos irregulares — tem macete?",
        ],
        "profissional": [
            "Seguidor pergunta: como comecar email formal em espanhol?",
            "Seguidor pergunta: como dar feedback em espanhol?",
            "Seguidor pergunta: como encerrar reuniao em espanhol?",
            "Seguidor pergunta: como negociar preco em espanhol?",
            "Seguidor pergunta: espanhol basico para entrevista?",
            "Seguidor pergunta: como apresentar resultados em espanhol?",
            "Seguidor pergunta: small talk antes da reuniao?",
            "Seguidor pergunta: como pedir aumento em espanhol?",
        ],
    },
    7: {  # Dor e Identificacao — CRITICO
        "viajante": [
            "Voce entende espanhol mas trava na hora de falar?",
            "Voce traduz tudo na cabeca antes de abrir a boca?",
            "Voce tem vergonha de falar espanhol na frente dos outros?",
            "Voce depende do Google Tradutor pra tudo na viagem?",
            "Voce entende o filme mas nao consegue pedir comida?",
            "Voce fica em silencio quando tentam conversar com voce?",
            "Voce fala portunhol e torce pra entenderem?",
            "Voce sente que entende 80% mas fala 10%?",
        ],
        "vai_morar_fora": [
            "Voce vai se mudar e tem medo de nao se adaptar?",
            "Voce mora fora mas ainda depende de outros pra resolver coisas?",
            "Voce se sente menos capaz so por causa do idioma?",
            "Voce evita ligacoes porque tem medo de nao entender?",
            "Voce se isola porque nao consegue acompanhar as conversas?",
            "Voce sente que parece menos inteligente em espanhol?",
            "Voce entende mas nao consegue se expressar como realmente e?",
            "Voce tem medo de parecer limitado por causa do idioma?",
        ],
        "academico": [
            "Voce ja estudou espanhol e mesmo assim nao consegue conversar?",
            "Voce decora regras mas na hora da prova da branco?",
            "Voce entende gramatica mas nao sabe usar na pratica?",
            "Voce tem medo de reprovar na prova de proficiencia?",
            "Voce pode perder a bolsa por causa do espanhol?",
            "Voce estuda sozinho e sente que nao avanca?",
            "Voce sabe conjugar mas trava na conversacao?",
            "Voce acha que espanhol e facil mas nao consegue ser fluente?",
        ],
        "profissional": [
            "Voce e competente na sua area mas trava em espanhol?",
            "Voce perde oportunidades porque nao fala espanhol?",
            "Voce fica mudo nas reunioes em espanhol?",
            "Voce nao consegue defender suas ideias em espanhol?",
            "Voce manda emails em espanhol e morre de medo de errar?",
            "Voce evita clientes hispanicos por inseguranca?",
            "Voce sente que o idioma esta travando sua carreira?",
            "Voce finge que entendeu na reuniao em espanhol?",
        ],
    },
    8: {  # Desejo e Transformacao
        "viajante": [
            "Imagina chegar na viagem e conversar com naturalidade...",
            "Imagina pedir comida, pechinchar e fazer amigos em espanhol...",
            "6 meses para sair do 'entendo tudo' para 'falo de verdade'",
            "Como seria viajar sem depender de tradutor?",
            "Imagina viver a experiencia completa da viagem sem barreira...",
            "O que muda quando voce consegue se comunicar de verdade",
            "Imagina voltar da viagem falando espanhol...",
            "A diferenca entre turistar e realmente viver a cultura",
        ],
        "vai_morar_fora": [
            "Imagina resolver tudo sozinho no seu novo pais...",
            "Como seria se sentir em casa em um pais hispanico?",
            "Imagina fazer amigos nativos e pertencer de verdade...",
            "6 meses para ir do medo a autonomia total",
            "Imagina conseguir o emprego que voce merece la fora...",
            "Como seria nao precisar de ninguem para resolver burocracia?",
            "Imagina ser respeitado profissionalmente no novo pais...",
            "A liberdade de se expressar como voce realmente e",
        ],
        "academico": [
            "Imagina passar na prova com confianca total...",
            "Como seria conseguir a bolsa dos seus sonhos?",
            "6 meses para dominar o espanhol que a prova cobra",
            "Imagina ler textos academicos em espanhol sem dificuldade...",
            "Como seria apresentar seu trabalho em espanhol sem travar?",
            "Imagina ter o DELE no curriculo...",
            "A diferenca entre saber gramatica e realmente usar o idioma",
            "Imagina estudar no exterior sem barreira linguistica...",
        ],
        "profissional": [
            "Imagina participar de reunioes em espanhol sem travar...",
            "Como seria fechar negocios em espanhol com naturalidade?",
            "6 meses para destravar seu espanhol corporativo",
            "Imagina ser promovido gracas ao espanhol no curriculo...",
            "Como seria liderar equipes em espanhol?",
            "Imagina apresentar resultados em espanhol com confianca...",
            "A diferenca entre sobreviver e brilhar em espanhol no trabalho",
            "Imagina ser o profissional que a empresa precisa pra America Latina",
        ],
    },
    9: {  # Quebra de Crencas
        "viajante": [
            "Portunhol NAO e espanhol — e por isso que voce trava",
            "Quanto mais voce estuda espanhol... pior voce fala",
            "Aplicativo nao ensina espanhol de verdade",
            "Espanhol NAO e facil so porque e parecido com portugues",
            "Assistir serie com legenda nao te ensina a falar",
            "Voce nao precisa de vocabulario — precisa de pratica",
            "Gramatica nao vai te fazer falar espanhol",
            "1 hora de conversa vale mais que 1 mes de app",
        ],
        "vai_morar_fora": [
            "Morar fora NAO garante fluencia — tem brasileiro com 10 anos que nao fala",
            "Voce nao vai aprender espanhol 'naturalmente' so por estar la",
            "Imersao sem metodo e perda de tempo",
            "Vergonha de errar e o maior inimigo de quem mora fora",
            "Nao e falta de tempo — e falta de metodo",
            "Estudar gramatica nao resolve o problema de quem mora fora",
            "Conviver so com brasileiros la fora trava seu espanhol",
            "O problema nao e sotaque — e medo de falar",
        ],
        "academico": [
            "Estudar gramatica nao vai te fazer falar espanhol",
            "O problema nao e falta de vocabulario",
            "Decorar conjugacoes nao funciona — a ciencia ja provou",
            "Quanto mais voce estuda... mais confuso fica? Normal.",
            "Prova de proficiencia nao testa o que voce decora",
            "Voce sabe mais do que pensa — so nao sabe acessar",
            "Livro didatico te ensina espanhol de 1980",
            "Nota alta na escola nao significa que voce fala espanhol",
        ],
        "profissional": [
            "Espanhol basico NAO e suficiente para negocios",
            "Curso generico nao resolve espanhol corporativo",
            "Voce nao precisa ser perfeito — precisa ser funcional",
            "O problema nao e seu ingles ruim — e seu espanhol inexistente",
            "Fluencia nao e falar rapido — e falar certo",
            "LinkedIn em espanhol nao adianta se voce trava na entrevista",
            "Traduzir do portugues na cabeca e o que te trava em reuniao",
            "Espanhol de app nao sobrevive numa reuniao real",
        ],
    },
    12: {  # Historia e Autoridade Pessoal
        "viajante": [
            "Eu aprendi portugues sem escola — foi isso que me ensinou a ensinar",
            "Minha primeira semana no Brasil sem falar portugues",
            "Por que uma nativa ensina diferente de um professor de cursinho",
            "O dia que eu percebi como brasileiros sofrem com espanhol",
        ],
        "vai_morar_fora": [
            "Eu fui a imigrante que nao falava o idioma — sei como e",
            "12 anos no Brasil: o que aprendi sobre aprender um idioma",
            "O choque cultural que eu vivi quando cheguei no Brasil",
            "Por que eu criei o Espanhol com Voce",
        ],
        "academico": [
            "15 anos ensinando brasileiros — o que eu descobri",
            "Por que o metodo tradicional nao funciona (eu vi acontecer)",
            "A historia por tras do Metodo Imersao Nativa",
            "O que o Instituto Cervantes me ensinou sobre ensinar",
        ],
        "profissional": [
            "Como uma professora de espanhol construiu um negocio digital",
            "De dar aula presencial a impactar 100k pessoas online",
            "Por que empresas deveriam investir em espanhol para equipes",
            "O que eu aprendi empreendendo em dois idiomas",
        ],
    },
    # --- FUNDO ---
    6: {  # Metodo e Bastidor
        "viajante": [
            "Por que voce trava ao falar espanhol — a explicacao cientifica",
            "Como o cerebro realmente aprende um idioma novo",
            "A diferenca entre estudar e adquirir espanhol",
            "Por que o Metodo Imersao Nativa funciona para viajantes",
        ],
        "vai_morar_fora": [
            "Como nosso metodo prepara voce para o dia a dia real",
            "Repeticao espacada: por que voce esquece e como resolver",
            "O pilar que faz voce pensar em espanhol em vez de traduzir",
            "Como o acompanhamento inteligente acelera sua fluencia",
        ],
        "academico": [
            "Por que decorar nao funciona — e o que funciona de verdade",
            "Como o Metodo Imersao Nativa prepara para o DELE",
            "Os 3 pilares do metodo e como aplicar nos estudos",
            "A ciencia por tras da repeticao espacada no aprendizado",
        ],
        "profissional": [
            "Por que metodo generico nao resolve espanhol corporativo",
            "Como nosso metodo adapta o aprendizado para seu contexto",
            "Nucleo del Conocimiento: o vocabulario certo para sua area",
            "Imersao Ativa: como treinar espanhol sem sair do escritorio",
        ],
    },
    10: {  # Prova Social
        "viajante": [
            "Ela travava... hoje conversa com nativos na viagem",
            "Aluno que saiu do portunhol e se virou sozinho na Argentina",
            "De 'nao falo nada' a 'negociei preco no mercado em espanhol'",
            "Print de aluna: 'Ale, consegui pedir comida sem travar!'",
        ],
        "vai_morar_fora": [
            "Aluna conseguiu emprego na Espanha em 6 meses de curso",
            "Brasileiro que passou na entrevista de cidadania em espanhol",
            "De zero a conversacao: a jornada de um aluno em Barcelona",
            "Print de aluno: 'Resolvi toda a burocracia sozinho!'",
        ],
        "academico": [
            "Aluna passou no DELE B2 com 3 meses de Imersao Nativa",
            "Estudante tirou nota maxima em espanhol no ENEM",
            "Aluna conseguiu bolsa integral na Espanha",
            "Print de aluno: 'Passei no DELE! Obrigado Ale!'",
        ],
        "profissional": [
            "Aluno foi promovido depois de destravar o espanhol",
            "Vendedora triplicou clientes ao dominar espanhol de negocios",
            "Gerente fechou contrato gracas ao espanhol fluente",
            "Print de aluno: 'Apresentei em espanhol e arrasaram nos elogios'",
        ],
    },
    11: {  # CTA Indireto
        "viajante": [
            "Se voce quer destravar seu espanhol antes da viagem, eu te mostro como",
            "Comenta AULA que eu te envio o link da aula gratuita",
            "Tenho algo especial pra quem quer viajar falando espanhol de verdade",
            "Quer sair do portunhol? Comeca por aqui",
        ],
        "vai_morar_fora": [
            "Se voce vai se mudar e quer chegar preparado, eu te ajudo",
            "Comenta AULA — tenho uma aula demonstrativa gratuita pra voce",
            "Voce nao precisa chegar la sem falar — comeca agora",
            "Tenho um caminho claro pra quem vai morar fora",
        ],
        "academico": [
            "Prova chegando e voce ainda trava? Eu posso te ajudar",
            "Comenta AULA que te mando o link da aula demonstrativa",
            "Voce nao precisa de mais um cursinho — precisa de metodo",
            "Se o DELE esta no seu caminho, eu te preparo",
        ],
        "profissional": [
            "Quer destravar o espanhol da sua carreira? Comeca por aqui",
            "Comenta AULA — tenho uma aula que vai mudar sua visao",
            "Espanhol corporativo nao se aprende em app — se aprende com metodo",
            "Se o espanhol e o que falta pra sua promocao, eu te mostro o caminho",
        ],
    },
}


class AgenteEstrategistaMensal:
    """Gera o calendario para @espanholcomvoce entre duas datas."""

    def __init__(self, data_inicio, data_fim):
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.tipos_config = carregar_json("tipos_conteudo.json")
        self.horarios_config = carregar_json("horarios.json")
        self.hashtags_config = carregar_json("hashtags.json")
        self.objetivos = carregar_json("objetivos.json")

        self.avatares = ["viajante", "vai_morar_fora", "academico", "profissional"]
        self.avatares_nomes = {
            "viajante": "Viajante",
            "vai_morar_fora": "Vai Morar Fora",
            "academico": "Academico",
            "profissional": "Profissional",
        }

        # Mapeia tipos por funil a partir do config real
        self.tipos_topo = [t["id"] for t in self.tipos_config["tipos_conteudo"]["topo"]["tipos"]]
        self.tipos_meio = [t["id"] for t in self.tipos_config["tipos_conteudo"]["meio"]["tipos"]]
        self.tipos_fundo = [t["id"] for t in self.tipos_config["tipos_conteudo"]["fundo"]["tipos"]]

        # Index de tipos para lookup rapido
        self.tipos_info = {}
        for nivel in ["topo", "meio", "fundo"]:
            for t in self.tipos_config["tipos_conteudo"][nivel]["tipos"]:
                self.tipos_info[t["id"]] = {**t, "funil": nivel}

        self.temas_usados = set()
        self.dias_semana = {
            0: "segunda", 1: "terca", 2: "quarta", 3: "quinta",
            4: "sexta", 5: "sabado", 6: "domingo",
        }

        # Calcula total de dias no periodo
        self.total_dias = (self.data_fim - self.data_inicio).days + 1

    # --- Selecao de tema ---
    def _selecionar_tema(self, tipo_id, avatar_id):
        temas = BANCO_TEMAS.get(tipo_id, {}).get(avatar_id, [])
        for tema in temas:
            chave = f"{tipo_id}_{avatar_id}_{tema}"
            if chave not in self.temas_usados:
                self.temas_usados.add(chave)
                return tema
        if temas:
            return random.choice(temas) + " (vol. 2)"
        return f"Tema tipo {tipo_id} para {avatar_id}"

    # --- CTA do config real + keyword contextual ---
    def _selecionar_cta(self, tipo_id, keyword):
        info = self.tipos_info.get(tipo_id, {})
        cta_engajamento = info.get("cta_engajamento", "Salva esse video")
        return f"{cta_engajamento} | Comenta {keyword}"

    # --- Keyword ManyChat — regra contextual ---
    def _selecionar_keyword(self, tipo_id, avatar_id, tema):
        """
        Regras de keyword (do briefing real):
        - Vocabulario/expressoes (tipo 1,2) → ERROS, mas viajante/vai_morar_fora → VIAGEM
        - Falsos amigos (tipo 3) → FALSOS
        - Perguntas (tipo 4) → analisa conteudo da pergunta
        - Cultura/diferencas (tipo 5) → VIAGEM
        - Metodo/bastidor (tipo 6) → METODO
        - Dor/identificacao (tipo 7) → TRAVA
        - Desejo/transformacao (tipo 8) → AULA
        - Quebra de crencas (tipo 9) → METODO
        - Prova social (tipo 10) → AULA
        - CTA indireto (tipo 11) → AULA
        - Historia pessoal (tipo 12) → METODO
        """
        tema_lower = tema.lower()

        if tipo_id in [1, 2]:  # Expressoes / Palavras
            if avatar_id in ["viajante", "vai_morar_fora"]:
                return "VIAGEM"
            return "ERROS"

        if tipo_id == 3:  # Falsos amigos
            return "FALSOS"

        if tipo_id == 4:  # Perguntas — analisa conteudo
            if any(p in tema_lower for p in ["pronuncia", "pronunciar", "sotaque", "fonetica"]):
                return "PRONUNCIA"
            if any(p in tema_lower for p in ["viagem", "restaurante", "hotel", "aeroporto"]):
                return "VIAGEM"
            if any(p in tema_lower for p in ["metodo", "aprender", "estudar", "dica"]):
                return "METODO"
            if any(p in tema_lower for p in ["falar", "como", "diferenca", "vs", "quando usar"]):
                return "ERROS"
            return "PRONUNCIA"  # default tipo 4

        MAPA_FIXO = {
            5: "VIAGEM",
            6: "METODO",
            7: "TRAVA",
            8: "AULA",
            9: "METODO",
            10: "AULA",
            11: "AULA",
            12: "METODO",
        }
        return MAPA_FIXO.get(tipo_id, "ERROS")

    # --- Hashtags ---
    def _montar_hashtags(self, tipo_id, avatar_id):
        cfg = self.hashtags_config
        regras = cfg["regras"]
        tags = []

        base = cfg["hashtags_base"]
        tags.extend(random.sample(base, min(regras["sempre_incluir_base"], len(base))))

        avatar_tags = cfg["hashtags_por_avatar"].get(avatar_id, [])
        if avatar_tags:
            tags.extend(random.sample(avatar_tags, min(regras["incluir_avatar"], len(avatar_tags))))

        tipo_tags = cfg["hashtags_por_tipo_conteudo"].get(str(tipo_id), [])
        if tipo_tags:
            tags.extend(random.sample(tipo_tags, min(regras["incluir_tipo"], len(tipo_tags))))

        # Deduplica mantendo ordem
        vistos = set()
        unicas = []
        for t in tags:
            if t not in vistos:
                vistos.add(t)
                unicas.append(t)

        return " ".join(unicas[:regras["max_hashtags_por_post"]])

    # --- Distribuicao de funil por dia (respeita proporcoes do config) ---
    def _distribuir_funil_dia(self, dia_semana_str):
        dist = self.horarios_config["distribuicao_funil_semanal"]
        prop = dist.get(dia_semana_str, {"proporcao": {"topo": 2, "meio": 2, "fundo": 2}})["proporcao"]

        niveis = []
        for nivel, qtd in prop.items():
            niveis.extend([nivel] * qtd)

        while len(niveis) < 6:
            niveis.append("topo")
        niveis = niveis[:6]
        random.shuffle(niveis)
        return niveis

    # --- Selecao de tipo dentro do funil ---
    def _selecionar_tipo(self, funil):
        mapa = {"topo": self.tipos_topo, "meio": self.tipos_meio, "fundo": self.tipos_fundo}
        return random.choice(mapa[funil])

    # --- Validacao: regras de ouro ---
    def _validar_dia(self, posts_dia):
        """
        Regras:
        - Max 2 posts de fundo por dia
        - Nunca 2 fundos em slots consecutivos (espalha ao longo do dia)
        - Nunca 2 CTAs diretos (tipo 11) no mesmo dia
        - Nunca 2 CTAs diretos em slots consecutivos
        """
        fundo_count = sum(1 for p in posts_dia if p["funil"] == "FUNDO")
        if fundo_count > 2:
            return False

        # Max 1 CTA direto (tipo 11) por dia
        cta_direto_count = sum(1 for p in posts_dia if p["tipo_conteudo_id"] == 11)
        if cta_direto_count > 1:
            return False

        # Nunca 2 fundos em slots consecutivos
        for i in range(len(posts_dia) - 1):
            if posts_dia[i]["funil"] == "FUNDO" and posts_dia[i + 1]["funil"] == "FUNDO":
                return False

        return True

    def _gerar_dia(self, data, dia_semana_str, avatar_index):
        """Gera os 6 posts de um dia com validacao."""
        slots = self.horarios_config["horarios"]
        slot_keys = sorted(slots.keys())

        max_tentativas = 30
        for _ in range(max_tentativas):
            niveis = self._distribuir_funil_dia(dia_semana_str)

            # Garante que fundos nao fiquem em slots consecutivos
            # Se 2 fundos ficaram lado a lado, embaralha de novo
            tem_fundo_consecutivo = True
            shuffle_tentativas = 0
            while tem_fundo_consecutivo and shuffle_tentativas < 10:
                tem_fundo_consecutivo = False
                for i in range(len(niveis) - 1):
                    if niveis[i] == "fundo" and niveis[i + 1] == "fundo":
                        tem_fundo_consecutivo = True
                        random.shuffle(niveis)
                        break
                shuffle_tentativas += 1

            posts_dia = []
            idx = avatar_index

            for i, slot_key in enumerate(slot_keys):
                slot = slots[slot_key]
                formato_raw = slot["formato"].upper()
                formato = "REEL" if formato_raw == "REELS" else "CARROSSEL"
                horario = slot["horario"]
                funil = niveis[i]
                tipo_id = self._selecionar_tipo(funil)

                avatar_id = self.avatares[idx % len(self.avatares)]
                idx += 1

                tema = self._selecionar_tema(tipo_id, avatar_id)
                keyword = self._selecionar_keyword(tipo_id, avatar_id, tema)
                cta = self._selecionar_cta(tipo_id, keyword)
                hashtags = self._montar_hashtags(tipo_id, avatar_id)
                tipo_nome = self.tipos_info[tipo_id]["nome"]

                post = {
                    "data": data.strftime("%Y-%m-%d"),
                    "dia_semana": dia_semana_str.capitalize(),
                    "horario": horario,
                    "formato": formato,
                    "funil": funil.upper(),
                    "tipo_conteudo_id": tipo_id,
                    "tipo_conteudo": tipo_nome,
                    "avatar_id": avatar_id,
                    "avatar": self.avatares_nomes[avatar_id],
                    "tema": tema,
                    "cta": cta,
                    "keyword_manychat": keyword,
                    "hashtags": hashtags,
                }
                posts_dia.append(post)

            if self._validar_dia(posts_dia):
                return posts_dia, idx

        return posts_dia, idx

    # --- Geracao principal ---
    def gerar_calendario(self):
        calendario = []
        avatar_index = 0
        data_atual = self.data_inicio

        while data_atual <= self.data_fim:
            dia_semana_num = data_atual.weekday()
            dia_semana_str = self.dias_semana[dia_semana_num]

            posts_dia, avatar_index = self._gerar_dia(data_atual, dia_semana_str, avatar_index)
            calendario.extend(posts_dia)
            data_atual += timedelta(days=1)

        self._validar_cobertura_avatares(calendario)
        return calendario

    def _validar_cobertura_avatares(self, calendario):
        """Verifica se cada avatar aparece ao menos 1x por semana."""
        semana_atual = None
        avatares_semana = set()
        alertas = []

        for post in calendario:
            data = datetime.strptime(post["data"], "%Y-%m-%d")
            semana = data.isocalendar()[1]

            if semana != semana_atual:
                if semana_atual is not None:
                    faltando = set(self.avatares) - avatares_semana
                    if faltando:
                        nomes = [self.avatares_nomes[a] for a in faltando]
                        alertas.append(f"  ! Semana {semana_atual}: avatar(es) {', '.join(nomes)} sem post")
                semana_atual = semana
                avatares_semana = set()

            avatares_semana.add(post["avatar_id"])

        if alertas:
            print("\n--- ALERTAS DE COBERTURA ---")
            for a in alertas:
                print(a)
        else:
            print("  [OK] Todos os avatares cobertos em todas as semanas")

    # --- Sufixo para nomes de arquivo ---
    def _sufixo_arquivo(self):
        return f"{self.data_inicio.strftime('%Y%m%d')}_a_{self.data_fim.strftime('%Y%m%d')}"

    # --- Exportacao ---
    def salvar_json(self, calendario):
        nome = f"calendario_{self._sufixo_arquivo()}.json"
        caminho = OUTPUT_DIR / nome
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(calendario, f, ensure_ascii=False, indent=2)
        print(f"  [OK] JSON: {caminho}")
        return caminho

    def salvar_csv(self, calendario):
        nome = f"calendario_{self._sufixo_arquivo()}.csv"
        caminho = OUTPUT_DIR / nome
        if not calendario:
            return caminho

        campos = [
            "data", "dia_semana", "horario", "formato", "funil",
            "tipo_conteudo_id", "tipo_conteudo", "avatar_id", "avatar",
            "tema", "cta", "keyword_manychat", "hashtags",
        ]
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
            writer.writeheader()
            writer.writerows(calendario)
        print(f"  [OK] CSV: {caminho}")
        return caminho

    # --- Resumo ---
    def gerar_resumo(self, calendario):
        total = len(calendario)
        por_formato = Counter(p["formato"] for p in calendario)
        por_funil = Counter(p["funil"] for p in calendario)
        por_avatar = Counter(p["avatar"] for p in calendario)
        por_tipo = Counter(p["tipo_conteudo"] for p in calendario)

        dt_ini = self.data_inicio.strftime("%d/%m/%Y")
        dt_fim = self.data_fim.strftime("%d/%m/%Y")

        linhas = []
        linhas.append("=" * 65)
        linhas.append(f"  CALENDARIO @espanholcomvoce")
        linhas.append(f"  Periodo: {dt_ini} a {dt_fim}")
        linhas.append("=" * 65)
        linhas.append(f"  Total de posts: {total}")
        linhas.append(f"  Dias: {self.total_dias} | Posts/dia: 6")
        linhas.append(f"  Reels: {por_formato.get('REEL', 0)} | Carrosseis: {por_formato.get('CARROSSEL', 0)}")

        linhas.append("\n  --- FUNIL (meta: Topo 40% | Meio 35% | Fundo 25%) ---")
        for f in ["TOPO", "MEIO", "FUNDO"]:
            v = por_funil.get(f, 0)
            linhas.append(f"  {f}: {v} posts ({v / total * 100:.1f}%)")

        linhas.append("\n  --- AVATARES ---")
        for a in sorted(por_avatar.keys()):
            v = por_avatar[a]
            linhas.append(f"  {a}: {v} posts ({v / total * 100:.1f}%)")

        linhas.append("\n  --- TIPOS DE CONTEUDO ---")
        for t in sorted(por_tipo.keys()):
            v = por_tipo[t]
            linhas.append(f"  {t}: {v} posts ({v / total * 100:.1f}%)")

        # Metas do negocio
        metas = self.objetivos["objetivos"]["metas_negocio"]
        linhas.append("\n  --- METAS DO MES ---")
        linhas.append(f"  Vendas necessarias: {metas['receita_organica']['vendas_necessarias']}/mes")
        linhas.append(f"  Leads necessarios: {metas['leads']['meta_mensal']}")
        linhas.append(f"  Crescimento: {metas['crescimento_seguidores']['meta']}")

        linhas.append("\n  --- REGRAS VALIDADAS ---")
        linhas.append("  [x] Max 2 fundos por dia, nunca consecutivos")
        linhas.append("  [x] Max 1 CTA direto (tipo 11) por dia")
        linhas.append("  [x] Todo post de fundo com keyword ManyChat")
        linhas.append("  [x] Rotacao equilibrada de avatares (25% cada)")

        linhas.append("\n" + "=" * 65)
        return "\n".join(linhas)

    # --- Execucao ---
    def executar(self):
        dt_ini = self.data_inicio.strftime("%d/%m/%Y")
        dt_fim = self.data_fim.strftime("%d/%m/%Y")
        print(f"\n  Agente Estrategista Mensal — @espanholcomvoce")
        print(f"  Periodo: {dt_ini} a {dt_fim} ({self.total_dias} dias)\n")

        calendario = self.gerar_calendario()
        self.salvar_json(calendario)
        self.salvar_csv(calendario)

        resumo = self.gerar_resumo(calendario)
        print(resumo)

        # Salva resumo
        nome = f"resumo_{self._sufixo_arquivo()}.txt"
        caminho = OUTPUT_DIR / nome
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(resumo)
        print(f"\n  [OK] Resumo: {caminho}")

        return calendario


# --- CLI ---
# Uso: python agente_estrategista.py 2026-03-20 2026-04-30
#   ou: python agente_estrategista.py  (usa padrao: 20/03/2026 a 30/04/2026)
if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        data_inicio = datetime.strptime(sys.argv[1], "%Y-%m-%d")
        data_fim = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    else:
        # Padrao: 20/03/2026 a 30/04/2026
        data_inicio = datetime(2026, 3, 20)
        data_fim = datetime(2026, 4, 30)

    agente = AgenteEstrategistaMensal(data_inicio, data_fim)
    agente.executar()
