import os
os.chdir("D:/EspanholComVoce/site-vendas/modulos")

changes = []

# === MODULE 02 ===
with open('MÓDULO 2 - Depoimentos Parte 1.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = ".sec-tag{display:inline-flex;align-items:center;gap:8px;font-size:.7rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;padding:5px 14px;border-radius:20px;margin-bottom:14px;background:rgba(10,22,40,0.05);color:#0d2140;border:1.5px solid rgba(10,22,40,0.15)}\n.sec-tag::before{content:'';display:inline-block;width:6px;height:6px;border-radius:50%;background:linear-gradient(135deg,#22c55e,#facc15);animation:pulse 2s ease-in-out infinite;flex-shrink:0}"

new = ".sec-tag{display:inline-flex;align-items:center;gap:10px;font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:8px 20px;border-radius:100px;margin-bottom:14px;background:rgba(10,22,40,0.05);color:#0d2140;border:1.5px solid rgba(10,22,40,0.15)}\n.sec-tag::before{content:'';width:8px;height:8px;border-radius:50%;background:#0d2140;box-shadow:0 0 12px rgba(10,22,40,0.4);animation:pulse 2s ease-in-out infinite;flex-shrink:0}"

if old in c:
    c = c.replace(old, new)
    changes.append('MOD02: OK')
else:
    changes.append('MOD02: not found')
with open('MÓDULO 2 - Depoimentos Parte 1.html', 'w', encoding='utf-8') as f:
    f.write(c)

# === MODULE 04 ===
with open('MÓDULO 4 - Objeções.html', 'r', encoding='utf-8') as f:
    c = f.read()

old04 = """.sec-label {
  display: inline-block;
  font-size: .7rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
  padding: 6px 18px;
  border-radius: 50px;
  border: 1.5px solid rgba(10,22,40,0.15);
  color: #0d2140;
  margin-bottom: 20px;
  background: rgba(10,22,40,0.05);
}
.sec-label::before {
  content: '';
  display: inline-block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #0d2140;
  margin-right: 8px;
  vertical-align: middle;
  animation: pulse 2s ease-in-out infinite;
}"""

new04 = """.sec-label {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: .75rem;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  padding: 8px 20px;
  border-radius: 100px;
  border: 1.5px solid rgba(10,22,40,0.15);
  color: #0d2140;
  margin-bottom: 20px;
  background: rgba(10,22,40,0.05);
}
.sec-label::before {
  content: '';
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #0d2140;
  box-shadow: 0 0 12px rgba(10,22,40,0.4);
  animation: pulse 2s ease-in-out infinite;
}"""

if old04 in c:
    c = c.replace(old04, new04)
    changes.append('MOD04: OK')
else:
    changes.append('MOD04: not found')
with open('MÓDULO 4 - Objeções.html', 'w', encoding='utf-8') as f:
    f.write(c)

# === MODULE 07 ===
with open('MÓDULO 7 - Depoimentos de transformação.html', 'r', encoding='utf-8') as f:
    c = f.read()

old07 = """.section-tag{
  display:inline-flex;align-items:center;gap:8px;
  font-size:.7rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  padding:6px 18px;border-radius:50px;
  border:1.5px solid rgba(10,22,40,.15);color:#0d2140;background:rgba(10,22,40,.05);margin-bottom:20px;
}
.section-tag span{
  display:inline-block;width:6px;height:6px;border-radius:50%;
  background:#0d2140;box-shadow:0 0 8px rgba(10,22,40,.3);animation:pulse 2s ease-in-out infinite;
}"""

new07 = """.section-tag{
  display:inline-flex;align-items:center;gap:10px;
  font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
  padding:8px 20px;border-radius:100px;
  border:1.5px solid rgba(10,22,40,.15);color:#0d2140;background:rgba(10,22,40,.05);margin-bottom:20px;
}
.section-tag::before{
  content:'';width:8px;height:8px;border-radius:50%;
  background:#0d2140;box-shadow:0 0 12px rgba(10,22,40,.4);animation:pulse 2s ease-in-out infinite;
}"""

if old07 in c:
    c = c.replace(old07, new07)
    c = c.replace('<div class="section-tag"><span></span> Vidas transformadas</div>', '<div class="section-tag">Vidas transformadas</div>')
    changes.append('MOD07: OK')
else:
    changes.append('MOD07: not found')
with open('MÓDULO 7 - Depoimentos de transformação.html', 'w', encoding='utf-8') as f:
    f.write(c)

# === MODULE 09 ===
with open('MÓDULO 9 - Depoimentos finais.html', 'r', encoding='utf-8') as f:
    c = f.read()

old09 = """.section-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: .7rem;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  padding: 6px 18px;
  border-radius: 50px;
  border: 1.5px solid rgba(10,22,40,0.15);
  color: #0d2140;
  background: rgba(10,22,40,0.05);
  margin-bottom: 20px;
}

.section-tag::before {
  content: '';
  display: block;
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #0d2140;
  box-shadow: 0 0 8px rgba(10,22,40,0.3);
}"""

new09 = """.section-tag {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: .75rem;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  padding: 8px 20px;
  border-radius: 100px;
  border: 1.5px solid rgba(10,22,40,0.15);
  color: #0d2140;
  background: rgba(10,22,40,0.05);
  margin-bottom: 20px;
}

.section-tag::before {
  content: '';
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #0d2140;
  box-shadow: 0 0 12px rgba(10,22,40,0.4);
  animation: pulse 2s ease-in-out infinite;
}"""

if old09 in c:
    c = c.replace(old09, new09)
    changes.append('MOD09: OK')
else:
    changes.append('MOD09: not found')
with open('MÓDULO 9 - Depoimentos finais.html', 'w', encoding='utf-8') as f:
    f.write(c)

# === MODULE 11 ===
with open('MÓDULO 11 - Preço.html', 'r', encoding='utf-8') as f:
    c = f.read()

old11 = """    .badge {
      display: inline-block;
      background: rgba(251,191,36,0.12);
      color: #b45309;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      padding: 7px 20px;
      border-radius: 100px;
      margin-bottom: 18px;
      border: 1px solid rgba(251,191,36,0.4);
    }"""

new11 = """    .badge {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      background: rgba(251,191,36,0.12);
      color: #b45309;
      font-size: .75rem;
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
      padding: 8px 20px;
      border-radius: 100px;
      margin-bottom: 18px;
      border: 1px solid rgba(251,191,36,0.4);
    }
    .badge::before {
      content: '';
      width: 8px; height: 8px;
      border-radius: 50%;
      background: #f59e0b;
      box-shadow: 0 0 12px rgba(245,158,11,0.6);
      animation: pulse 2s ease-in-out infinite;
      flex-shrink: 0;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.8); }
    }"""

if old11 in c:
    c = c.replace(old11, new11)
    changes.append('MOD11: OK')
else:
    changes.append('MOD11: not found')
with open('MÓDULO 11 - Preço.html', 'w', encoding='utf-8') as f:
    f.write(c)

# === MODULE 13 ===
with open('MÓDULO 13 - FAQ.html', 'r', encoding='utf-8') as f:
    c = f.read()

old13 = """    .faq-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: #0d2140;
      background: rgba(10, 22, 40, 0.05);
      border: 1.5px solid rgba(10, 22, 40, 0.15);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      padding: 7px 20px;
      border-radius: 999px;
      margin-bottom: 22px;
    }
    .faq-eyebrow::before {
      content: '';
      display: inline-block;
      width: 6px;
      height: 6px;
      background: #0d2140;
      border-radius: 50%;
      animation: pulse 2s ease-in-out infinite;
    }"""

new13 = """    .faq-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      color: #0d2140;
      background: rgba(10, 22, 40, 0.05);
      border: 1.5px solid rgba(10, 22, 40, 0.15);
      font-size: .75rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding: 8px 20px;
      border-radius: 100px;
      margin-bottom: 22px;
    }
    .faq-eyebrow::before {
      content: '';
      width: 8px;
      height: 8px;
      background: #0d2140;
      border-radius: 50%;
      box-shadow: 0 0 12px rgba(10,22,40,0.4);
      animation: pulse 2s ease-in-out infinite;
    }"""

if old13 in c:
    c = c.replace(old13, new13)
    changes.append('MOD13: OK')
else:
    changes.append('MOD13: not found')
with open('MÓDULO 13 - FAQ.html', 'w', encoding='utf-8') as f:
    f.write(c)

for ch in changes:
    print(ch)
print('\nDone!')
