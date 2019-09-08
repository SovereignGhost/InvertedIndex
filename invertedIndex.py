# Program to create Inverted Index
# from given corpus
# Parse HTML from corpus
# Tokenize
# Construct Index
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import nltk
from nltk import PorterStemmer

def visible(element):
    # return true only if text
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    elif isinstance(element, Comment):  # filter out comments
        return False
    return True


def parsehtml(rawcontent):
    # Parse HTML code to extract text
    soup = BeautifulSoup(rawcontent, 'html.parser')
    data = soup.findAll(text=True)
    text = filter(visible, data)
    return u" ".join(t.strip() for t in text)


def tokenizer(direc_path):
    # get stop-list
    # change working directory to specified one
    # process all files and tokenize

    # get all lines of stop-list
    # remove newline character at the end
    fp = open('stoplist.txt', 'r')
    stoplist = list(fp)
    fp.close()
    for i in range(len(stoplist)):
        stoplist[i] = stoplist[i][:-1]

    # change path to where corpus is
    current_dir = os.getcwd()
    os.chdir(direc_path)
    flist = []
    flist.extend(os.listdir(direc_path))

    term_dictionary = {}
    doc_dictionary = {}
    doc_id = 1
    term_id = 3

    # main loop
    for fname in os.listdir():

        # read file and add its name and ID to a dictionary
        fp = open(fname, 'r', encoding='latin-1', errors='replace')
        content = fp.read()
        fp.close()
        doc_dictionary[doc_id] = fname
        doc_id += 1

        # ignoring initial headers
        substr = "<!DOCTYPE"
        index = content.find(substr)
        htmlcode = content[index:]
        # get parsed result
        result = parsehtml(htmlcode)

        # Tokenize and turn to lower case
        token_list = nltk.word_tokenize(result)
        for i in range(len(token_list)):
            token_list[i] = token_list[i].lower()

        # print(len(token_list))

        # ignore tokens if they're in stop list
        i = 0
        deleteflag = False
        while i < len(token_list):
            for s in stoplist:
                if s == token_list[i]:
                    del token_list[i]
                    deleteflag = True
                    break
            if deleteflag:
                deleteflag = False
            else:
                i += 1

        # print(len(token_list))

        # stem the token list
        stemmer = PorterStemmer()
        for i in range(len(token_list)):
            token_list[i] = stemmer.stem(token_list[i])
        # print(token_list)

        # calculate unique term id
        for i in range(len(token_list)):
            for char in token_list[i]:
                term_id = term_id * 7 + ord(char)
            term_dictionary[term_id] = token_list[i]
            term_id = 3
        break
    # write doc dictionary to file
    os.chdir(current_dir)
    f = open('docids.txt', 'w')
    for key, value in doc_dictionary.items():
        f.write(str(key) + '\t' + str(value) + '\n')
    f.close()

    # write term dictionary to file
    f = open('termids.txt', 'w')
    for key, value in term_dictionary.items():
        f.write(str(key) + '\t' + str(value) + '\n')
    f.close()



directory = 'D:\Academics\Semester 5\Information Retrieval\Assignment 1\corpus\corpus\corpus'

tokenizer(directory)
