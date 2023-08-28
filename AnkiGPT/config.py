
OUTPUT_FOLDER = "flashcards"
OUTPUT_FILE = "flashcards-{time}.txt"
LECTURE = "Informationssicherheit"
SYSTEM_PROMPT = "Sie sind ein hilfreicher Professor, der einem Studenten hilft, den Inhalt einer Vorlesung zu verstehen."
PROMPT = """Ich bin ein Masterstudent der Informatik. Sie werden mir helfen, meine Vorlesung zu "{lecture}" zu lernen, indem Sie Karteikarten erstellen, um den Inhalt der Vorlesung für die Prüfung zu lernen.
Erstelle 2-5 Karteikarten pro Thema, die die wichtigsten Inhalte der Vorlesung zusammenfassen.
---
{lecture_content}
---
Das Format der Karteikarten ist wie folgt:
---
Frage;Antwort
Frage;Antwort
...
---
Zum Beispiel:
---
Was ist der ECB-Modus?; Ein Blockchiffre-Modus, bei dem jeder Datenblock unabhängig verschlüsselt wird. Gleiche Klartextblöcke erzeugen gleiche Chiffretextblöcke.
Vor- und Nachteile des ECB-Modus?; Vorteile: Einfach, effizient, parallelisierbar. Nachteile: Anfällig für Mustererkennung, unsicher für große Datenmengen.
---
"""
