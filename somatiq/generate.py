import os
from openai import OpenAI
from .config import ROOT,load_settings
from .curriculum import load_rows,pending_indices,save_rows
from .render import render_json,render_metadata,render_markdown,render_jsonl,render_docx,safe_name
from .schema import ModuleContent
from .validation import validate
SYSTEM=ROOT/'prompts'/'system.md'; MODULE=ROOT/'prompts'/'module.md'; DRAFTS=ROOT/'drafts'
def generate_one(client,model,row):
    prompt=MODULE.read_text(encoding='utf-8').format(**row)
    c=client.chat.completions.parse(model=model,messages=[{'role':'system','content':SYSTEM.read_text(encoding='utf-8')},{'role':'user','content':prompt}],response_format=ModuleContent)
    msg=c.choices[0].message
    if msg.refusal: raise RuntimeError(f'Model refusal: {msg.refusal}')
    if msg.parsed is None: raise RuntimeError('No parsed structured output returned.')
    return msg.parsed
def main():
    model=os.environ.get('OPENAI_MODEL','').strip(); count=int(os.environ.get('MODULE_COUNT','1'))
    if not model: raise RuntimeError('OPENAI_MODEL is missing.')
    if not 1<=count<=5: raise ValueError('MODULE_COUNT must be 1-5.')
    client=OpenAI(api_key=os.environ['OPENAI_API_KEY']); settings=load_settings(); rows=load_rows(); ids=pending_indices(rows,count)
    if not ids: print('No pending modules remain.'); return
    for i in ids:
        row=rows[i]; print(f"Generating {row['module_id']} with {model}"); m=generate_one(client,model,row); validate(m,row['module_id'],settings)
        folder=DRAFTS/f'{m.module_id}_{safe_name(m.title)}'; folder.mkdir(parents=True,exist_ok=True)
        render_json(m,folder/'module.json'); render_metadata(m,folder/'metadata.json'); render_markdown(m,folder/'module.md'); render_jsonl(m,folder/'rag_chunks.jsonl'); render_docx(m,folder/'module.docx')
        rows[i]['status']='draft-generated'; save_rows(rows); print(f'Completed {m.module_id}')
