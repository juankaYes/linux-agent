import pdfplumber


def get_pdf_metadata_and_text(file_path: str):
    with pdfplumber.open(file_path) as pdf:
        print(pdf.metadata)  # Print the metadata for debugging
        yield pdf.metadata
        # for page in pdf.pages:
        #     text = "\n".join(page.extract_text().splitlines()[:-1])
        #     yield text

print(list(get_pdf_metadata_and_text("docs/lpic2book.pdf")))
print(list(get_pdf_metadata_and_text("docs/LPI-Learning-Material-101-500-en.pdf")))