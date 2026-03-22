"""
Agente Auditor — @espanholcomvoce
==================================
Audita roteiros via Claude Code CLI (claude -p).
Cada roteiro e avaliado em 4 dimensoes (0-25 pts cada).
Aprovado (80+), Corrigido (60-79) ou Substituido (<60 ou 3 falhas).
"""

import json
import time
import logging
import subprocess
import tempfile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("auditor")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

INPUT_FILE  = OUTPUT_DIR / "roteiros_20260320_a_20260430.json"
OUTPUT_FILE = OUTPUT_DIR / "roteiros_auditados_20260320_a_20260430.json"
LOG_FILE    = OUTPUT_DIR / "log_auditoria_20260320_a_20260430.json"

MAX_TENTATIVAS = 3
PAUSA_ENTRE_CHAMADAS = 2

SYSTEM_AUDITOR = """
Voce e o Auditor de Qualidade do canal @espanholcomvoce da Alejandra Fajardo (Ale),
professora uruguaia certificada pelo Instituto Cervantes, especialista em ensinar
espanhol para brasileiros adultos (25-50 anos, niveis A1-B1).

Seu trabalho: avaliar roteiros de Reels e Carrosseis em 4 dimensoes.
Retorne SOMENTE um JSON valido. Sem texto antes ou depois. Sem markdown. Sem ```json.

4 DIMENSOES DE AUDITORIA (0-25 pts cada)

1. VERACIDADE LINGUISTICA (0-25)
   Toda informacao sobre espanhol e correta e verificavel.
   Nenhuma generalizacao falsa. Exemplos naturais como nativos realmente falam.
   Penalizar: regras inventadas, exemplos artificiais, marcador [TRADUCAO — verificar no dicionario].

2. VALOR / AHA MOMENT (0-25)
   Entrega insight real, nao obvio para brasileiros.
   Util para o avatar declarado no nivel declarado (A1-B1, 25-50 anos).
   Penalizar: generico, repetitivo, obvio, ja visto em mil perfis de idioma.

3. VOZ DA ALE (0-25)
   Tom: proximo, direto, confiante — nunca condescendente.
   SEMPRE nos nativos falamos assim — NUNCA os nativos falam.
   Comeca pela dor ou realidade concreta — nunca pelo conceito abstrato.
   Penalizar: voce deveria estudar, e importante que, tom academico, listas genericas.

4. COERENCIA DE FUNIL (0-25)
   Tipo TOPO/MEIO/FUNDO alinhado com o objetivo declarado.
   CTA correto para a etapa. TOPO nao queima CTA direto de venda.
   Penalizar: CTA de venda em conteudo de atracao, ausencia de CTA em fundo.

CRITERIOS DE DECISAO:
80-100 -> APROVADO
60-79  -> CORRIGIR (retorna roteiro_corrigido com todos os problemas resolvidos)
0-59   -> REPROVAR (roteiro_corrigido = null)

FORMATO DE RESPOSTA — JSON OBRIGATORIO:
{
  "status": "APROVADO" | "CORRIGIR" | "REPROVAR",
  "score": <0-100>,
  "dimensoes": {
    "veracidade": <0-25>,
    "valor": <0-25>,
    "voz": <0-25>,
    "funil": <0-25>
  },
  "problemas": ["problema 1", "problema 2"],
  "roteiro_corrigido": { mesmo schema do roteiro original com correcoes } | null
}
""".strip()


# ─────────────────────────────────────────────────────────────
# SUBSTITUTO (quando roteiro e reprovado)
# ─────────────────────────────────────────────────────────────

