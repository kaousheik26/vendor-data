import os

entry_dir = 'large'
lang_ = 'large'
types = ['eval', 'dev', 'train']
target = "large_tagged"
tags = {
    "hindi": "<hi",
    "english": "<en",
    "": ""
}

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





for typ in types:
    with open(f"{entry_dir}/{typ}.cls") as f:
        cls_lines = f.readlines()
    with open(f"{entry_dir}/{typ}.{lang_}") as f:
        ns_lines = f.readlines()
    cls_ = []
    ns_ = []
    for i, (j, k) in enumerate(zip(cls_lines, ns_lines)):
        prev_lang = None
        s1 = ""
        s2 = ""
        prev_lang = identify_lang(k.strip().split(" ")[0])
        s1 += tags[prev_lang] + " "
        s2 += tags[prev_lang] + " "
        for word1, word2 in zip(j.strip().split(" "), k.strip().split(" ")):
            word1 = word1.strip()
            word2 = word2.strip()
            lang = identify_lang(word2)
            if lang != prev_lang:
                tag = tags[lang]
                prev_lang = lang
                s1 += tag + " "
                s2 += tag + " "
            s1 += word1 + " "
            s2 += word2 + " "
        s1 += "\n"
        s2 += "\n"
        cls_.append(s1)
        ns_.append(s2)
    with open(f"{target}/{typ}.cls", "w") as f:
        f.writelines(cls_)
    with open(f"{target}/{typ}.{target}", "w") as f:
        f.writelines(ns_)
    
# for file in listdir:
#     org_path = os.path.join("large", file)
#     with open(org_path) as f:
#         lines = f.readlines()
#     full_path = os.path.join("large_tagged", file)
#     print("Writing file: ", full_path)
#     with open(full_path, "w") as f:
#         for line in lines:
#             prev_lang = None
#             s = ""
#             prev_lang = identify_lang(line.strip().split(" ")[0])
#             s += tags[prev_lang] + " "
#             line = line.strip()
#             for word in line.split(" "):
                
#                 word = word.strip()
#                 lang = identify_lang(word)

#             f.write(s + "\n")


