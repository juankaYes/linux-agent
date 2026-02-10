import os

def get_docs():
    docs_folder = "./docs"
    yield from (os.path.join(docs_folder, f) for f in os.listdir(docs_folder))