def gerar_substituto(post_id, formato, funil, tipo_id, tipo_nome, avatar, keyword):
    """Gera roteiro substituto generico quando o original e reprovado."""
    sub = {
        "post_id": post_id,
        "formato": formato,
        "funil": funil,
        "tipo_conteudo_id": tipo_id,
        "tipo_conteudo": tipo_nome,
        "avatar": avatar,
        "keyword_manychat": keyword,
        "origem": "substituto_auditor",
    }

    if formato == "REEL":
        sub["roteiro"] = {
            "hook_3s": {
                "fala": "Para! Voce fala isso em espanhol mas nenhum nativo entende.",
                "instrucao_gravacao": "Olhar direto pra camera. Energia alta. Tom de revelacao."
            },
            "pilulas_visuais": {
                "pilula_1": {"texto": "COMO FALAR", "fundo": "#fbbf24", "texto_cor": "branco"},
                "pilula_2": {"texto": "EM ESPANHOL", "fundo": "#FFFFFF", "texto_cor": "preto bold"},
                "pilula_3": {"texto": "DO JEITO CERTO", "fundo": "#fbbf24", "texto_cor": "branco"}
            },
            "desenvolvimento": [
                "Brasileiros aprendem expressoes que soam artificiais para nativos.",
                "Nos, nativos, usamos versoes muito mais naturais no dia a dia.",
                "A diferenca nao esta na gramatica — esta no vocabulario real."
            ],
            "cta_final": {
                "fala": f"Comenta {keyword} que te mando os 3 erros mais comuns agora",
                "instrucao_gravacao": "Apontar pra baixo. Tom convidativo."
            }
        }
        sub["legenda"] = (
            f"Voce fala espanhol mas os nativos nao entendem? Esse e o motivo.\n\n"
            f"Nos, nativos, falamos de um jeito bem diferente do que ensina a escola.\n\n"
            f"Comenta {keyword} que te mando o conteudo completo na hora!\n\n"
            f"#espanhol #aprenderespanhol #espanholparaBrasileiros"
        )
        sub["duracao_estimada"] = "30-60 segundos"
    else:
        sub["roteiro"] = {
            "slides": [
                {"numero": 1, "tipo": "capa", "texto_principal": "O QUE VOCE\nFALA EM\nESPANHOL", "subtexto": "...e o que nenhum nativo entende", "tag_pilula": "O PROBLEMA"},
                {"numero": 2, "tipo": "conteudo", "texto_principal": "A ESCOLA\nTE ENSINOU\nERRADO", "subtexto": "Expressoes que soam artificiais para nativos", "tag_pilula": "A REALIDADE"},
                {"numero": 3, "tipo": "conteudo", "texto_principal": "NOS, NATIVOS,\nFALAMOS\nASSIM", "subtexto": "Versao real do dia a dia — simples e direta", "tag_pilula": "A SOLUCAO"},
                {"numero": 4, "tipo": "cta", "texto_principal": keyword, "subtexto": "Comenta agora que te mando o conteudo completo", "manuscrito_rodape": "chega de travar"}
            ]
        }
        sub["total_slides"] = 4
        sub["legenda"] = (
            f"Voce estuda espanhol mas na hora de falar trava? Isso tem solucao.\n\n"
            f"Nos, nativos, falamos de um jeito que nenhuma escola te ensina.\n\n"
            f"Comenta {keyword} que te mando o conteudo completo agora!\n\n"
            f"#espanhol #aprenderespanhol #espanholparaBrasileiros"
        )

    return sub


def roteiro_substituto(roteiro_original):
    """Wrapper para gerar substituto a partir do roteiro original."""
    return gerar_substituto(
        post_id=roteiro_original.get("post_id", "unknown"),
        formato=roteiro_original.get("formato", "REEL"),
        funil=roteiro_original.get("funil", "TOPO"),
        tipo_id=roteiro_original.get("tipo_conteudo_id", 0),
        tipo_nome=roteiro_original.get("tipo_conteudo", ""),
        avatar=roteiro_original.get("avatar", ""),
        keyword=roteiro_original.get("keyword_manychat", "ERROS"),
    )


# ─────────────────────────────────────────────────────────────
# CHAMAR CLAUDE VIA CLI (claude -p)
# ─────────────────────────────────────────────────────────────

def chamar_claude_cli(prompt_completo):
    """
    Chama o Claude Code CLI via subprocess.
    Envia o prompt via stdin para evitar limites de tamanho de argumento.
    Retorna o JSON parseado da resposta.
    """
    # Monta prompt com system + user numa unica chamada
    prompt_final = f"{SYSTEM_AUDITOR}\n\n---\n\n{prompt_completo}"

    claude_path = r"C:\Users\alita\AppData\Roaming\npm\claude.cmd"
    resultado = subprocess.run(
        [claude_path, "-p", "--output-format", "text"],
        input=prompt_final,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )

    if resultado.returncode != 0:
        raise RuntimeError(f"claude -p falhou (exit {resultado.returncode}): {resultado.stderr[:200]}")

    resposta = resultado.stdout.strip()

    # Limpa possivel markdown wrapping
    if resposta.startswith("```json"):
        resposta = resposta[7:]
    if resposta.startswith("```"):
        resposta = resposta[3:]
    if resposta.endswith("```"):
        resposta = resposta[:-3]
    resposta = resposta.strip()

    return json.loads(resposta)


# ─────────────────────────────────────────────────────────────
# LOOP DE AUDITORIA DE UM ROTEIRO
# ─────────────────────────────────────────────────────────────

