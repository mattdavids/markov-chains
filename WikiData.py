import wikipedia, csv, time

__author__ = 'Matthew Davids'


def wikiDatabase(num):
    '''
    Gets random articles from Wikipedia, creates dictionaries from them, then writes them to csv files
    @param num: how many articles to get
    @return:
    '''
    wikipedia.set_rate_limiting(True)
    wikipedia.set_lang("en")

    allWords = []

    fives = num // 500
    others = num % 500

    titles = []

    for i in range(fives):
        [titles.append(j) for j in wikipedia.random(500)]
    if others > 0:
        [titles.append(j) for j in wikipedia.random(others)]

    print("startingWIkidata, len = " + str(len(titles)))
    for page in titles:
        pageList = []
        try:
            words = wikipedia.page(page).content.split(' ')
        except (KeyError, ValueError, RuntimeError, ConnectionError, wikipedia.exceptions.WikipediaException,
                wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            pass
        for word in words:
            for i in word.split('\n'):
                pageList.append(i)
        allWords.append(pageList)

    print("completed " + str(len(allWords)) + " articles\nnow generating dict and writing to csv")

    for k in range(1, 10):
        dictionaryChain = makeDictFromListofLists(allWords, k)
        writeToCSV(dictionaryChain, 'wikipediaDatabase' + str(k) + '.csv')

        # print(allWords)


def writeToCSV(dictToWrite, file):
    '''
    Writes a dictionary to a csv file with rows representing key, value pairs
    @param dictToWrite: the dictionary to write to disk
    @param file: the file name to write to
    @return:
    '''
    with open(file, 'w', encoding='utf-8') as f:
        w = csv.writer(f)
        for key in list(dictToWrite.keys()):
            w.writerow([key] + dictToWrite[key])


def makeDictFromListofLists(lst, k=1):
    '''
    Takes a list of lists and generates a Markov chain dictionary
    @param lst: the list of lists of data
    @param k: the number of words to use as states or keys
    @return: the Markov chain dictionary
    '''
    dictionaryChain = {}

    for page in lst:
        for t in range(0, len(page) - k):
            accum = ""
            for i in range(k):
                accum += page[t + i] + ' '
            key = accum.strip()
            word = page[t + k]
            dictionaryChain.setdefault(key, [])
            if word != '':
                dictionaryChain[key].append(word.strip())

    return dictionaryChain


start = time.localtime()
wikiDatabase(40000)
end = time.localtime()
ans = end.tm_hour * 60 * 60 + end.tm_min * 60 + end.tm_sec - (
    start.tm_hour * 60 * 60 + start.tm_min * 60 + start.tm_sec)
print("time in minutes: " + str(ans / 60.0))
