from docraptor import DocRaptor

if __name__ == "__main__":
    docraptor = DocRaptor()

    print("Create test_basic_content.pdf")
    with open("test_basic_content.pdf", "wb") as f:
        f.write(
            docraptor.create(
                {
                    "document_content": "<h1>python-docraptor</h1><p>Basic Test</p>",
                    "test": True,
                }
            ).content
        )
