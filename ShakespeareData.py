import csv

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
            accum = word
            dictionaryChain.setdefault(key, [])
            if accum != '':
                dictionaryChain[key].append(accum.strip())

    return dictionaryChain


from lxml import html
import requests

playIndices = ['allswell', 'asyoulikeit', 'comedy_errors', 'cymbeline', 'lll',
               'measure', 'merry_wives', 'merchant', 'midsummer', 'much_ado',
               'pericles', 'taming_shrew', 'tempest', 'troilus_cressida',
               'twelfth_night', 'two_gentlemen', 'winters_tale', '1henryiv',
               '2henryiv', 'henryv', '1henryvi', '2henryvi', '3henryvi',
               'henryviii', 'john', 'richardii', 'richardiii', 'cleopatra',
               'coriolanus', 'hamlet', 'julius_caesar', 'lear', 'macbeth',
               'othello', 'romeo_juliet', 'timon', 'titus']

allPlays = []

print('getting play data')

'''
Gets all Shakespeare plays from shakespeare.mit.edu, creates dictionaries, and writes them to file as csv
'''
for play in playIndices:

    page = requests.get('http://shakespeare.mit.edu/' + play + '/full.html')
    tree = html.fromstring(page.content)
    lines = tree.xpath('/html/body/blockquote[*]/a/text()')

    thisPlay = []
    for line in lines:
        [thisPlay.append(word) for word in line.split(' ')]

    allPlays.append(thisPlay)

for k in range(1, 10):
    print('making dict and writing to csv, k = ' + str(k))

    dictionaryChain = makeDictFromListofLists(allPlays, k)
    writeToCSV(dictionaryChain, 'shakespeareDatabase' + str(k) + '.csv')
