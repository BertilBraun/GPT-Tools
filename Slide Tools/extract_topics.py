import os

from pypdf import PdfReader

from util import CONTENT_FORMAT, gpt3_summarize
from util.gpt import GPT3, chat_completion, gpt_in_parallel

PROMPTS = [
    """Wie kann ich helfen?""",
    """
Dies ist meine Informationssicherheit Vorlesung am KIT.
Erstellen Sie eine Liste mit Aufzählungspunkten, die **alle** großen Themen enthält, die in der Vorlesung behandelt wurden.
""",
    """
Z.B.:
Im Folgenden der Inhalt einer Beispiel Vorlesung:
---

Electronic Codebook (ECB) Mode
▶ Erinnerung: E, D : {0, 1}
k × {0, 1}
ℓ → {0, 1}
ℓ
▶ Einfachster Weg, zu verschlüsseln:
▶ Teile M in ℓ-Bit-Blöcke M1, . . . ∈ {0, 1}
ℓ
auf
▶ Setze C := (C1, . . .) mit Ci
:= E(K, Mi) ∈ {0, 1}
ℓ
▶ Entschlüsselung funktioniert genauso, nur mit D
▶ Frage: Vorteile/Nachteile?
33 / 64
Cipher Block Chaining (CBC) Mode
▶ Erinnerung: E, D : {0, 1}
k × {0, 1}
ℓ → {0, 1}
ℓ
▶ Problem des ECB: Chiffratblöcke „unabhängig“
▶ Idee des CBC: Chiffratblöcke verketten:
▶ Teile M in ℓ-Bit-Blöcke M1, . . . ∈ {0, 1}
ℓ
auf
▶ Setze C0 := IV (Initialisierungsvektor)
▶ Setze Ci
:= E(K, Mi ⊕ Ci−1)
▶ Entschlüsselung: Mi
:= D(K, Ci) ⊕ Ci−1
M1 M2
E E . . .
C0 C1 C2 M1 M2
. . .
D D
C0 C1 C2
▶ IV muss mit übertragen werden (oder konstant sein)
▶ Frage: Vorteile/Nachteile?

---
Stelle sicher, dass die Liste alle großen Themen enthält, die in der Vorlesung behandelt wurden.
""",
    """
Deine Antwort auf diese Beispiel Vorlesung sieht wie folgt aus:
---
- Electronic Codebook (ECB)
- Cipher Block Chaining (CBC)
- ...
---
""",
    """
Im Folgenden der Inhalt der Vorlesung:
---

{text}

---
Stelle sicher, dass die Liste alle großen Themen enthält, die in der Vorlesung behandelt wurden.
"""]

OUTPUT_FILE = 'topics.md'
INPUT_DIR = R'C:\Users\berti\OneDrive\Documents\Studium\Semester 6\Informationssicherheit\Vorlesungen'

CONTENT_FORMAT = "\n## {title}\n\n{content}\n"


def extract_text_from_pdf(filename: str) -> str:
    """
    Function to extract the text from a pdf file
    """
    reader = PdfReader(filename)
    return '\n'.join(page.extract_text() for page in reader.pages)


pdfs = [filename for filename in os.listdir(INPUT_DIR) if filename.endswith('.pdf')]

prompts = []

for filename in pdfs:
    content = extract_text_from_pdf(os.path.join(INPUT_DIR, filename))
    prompt = [p for p in PROMPTS]
    prompt[-1] = prompts[-1].format(text=content)
    prompts.append(prompt)

summaries = gpt_in_parallel(prompts, model=GPT3)

with open(OUTPUT_FILE, 'w') as f:
    f.write('# Themen\n\n')

    for filename, summary in zip(pdfs, summaries):
        lecture_name = filename.replace('.pdf', '')
        f.write(CONTENT_FORMAT.format(title=lecture_name, content=summary))
