import requests
import sys
import errors

from bs4 import BeautifulSoup

supported_lang = ['Arabic', 'German', 'English', 'Spanish', 'French',
                  'Hebrew', 'Japanese', 'Dutch', 'Polish',
                  'Portuguese', 'Romanian', 'Russian', 'Turkish']


def build_url(word='', in_lang='', out_lang=''):
    url = 'https://context.reverso.net/translation/'
    if in_lang != '':
        url += in_lang.lower() + '-'
        url += out_lang.lower() + '/'
        url += word.strip().replace(" ", "+")
    return url


def get_input():
    args = sys.argv
    if len(args) != 4:
        raise errors.WrongNoArguments(len(args))
    input_lang = args[1].title()
    if input_lang not in supported_lang:
        raise errors.UnsupportedLanguageError(input_lang)
    output_lang = args[2].title()
    if output_lang not in supported_lang + ['All']:
        raise errors.UnsupportedLanguageError(output_lang)
    word = args[3]
    return input_lang, output_lang, word


def create_text_file(word):
    text_file = open(word+'.txt', mode='w', encoding='UTF-8')
    return text_file


def write_to_file(text_file, lang, translated_words, example_sentences):
    text_file.writelines(f"\n\n{lang} Translations:\n")
    [text_file.writelines(word.text.strip('nmf').strip()+'\n') for word in translated_words]
    text_file.writelines(f"\n{lang} Examples:\n")
    text_file.writelines(example_sentences[0]+':\n')
    text_file.writelines(example_sentences[1].strip() + '\n')


def print_result(lang, translated_words, example_sentences):
    print(f"\n\n{lang} Translations:")
    [print(word.text.strip('nmf').strip()) for word in translated_words]
    print(f"\n{lang} Examples:")
    print(example_sentences[0]+':')
    print(example_sentences[1].strip())


def check_url(link, word=''):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(link, headers=headers)
    if page:
        return page
    else:
        raise errors.BrokenLinkError(word)


def get_data(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    translated_words = soup.find_all(attrs={'data-term': True})
    example_sentences = soup.find(attrs={'class': ['example']}).text.strip().splitlines()
    example_sentences = [x for x in example_sentences if x != '']
    return translated_words, example_sentences


def main():
    try:
        input_lang, output_lang, word = get_input()
        text_file = create_text_file(word)
        url = build_url()
        check_url(url)
    except errors.WrongNoArguments as err1:
        print(err1)
    except errors.UnsupportedLanguageError as err2:
        print(err2)
    except errors.BrokenLinkError as err3:
        print(err3)
    else:
        url = []

        if output_lang.lower() == 'all':
            all_lang = supported_lang
            all_lang.remove(input_lang)
        else:
            all_lang = [output_lang]

        url = [build_url(word, input_lang, lang) for lang in all_lang]
        for link, lang in zip(url, all_lang):
            try:
                page = check_url(link, word)
            except errors.BrokenLinkError as err4:
                print(err4)
            else:
                translated_words, example_sentences = get_data(page)
                print_result(lang, translated_words, example_sentences)
                write_to_file(text_file, lang, translated_words, example_sentences)

        text_file.close()


if __name__ == '__main__':
    main()
