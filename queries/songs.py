from SPARQLWrapper import JSON, SPARQLWrapper

import tags

# senteças do tipo
# What are the songs on Houses of the Holy by Led Zeppelin?
# What are the musics in Ben from Michael Jackson?
# What are the musics on Ray of Light from Madonna?
identifiers_one = [
    'songs on',
    'musics on',
    'songs in',
    'musics in'
]

identifiers_two = [
    'from',
    'by'
]

def match(word_tag):
    print(word_tag)
    first_word = word_tag[0]
    sentence = ' '.join([word[tags.WORD_INDEX] for word in word_tag])
    if first_word[tags.TAG_INDEX] == tags.WH_DETERMINER or \
            first_word[tags.TAG_INDEX] == tags.WH_PRONOUN:

        for identifier_one in identifiers_one:
            if identifier_one in sentence:
                for identifier_two in identifiers_two:
                    if identifier_two in sentence:
                        album_name, artist = sentence.split(identifier_two, 1)
                        nothing_much, album_name = album_name.split(identifier_one, 1)
                        print(artist)
                        return sparql(album_name.split(), artist[:-1].split())


def songs(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers_one and \
             word[tags.WORD_INDEX] != 'musics' and \
             word[tags.WORD_INDEX] != 'songs']
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return words
    return None

def by(words):
    words = [word for word in words
             if tags.NOUN_PROPER_SINGULAR in word[tags.TAG_INDEX] and \
             word[tags.WORD_INDEX] not in identifiers_two and \
             word[tags.WORD_INDEX] != 'by' and \
             word[tags.WORD_INDEX] != 'from']
    words = [word[tags.WORD_INDEX] for word in words]
    if len(words) > 0:
        return words
    return None

def sparql(albums_name, artist):
    albums_name_buffer = '_'.join(albums_name)
    artist_buffer = ' '.join(artist)
    wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
    wrapper.setReturnFormat(JSON)
    wrapper.setQuery(
        """ 
SELECT  DISTINCT ?songs

    WHERE
      { 
       
        ?album dbp:title ?musics ;
          dbp:thisAlbum ?name;
          dbo:artist ?artist.
        ?musics rdfs:label ?songs.
        ?artist rdfs:label ?artistname.
        ?name bif:contains "'%s'".
        ?artistname bif:contains "'%s'"
FILTER (LANG(?songs) = 'en')    
        
        
      } 
            """ % (albums_name_buffer, artist_buffer)
    )

    results = wrapper.query().convert()['results']['bindings']
    if len(results) > 0:
        genres = []
        for result in results:
            genres.append(result['songs']['value'])
        answer = "The album " + ' '.join(albums_name) + " by " + ' '.join(artist) + " contains the following list of songs: \n" + '\n- '.join(genres)
        return answer
    return None
