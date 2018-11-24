import tags

identifiers = [
    'genre',
    'kind of music',
    'kind of genre'
]

def match(word_tag):
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_DETERMINER or \
            first_word[tags.TAG_INDEX] == tags.WH_PRONOUN:

        for identifier in identifiers:
            if identifier in sentence:
                return genre(word_tag)

def genre(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers and \
             word[tags.WORD_INDEX] != 'music' and \
             word[tags.WORD_INDEX] != 'kind']
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return ' '.join(words)
    return None
