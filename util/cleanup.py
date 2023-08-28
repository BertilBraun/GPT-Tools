
def cleanup_gpt_output(string: bytes) -> bytes:
    """
    Function to cleanup the output of GPT

    Tries to replace � with correct characters.
    """

    string = string.replace(b'\xe4', 'ä'.encode('utf-8'))
    string = string.replace(b'\xf6', 'ö'.encode('utf-8'))
    string = string.replace(b'\xfc', 'ü'.encode('utf-8'))
    string = string.replace(b'\xc4', 'Ä'.encode('utf-8'))
    string = string.replace(b'\xd6', 'Ö'.encode('utf-8'))
    string = string.replace(b'\xdc', 'Ü'.encode('utf-8'))
    string = string.replace(b'\xdf', 'ß'.encode('utf-8'))

    string = string.decode('utf-8', errors='ignore')

    mp = {
        'r�vention': 'rävention',
        'h�ren': 'hören',
        'k�nnen': 'können',
        'h�ufig': 'häufig',
        'f�r': 'für',
        '�glich': 'öglich',
        'ur�ck': 'urück',
        '�ber': 'über',
        'alit�t': 'alität',
        'sch�d': 'schäd',
        'schlie�': 'schließ',
        '�hren': 'ühren',
        'pr�fung': 'prüfung',
        'r�t': 'rät',
        'ktivit�t': 'ktivität',
        '�hnlich': 'ähnlich',
        'f�hr': 'führ',
        'chl�ssel': 'chlüssel',
        'f�hr': 'führ',
        '�nder': 'änder',
        'ma�': 'maß',
        'w�nsch': 'wünsch',
        'ei�': 'eiß',
    }

    for key, value in mp.items():
        string = string.replace(key, value)

    string = string.replace('�', 'ä')

    string = string.encode('utf-8')

    return string


def markdownify(text: str) -> str:
    while "  " in text:
        text = text.replace("  ", " ")

    while " \n" in text:
        text = text.replace(" \n", " ")

    while " \r\n" in text:
        text = text.replace(" \r\n", " ")

    if text[-1] != "\n":
        text += "\n"

    return text


def split_into_paragraphs(text: str) -> list[str]:
    return [p if p.startswith('#') else '##' + p for p in text.split("##")]
