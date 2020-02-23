import database

words_raw = database.get_all()
words = []
for word in words_raw:
    words.append([word[1], word[2]])
del words_raw

words.sort(key=lambda x: (x[0][0], -len(x[0])))

print(words[0])