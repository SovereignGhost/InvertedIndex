import sys
from nltk import PorterStemmer

def readfile(arg):

    if str(arg[0]) == '--term':
        termdict = {}
        fp = open("termids.txt", 'r')
        termlist = list(fp)
        fp.close()
        for entry in termlist:
            entry = entry[0:-1]
            pair = entry.split('\t')
            termdict[pair[1]] = int(pair[0])
        termlist = []

        stemmer = PorterStemmer()   # stem the term
        term = stemmer.stem(str(arg[1]))
        termid = termdict.get(term)

        index = open("term_index.txt", "r")
        dictionary = {}
        for line in index:
            List = line.split()
            dictionary[int(List[0])] = (List[1], List[2])
        index.close()

        if termid in dictionary:
            print("Listing for term: " + str(arg[1]) + "\n")
            print("TERMID: " + str(termid) + "\n")
            tuple = dictionary.get(termid)  # tuple format: (frequency in corpus, total documents containing term)
            print("Number of documents containing term: " + str(tuple[1]) + "\n")
            print("Term frequency in corpus: " + str(tuple[0]) + "\n")
        else:
            print(term + " is not present in index")


readfile(sys.argv[1:])
