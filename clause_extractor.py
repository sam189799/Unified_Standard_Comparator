import re


def extract_clauses(text):
    """
    Extract ISO clauses from document text.

    Example:
    Clause 4.1
    Clause 5.2
    """

    clauses = {}

    pattern = r"(Clause\s+\d+\.\d+)"

    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    for i in range(len(matches)):

        start = matches[i].start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        clause_text = text[start:end].strip()

        first_line = clause_text.split("\n")[0].strip()

        clauses[first_line] = clause_text

    return clauses