def auditar_roteiro(roteiro: dict, indice: int) -> tuple:
    post_id = roteiro.get("post_id", f"post_{indice}")

    entrada_log = {
        "indice": indice,
        "post_id": post_id,
        "data": roteiro.get("data"),
        "formato": roteiro.get("formato"),
        "avatar": roteiro.get("avatar"),
        "tema": roteiro.get("tema"),
        "funil": roteiro.get("funil"),
        "tentativas": [],
        "resultado_final": None,
        "substituido": False
    }

    roteiro_atual = roteiro

    for tentativa in range(1, MAX_TENTATIVAS + 1):
        logger.info(f"  [{indice+1}] {post_id} — tentativa {tentativa}/{MAX_TENTATIVAS}")

        if tentativa == 1:
            prompt = f"Audite este roteiro e retorne APENAS o JSON de resultado:\n\n{json.dumps(roteiro_atual, ensure_ascii=False, indent=2)}"
        else:
            problemas_anteriores = entrada_log["tentativas"][-1].get("problemas", [])
            prompt = (
                f"Re-audite este roteiro corrigido (tentativa {tentativa}/{MAX_TENTATIVAS}).\n"
                f"Problemas da auditoria anterior: {json.dumps(problemas_anteriores, ensure_ascii=False)}\n\n"
                f"Retorne APENAS o JSON de resultado:\n\n{json.dumps(roteiro_atual, ensure_ascii=False, indent=2)}"
            )

        try:
            resultado = chamar_claude_cli(prompt)
        except json.JSONDecodeError as e:
            logger.error(f"  [{post_id}] JSON invalido tentativa {tentativa}: {e}")
            entrada_log["tentativas"].append({"tentativa": tentativa, "erro": f"JSON invalido: {str(e)}", "status": "ERRO"})
            time.sleep(PAUSA_ENTRE_CHAMADAS)
            continue
        except Exception as e:
            logger.error(f"  [{post_id}] Erro CLI tentativa {tentativa}: {e}")
            entrada_log["tentativas"].append({"tentativa": tentativa, "erro": str(e), "status": "ERRO"})
            time.sleep(PAUSA_ENTRE_CHAMADAS)
            continue

        status = resultado.get("status", "REPROVAR")
        score = resultado.get("score", 0)
        problemas = resultado.get("problemas", [])

        entrada_log["tentativas"].append({
            "tentativa": tentativa,
            "status": status,
            "score": score,
            "dimensoes": resultado.get("dimensoes", {}),
            "problemas": problemas
        })

        logger.info(f"  [{post_id}] Score: {score} | Status: {status}")

        if status == "APROVADO":
            entrada_log["resultado_final"] = "APROVADO"
            roteiro_aprovado = resultado.get("roteiro_corrigido") or roteiro_atual
            roteiro_aprovado["_auditado"] = True
            roteiro_aprovado["_score"] = score
            return roteiro_aprovado, entrada_log

        elif status in ("CORRIGIR", "REPROVAR"):
            # Tenta usar roteiro corrigido se disponivel
            corrigido = resultado.get("roteiro_corrigido")
            if corrigido:
                roteiro_atual = corrigido
            else:
                logger.warning(f"  [{post_id}] {status} sem roteiro_corrigido — mantendo versao atual")

            # So substitui pelo generico na ultima tentativa
            if tentativa == MAX_TENTATIVAS:
                entrada_log["resultado_final"] = "REPROVADO" if status == "REPROVAR" else "CORRIGIR_NAO_APROVADO"
                entrada_log["substituido"] = True
                return roteiro_substituto(roteiro), entrada_log

        time.sleep(PAUSA_ENTRE_CHAMADAS)

    logger.warning(f"  [{post_id}] 3 tentativas sem aprovacao — substituindo")
    entrada_log["resultado_final"] = "SUBSTITUIDO_APOS_3_TENTATIVAS"
    entrada_log["substituido"] = True
    return roteiro_substituto(roteiro), entrada_log


# ─────────────────────────────────────────────────────────────
# EXECUCAO PRINCIPAL
# ─────────────────────────────────────────────────────────────

def executar():
    logger.info("=" * 60)
    logger.info("AGENTE AUDITOR — @espanholcomvoce (via claude -p)")
    logger.info(f"Entrada: {INPUT_FILE}")
    logger.info(f"Saida:   {OUTPUT_FILE}")
    logger.info("=" * 60)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        roteiros = json.load(f)

    total = len(roteiros)
    logger.info(f"Total de roteiros a auditar: {total}")

    roteiros_auditados = []
    log_completo = []
    aprovados = 0
    substituidos = 0

    for i, roteiro in enumerate(roteiros):
        roteiro_final, entrada_log = auditar_roteiro(roteiro, i)
        roteiros_auditados.append(roteiro_final)
        log_completo.append(entrada_log)

        if entrada_log["resultado_final"] == "APROVADO":
            aprovados += 1
        elif entrada_log["substituido"]:
            substituidos += 1

        if (i + 1) % 10 == 0:
            parcial = OUTPUT_DIR / f"roteiros_auditados_PARCIAL_{i+1}de{total}.json"
            with open(parcial, "w", encoding="utf-8") as f:
                json.dump(roteiros_auditados, f, ensure_ascii=False, indent=2)
            logger.info(f"  [PARCIAL] {i+1}/{total} salvos")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(roteiros_auditados, f, ensure_ascii=False, indent=2)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_completo, f, ensure_ascii=False, indent=2)

    corrigidos = total - aprovados - substituidos
    logger.info("=" * 60)
    logger.info("AUDITORIA CONCLUIDA")
    logger.info(f"Total:        {total}")
    logger.info(f"Aprovados:    {aprovados} ({aprovados/total*100:.1f}%)")
    logger.info(f"Corrigidos:   {corrigidos} ({corrigidos/total*100:.1f}%)")
    logger.info(f"Substituidos: {substituidos} ({substituidos/total*100:.1f}%)")
    logger.info(f"Output: {OUTPUT_FILE}")
    logger.info("=" * 60)


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        INPUT_FILE = Path(sys.argv[1])
    executar()
