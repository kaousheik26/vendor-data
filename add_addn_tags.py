import os
import sys

hyp = sys.argv[1]
ref = sys.argv[2]
ref_tok = "zoomakazoo"
hyp_tok = "zUmakAzo"
with open(hyp) as f:
    hyp_lines = f.readlines()

with open(ref) as f:
    ref_lines = f.readlines()

hyp_words = []
ref_words = []
for hyp_line, ref_line in zip(hyp_lines, ref_lines):
    hyp_line = hyp_line.strip()
    ref_line = ref_line.strip()
    
    hyp_len = len(hyp_line.split(" "))
    ref_len = len(ref_line.split(" "))
    print(hyp_len, ref_len)
    hyp_words.extend(hyp_line.split(" "))
    ref_words.extend(ref_line.split(" "))
    if hyp_len > ref_len:
        extra = hyp_len - ref_len
        ref_words.extend([ref_tok]*extra)
    elif ref_len > hyp_len:
        extra = ref_len - hyp_len
        hyp_words.extend([hyp_tok]*extra)

with open("large/eval-asr.cls", "w") as f:
    f.writelines(word + '\n' for word in hyp_words)
        
with open("large/eval-asr.large", "w") as f:
    f.writelines(word + '\n' for word in ref_words)