import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import nltk
from nltk import PorterStemmer

class TermAppearance:
    def __init__(self, termid):
        self.termid = termid    # term id
        self.doclist = []       # a list of list containing document and positionid
        self.totalappearance = 0
        self.docsappeared = 0


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


def indexconstructor(direc_path):
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

    doc_id = 1
    term_id = 3
    term_dictionary = {}

    # main loop
    for fname in os.listdir():

        # read file and add its name and ID to a dictionary
        fp = open(fname, 'r', errors='ignore')
        content = fp.read()
        fp.close()

        # ignoring initial headers
        substr = "<!DOCTYPE"
        index = content.find(substr)
        htmlcode = content[index:]
        # get parsed result
        result = parsehtml(htmlcode)

        # Tokenize and turn to lower case
        token_list = nltk.regexp_tokenize(result, "[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+")
        for i in range(len(token_list)):
            token_list[i] = token_list[i].lower()

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

        # stem the token list
        stemmer = PorterStemmer()
        for i in range(len(token_list)):
            token_list[i] = stemmer.stem(token_list[i])

        position = 0
        for i in range(len(token_list)):
            position += 1
            for char in token_list[i]:
                term_id = term_id * 7 + ord(char)

            if term_id not in term_dictionary:
                termdocs = []
                docposition_list = [doc_id, position]    # document id, first position
                termdocs.append(docposition_list)
                term_dictionary[term_id] = termdocs     # 2d posting list
            else:
                termdocs = term_dictionary.get(term_id)  # get posting list
                lastdocid = 0

                for array in termdocs:  # calculate latest docid
                    lastdocid = lastdocid + array[0]

                if doc_id == lastdocid:  # calculate latest position id and insert current position with gap encoding
                    latestposition = 0
                    for positions in termdocs[-1][1:]:
                        latestposition = latestposition + positions
                    termdocs[-1].append(position - latestposition)
                else:
                    docposition_list = [doc_id - lastdocid, position]
                    termdocs.append(docposition_list)
            term_id = 3
        doc_id += 1

    # writing to term_index.txt
    os.chdir(current_dir)
    fp = open('term_index.txt', 'w')
    for term_id, postinglist in term_dictionary.items():
        totaldocsappeared = len(postinglist)
        totalappearence = 0
        for array in postinglist:
            totalappearence = totalappearence + (len(array) - 1)
        fp.write(str(term_id)+" "+str(totalappearence)+" "+str(totaldocsappeared))
        for array in postinglist:
            fp.write(" ")
            for i in range(len(array)):
                if i == len(array)-1:
                    fp.write(str(array[i]))
                else:
                    fp.write(str(array[i]) + ",")
        fp.write("\n")
    fp.close()





directory = 'D:\Academics\Semester 5\Information Retrieval\Assignment 1\corpus\corpus\corpus'
indexconstructor(directory)