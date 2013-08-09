# python-docraptor

A wrapper for the Doc Raptor API.

# Example

    from docraptor import DocRaptor

    docraptor = DocRaptor()
    with open("test.pdf", "wb") as f:
        f.write(docraptor.create({
            'document_content': '<p>python-docraptor Test</p>', 
            'test': True
        }).content)

# Async Example

    import time
    from docraptor import DocRaptor

    docraptor = DocRaptor()

    resp = docraptor.create({
        'document_content': '<p>python-docraptor Async Test</p>', 
        'test': True, 
        'async': True 
    })
    status_id = resp['status_id']

    resp = docraptor.status(status_id)
    while resp['status'] != 'completed':
        time.sleep(3)
        resp = docraptor.status(status_id)
    
    with open("test_async.pdf", "wb") as f:
        f.write(docraptor.download(resp['download_key']).content)

# Build Status

[![Build Status](https://travis-ci.org/jkeyes/python-docraptor.png?branch=master)](https://travis-ci.org/jkeyes/python-docraptor)
