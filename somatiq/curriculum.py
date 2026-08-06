import csv
from .config import ROOT
PATH=ROOT/'config'/'curriculum.csv'
def load_rows():
    with PATH.open('r',encoding='utf-8-sig',newline='') as h: return list(csv.DictReader(h))
def save_rows(rows):
    with PATH.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def pending_indices(rows,limit):
    out=[]
    for i,row in enumerate(rows):
        if row['status'].strip().lower()=='pending':
            out.append(i)
            if len(out)>=limit: break
    return out
