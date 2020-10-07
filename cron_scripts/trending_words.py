import nltk;nltk.download('popular')

def trending_words(rep, dem):
    status_list_rep = []
    status_list_dem = []
    status_dict = {}

    for status in rep['status']:
        for word in status.split():
            token = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(token)
            if tagged[0][1][0] == 'N' and word[0] != "@" and word[:4].lower() != "http":
                status_list_rep.append(word.lower())

    for status in dem['status']:
        for word in status.split():
            token = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(token)
            if tagged[0][1][0] == 'N' and word[0] != "@" and word[:4].lower() != "http":
                status_list_dem.append(word.lower())

    word_dict_rep = {}
    word_dict_dem = {}

    for word in status_list_rep:
        if word not in word_dict_rep.keys():
            word_dict_rep[word] = 0
        else:
            word_dict_rep[word] = word_dict_rep.get(word) + 1

    for word in status_list_dem:
        if word not in word_dict_dem.keys():
            word_dict_dem[word] = 0
        else:
            word_dict_dem[word] = word_dict_dem.get(word) + 1

    word_dict_rep = sorted(word_dict_rep.items(), key=lambda x: x[1], reverse=True)
    word_dict_dem = sorted(word_dict_dem.items(), key=lambda x: x[1], reverse=True)

    tweet = "Republicans:\n"
    for tup in word_dict_rep[:10]:
        tweet += "\t" + str(tup[0]) + " => " + str(tup[1]) + "\n"

    tweet += "\nDemocrats:\n"
    for tup in word_dict_dem[:10]:
        tweet += "\t" + str(tup[0]) + " => " + str(tup[1]) + "\n"

    return tweet
