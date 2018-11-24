import extraction

params = {
    "What is the genre of the Beatles?": "Beatles",
    "What is the Beatles genre?": "Beatles",
    "What genre of music do The Beatles fall under?": "Beatles",
    "What kind of music is Coldplay?": "Coldplay",
    "What kind of genre is Taylor Swift?": "Taylor Swift",
    "What is the genre of Iron Maiden?": "Iron Maiden",
    "What is JoJo genre?": "JoJo",
    "What kind of music is OneRepublic?": "OneRepublic",
    "What kind of genre is Kodaline?": "Kodaline"
}

for key, value in params.items():
    result = extraction.process(key)
    if result != value:
        print("Don't match")
        print("key: %s" % key)
        print("value: %s" % value)
        print("result: %s" % result)