from SPARQLWrapper import JSON, SPARQLWrapper
 
import tags
 
identifiers = [
    'release',
    'album',
    'date'
]
 
def match(word_tag):
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_DETERMINER or \
            first_word[tags.TAG_INDEX] == tags.WH_PRONOUN:
 
        for identifier in identifiers:
            if identifier in sentence:
                return album(word_tag)
 

def album(words):
    words = [word for word in words
            if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
            word[tags.WORD_INDEX] not in identifiers]
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return sparql(words)
    return None

def sparql(album):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        """
       PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/>
       PREFIX dbpedia2: <http://dbpedia.org/property/>
       SELECT (CONCAT(STR(DAY(?date)), 
                     "/", 
                     STR(MONTH(?date)), 
                     "/", 
                    STR(YEAR(?date))) as ?displayDate)
        WHERE {
        ?thing foaf:name "%s"@en ;
        dbpedia2:thisAlbum ?y;
        dbo:releaseDate ?date.
        
        }
        limit 1
       """ % ' '.join(album)
    )
    
    results = wrapper.query().convert()['results']['bindings']
    if len(results)>0:
        date = []
        for result in results:
            date.append(result['displayDate']['value'])
        answer = 'The release date is ' + "".join(date)
        return answer
    return None