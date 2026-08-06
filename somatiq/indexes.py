import csv,json
from .config import ROOT
def main():
    out=ROOT/'indexes'; out.mkdir(exist_ok=True); rows=[]
    for stage in ['drafts','approved']:
        for p in sorted((ROOT/stage).glob('*/module.json')):
            d=json.loads(p.read_text(encoding='utf-8')); rows.append({'module_id':d['module_id'],'title':d['title'],'domain':d['domain'],'category':d['category'],'version':d['version'],'stage':stage,'path':str(p.relative_to(ROOT))})
    with (out/'module_index.csv').open('w',encoding='utf-8',newline='') as h:
        names=['module_id','title','domain','category','version','stage','path']; w=csv.DictWriter(h,fieldnames=names); w.writeheader(); w.writerows(rows)
    print(f'Indexed {len(rows)} modules.')
