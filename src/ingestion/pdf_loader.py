import pdfplumber

def load_pdf_chunks(pdf_path, max_chars=800):
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            text = text.strip().replace("\n", " ")
            # Splitting into smaller pieces to avoid token overload
            for i in range(0, len(text), max_chars):
                part = text[i:i + max_chars].strip()
                if len(part) > 20:  # ignoring useless tiny chunks 
                    chunks.append({
                        "content": part,
                        "page": page_index,
                        "modality": "text"
                    })
    return chunks


if __name__ == "__main__":
    pdf_file = "data/qatar_imf.pdf"
    c = load_pdf_chunks(pdf_file)
    print("Total chunks extracted:", len(c))
    print("Example chunk:", c[0] if c else "No text found")
