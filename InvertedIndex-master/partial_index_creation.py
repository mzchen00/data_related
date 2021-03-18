import os
from collections import defaultdict
from simhash import simhash
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from bs4 import BeautifulSoup
import math

inverted_index = defaultdict(list)

class posting:
    def __init__(self,docID,occurence,importance):
        self.docID = docID
        self.occurence = occurence
        self.importance = importance

def fetch(file, num_file):
    f = open(file)
    json_file = json.load(f)
    url = json_file["url"]
    soup = BeautifulSoup(json_file["content"].encode(json_file["encoding"], "strict"),features = "html.parser")
    important_words = []
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
    for word in soup.find_all('h1'):
        important_words+=tokenizer.tokenize(word.get_text().lower())
    for word in soup.find_all('h2'):
        important_words+=tokenizer.tokenize(word.get_text().lower())
    for word in soup.find_all('h3'):
        important_words+=tokenizer.tokenize(word.get_text().lower())
    for word in soup.find_all('b'):
        important_words+=tokenizer.tokenize(word.get_text().lower())
    stemmer = PorterStemmer()
    important_words = set(stemmer.stem(word) for word in important_words)
    text = soup.get_text().lower()
    tokens = [stemmer.stem(word) for word in tokenizer.tokenize(text)]
    frequency_dict = {}
    for word in tokens:
        if word in frequency_dict:
            frequency_dict[word]+=1
        else:
            frequency_dict[word] = 1 
    return_dict = {}
    for word,freq in frequency_dict.items():
        return_dict[word] = posting(num_file,freq,1 if word in important_words else 0)
    return return_dict, url, simhash(frequency_dict)

def off_load(file_name):
    global inverted_index
    print("off_load")
    f = open(file_name,'w')
    for token,postings in sorted(inverted_index.items(),key = lambda x: x[0]):
        f.write(token+':')
        for posting in postings:
            f.write(str(posting.docID)+" "+str(posting.occurence)+" "+str(posting.importance)+"\t")
        f.write("\n")
    f.close()
    inverted_index = defaultdict(list)
  
if __name__ == "__main__":
    num_file = 0
    doc_info = {}
    f_table = open("document_info.txt",'a+')
    for root1, dirs1, files1 in os.walk("DEV"):
        for dir in dirs1:
            for root2, dirs2, files2 in os.walk(root1+os.path.sep+dir):
                for file in files2:
                    num_file+=1
                    file_dict, url, sim = fetch(root1+os.path.sep+dir+os.path.sep+file, num_file)
                    doc_info[num_file] = (url, sim)
                    for k,v in file_dict.items():
                        inverted_index[k].append(v)
                    if num_file%20000==0:
                        off_load("partial_index"+os.path.sep+f"inverted_index{num_file//20000}.txt")
    off_load("partial_index"+os.path.sep+f"inverted_index{num_file//20000+1}.txt")
    with open("document_info.txt",'w') as outfile:
        json.dump(doc_info,outfile)
#     for num, (url, sim) in sorted(doc_info.items(), key = lambda x:x[0]):
#         f_table.write(str(num)+"\t"+url+"\t"+str(sim)+'\n')
    print(num_file)

