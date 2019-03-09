python-docraptor
================

.. image:: https://travis-ci.org/jkeyes/python-docraptor.png?branch=master
    :target: https://travis-ci.org/jkeyes/python-docraptor

.. image:: https://codecov.io/gh/jkeyes/python-docraptor/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jkeyes/python-docraptor

python-docraptor is an MIT Licensed wrapper for the docraptor API.

Synchronous Example
-------------------

.. code-block:: pycon

    from docraptor import DocRaptor

    docraptor = DocRaptor()
    with open("test.pdf", "wb") as f:
        f.write(docraptor.create({
            'document_content': '<p>python-docraptor Test</p>', 
            'test': True
        }).content)

Asynchronous Example
--------------------

.. code-block:: pycon

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


Installation
------------

To install python-docraptor, simply:

.. code-block:: bash

    $ pip install python-docraptor

