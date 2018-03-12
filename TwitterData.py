import csv, time, os

__author__ = 'Matthew Davids'


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

try:
    import json
except ImportError:
    import simplejson as json

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

NUM_TWEETS = 5000000
k = 1

ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
API_KEY = os.environ.get('TWITTER_API_KEY')
API_SECRET = os.environ.get('TWITTER_API_SECRET')

print("starting")

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, API_KEY, API_SECRET)

twitter_stream = TwitterStream(auth=oauth)

tweets = twitter_stream.statuses.sample()

allTweets = []

print("getting tweets")

tweetTotal = NUM_TWEETS

'''
Gets tweets from Twitter, creates dictionaries from them, and writes them to file as csv
'''

for tweet in tweets:

    trueTweet = json.loads(json.dumps(tweet))
    if 'text' in trueTweet:
        current = trueTweet['text'].split(' ')
        for word in current:
            if word.startswith('http'):
                current.remove(word)
            if word == '':
                current.remove(word)
        allTweets.append(current)
        tweetTotal -= 1
        if tweetTotal % 100000 == 0:
            print(str(tweetTotal) + ' left')

    if tweetTotal <= 0:
        break

print(str(NUM_TWEETS - tweetTotal) + " tweets completed")

print("making dict and writing to csv")

for k in range(1, 10):
    dictionaryChain = makeDictFromListofLists(allTweets, k)
    writeToCSV(dictionaryChain, 'twitterDatabase' + str(k) + '.csv')

end = time.localtime()
ans = end.tm_hour * 60 * 60 + end.tm_min * 60 + end.tm_sec - (
    start.tm_hour * 60 * 60 + start.tm_min * 60 + start.tm_sec)
print(str(NUM_TWEETS) + " tweets, time in minutes: " + str(ans / 60.0))
