import jiwer


hyp = ''
ref = ''

with open(hyp) as f:
    hyp_lines = f.readlines()
    
with open(ref) as f:
    ref_lines = f.readlines()

hyp_lines = [x.strip() for x in hyp_lines]
ref_lines = [x.strip() for x in ref_lines]
    
out = jiwer.process_words(
    ref_lines,
    hyp_lines,
)

error = jiwer.wer(ref_lines, hyp_lines)
print(error)
output = jiwer.visualize_alignment(out)

with open("results.txt", "w") as f:
    f.write(output)