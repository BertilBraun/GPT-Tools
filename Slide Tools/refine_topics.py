
from util.gpt import chat_completion

PROMPT = """
Dies ist meine Informationssicherheit Vorlesung am KIT.
Im Folgenden die Themengebiete der Vorlesung:
---

{text}

---
Entferne Thematisch gedoppelte Einträge und ordne die Themen in eine sinnvolle Reihenfolge.
Gib mir eine Liste mit Aufzählungspunkten die diese Themen enthält zurück.
"""

OUTPUT_FILE = 'topics_refined.md'
INPUT_FILE = 'topics.md'


topics = open(INPUT_FILE, 'r').read()

response = chat_completion([PROMPT.format(text=topics)])

open(OUTPUT_FILE, 'w').write(response)
