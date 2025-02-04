import os

import sys

hyp = sys.argv[1]
ref = sys.argv[2]

    
hyp_words = hyp.strip().split(" ")
ref_words = ref.strip().split(" ")
    
with open("eval-tmp.large", "w") as f:
    f.writelines(word + "\n" for word in ref_words)
with open("eval-tmp.cls", "w") as f:
    f.writelines(word + "\n" for word in hyp_words)