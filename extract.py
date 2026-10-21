import extract_pdf
from pathlib import Path

folderpath = Path("papers")

extraction_path = Path("paper-extraction-results.txt")
extraction_path.unlink(missing_ok=True)


for pdf in folderpath.glob("*.pdf"):
    text = extract_pdf.extract(pdf)
    text = extract_pdf.clean(text)
    name = pdf.stem + ".txt"
    with open(f"paper-text/{name}", "w") as file:
        file.write(f"\n\n{text}")
    with open(extraction_path, "a") as file:
        file.write(f"{pdf.name}: {len(text)} characters\n")