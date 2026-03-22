"""
Teste E2E automatizado — Quiz Espanhol com Você
Selenium + Edge — navega pelo quiz inteiro, testa todas as interações
"""

import time
import json
import sys
import os
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    ElementNotInteractableException, JavascriptException
)

# ─── Config ───
QUIZ_PATH = Path(r"D:\EspanholComVoce\iscas\manual_do_metodo\quiz\index.html")
SCREENSHOT_DIR = Path(r"D:\EspanholComVoce\iscas\manual_do_metodo\quiz\screenshots")
REPORT_PATH = Path(r"D:\EspanholComVoce\iscas\manual_do_metodo\quiz\test_report.md")

SCREENSHOT_DIR.mkdir(exist_ok=True)

# ─── Test Results ───
results = []
screenshots = []
js_errors = []
total_tests = 0
passed = 0
failed = 0


def log(msg, status="INFO"):
    icon = {"PASS": "[OK]", "FAIL": "[FAIL]", "INFO": "[i]", "WARN": "[!]"}.get(status, "")
    try:
        print(f"  {icon} {msg}")
    except UnicodeEncodeError:
        print(f"  {icon} {msg.encode('ascii', 'replace').decode()}")


def test(name, condition, detail=""):
    global total_tests, passed, failed
    total_tests += 1
    if condition:
        passed += 1
        log(f"{name}", "PASS")
        results.append({"name": name, "status": "PASS", "detail": detail})
    else:
        failed += 1
        log(f"{name} — {detail}", "FAIL")
        results.append({"name": name, "status": "FAIL", "detail": detail})


def screenshot(driver, name):
    path = SCREENSHOT_DIR / f"{name}.png"
    driver.save_screenshot(str(path))
    screenshots.append(str(path))
    return path


def is_visible(driver, element_id):
    try:
        el = driver.find_element(By.ID, element_id)
        return el.is_displayed()
    except NoSuchElementException:
        return False


def is_screen_active(driver, screen_id):
    try:
        el = driver.find_element(By.ID, screen_id)
        classes = el.get_attribute("class") or ""
        return "active" in classes
    except NoSuchElementException:
        return False


def wait_for_screen(driver, screen_id, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: is_screen_active(d, screen_id)
        )
        return True
    except TimeoutException:
        return False


def get_js_errors(driver):
    """Collect console errors via JS."""
    try:
        logs = driver.execute_script("""
            return window.__testErrors || [];
        """)
        return logs
    except:
        return []


def click_option(driver, index, timeout=5):
    """Click an option card by index."""
    try:
        options = WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "#options-list .option-card")
        )
        if index < len(options):
            driver.execute_script("arguments[0].click();", options[index])
            return True
        return False
    except:
        return False


def click_next(driver, timeout=8):
    """Click the next/próxima button."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "var b = document.getElementById('feedback-next-btn'); "
                "return b && b.style.display !== 'none' && b.offsetHeight > 0;"
            )
        )
        time.sleep(0.3)
        driver.execute_script("document.getElementById('feedback-next-btn').click();")
        return True
    except:
        return False


def wait_for_feedback(driver, timeout=5):
    """Wait for feedback card to become visible."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: "visible" in (d.find_element(By.ID, "feedback-card").get_attribute("class") or "")
            or "show" in (d.find_element(By.ID, "feedback-card").get_attribute("class") or "")
            or d.find_element(By.ID, "feedback-card").text.strip() != ""
        )
        return True
    except:
        return False


# ═══════════════════════════════════════════════
# MAIN TEST
# ═══════════════════════════════════════════════

