# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 17:32:32 2014

@author: swalters
"""

import re

### FILE HANDLING METHODS

def openFile(filename):
    ''' returns text in a file as a string
        input: filename
        output: text string
    '''
    f = open(filename, 'r')
    fulltext = f.read()
    f.close()
    return fulltext
    
def readFile(filename):
    ''' returns dictionary representing sentences/categories in filename
        input: filename
        output: dictionary, key=statement & value=1/0
    '''
    ds = openFile(filename) # data string
    dl = re.split('\n', ds) # data list, with each entry a 'question***1' string
    res = {}
    for line in dl:
        temp = re.split(',', line)
        if len(temp) > 1:
            res[temp[0]] = temp[1] # key is sentence, value is categorization
    return res
    
def writeFile(dictionary, filename):
    ''' writes contents of dictionary into training data structure, filename.txt
        input: dictionary to be written, filename
        output: file is written
    '''
    res = ''
    for key in dictionary:
        res += key + ',' + str(dictionary[key]) + '\n' # specified format
    f = open(filename, 'w+')
    f.write(res)
    f.close()
    
def clean(gutenbergText):
    ''' strips Project Gutenberg boilerplate from the text of a book
        input: gutenbergText (string), from Project Gutenberg book
        output: substring of gutenbergText which is the body of the book
    '''
    startIndex = gutenbergText.find(' ***') # always at the end of introductory boilerplate
    endIndex = gutenbergText.find('End of the Project Gutenberg') # at beginning of ending boilerplate
    return gutenbergText[startIndex+4:endIndex] # startIndex is space before three asterisks
    
    
### PARSING METHODS

def parseQuestions():
    ''' gets questions/categorizations from (uniquely, not like trainingData.txt) structured .txt file
        input: none
        output: 
    '''
    qs = openFile('questions.txt')
    ql = re.split('\n', qs)
    res = {}
    for line in ql:
        sp = ['\r', '\n']
        rem = [',', '.']
        for char in sp:
            line = line.replace(char, ' ')
        for char in rem:
            line = line.replace(char, '')
        line = line.strip()
        space = line.find(' ')
        qmark = line.find('?')
        if qmark != -1:
            qtext = line[space:qmark].strip()
            res[qtext] = 1
    return res
    
def parseBooks(books): # books of format ['book1.txt', 'book2.txt']
    res = {}
    for book in books:
        text = clean(openFile(book))
        sentenceList = re.split("(?<=[\.?!])\W",text)
        for sentence in sentenceList:
            sp = ['\r', '\n']
            rem = [',', '.']
            for char in sp:
                sentence = sentence.replace(char, ' ')
            for char in rem:
                sentence = sentence.replace(char, '')
            sentence = sentence.strip()
            print sentence
            if len(sentence) > 0:
                if sentence[-1] == '?':
                    res[sentence] = 1
                else:
                    res[sentence] = 0
    return res
    

### DATA STORAGE METHOD
def build(filename):
    #d = readFile('trainingData.txt')
    d = {}
    q = parseQuestions()
    b = parseBooks(['book1.txt'])
    for sentence in q:
        if sentence not in d:
            d[sentence] = q[sentence]
    for sentence in b:
        if sentence not in d:
            d[sentence] = b[sentence]
    writeFile(d, filename)
    return d
    

### MAIN METHOD

if __name__ == '__main__':
    build('trainingData.txt')
    f = readFile('trainingData.txt')
    
    questions = []
    statements = []
    for key in f:
        if f[key] == '1':
            questions.append(key)
        else:
            statements.append(key)