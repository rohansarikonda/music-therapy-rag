from chunk_papers import chunk
import json
from pathlib import Path
import csv


folderpath = Path("paper-text")
all_chunks = []
p = {}

with open(f"papers/manifest.csv", "r") as file:
    reader = csv.DictReader(file)
    p = {row["file"]: (row["year"], row["title"]) for row in reader} #retrieve title and year of paper for citations
    
for pdf in folderpath.glob("*.txt"): 
    name = pdf.stem
    r = p.get(f"{name}.pdf")
    year = int(float(r[0])) if r[0] else None
    title = r[1]
    with open(f"paper-text/{name}.txt", "r") as file:
        text = file.read()
    chunks = chunk(text)
    for i, c in enumerate(chunks):
        all_chunks.append({ # add every chunk to all_chunks
            "id": f"{name}_{i}",
            "title": title,
            "paper": name,
            "year": year,
            "index": i,
            "text": c
        })
with open(f"chunks.json", "w", encoding="utf-8") as file:
    json.dump(all_chunks, file, indent=2, ensure_ascii=False)
