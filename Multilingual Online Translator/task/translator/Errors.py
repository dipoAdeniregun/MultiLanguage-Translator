class WrongNoArguments(Exception):
    def __init__(self, num):
        self.message = "Expected 3 arguments for input language, output language and the word to translate. Got %s" % str(num)
        super().__init__(self.message)


class UnsupportedLanguageError(Exception):
    def __init__(self, lang):
        self.message = f"Sorry the program doesn't support {lang.lower()}"
        super().__init__(self.message)


class BrokenLinkError(Exception):
    def __init__(self, word):
        if word == '':
            self.message = "Something wrong with your internet connection"
        else:
            self.message = "Sorry, unable to find " + word
        super().__init__(self.message)
