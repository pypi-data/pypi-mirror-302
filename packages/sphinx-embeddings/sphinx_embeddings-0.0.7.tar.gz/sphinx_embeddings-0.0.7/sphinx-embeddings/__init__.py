import hashlib
import json
import os


import google.generativeai as gemini
import voyageai


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini.configure(api_key=GEMINI_API_KEY)
VOYAGE_API_KEY = os.getenv('VOYAGE_API_KEY')
voyage = voyageai.Client(api_key=VOYAGE_API_KEY)


def on_build_finished(app, exception):
    with open(srcpath, 'w') as f:
        json.dump(data, f, indent=4)


def embed_with_gemini(text):
    try:
        response = gemini.embed_content(
            model='models/text-embedding-004',
            content=text,
            task_type='SEMANTIC_SIMILARITY'
        )
        return response['embedding'] if 'embedding' in response else None
    except Exception as e:
        return None


def embed_with_voyage(text):
    try:
        embedding = voyage.embed([text], model='voyage-3', input_type='document').embeddings[0]
        return embedding
    except Exception as e:
        return None


def on_doctree_resolved(app, doctree, docname):
    text = doctree.astext()
    md5 = hashlib.md5(text.encode('utf-8')).hexdigest()
    embedding = embed_with_voyage(text)
    data[docname] = {
        'md5': md5,
        'embedding': embedding
    }


def init_globals(srcdir, outdir):
    global filename
    global srcpath
    global outpath
    global data
    filename = 'embeddings.json'
    srcpath = f'{srcdir}/{filename}'
    data = {}


def setup(app):
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
