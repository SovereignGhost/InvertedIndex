import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import nltk
from nltk import PorterStemmer
import heapq


class PriorityNode:
    def __init__(self, arraynumber, arrayindex, value):
        self.arraynumber = arraynumber  # array number from which value is picked
        self.arrayindex = arrayindex    # index within that array where the value was
        self.value = value

    def __lt__(self, other):
        return self.value < other.value


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


def sortonterm(val):
    return val[0], val[2]


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
    corpustuples = []

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

        tuplelist = []
        position_id = 1
        # calculate unique term id, and make a new tuple of format termid, docid, positionid
        for i in range(len(token_list)):
            for char in token_list[i]:
                term_id = term_id * 7 + ord(char)

            newtuple = (term_id, doc_id, position_id)
            tuplelist.append(newtuple)
            term_id = 3
            position_id += 1
        doc_id += 1

        # local sort
        tuplelist.sort(key=sortonterm)
        corpustuples.append(tuplelist)

    # Priority queue for merging
    prioritylist = []
    i = 0
    while i < len(corpustuples):
        if len(corpustuples[i]) > 0:
            node = PriorityNode(i, 0, corpustuples[i][0])
            prioritylist.append(node)
        i += 1

    heapq.heapify(prioritylist)
    # merging in final_list
    final_list = []
    while len(prioritylist) > 0:
        node = heapq.heappop(prioritylist)
        final_list.append(node.value)
        if node.arrayindex + 1 < len(corpustuples[node.arraynumber]):
            newnode = PriorityNode(node.arraynumber, node.arrayindex+1, corpustuples[node.arraynumber][node.arrayindex+1])
            heapq.heappush(prioritylist, newnode)

    term_index = []
    i = 0
    # making the index with docid and positionid gap encoded from final sorted list of tuples
    # tuple attributes: termid, docid, positionid
    # doc_list first appends all positions of a term for specific document then appends to node

    while i < len(final_list):
        curterm = final_list[i][0]
        termnode = TermAppearance(curterm)
        curpos = curdoc = 0
        doc_list = []
        while i < len(final_list) and final_list[i][0] == curterm:
            if final_list[i][1] != curdoc:
                doc_list = []
                termnode.docsappeared += 1
                doc_list.append(final_list[i][1] - curdoc)
                curdoc = final_list[i][1]
                curpos = 0
                doc_list.append(final_list[i][2] - curpos)
                curpos = final_list[i][2]
                termnode.doclist.append(doc_list)
            else:
                doc_list.append(final_list[i][2] - curpos)
                curpos = final_list[i][2]
            termnode.totalappearance += 1
            i += 1
        term_index.append(termnode)

    # writing to term_index.txt
    os.chdir(current_dir)
    fp = open('term_index.txt', 'w')
    for i in range(len(term_index)):
        fp.write(str(term_index[i].termid)+" "+str(term_index[i].totalappearance)+" "+str(term_index[i].docsappeared))
        for j in range(len(term_index[i].doclist)):
            fp.write(" ")
            for k in range(len(term_index[i].doclist[j])):
                if k < len(term_index[i].doclist[j]) - 1:
                    fp.write(str(term_index[i].doclist[j][k]) + ",")
                else:
                    fp.write(str(term_index[i].doclist[j][k]))
        fp.write("\n")
    fp.close()



directory = 'D:\Academics\Semester 5\Information Retrieval\Assignment 1\corpus\corpus\corpus'
indexconstructor(directory)
