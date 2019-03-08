import time
from docraptor import DocRaptor

docraptor = DocRaptor()

print("Create PDF")
resp = docraptor.create({
    'document_content': '<h1>python-docraptor</h1><p>Async Test</p>',
    'test': True,
    'async': True
})
print(f"Status ID: {resp['status_id']}")

status_id = resp['status_id']
resp = docraptor.status(status_id)

print(f"    {resp['status']}")
while resp['status'] != 'completed':
    time.sleep(3)
    resp = docraptor.status(status_id)
    print(f"    {resp['status']}")

print("Download to test_async.pdf")
with open("test_async.pdf", "wb") as f:
    f.write(docraptor.download(resp['download_key']).content)
print("[DONE]")