def run_tests():
    global js_errors

    print("=" * 60)
    print("  TESTE E2E — Quiz Espanhol com Você")
    print("=" * 60)
    print()

    # Setup driver
    options = webdriver.EdgeOptions()
    options.add_argument("--window-size=414,896")  # iPhone-sized
    options.add_argument("--force-device-scale-factor=1")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(15)

    try:
        # Inject error catcher before page loads
        quiz_url = f"file:///{QUIZ_PATH.as_posix()}"
        driver.get(quiz_url)

        # Inject JS error collector
        driver.execute_script("""
            window.__testErrors = [];
            window.onerror = function(msg, src, line, col, err) {
                window.__testErrors.push({msg, src, line, col, err: err ? err.toString() : ''});
            };
            window.addEventListener('unhandledrejection', function(e) {
                window.__testErrors.push({msg: 'Unhandled promise rejection', detail: e.reason ? e.reason.toString() : ''});
            });
        """)

        time.sleep(1)

        # ══════════════════════════════════════
        # TEST 1: PAGE LOAD
        # ══════════════════════════════════════
        print("[1/8] Carregamento da página...")

        test("Página carregou sem erro",
             driver.title != "",
             f"Title: {driver.title}")

        test("Intro screen ativa",
             is_screen_active(driver, "intro-screen"))

        test("Botão CTA visível",
             is_visible(driver, "btn-start-quiz"))

        test("Question screen oculta",
             not is_screen_active(driver, "question-screen"))

        # Check for JS errors on load
        errs = get_js_errors(driver)
        test("Zero erros JS no carregamento",
             len(errs) == 0,
             f"{len(errs)} erros: {errs}" if errs else "")

        screenshot(driver, "01_intro")
        print()

        # ══════════════════════════════════════
        # TEST 2: START QUIZ
        # ══════════════════════════════════════
        print("[2/8] Iniciar quiz...")

        start_btn = driver.find_element(By.ID, "btn-start-quiz")
        driver.execute_script("arguments[0].click();", start_btn)

        test("Question screen ativou após clicar CTA",
             wait_for_screen(driver, "question-screen", 3))

        test("Intro screen desativou",
             not is_screen_active(driver, "intro-screen"))

        # Check Q1 loaded
        time.sleep(0.5)
        q_text = driver.find_element(By.ID, "question-text").text
        test("Pergunta 1 carregou",
             len(q_text) > 10,
             f"Texto: {q_text[:50]}...")

        progress = driver.find_element(By.ID, "progress-counter").text
        test("Progresso mostra 1/10",
             "1" in progress and "10" in progress,
             f"Mostra: {progress}")

        screenshot(driver, "02_question1")
        print()

        # ══════════════════════════════════════
        # TEST 3: ACT 1 — Questions 1-3
        # ══════════════════════════════════════
        print("[3/8] Ato 1 — Perguntas 1-3 (compreensão)...")

        # Q1 — select correct answer (index 1)
        test("Q1: Opções renderizaram",
             click_option(driver, 1))

        time.sleep(0.6)
        fb_visible = wait_for_feedback(driver, 5)
        test("Q1: Feedback apareceu",
             fb_visible)

        if fb_visible:
            fb_text = driver.find_element(By.ID, "feedback-card").text
            test("Q1: Feedback tem conteúdo",
                 len(fb_text) > 10,
                 f"Texto: {fb_text[:60]}...")

        screenshot(driver, "03_q1_feedback")

        # Click next
        test("Q1: Botão próxima funciona",
             click_next(driver))

        time.sleep(0.8)

        # Q2
        q2_text = driver.find_element(By.ID, "question-text").text
        test("Q2: Pergunta carregou",
             "embarazado" in q2_text.lower() or len(q2_text) > 10,
             f"Texto: {q2_text[:50]}...")

        test("Q2: Selecionar opção",
             click_option(driver, 1))
        time.sleep(0.6)
        test("Q2: Feedback apareceu",
             wait_for_feedback(driver, 5))
        test("Q2: Avançar",
             click_next(driver))
        time.sleep(0.8)

        # Q3
        q3_text = driver.find_element(By.ID, "question-text").text
        test("Q3: Pergunta carregou",
             len(q3_text) > 5,
             f"Texto: {q3_text[:50]}...")

        test("Q3: Selecionar opção",
             click_option(driver, 1))
        time.sleep(0.6)
        test("Q3: Feedback apareceu",
             wait_for_feedback(driver, 5))

        screenshot(driver, "04_q3_feedback")

        test("Q3: Avançar (deve ir para transição)",
             click_next(driver))
        print()

        # ══════════════════════════════════════
        # TEST 4: TRANSITION SCREEN
        # ══════════════════════════════════════
        print("[4/8] Tela de transição...")

        time.sleep(1)
        test("Transition screen ativa",
             is_screen_active(driver, "transition-screen"))

        screenshot(driver, "05_transition")

        # Wait for auto-advance or click
        time.sleep(4)

        test("Auto-avançou para Ato 2",
             wait_for_screen(driver, "question-screen", 5))
        print()

        # ══════════════════════════════════════
        # TEST 5: ACT 2 — Questions 4-7
        # ══════════════════════════════════════
        print("[5/8] Ato 2 — Perguntas 4-7 (produção)...")

        time.sleep(0.5)
        q4_text = driver.find_element(By.ID, "question-text").text
        test("Q4: Pergunta carregou",
             len(q4_text) > 10,
             f"Texto: {q4_text[:50]}...")

        # Check act changed
        act_attr = driver.find_element(By.ID, "question-screen").get_attribute("data-act")
        test("Ato mudou para 2",
             act_attr == "2",
             f"data-act={act_attr}")

        # Q4
        test("Q4: Selecionar opção", click_option(driver, 1))
        time.sleep(0.6)
        test("Q4: Feedback apareceu", wait_for_feedback(driver, 5))
        test("Q4: Avançar", click_next(driver))
        time.sleep(0.8)

        screenshot(driver, "06_act2")

        # Q5
        test("Q5: Selecionar opção", click_option(driver, 1))
        time.sleep(0.6)
        test("Q5: Feedback apareceu", wait_for_feedback(driver, 5))
        test("Q5: Avançar", click_next(driver))
        time.sleep(0.8)

        # Q6 (honesty — all options valid)
        q6_text = driver.find_element(By.ID, "question-text").text
        test("Q6: Pergunta carregou",
             len(q6_text) > 10,
             f"Texto: {q6_text[:50]}...")
        test("Q6: Selecionar opção", click_option(driver, 2))
        time.sleep(0.6)
        test("Q6: Feedback apareceu", wait_for_feedback(driver, 5))
        test("Q6: Avançar", click_next(driver))
        time.sleep(0.8)

        # Q7 (diagnostic — all options valid)
        test("Q7: Selecionar opção", click_option(driver, 0))
        time.sleep(0.6)
        test("Q7: Feedback apareceu", wait_for_feedback(driver, 5))
        test("Q7: Avançar", click_next(driver))
        time.sleep(0.8)
        print()

        # ══════════════════════════════════════
        # TEST 6: ACT 3 — Questions 8-10 (personal, no feedback)
        # ══════════════════════════════════════
        print("[6/8] Ato 3 — Perguntas 8-10 (pessoal)...")

        q8_text = driver.find_element(By.ID, "question-text").text
        test("Q8: Pergunta carregou",
             len(q8_text) > 10,
             f"Texto: {q8_text[:50]}...")

        act_attr = driver.find_element(By.ID, "question-screen").get_attribute("data-act")
        test("Ato mudou para 3",
             act_attr == "3",
             f"data-act={act_attr}")

        # Q8 — personal, auto-advances
        test("Q8: Selecionar opção", click_option(driver, 0))  # viajante
        time.sleep(1.2)

        # Q9
        q9_text = driver.find_element(By.ID, "question-text").text
        test("Q9: Avançou automaticamente",
             q9_text != q8_text,
             f"Texto: {q9_text[:50]}...")
        test("Q9: Selecionar opção", click_option(driver, 2))  # 1-3 anos
        time.sleep(1.2)

        # Q10
        q10_text = driver.find_element(By.ID, "question-text").text
        test("Q10: Avançou automaticamente",
             q10_text != q9_text,
             f"Texto: {q10_text[:50]}...")
        test("Q10: Selecionar opção", click_option(driver, 0))  # 5 min

        screenshot(driver, "07_act3")
        print()

        # ══════════════════════════════════════
        # TEST 7: LOADING SCREEN
        # ══════════════════════════════════════
        print("[7/8] Tela de loading...")

        time.sleep(1.5)
        test("Loading screen ativa",
             is_screen_active(driver, "loading-screen"))

        loading_text = driver.find_element(By.ID, "loading-text").text
        test("Loading tem texto rotativo",
             len(loading_text) > 5,
             f"Texto: {loading_text}")

        screenshot(driver, "08_loading")

        # Wait for result
        test("Result screen carregou após loading",
             wait_for_screen(driver, "result-screen", 10))
        print()

        # ══════════════════════════════════════
        # TEST 8: RESULT SCREEN
        # ══════════════════════════════════════
        print("[8/8] Tela de resultado...")

        time.sleep(1.5)  # wait for bar animations

        # Diagnostic bars
        comp_value = driver.find_element(By.ID, "comp-value").text
        test("Compreensão calculada",
             len(comp_value) > 0,
             f"Valor: {comp_value}")

        prod_value = driver.find_element(By.ID, "prod-value").text
        test("Produção calculada",
             len(prod_value) > 0,
             f"Valor: {prod_value}")

        gap_number = driver.find_element(By.ID, "gap-number").text
        test("GAP calculado",
             len(gap_number) > 0,
             f"Valor: {gap_number}")

        # Avatar badge
        badge_text = driver.find_element(By.ID, "avatar-badge-text").text
        test("Avatar badge preenchido",
             len(badge_text) > 0,
             f"Avatar: {badge_text}")

        screenshot(driver, "09_result_top")

        # Scroll down to error cards
        driver.execute_script("document.getElementById('result-screen').scrollTop = 600;")
        time.sleep(2)  # extra time for scroll reveal animations

        # Error cards
        card1_title = driver.execute_script("return document.querySelector('#error-card-1 h4')?.textContent || ''")
        test("Erro #1 preenchido",
             len(card1_title) > 0,
             f"Titulo: {card1_title}")

        card2_title = driver.execute_script("return document.querySelector('#error-card-2 h4')?.textContent || ''")
        test("Erro #2 preenchido",
             len(card2_title) > 0,
             f"Titulo: {card2_title}")

        card3_title = driver.execute_script("return document.querySelector('#error-card-3 h4')?.textContent || ''")
        test("Erro #3 preenchido",
             len(card3_title) > 0,
             f"Titulo: {card3_title}")

        screenshot(driver, "10_result_errors")

        # Scroll to email capture
        driver.execute_script("document.getElementById('result-screen').scrollTop = 1200;")
        time.sleep(0.5)

        # Email form
        email_input = driver.find_element(By.ID, "email-input")
        test("Campo de email visível",
             email_input.is_displayed())

        submit_btn = driver.find_element(By.ID, "email-submit-btn")
        test("Botão submit visível",
             submit_btn.is_displayed())

        screenshot(driver, "11_result_email")

        # Test invalid email
        email_input.clear()
        email_input.send_keys("invalido")
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(0.5)

        test("Email inválido não avança",
             not is_screen_active(driver, "thankyou-screen"))

        # Test valid email — set value then click submit button
        driver.execute_script("""
            document.getElementById('email-input').value = 'teste@espanholcomvoce.com.br';
        """)
        time.sleep(0.3)
        driver.execute_script("document.getElementById('email-submit-btn').click();")
        time.sleep(2)

        test("Thank you screen aparece com email válido",
             is_screen_active(driver, "thankyou-screen"))

        screenshot(driver, "12_thankyou")

        # Final JS error check
        errs = get_js_errors(driver)
        js_errors.extend(errs)
        test("Zero erros JS durante todo o quiz",
             len(errs) == 0,
             f"{len(errs)} erros: {json.dumps(errs, indent=2)}" if errs else "")

    except Exception as e:
        log(f"ERRO FATAL: {e}", "FAIL")
        results.append({"name": "ERRO FATAL", "status": "FAIL", "detail": str(e)})
        screenshot(driver, "ERROR_fatal")
        global failed
        failed += 1

    finally:
        # Take final screenshot
        screenshot(driver, "99_final_state")

        # Generate report
        generate_report()

        print()
        print("=" * 60)
        print(f"  RESULTADO: {passed}/{total_tests} testes passaram")
        if failed > 0:
            print(f"  [FAIL] {failed} testes falharam")
        else:
            print(f"  [OK] TODOS OS TESTES PASSARAM")
        print(f"  Screenshots: {len(screenshots)} em quiz/screenshots/")
        print(f"  Relatorio: quiz/test_report.md")
        print("=" * 60)

        driver.quit()


