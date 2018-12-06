from SPARQLWrapper import JSON, SPARQLWrapper

import tags

identifiers = [
    'next',
    'previous',
    'sequence'
]

def match(word_tag):

    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_PRONOUN:
        for identifier in identifiers:
            if identifier in sentence:
                return previousSub(word_tag, sentence)

def previousSub(words, sentence):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers]
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return sparql(words, sentence)
    return None

def sparql(book, sentence):
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    sql = (""" 
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

          SELECT ?bookPrevious, ?bookSubsequent WHERE {
                ?book rdfs:label ?label ;
                      rdf:type dbo:Book .
                OPTIONAL {?book  dbo:previousWork ?bookPrevious }. 
                OPTIONAL {?book  dbo:subsequentWork ?bookSubsequent} .
                filter contains(?label,"%s")
           }
            LIMIT 1
           """ % ' '.join(book))
    wrapper.setQuery(sql)

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
        res = ''
        if(results[0]["bookPrevious"]["value"] and (identifiers[1] in sentence or identifiers[2] in sentence)):
            res = res + " The previous book is " + results[0]["bookPrevious"]["value"]
        if (results[0]["bookSubsequent"]["value"] and (identifiers[0] in sentence or identifiers[2] in sentence)):
            res = res + " The next book is " + results[0]["bookSubsequent"]["value"]
        return res
    return None





