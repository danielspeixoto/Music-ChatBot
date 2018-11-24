from SPARQLWrapper import JSON, SPARQLWrapper

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
        return sparql(words)
    return None

def sparql(artist):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        """ 
PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/>

SELECT DISTINCT ?label WHERE {
    ?thing foaf:name ?name ;
    foaf:isPrimaryTopicOf ?url .
    ?name  bif:contains "'%s'" .
    {
        ?thing dbpedia-owl:genre ?genre ;
        a                 dbpedia-owl:Band
    }
    UNION
    {
        ?thing dbpedia-owl:genre ?genre ;
        a                 dbpedia-owl:MusicalArtist
    }
    UNION
    {
        ?thing a <http://umbel.org/umbel/rc/MusicalPerformer>
    }
    
    ?genre rdfs:label ?label
    FILTER (LANG(?label) = 'en') 
}
LIMIT 5
        """ % ' '.join(artist)
    )

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
        genres = []
        for result in results:
            genres.append(result['label']['value'])
        answer = ' '.join(artist) + " plays " + ', '.join(genres)
        return answer
    return None
