# from enchant import Dict
from pythainlp import correct
from pythainlp.util import isthai
from textblob import TextBlob, Word

# d = Dict("en_US")


def normalize(word):
    if isthai(word):
        word = correct(word)
    # elif d.check(word):
        # word = str(TextBlob(word).correct())
        # word = Word(word).singularize()
    # else:
    #     print(word, "Alien language")
    return word.lower()


if __name__ == "__main__":
    print('import success')
