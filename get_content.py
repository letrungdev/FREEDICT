import json
import os
from bs4 import BeautifulSoup
import re

def get_content(file_path):
    lang_src = file_path.split("/")[1].split("-")[0][:2]
    lang_tg = file_path.split("/")[1].split("-")[1][:2]
    f = open(file_path, encoding="utf8")
    entries = re.findall('<entry.*?</entry>', f.read().replace("\n", " "))
    dictionary = []
    for entry in entries:
        entry = BeautifulSoup(entry, "xml")
        word = entry.form.find_all("orth")[0].text
        means = []
        try:
            cits =  entry.sense.find_all('cit', recursive=False)
            for index, cit in enumerate(cits):
                if cit.get('type') == "trans":
                    examples = []
                    kind = ""
                    meaning = cit.quote.text.strip()
                    kinds = cit.find_all('pos')
                    if len(kinds) > 0:
                        kind = kinds[0].text
                    for next_cit in cits[(index+1):]:
                        if next_cit.get('type') == "trans":
                            break
                        elif next_cit.get('type') == "example":
                            source = re.findall('<quote xml:lang=\"{}\">(.*?)</quote>'.format(lang_src), str(next_cit))
                            if len(source) > 0:
                                source = source[0]
                                trans = re.findall('<quote xml:lang=\"{}\">(.*?)</quote>'.format(lang_tg), str(next_cit))
                                if len(trans) > 0:
                                    example = source.strip() + "#####" + trans[0].strip()
                                    if example not in examples:
                                        examples.append(example)

                    mean = {
                        "kind": kind,
                        "mean": meaning,
                        "examples": examples

                    }
                    means.append(mean)
        except:
            pass

        item = {
            "word": word,
            "phonetic": "",
            "means": means
        }
        print(item)
        dictionary.append(item)
    with open('Content/{}_{}.json'.format(lang_src, lang_tg), 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    trans = os.listdir('Data')
    for tran in trans:
        path = 'Data' + '/' + tran
        all_files = os.listdir(path)
        content_file = tran + '.tei'
        if content_file in all_files:
            path = 'Data' + '/' + tran + '/' + content_file
            get_content(path)
