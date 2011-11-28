# python-docraptor

A wrapper for the Doc Raptor API.

    from docraptor import pdf
    pdf(
        "API_KEY",
        { "doc[name]": "hi.pdf",
          "doc[test]": "true",
          "doc[document_content]": "<html><body>Hi</body></html>" }
    )

    from docraptor import xls
    xls(
        "API_KEY",
        { "doc[name]": "hi.pdf",
          "doc[test]": "true",
          "doc[document_content]": "<table>...</table>" }
    )
