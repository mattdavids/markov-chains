import random, csv, string, time

__author__ = 'Matthew Davids'


def init(k, common, source="shakespeare"):
    '''
    reads databases and imports them as dictionaries
    @param k: the number of words to use as a state or key
    @param common: boolean, true if trying to find the average sentence
    @param source: name of the source to import
    @return: the first key to use and a Markov chain dictionary
    '''
    file = ''

    if source == "shakespeare":
        file = "shakespeareDatabase" + str(k) + ".csv"
    if source == "wiki":
        file = "wikipediaDatabase" + str(k) + ".csv"
    if source == "twitter":
        file = 'twitterDatabase' + str(k) + ".csv"

    dictionaryChain = readFromCSV(file)

    if common:
        return findFirstKey(dictionaryChain, k)[0], dictionaryChain
    else:
        return list(dictionaryChain.keys())[random.randrange(0, len(dictionaryChain))], dictionaryChain


def next(str, dictionaryChain, k, enableRandom=False):
    '''
    Finds the next word that follows an input word
    @param str: the key to use as the current state
    @param dictionaryChain: the Markov chain dictionary that contains the states
    @param k: the number of words to use as a state or key
    @param enableRandom: boolean, true if the program can pick a random key if there is no next state
    @return: the next word, and an error value
    '''
    try:
        n = len(dictionaryChain[str])

    except KeyError:
        if enableRandom:
            return list(dictionaryChain.keys())[random.randrange(0, len(dictionaryChain))], 0
        else:
            return '', -1

    if n > 0:
        # print(dictionaryChain[str])
        nextWord = dictionaryChain[str][random.randrange(0, n)]
    else:
        nextWord = list(dictionaryChain.keys())[random.randrange(0, len(dictionaryChain))]
    return nextWord, 0


def nextMostCommon(str, dict, k, enableRandom=False):
    '''
    Finds the next most common word that follows an input word, breaks if the next word it finds is not significantly
    common enough
    @param str: the key to use as the current state
    @param dict: the Markov chain dictionary that contains the states
    @param k: the number of words to use as a state or key
    @param enableRandom: boolean, true if the program can pick a random key if there is no next state
    @return: the next word, and an error value
    '''
    appearances = {}

    maxKey = ''
    maxVal = -1

    try:
        dict[str]
    except KeyError:
        return '', -1

    if k > 1:
        accum = ''
        for j in range(k - 1):
            accum += str.split()[j + 1] + ' '
        prev = accum.strip()
        for word in dict[str]:
            word = removePunctuation(word).lower()
            key = prev + ' ' + word
            appearances[key] = appearances.setdefault(key, 0) + 1
            if appearances[key] > maxVal:
                maxKey = key.split()[-1].strip()
                maxVal = appearances[key]
        if str != str.lower():
            for word in dict.setdefault(str.lower(), []):
                word = removePunctuation(word).lower()
                key = prev + ' ' + word
                appearances[key] = appearances.setdefault(key, 0) + 1
                if appearances[key] > maxVal:
                    maxKey = key.split()[-1].strip()
                    maxVal = appearances[key]
        if str != str[0].upper() + str[1:]:
            for word in dict.setdefault(str[0].upper() + str[1:], []):
                word = removePunctuation(word).lower()
                key = prev + ' ' + word
                appearances[key] = appearances.setdefault(key, 0) + 1
                if appearances[key] > maxVal:
                    maxKey = key.split()[-1].strip()
                    maxVal = appearances[key]
    else:
        for word in dict[str]:
            word = removePunctuation(word).lower()
            appearances[word] = appearances.setdefault(word, 0) + 1
            if appearances[word] > maxVal:
                maxKey = word
                maxVal = appearances[word]
        if str != str.lower():
            for word in dict.setdefault(str.lower(), []):
                word = removePunctuation(word).lower()
                key = word
                appearances[key] = appearances.setdefault(key, 0) + 1
                if appearances[key] > maxVal:
                    maxKey = key.split()[-1].strip()
                    maxVal = appearances[key]
        if str != str[0].upper() + str[1:]:
            for word in dict.setdefault(str[0].upper() + str[1:], []):
                word = removePunctuation(word).lower()
                key = word
                appearances[key] = appearances.setdefault(key, 0) + 1
                if appearances[key] > maxVal:
                    maxKey = key.split()[-1].strip()
                    maxVal = appearances[key]

    if maxVal == 1:
        return maxKey, -1

    # print(maxKey, maxVal)

    return maxKey, 0


def readFromCSV(file):
    '''
    Reads a csv file into a dictionary where each row is a key, value pair.
    @param file: a file name or path
    @return: a dictionary that was created from the csv
    '''
    result = {}

    with open(file, 'r', encoding='utf-8') as f:
        w = csv.reader(f)
        for row in w:
            if row:
                key = row[0]
                value = row[1:]
                result[key] = value
    return result


def findFirstKey(dict, k):
    '''
    Finds the most common first word in a sentence
    @param dict: the Markov chain dictionary that contains the states
    @param k: the number of words to use as a state or key
    @return: most common start to a sentence string and the number of times it appears
    '''
    appearances = {}

    maxKey = ''
    maxVal = -1

    for key in dict.keys():
        if len(key.split()) == k:
            if key[0].isupper():
                noPunKey = removePunctuation(key)
                appearances[noPunKey] = len(dict[key]) + appearances.setdefault(noPunKey, 0)
                if appearances[noPunKey] > maxVal:
                    maxKey = noPunKey
                    maxVal = appearances[noPunKey]

    return maxKey, maxVal


def removePunctuation(str):
    '''
    Removes the punctuation from a string
    @param str: an input string that may contain punctuation
    @return: a punctuationless string
    '''
    accum = ''
    for i in range(0, len(str)):
        if str[i] not in string.punctuation:
            accum += str[i]
    return accum


def main(n, k, common=False, enableRandom=False, source="shakespeare"):
    '''
    Generates text from an input source and writes it to a file
    @param n: length of text to generate in words, will be shorter if common=True
    @param k: the number of words to use as a state or key
    @param common: boolean, true if trying to find the average sentence
    @param enableRandom: boolean, true if the program can pick a random key if there is no next state
    @param source: name of the source to import
    @return: the text it has written to a file
    '''
    start, dictionaryChain = init(k, common, source=source)
    fullText = start

    if common:
        findNext = nextMostCommon
    else:
        findNext = next

    for i in range(n):

        if k > 1:
            accum = ''
            for j in range(k - 1):
                accum += start.split()[j + 1] + ' '
            prev = accum.strip()
        else:
            prev = ''

        start = findNext(start, dictionaryChain, k, enableRandom)
        if start[1] == -1:
            fullText += ' ' + start[0]
            break
        start = start[0]

        if start.endswith('.'):
            fullText += " " + start + '\n'
        else:
            fullText += " " + start

        start = prev + ' ' + start
        start = start.strip()

    # print(fullText)

    with open('output.txt', "w", encoding='utf-8') as output:
        output.write(fullText)

    return fullText


start = time.localtime()
main(n=100, k=2, common=False, enableRandom=False, source="shakespeare")
end = time.localtime()
ans = end.tm_hour * 60 * 60 + end.tm_min * 60 + end.tm_sec - (
    start.tm_hour * 60 * 60 + start.tm_min * 60 + start.tm_sec)
print("time in minutes: " + str(ans / 60.0))