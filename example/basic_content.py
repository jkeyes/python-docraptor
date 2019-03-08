"""Generate a PDF using the DocRaptor content style."""
from docraptor import DocRaptor


def main():
    """Generate a PDF with specified content."""
    docraptor = DocRaptor()

    print("Create test_basic_content.pdf")
    with open("test_basic_content.pdf", "wb") as pdf_file:
        pdf_file.write(
            docraptor.create(
                {
                    "document_content": "<h1>python-docraptor</h1><p>Basic Test</p>",
                    "test": True,
                }
            ).content
        )


if __name__ == "__main__":
    main()
