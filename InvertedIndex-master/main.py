import os
from collections import defaultdict
from posting import posting
from simhash import simhash
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from bs4 import BeautifulSoup
import math

inverted_index = defaultdict(list)

def fetch(file):
    f_table = open("document_info.txt",'a+')
    f = open(file)
    json_file = json.load(f)
    url = json_file["url"]
    soup = BeautifulSoup(json_file["content"],features = "html.parser")
    important_words = []
    tokenizer = RegexpTokenizer(r'\w+')
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
    f_table.write(str(file.rstrip('.json').split(os.path.sep)[-1])+"\t"+url+"\t"+str(simhash(frequency_dict))+'\n')
    for word,freq in frequency_dict.items():
        return_dict[word] = posting(file.rstrip('.json').split(os.path.sep)[-1],freq,1 if word in important_words else 0)
    return return_dict

def off_load(file_name):
    global inverted_index
    print("off_load")
    f = open(file_name,'w')
    for token,postings in sorted(inverted_index.items(),key = lambda x: x[0]):
        f.write(token+':')
        for posting in postings:
            f.write(posting.docID+" "+str(posting.occurence)+" "+str(posting.importance)+"\t")
        f.write("\n")
    f.close()
    inverted_index = defaultdict(list)
  
if __name__ == "__main__":
    num_file = 0
    for root1, dirs1, files1 in os.walk("DEV"):
        for dir in dirs1:
            for root2, dirs2, files2 in os.walk(root1+os.path.sep+dir):
                for file in files2:
                    file_dict = fetch(root1+os.path.sep+dir+os.path.sep+file)
                    for k,v in file_dict.items():
                        inverted_index[k].append(v)
                    num_file+=1
                    if num_file%20000==0:
                        off_load(f"inverted_index{num_file//20000}.txt")
    off_load(f"inverted_index{num_file//20000+1}.txt")
    
    f1 = open("inverted_index1.txt",'r')
    f2 = open("inverted_index2.txt",'r')
    f3 = open("inverted_index3.txt",'r')
      
    f_merge = open("inverted_index.txt","w")
    merge_list = []
    line1 = f1.readline()
    line2 = f2.readline()
    line3 = f3.readline()
    while(line1 or line2 or line3):
        tokens = []
        if line1 != "":
            token1 = line1.split(':',1)[0]
            tokens.append(token1)
        if line2!= "":
            token2 = line2.split(':',1)[0]
            tokens.append(token2)
        if line3!= "":
            token3 = line3.split(':',1)[0]
            tokens.append(token3)
        token = min(tokens)
        posting1=[]
        posting2=[]
        posting3 = []
        if token1 == token:
            posting1= line1.rstrip('\n').split(':')[1].rstrip('\t').split('\t')
            line1 = f1.readline()
        if token2 == token:
            posting2= line2.rstrip('\n').split(':')[1].rstrip('\t').split('\t')
            line2 = f2.readline()
        if token3 == token:
            posting3= line3.rstrip('\n').split(':')[1].rstrip('\t').split('\t')
            line3 = f3.readline()
        postinglist = posting1+ posting2+posting3
        f_merge.write(token+':')
        len_postinglist = len(postinglist)
        for posting in postinglist:
            f_merge.write(posting+' '+str(int(posting.split(' ')[1])*math.log(num_file/len_postinglist))+'\t')
        f_merge.write('\n')

      
              