import os

import sys

hyp = sys.argv[1]
ref = sys.argv[2]

    
with open(hyp) as f:
    lines = f.readlines()
  
words = []  
for line in lines:
    line = line.strip()
    for word in line.split(" "):
        words.append(word)
        
with open("large/eval-temp.cls", "w") as f:
    f.writelines(words)
    
with open(ref) as f:
    lines = f.readlines()
words = []  
for line in lines:
    line = line.strip()
    for word in line.split(" "):
        words.append(word)

with open("large/eval-temp.large", "w") as f:
    f.writelines(words)