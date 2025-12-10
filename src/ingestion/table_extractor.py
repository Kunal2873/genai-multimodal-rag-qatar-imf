import camelot

def extract_tables(pdf_path):
    # Read tables from all pages using the camelot
    tables = camelot.read_pdf(pdf_path, pages="all")
    chunks = []

    for i, table in enumerate(tables):
        table_text = table.df.to_string()

        chunks.append({
            "content": "TABLE DATA:\n" + table_text,
            "page": table.page,
            "modality": "table"
        })
    return chunks


if __name__ == "__main__":
    pdf_file = "data/qatar_imf.pdf"
    data = extract_tables(pdf_file)
    print("Total tables extracted:", len(data))
    if data:
        print("Sample table:\n", data[0]["content"][:400])
