import re

def split_sentences(text):
    split = re.split(r'(?<=[\?!.]) +', text)
    return split

def chunk(text, size=1200):
    sentences = split_sentences(text)
    chunks = []
    curr = []
    for s in sentences:
        if len(" ".join(curr)) + len(s) > size:
            if curr:
                chunks.append(" ".join(curr))
            old = curr
            curr = old[-2:] + [s]
        else:
            curr.append(s)
    if curr:
        chunks.append(" ".join(curr))
    return chunks

