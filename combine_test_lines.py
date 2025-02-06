import os
import sys
full_path = sys.argv[1]
hyp = 'hyp.txt'
ref = 'ref.txt'
org = 'large/eval-org.cls'

with open(os.path.join(full_path, hyp)) as f:
    hyp_lines = f.readlines()
    
with open(os.path.join(full_path, ref)) as f:
    ref_lines = f.readlines()
    
with open(org) as f:
    org_lines = f.readlines()

final_hyp = []
final_ref = []
count = 0
for line in org_lines:
    length = len(line.strip().split(" "))
    h = ' '.join(hyp_lines[count:count+length])
    r = ' '.join(ref_lines[count:count+length])
    final_hyp.append(h)
    final_ref.append(r)
    count += length

with open(os.path.join(full_path, "hyp"), "w" ) as f:
    f.writelines(final_hyp)

with open(os.path.join(full_path, "ref"), "w") as f:
    f.writelines(final_ref)