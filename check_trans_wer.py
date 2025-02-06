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
total_words = 0
correct_lang_switch = 0
correct_hindi_switch = 0
correct_english_switch = 0
correct_lang_but_incorrect_word_hindi = 0
correct_lang_but_incorrect_word_english = 0
ref_hindi_hyp_eng = 0
ref_eng_hyp_hindi = 0
for ref_line, hyp_line in zip(ref_lines, hyp_lines):
    
    for word_ref, word_hyp in zip(ref_line.strip().split(" "), hyp_line.strip().split(" ")):
        ref_lang = identify_lang(word_ref)
        hyp_lang = identify_lang(word_hyp)
        total_words += 1
        if ref_lang == hyp_lang:
            correct_lang_switch += 1
            if word_hyp == word_ref:
                if ref_lang == 'hindi':
                    correct_hindi_switch += 1
                else:
                    correct_english_switch +=1 
            else:
                if ref_lang == 'hindi':
                    correct_lang_but_incorrect_word_hindi += 1
                else:
                    correct_lang_but_incorrect_word_english += 1
        else:
            if ref_lang == 'hindi':
                ref_hindi_hyp_eng += 1
            else:
                ref_eng_hyp_hindi += 1
                

print("Total Words: ", total_words)
print("Total correct Switches: ", correct_lang_switch, "--", float(correct_lang_switch / total_words))
print("Correct English Switches: ", correct_english_switch, "out of ", correct_english_switch + correct_lang_but_incorrect_word_english + ref_eng_hyp_hindi, "--", float(correct_english_switch/(correct_english_switch + correct_lang_but_incorrect_word_english + ref_eng_hyp_hindi)))
print("Correct Hindi Switches: ", correct_hindi_switch, "out of ", correct_hindi_switch + correct_lang_but_incorrect_word_hindi + ref_hindi_hyp_eng, "--", float(correct_hindi_switch/(correct_hindi_switch + correct_lang_but_incorrect_word_hindi + ref_hindi_hyp_eng)))
print("Correctly Switched to hindi but incorrect word ", correct_lang_but_incorrect_word_hindi, "--", float(correct_lang_but_incorrect_word_hindi / total_words))
print("Correctly Switched to english but incorrect word ", correct_lang_but_incorrect_word_english, "--", float(correct_lang_but_incorrect_word_english / total_words))
print("Incorrect Lang switches - Hindi Ref: ", ref_hindi_hyp_eng, "--", float(ref_hindi_hyp_eng / total_words))
print("Incorrect Lang Switches - English Ref: ", ref_eng_hyp_hindi, "--", float(ref_eng_hyp_hindi / total_words))