import os,sys
from openai import OpenAI
from .config import ROOT
def main():
    print('SOMatiq Studio V2 doctor'); print('Python:',sys.version.split()[0])
    for p in [ROOT/'config'/'curriculum.csv',ROOT/'config'/'settings.json',ROOT/'prompts'/'system.md',ROOT/'prompts'/'module.md']:
        if not p.exists(): raise RuntimeError(f'Missing {p.relative_to(ROOT)}')
    key=os.environ.get('OPENAI_API_KEY'); model=os.environ.get('OPENAI_MODEL','').strip()
    if not key: raise RuntimeError('OPENAI_API_KEY is missing.')
    if not model: raise RuntimeError('OPENAI_MODEL is missing.')
    ids={x.id for x in OpenAI(api_key=key).models.list().data}; print('Configured model:',model)
    if model not in ids:
        examples=sorted(x for x in ids if 'gpt-4.1' in x or 'gpt-4o' in x)[:20]
        raise RuntimeError(f'Model {model!r} unavailable. Examples: {examples}')
    print('API key and model access verified.')
