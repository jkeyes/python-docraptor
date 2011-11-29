import time
from docraptor import DocRaptor

docraptor = DocRaptor()

print "Create test_basic_url.pdf"
with open("test_basic_url.pdf", "wb") as f:
    f.write(docraptor.create({
        'document_url': 'http://docraptor.com', 
        'test': True
    }).content)
