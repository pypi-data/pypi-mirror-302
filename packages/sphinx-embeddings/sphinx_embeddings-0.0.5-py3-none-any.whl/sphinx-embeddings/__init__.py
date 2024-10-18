import hashlib
import json
import logging
import os
from typing import Dict, Union, List, Callable


from docutils.nodes import section
import dotenv
import google.generativeai as gemini
from sphinx.application import Sphinx
from sphinx.addnodes import document


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini.configure(api_key=GEMINI_API_KEY)
log_id = 'sphinx-embeddings'
logger = logging.getLogger(log_id)
handler = logging.FileHandler(f'{log_id}.log')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


# def prune_docs(actual_docs):
#     maybe_docs = data.keys()
#     old_docs = [doc for doc in maybe_docs if doc not in actual_docs]
#     for doc in old_docs:
#         del data[doc]
# 
# 
# def on_build_finished(app: Sphinx, exception) -> None:
#     prune_docs(app.env.found_docs)
#     with open(srcpath, 'w') as f:
#         json.dump(data, f, indent=4)
#     with open(outpath, 'w') as f:
#         json.dump(data, f, indent=4)
# 
# 
# def prune_sections(docname, before, after):
#     old_data = [hash for hash in before if hash not in after]
#     for hash in old_data:
#         del data[docname][hash]
# 
# 
# def embed(text: str) -> typing.Dict:
#     response = gemini.embed_content(
#         model='models/text-embedding-004',
#         content=text,
#         task_type='SEMANTIC_SIMILARITY'
#     )
#     return response['embedding'] if 'embedding' in response else None
# 
# 
# def on_doctree_resolved(app: Sphinx, doctree: document, docname: str) -> None:
#     before = []
#     after = []
#     if docname not in data:
#         data[docname] = {}
#     else:
#         before = data[docname].keys()
#     for node in doctree.traverse(section):
#         text = node.astext()
#         hash = hashlib.md5(text.encode('utf-8')).hexdigest()
#         after.append(hash)
#         if hash in data[docname]:
#             continue
#         data[docname][hash] = {}
#         data[docname][hash]['text'] = text[0:50]
#         embedding = app.config.sphinx_embeddings_function(text)
#         data[docname][hash]['embedding'] = embedding
#     prune_sections(docname, before, after)


def on_build_finished(app: Sphinx, exception) -> None:
    with open(srcpath, 'w') as f:
        json.dump(data, f, indent=4)
    with open(outpath, 'w') as f:
        json.dump(data, f, indent=4)


def embed(text: str):
    response = gemini.embed_content(
        model='models/text-embedding-004',
        content=text,
        task_type='SEMANTIC_SIMILARITY'
    )
    return response['embedding'] if 'embedding' in response else None


def on_doctree_resolved(app: Sphinx, doctree: document, docname: str) -> None:
    for node in doctree.traverse(section):
        text = node.astext()
        md5 = hashlib.md5(text.encode('utf-8')).hexdigest()
        embedding = embed(text)
        data[md5] = {
            'docname': docname,
            'embedding': embedding,
            'text': text
        }


def init_globals(srcdir: str, outdir: str) -> None:
    global filename
    global srcpath
    global outpath
    global data
    filename = 'embeddings.json'
    srcpath = f'{srcdir}/{filename}'
    outpath = f'{outdir}/{filename}'
    data = {}
    if os.path.exists(srcpath):
        with open(srcpath, 'r') as f:
            data = json.load(f)


def setup(app: Sphinx) -> Dict[str, Union[bool, str]]:
    init_globals(app.srcdir, app.outdir)
    # https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx-core-events
    app.connect('doctree-resolved', on_doctree_resolved)
    app.connect('build-finished', on_build_finished)
    cwd = os.path.abspath(os.path.dirname(__file__))
    with open(f'{cwd}/version.json', 'r') as f:
        version = json.load(f)['version']
    return {
        'version': version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
