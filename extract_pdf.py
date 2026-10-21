import pymupdf
import unicodedata as ucd
import re
from collections import Counter

def extract(pdf) -> str:
    full = ""
    doc = pymupdf.open(pdf)
    for p in range(len(doc)):
        page = doc[p]
        text = page.get_text()
        if len(text) < 500:
            dimensions = page.rect
            
            ocr = page.get_textpage_ocr(
                language="eng", 
                dpi=300, 
                full=True
                )
            text = page.get_text("text", textpage=ocr)
        full += text
        #print(f"Page {p + 1}:\n{text}\n{'-' * 40}\n")
    doc.close()
    return full

def clean(text: str) -> str:
    text = ucd.normalize("NFKC", text) #remove ligatures and other special characters

    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text) #fix hyphenated words at line breaks
    text = re.sub(r"\u00ad\s*", "", text)  # remove soft hyphens and the line break after them

    matches = list(re.finditer(r"^\s*(References|Références)\s*$", text, flags=re.MULTILINE | re.IGNORECASE))
    
    if matches:
        last = matches[-1]
        after = text[last.end():]   # everything after the "References" heading

        sup = re.search(r"^\s*(Supplement(al|ary)? (Table|Figure|Material)|Appendix\b)",
                        after, flags=re.MULTILINE | re.IGNORECASE)
        if sup:
            # keep: before references + supplement onward
            text = text[:last.start()] + "\n" + after[sup.start():]
        else:
            text = text[:last.start()]

    lines = [line.strip() for line in text.splitlines()] #remove headers and footers
    counts = Counter(lines)
    keep = []

    for line in lines:
        if len(line) >= 3 and line.isdigit():
            continue
        if len(line) > 20 and counts[line] >= 3: #length > 20 to keep table column labels, etc
            continue
        keep.append(line)
    text = "\n".join(keep)

    text = re.sub(r"\s+", " ", text) #fix one-word lines
    return text


#print(clean(extract("papers/White_1999.pdf")))