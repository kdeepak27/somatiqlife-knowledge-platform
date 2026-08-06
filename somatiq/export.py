import shutil
from .config import ROOT
def main():
    a=ROOT/'approved'; e=ROOT/'bedrock-export'; e.mkdir(exist_ok=True)
    for p in e.iterdir():
        if p.is_file() and p.name!='.gitkeep': p.unlink()
    n=0
    for f in sorted(a.iterdir()):
        if not f.is_dir(): continue
        mid=f.name.split('_',1)[0]
        for src,suf in [('module.md','.md'),('rag_chunks.jsonl','.jsonl'),('metadata.json','.metadata.json')]:
            p=f/src
            if p.exists(): shutil.copy2(p,e/f'{mid}{suf}'); n+=1
    print(f'Exported {n} files.')
