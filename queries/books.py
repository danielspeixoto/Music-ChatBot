from SPARQLWrapper import JSON, SPARQLWrapper

import tags

identifiers = [
    'books',
    'works',
    'wrote'
]

def match(word_tag):
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_DETERMINER:
        for identifier in identifiers:
            if identifier in sentence:
                return birthName(word_tag)

def birthName(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers]
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return sparql(words)
    return None

def sparql(writer):

    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    sql = (""" 
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

           SELECT ?bookName, ?numberPages WHERE {
                ?writer rdf:type dbo:Writer ;
                        dbp:name ?label .
                ?book dbo:author ?writer ;
                      dbo:numberOfPages ?numberPages ;
                      rdfs:label ?bookName
                FILTER regex(?label, "^%s", "i")
                FILTER (LANG(?bookName) = 'pt')
            }
           """ % ' '.join(writer))
    wrapper.setQuery(sql)

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
        books = []
        for result in results:
            books.append('Book:' + result['bookName']['value'] + ' Pages:' + result['numberPages']['value'])
        answer = "The writer " + ' '.join(writer) + " wrote this books: \n" + '\n- '.join(books)
        return answer
    return None
