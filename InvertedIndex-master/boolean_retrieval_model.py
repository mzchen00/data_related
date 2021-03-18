import os
import time
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from collections import defaultdict
from urllib.parse import urlparse

def compute_similarity(vector1,vector2):
    same = 0
    for i in range(32):
        if vector1[i] == vector2[i]:
            same +=1
    #the threshold value for similarity is 90%
    if same/32 >= 0.9:
        return True
    else:
        return False
    
if __name__ == "__main__":
    possible_postings =[]
    with open("invert_invert_index.txt") as file1:
        invert_invert_index = json.load(file1)
    with open("document_info.txt") as file2:
        doc_info = json.load(file2)
    inverted_index = open("inverted_index.txt","r")
    print("Welcome to our search engine!")
    query = input("Please enter your query: ")
 
    start = time.time()
    #process the query
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
    stemmer = PorterStemmer()
    query_list = tokenizer.tokenize(query.lower())
    query_list = [stemmer.stem(word) for word in query_list]
    position = 0
    for word in query_list:
        position = invert_invert_index[word]
        inverted_index.seek(position,0)
        line = inverted_index.readline()
        temp = {}
        for posting in line.split(':',2)[-1].rstrip('\t\n').split('\t'):
            temp[posting.split(" ")[0]] = float(posting.split(" ")[-1]) * (int(posting.split(" ")[2])+1)
        possible_postings.append(temp)
    shortest_postings = min(possible_postings,key = lambda x: len(x))
    result_docIDs = defaultdict(int)
    for id in shortest_postings.keys():
        for dict in possible_postings:
            if id in result_docIDs and id not in dict:
                del result_docIDs[id]
                break
            elif  id not in dict:
                break
            else:
                result_docIDs[id]+= dict[id]    
    
    count = 0
    urls = []
    simhash_values = set()
    for id,ifndf in sorted(result_docIDs.items(),key = lambda x:-x[1]):
        url,simhash = doc_info[id]
        parsed = urlparse(url)
        defragment_url = parsed.scheme+'://'+parsed.netloc+parsed.path+parsed.query
        if defragment_url not in urls:
            similar = False
            for exist_simhash in simhash_values:
                if compute_similarity(exist_simhash, simhash):
                    similar = True
                    break
            if similar == False:
                urls.append(defragment_url)
                print(url)
                count+=1
        if count == 5:
            break
    end = time.time()
    print("it takes",(end-start)*1000,"ms")
    