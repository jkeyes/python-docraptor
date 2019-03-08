from docraptor import DocRaptor

if __name__ == "__main__":
    print(">>><<<" * 20)
    docraptor = DocRaptor()

    print("Create test_basic_url.pdf")
    with open("test_basic_url.pdf", "wb") as f:
        f.write(
            docraptor.create({"document_url": "http://docraptor.com", "test": True}).content
        )
