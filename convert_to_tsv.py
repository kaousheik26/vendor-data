import os 

data_set = 'large'

sets = ['train', 'dev','eval']


for s in sets:
    with open(f"mlp/{s}.tsv", "w") as f2:
        with open(f'{data_set}/{s}.large') as f:
            ns_lines = f.readlines()
        with open(f'{data_set}/{s}.cls') as f:
            cls_lines = f.readlines()
        
        for ns_line, cls_line in zip(ns_lines, cls_lines):
            ns_line = ns_line.strip()
            cls_line = cls_line.strip()
            for ns_word, cls_word in zip(ns_line.split(" "), cls_line.split(" ")):
                f2.write(f"{cls_word}\t{ns_word}\n")