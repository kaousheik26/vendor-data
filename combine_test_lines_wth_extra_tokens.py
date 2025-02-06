import os
import sys

hyp_org = sys.argv[1]
ref_org = sys.argv[2]
hyp_res = f'{sys.argv[3]}/hyp.txt'
ref_res = f'{sys.argv[3]}/ref.txt'
with open(hyp_org) as f:
    hyp_org_lines = f.readlines()
    
with open(ref_org) as f:
    ref_org_lines = f.readlines()

with open(hyp_res) as f:
    hyp_res_lines = f.readlines()
    
with open(ref_res) as f:
    ref_res_lines = f.readlines()
    
count = 0
final_hyp = []
final_ref = []
hyp_res_lines = [line.strip() for line in hyp_res_lines]
ref_res_lines = [line.strip() for line in ref_res_lines]
for hyp_line, ref_line in zip(hyp_org_lines, ref_org_lines):
    hyp_line = hyp_line.strip()
    ref_line = ref_line.strip()
    
    hyp_len = len(hyp_line.split(" "))
    ref_len = len(ref_line.split(" "))
    length = max(hyp_len, ref_len)
    
    h = ' '.join(hyp_res_lines[count:count+length])
    r = ' '.join(ref_res_lines[count:count+length])
    final_hyp.append(h + '\n')
    final_ref.append(r + '\n')
    count += length

with open(os.path.join(sys.argv[3], "hyp_final"), "w" ) as f:
    f.writelines(final_hyp)

with open(os.path.join(sys.argv[3], "ref_final"), "w") as f:
    f.writelines(final_ref)