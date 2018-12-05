import nltk
from nltk.corpus import stopwords

# Setup
import tags
from queries import albumrelease, birthdate, birthname, birthplace, genre, songs
from contextlib import redirect_stdout
import os
from nltk.tag import tnt

with redirect_stdout(open(os.devnull, "w")):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')

    stop_words = stopwords.words('english')

def route(word_tag):
    possible_matches = [
        genre.match,
        songs.match,
        albumrelease.match,
        birthname.match,
        birthplace.match,
        birthdate.match
    ]
    for candidate in possible_matches:
        result = candidate(word_tag)
        if result is not None:
            return result
    return 'We could not answer your question'

def process(sentence):
    words = nltk.word_tokenize(sentence)
    word_tag = nltk.pos_tag(words)
    return route(word_tag)

