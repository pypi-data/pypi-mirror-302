import json
import os


def get_version():
    cwd = os.path.abspath(os.path.dirname(__file__))
    with open(f'{cwd}/../sphinx-embeddings/version.json', 'r') as f:
        data = json.load(f)
    return data['version']


project = 'sphinx-embeddings'
copyright = '2024, Kayce Basques'
author = 'Kayce Basques'
release = get_version()
extensions = ['sphinx-embeddings']
templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'build.sh',
    'venv', 
]
html_theme = 'alabaster'
