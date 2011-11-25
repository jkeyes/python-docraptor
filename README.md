# python-docraptor

A wrapper for the Doc Raptor API.

    from docraptor import pdf
    pdf(
        "API_KEY", 
        "<html><body>Hi</body></html>",
        { "doc[name]": "hi.pdf", "doc[test]": "true" }
    )
    
    from docraptor import xls
    xls(
        "API_KEY", 
        "<table>...</table>",
        { "doc[name]": "hi.pdf", "doc[test]": "true" }
    )
    