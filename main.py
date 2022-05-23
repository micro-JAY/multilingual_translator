import sys
import requests
import itertools
from bs4 import BeautifulSoup

args = sys.argv
languages = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
             8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}
language_val = list(languages.values())
all_lang = "all"
# print("Hello, welcome to the translator. Translator supports:")
# for key, value in languages.items():
#     print(f"{key}. {value}")
if args[1].title() not in languages.values() and args[2] is not "all":
    print(f"Sorry, the program doesn't support {args[1]}")
    exit()
elif args[2].title() not in languages.values() and args[2] is not "all":
    print(f"Sorry, the program doesn't support {args[2]}")
    exit()
if args[2] != all_lang:
    translate_from = language_val.index(args[1].title()) + 1
    translate_to = language_val.index(args[2].title()) + 1
else:
    translate_from = language_val.index(args[1].title()) + 1
# translate_from = int(input('Type the number of your language:\n'))
# translate_to = int(input("Type the number of language you want to translate to or
# '0' to translate to all languages:\n"))

# print("Type the word you want to translate:")
translate_phrase = args[3]
# translate_phrase = input()


# begin html data retrieval
if args[2] == all_lang:
    s = requests.session()
    output_text = ""

    for key in languages.values():
        words = []
        if languages[translate_from].lower() == key.lower():
            continue
        translate_pair = f"{languages[translate_from].lower()}-{key.lower()}"
        try:
            link = s.get(f"https://context.reverso.net/translation/{translate_pair}/{translate_phrase}",
                         headers={'User-Agent': 'Chrome/101.0.4951.67'})
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')
            exit()
        soup = BeautifulSoup(link.content, 'html.parser')
        # find words substitutions
        p1 = soup.find_all('span', class_='display-term')
        for data in p1:
            words.append(data.text)
        if not p1:
            print(f"Sorry, unable to find {translate_phrase}")
            exit()
        print(f"{key} Translations:")
        output_text += f"{key} Translations:\n"
        for word in words:
            print(word)
            output_text += word + "\n"
            # file.write(word)
        output_text += "\n"
        # find phrases
        phrases_1 = []
        phrases_2 = []
        p2 = soup.find_all('div', {"class": ['src ltr', 'trg rtl', 'trg rtl arabic']})
        p3 = soup.find_all('div', {"class": ['trg ltr', 'trg rtl', 'trg rtl arabic']})
        for data in p2:
            phrases_1.append(data.text.strip())
        for data in p3:
            phrases_2.append(data.text.strip())

        # english phrase1, french phrase1, english phrase2, french phrase2
        ordered_phrases = (list(itertools.chain.from_iterable(zip(phrases_1, phrases_2))))

        print(f"\n{key} Examples:")
        output_text += f"{key} Examples:\n"
        print("\n\n".join(("\n".join(j for j in ordered_phrases[i:i + 2])
                           for i in range(0, len(ordered_phrases), 2))), "\n")
        output_text += ("\n\n".join(("\n".join(j for j in ordered_phrases[i:i + 2])
                                     for i in range(0, len(ordered_phrases), 2))))
        output_text += "\n\n"
    file = open(f"{translate_phrase}.txt", 'w+', encoding='utf-8')
    file.write(output_text)
    file.seek(0)
    print(file.read())

else:
    output_text = ""
    translate_pair = f"{languages[translate_from].lower()}-{languages[translate_to].lower()}"
    link = requests.get(f"https://context.reverso.net/translation/{translate_pair}/{translate_phrase}",
                        headers={'User-Agent': 'Chrome/101.0.4951.67'})
    # print(f"{link.status_code} OK\n")
    soup = BeautifulSoup(link.content, 'html.parser')
    # find words substitutions
    words = []
    p1 = soup.find_all('span', class_='display-term', limit=2)
    for data in p1:
        words.append(data.text)
    if not p1:
        print(f"Sorry, unable to find {translate_phrase}")
        exit()
    print(f"{languages[translate_to]} Translations:")
    output_text += f"{languages[translate_to]} Translations:\n"
    for word in words:
        print(word)
        output_text += word + "\n"

    # find phrases
    phrases_1 = []
    phrases_2 = []
    p2 = soup.find_all('div', class_='src ltr', limit=2)
    p3 = soup.find_all('div', class_='trg ltr', limit=2)
    for data in p2:
        phrases_1.append(data.text.strip())
    for data in p3:
        phrases_2.append(data.text.strip())

    # english phrase1, french phrase1, english phrase2, french phrase2
    ordered_phrases = (list(itertools.chain.from_iterable(zip(phrases_1, phrases_2))))

    print(f"{languages[translate_to]} Examples:")
    output_text += f"{languages[translate_to]} Examples:\n"
    print("\n\n".join(("\n".join(j for j in ordered_phrases[i:i + 2]) for i in range(0, len(ordered_phrases), 2))))
    output_text += ("\n\n".join(("\n".join(j for j in ordered_phrases[i:i + 2])
                                 for i in range(0, len(ordered_phrases), 2))))
    output_text += "\n\n"
    file = open(f"{translate_phrase}.txt", 'w+', encoding='utf-8')
    file.write(output_text)
    file.close()