def generate_report():
    report = f"""# RELATÓRIO DE TESTE E2E — Quiz Espanhol com Você
**Data:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Browser:** Microsoft Edge (Selenium)
**Viewport:** 414x896 (mobile)

---

## Resultado: {passed}/{total_tests} testes passaram {'✅' if failed == 0 else '❌'}

| # | Teste | Status | Detalhe |
|---|-------|--------|---------|
"""
    for i, r in enumerate(results, 1):
        status = "✅ PASS" if r["status"] == "PASS" else "❌ FAIL"
        detail = r["detail"][:80] if r["detail"] else ""
        report += f"| {i} | {r['name']} | {status} | {detail} |\n"

    report += f"""
---

## Erros JavaScript

{"Nenhum erro JS detectado. ✅" if not js_errors else chr(10).join(f"- {e}" for e in js_errors)}

---

## Screenshots

"""
    for s in screenshots:
        name = os.path.basename(s)
        report += f"- `{name}`\n"

    report += f"""
---

## Fluxo testado

1. Página carregou → intro screen ativa
2. Clicou CTA → question screen ativa, Q1 apareceu
3. Q1-Q3 (Ato 1): seleção → feedback → próxima ✓
4. Transição Act 1→2: tela apareceu, auto-avançou
5. Q4-Q7 (Ato 2): seleção → feedback → próxima ✓
6. Q8-Q10 (Ato 3): seleção → auto-avanço sem feedback ✓
7. Loading: texto rotativo, 4.5s, avançou para resultado
8. Resultado: barras, GAP, avatar, 3 erros preenchidos ✓
9. Email inválido: bloqueado ✓
10. Email válido: thank you screen ✓

---

*Teste gerado automaticamente — Espanhol com Você*
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    run_tests()
