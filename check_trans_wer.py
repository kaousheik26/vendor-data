import os
import sys
ref = f'{sys.argv[1]}/ref'
hyp = f'{sys.argv[1]}/hyp'

unicode_ranges = {
    'english': (0x0041, 0x007A),
    'hindi': (0x0900, 0x097F),
}

def identify_lang(text):
    scores = {lang: 0 for lang in unicode_ranges}
    start_lang = None
    for char in text.strip():
        char_code = ord(char)
        for lang, (start, end) in unicode_ranges.items():
            if start <= char_code <= end:
                scores[lang] += 1
                if start_lang == None:
                    start_lang = lang
    detected_language = max(scores, key=scores.get)
    return detected_language if scores[detected_language] else ""


with open(ref) as f:
    ref_lines = f.readlines()
    
with open(hyp) as f:
    hyp_lines = f.readlines()
lines = []
total_english_count = 0
error_count = 0
for ref_line, hyp_line in zip(ref_lines, hyp_lines):
    
    for word_ref, word_hyp in zip(ref_line.strip().split(" "), hyp_line.strip().split(" ")):
        if word_hyp == word_ref:
            lang = identify_lang(word_ref):
            if lang == 'english':
                total_english_count += 1
        if word_hyp != word_ref:
            lang = identify_lang(word_ref)
            if lang == 'english':
                total_english_count += 1
                print(word_hyp, word_ref)
                error_count += 1
            lines.append(f"{word_ref} {word_hyp} /n")
            

print(error_count, total_english_count)
with open(f"{sys.argv[1]}/trans-errors", "w") as f:
    f.writelines(lines)