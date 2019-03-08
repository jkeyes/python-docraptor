"""Generate an XLS using the DocRaptor content style."""
from docraptor import DocRaptor


def main():
    """Generate an XLS with specified content."""
    table = """<table>
    <thead>
    <tr><th>First Name</th><th>Last Name</th></tr>
    </thead>
    <tbody>
    <tr><td>Paul</td><td>McGrath</td></tr>
    <tr><td>Liam</td><td>Brady</td></tr>
    <tr><td>John</td><td>Giles</td></tr>
    </tbody>
    </table>"""
    docraptor = DocRaptor()

    print("Create test_basic.xls")
    with open("test_basic.xls", "wb") as f:
        f.write(
            docraptor.create(
                {"document_content": table, "document_type": "xls", "test": True}
            ).content
        )


if __name__ == "__main__":
    main()
