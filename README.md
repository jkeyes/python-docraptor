# python-docraptor

A wrapper for the Doc Raptor API.


    from docraptor import DocRaptor
    docraptor = DocRaptor()
    with open("test.pdf", "wb") as f:
        f.write(docraptor.create({
            'document_content': '<p>Test</p>', 
            'test': True
        }))

    resp = docraptor.create({
        'document_content': '<p>Test</p>', 
        'test': True, 
        'async': True 
    })
    resp = docraptor.status(docraptor.status_id)
