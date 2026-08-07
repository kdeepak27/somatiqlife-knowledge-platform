from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/"config"/"curriculum.csv"; TARGET=ROOT/"config"/"curricula"
NAMES={"BIO":"biology.csv","NUT":"nutrition.csv","EXE":"exercise.csv","SLP":"sleep.csv","STR":"stress.csv",
       "LIF":"lifestyle.csv","AGE":"aging.csv","DIS":"disease_prevention.csv","WOM":"womens_health.csv",
       "MEN":"mens_health.csv","CHD":"children.csv"}
def main():
    with SOURCE.open("r",encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
    groups=defaultdict(list)
    for row in rows: groups[row["module_id"].split("-",1)[0].upper()].append(row)
    TARGET.mkdir(parents=True,exist_ok=True)
    for prefix,group in groups.items():
        path=TARGET/NAMES.get(prefix,f"{prefix.lower()}.csv")
        if path.exists() and prefix=="EXE":
            print(f"Keeping supplied {path.name}; not overwriting."); continue
        with path.open("w",encoding="utf-8",newline="") as h:
            w=csv.DictWriter(h,fieldnames=list(group[0].keys())); w.writeheader(); w.writerows(group)
        print(f"{len(group)} rows -> {path}")
if __name__=="__main__": main()
