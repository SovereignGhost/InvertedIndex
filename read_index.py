import sys
from nltk import PorterStemmer

def readfile(arg):

    if str(arg[0]) == '--term':

        stemmer = PorterStemmer()   # stem the term
        term = stemmer.stem(str(arg[1]))
        termid = 3
        for char in term:  # calculate term id
            termid = termid * 7 + ord(char)
        index = open("term_index.txt", "r")
        dictionary = {}
        for line in index:
            list = line.split()
            dictionary[list[0]] = (list[1], list[2])
        index.close()

        if str(termid) in dictionary:
            lol = 3
            print("Listing for term: " + str(arg[1]) + "\n")
            print("TERMID: " + str(termid) + "\n")
            tuple = dictionary.get(str(termid))  # tuple format: (frequency in corpus, total documents containing term)
            print("Number of documents containing term: " + str(tuple[1]) + "\n")
            print("Term frequency in corpus: " + str(tuple[0]) + "\n")


readfile(sys.argv[1:])
