from SPARQLWrapper import JSON, SPARQLWrapper

import tags

identifiers = [
    'songs',
    'musics',
    'list of songs',
    'list of musics',
]

def match(word_tag):
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_DETERMINER or \
            first_word[tags.TAG_INDEX] == tags.WH_PRONOUN:

        for identifier in identifiers:
            if identifier in sentence:
                return songs(word_tag)

def songs(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers and \
             word[tags.WORD_INDEX] != 'musics' and \
             word[tags.WORD_INDEX] != 'songs']
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return sparql(words)
    return None

def sparql(artist):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        """ 
SELECT  DISTINCT ?songs

    WHERE
      { 
       
        ?album dbp:title ?musics ;
          dbp:thisAlbum ?name;
          rdf:type dbo:Album.
        ?musics rdfs:label ?songs.
        ?name bif:contains "'%s'"
FILTER (LANG(?songs) = 'en') 
   
        
        
      } 
            """ % '_'.join(artist)
    )

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
        genres = []
        for result in results:
            genres.append(result['songs']['value'])
        answer = "The album " + ' '.join(artist) + " contains the following list of songs: \n" + '\n- '.join(genres)
        return answer
    return None
