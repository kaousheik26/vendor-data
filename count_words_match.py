import os

entry_dir = 'large'
lang = 'large'
types = ['eval', 'dev', 'train']

for typ in types:
    with open(f"{entry_dir}/{typ}.cls") as f:
        cls_lines = f.readlines()
    with open(f"{entry_dir}/{typ}.{lang}") as f:
        ns_lines = f.readlines()
    
    for i, (j, k) in enumerate(zip(cls_lines, ns_lines)):
        if len(j.strip().split(" ")) == len(k.strip().split(" ")):
            continue
        print(i)
        break
        