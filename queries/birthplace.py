from SPARQLWrapper import JSON, SPARQLWrapper

import tags

identifiers = [
    'birth place',
    'birth city',
    'born'
]

def match(word_tag):
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_PRONOUN or first_word[tags.TAG_INDEX] == tags.WH_ADVERB \
            and first_word[tags.WORD_INDEX] != 'When':
        for identifier in identifiers:
            if identifier in sentence:
                return birthPlace(word_tag)

def birthPlace(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers and \
             word[tags.WORD_INDEX] != 'place' and \
             word[tags.WORD_INDEX] != 'city']
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return sparql(words)
    return None

def sparql(artist):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery( """
            PREFIX dbo: <http://dbpedia.org/ontology/>
          SELECT ?city_name WHERE
          {
          ?song dbo:musicalArtist ?artist.
          ?artist dbo:birthPlace ?city ;
                  rdfs:label ?label.
            ?city rdfs:label ?city_name
           FILTER regex(?label, "^%s", "i")
          }
            LIMIT 1
          """ % ' '.join(artist)
    )

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
       return "The city is " + results[0]["city_name"]["value"]
    return None
