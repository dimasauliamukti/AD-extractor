import re

def text_cleaning(text):
    text = text.strip()
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text

def merge_paragraph(prev_line, next_line):
    prev_line = prev_line.strip()
    next_line = next_line.strip()
    
    if re.search(r"[.;]\s*$", prev_line):
        return prev_line
    if re.match(r"^([A-Z][\w\s]{0,20}:|[-•\*])", prev_line):
        return prev_line
    if re.match(r"^([A-Z][\w\s]{0,20}:|[-•\*])", next_line):
        return prev_line
    match = re.match(r"^\((\d+)\)(.)", next_line)
    if match:
        char_after_paren = match.group(2)
        if char_after_paren.isupper():
            return prev_line

    return prev_line + " " + next_line

def tag(line):
    scores = {}
    matched_keywords = {}
    tags = {
        "ad_number": [
    (re.compile(r"\bFAA\s+AD\s+(?:No\.?\s*:?\s*)?\d{4}-\d{2}-\d{2}\b", re.IGNORECASE), 6),
    (re.compile(r"\bEASA\s+AD\s+(?:No\.?\s*:?\s*)?\d{4}[\s\-–—]\d{3,4}(?:R\d+)?\b", re.IGNORECASE), 6),
    ("effective date", 6),(re.compile(r"\bissue(?:d)?\b", re.IGNORECASE), 3)],
        
    "applicability": [
            ("applicability", 6), ("summary", 6), ("applies", 3),
            ("except", 3), ("airplanes", 3), ("model", 3),
            ("modification", 3), ("mod", 3),
            ("manufacturer serial number", 3), ("MSN", 3), ("embodied", 3)
        ],

        "reason": [
            ("reason", 6), ("background", 6), ("detected", 3),("addres", 3),("unsafe",3),("accident",3)
        ]    
    }
    
    for tag, keywords in tags.items():
        value = 0
        matches = []
        for keyword, score in keywords:
            if isinstance(keyword, re.Pattern):
                if keyword.search(line):
                    value += score
                    matches.append(keyword.pattern)
            elif keyword.lower() in line.lower():
                value += score
                matches.append(keyword)

        if value > 0:
            scores[tag] = value
            matched_keywords[tag] = matches
    if not scores:
        return None

    return max(scores.items(), key=lambda x: x[1])
 
