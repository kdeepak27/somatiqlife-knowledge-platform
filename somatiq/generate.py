from __future__ import annotations
import json, os, random, subprocess, time
from datetime import datetime, timezone
from openai import OpenAI, RateLimitError, APITimeoutError, APIConnectionError, InternalServerError
from .config import ROOT, load_settings
from .curriculum import pending_items, set_status
from .render import render_docx, render_json, render_jsonl, render_markdown, render_metadata, safe_name
from .schema import ModuleContent
from .validation import validate

SYSTEM=ROOT/"prompts"/"system.md"; MODULE=ROOT/"prompts"/"module.md"; DRAFTS=ROOT/"drafts"; REPORTS=ROOT/"indexes"
MAX_VALIDATION_ATTEMPTS=3; MAX_API_ATTEMPTS=5

def _call(client, model, messages):
    last=None
    for attempt in range(MAX_API_ATTEMPTS):
        try:
            c=client.chat.completions.parse(model=model,messages=messages,response_format=ModuleContent)
            m=c.choices[0].message
            if m.refusal: raise RuntimeError(f"Model refusal: {m.refusal}")
            if m.parsed is None: raise RuntimeError("No parsed output returned.")
            return m.parsed
        except (RateLimitError,APITimeoutError,APIConnectionError,InternalServerError) as exc:
            last=exc
            if attempt==MAX_API_ATTEMPTS-1: break
            time.sleep(min(30,(2**(attempt+1))+random.random()))
    raise RuntimeError("OpenAI request failed after retries.") from last

def generate_one(client,model,item,correction=""):
    prompt=MODULE.read_text(encoding="utf-8").format(**item.row)
    if correction:
        prompt += "\n\nPrevious draft failed validation. Regenerate the COMPLETE module and fix:\n"+correction
    return _call(client,model,[{"role":"system","content":SYSTEM.read_text(encoding="utf-8")},
                               {"role":"user","content":prompt}])

def generate_valid(client,model,item,settings):
    correction=""; last=None
    for attempt in range(1,MAX_VALIDATION_ATTEMPTS+1):
        print(f"Generating {item.row['module_id']} with {model}; attempt {attempt}")
        module=generate_one(client,model,item,correction)
        try:
            validate(module,item.row["module_id"],settings); return module
        except ValueError as exc:
            last=exc; correction=str(exc); print(correction)
    raise RuntimeError("Validation failed after retries.") from last

def save_module(m):
    folder=DRAFTS/f"{m.module_id}_{safe_name(m.title)}"; folder.mkdir(parents=True,exist_ok=True)
    render_json(m,folder/"module.json"); render_metadata(m,folder/"metadata.json")
    render_markdown(m,folder/"module.md"); render_jsonl(m,folder/"rag_chunks.jsonl")
    render_docx(m,folder/"module.docx")
    return folder

def checkpoint(successes,interval):
    if successes % interval: return
    subprocess.run(["git","config","user.name","somatiq-content-bot"],check=True)
    subprocess.run(["git","config","user.email","somatiq-content-bot@users.noreply.github.com"],check=True)
    subprocess.run(["git","add","drafts","config/curricula"],check=True)
    if subprocess.run(["git","diff","--cached","--quiet"]).returncode==0: return
    subprocess.run(["git","commit","-m",f"Generation checkpoint {successes}"],check=True)
    subprocess.run(["git","push"],check=True)

def main():
    model=os.environ.get("OPENAI_MODEL","").strip()
    if not model: raise RuntimeError("OPENAI_MODEL is missing.")
    count=int(os.environ.get("MODULE_COUNT","1"))
    if not 1<=count<=50: raise ValueError("MODULE_COUNT must be between 1 and 50.")
    client=OpenAI(api_key=os.environ["OPENAI_API_KEY"]); settings=load_settings()
    selected=pending_items(count)
    if not selected: print("No pending modules remain."); return
    successes=[]; failures=[]; started=datetime.now(timezone.utc)
    for pos,item in enumerate(selected,1):
        mid=item.row["module_id"]; print(f"[{pos}/{len(selected)}] {mid}")
        try:
            m=generate_valid(client,model,item,settings); save_module(m)
            set_status(item,"draft-generated"); successes.append(mid)
            checkpoint(len(successes),5)
        except Exception as exc:
            failures.append({"module_id":mid,"error_type":exc.__class__.__name__,"error":str(exc)})
            print(f"FAILED {mid}: {exc}")
    REPORTS.mkdir(exist_ok=True)
    report={"started_utc":started.isoformat(),"finished_utc":datetime.now(timezone.utc).isoformat(),
            "model":model,"selected":len(selected),"successful_modules":successes,"failures":failures}
    (REPORTS/"last_generation_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(f"Successful: {len(successes)} | Failed: {len(failures)}")
