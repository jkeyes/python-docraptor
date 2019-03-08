"""Generate a PDF using the DocRaptor url style."""
from docraptor import DocRaptor


def main():
    """Generate a PDF with specified url."""
    docraptor = DocRaptor()

    print("Create test_basic_url.pdf")
    with open("test_basic_url.pdf", "wb") as pdf_file:
        pdf_file.write(
            docraptor.create(
                {"document_url": "http://docraptor.com", "test": True}
            ).content
        )


if __name__ == "__main__":
    main()
