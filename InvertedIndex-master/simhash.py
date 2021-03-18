import re

def word_hash(word):
    return list(str(bin(abs(hash(word))))[2:][-32:])

def simhash(word_frequency):
    word_hash_value = {}
    for word in word_frequency:
        word_hash_value[word] = word_hash(word)
    simhash_list = [0]*32
    for word in word_frequency:
        for i in range(0,32):
            if word_hash_value[word][i]=='0':
                simhash_list[i]+=word_frequency[word]
            else:
                simhash_list[i]-=word_frequency[word]
    return simhash_list

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
    
def computeWordFrequencies(TokenList):
    frequency_dict = {}
    for word in TokenList:
        if word in frequency_dict:
            frequency_dict[word]+=1
        else:
            frequency_dict[word] = 1 
    return frequency_dict

if __name__ == "__main__":
    url_dict={}
    f = open("similar_pages.txt",'w')
    for line in open("tokens.txt"):
        url = line.split('\t',1)[0]
        words = line.split('\t')[1:]
        url_dict[url] = simhash(computeWordFrequencies(words))
    for url1 in url_dict:
        similar_url = []
        for url2 in url_dict:
            if url1!= url2:
                if compute_similarity(url_dict[url1],url_dict[url2]):
                    similar_url.append(url2)
        if similar_url != []:
            f.write(f"{url1} has {len(similar_url)} similar pages: \n")
            for url in similar_url:
                f.write('\t'+url+'\n')
                f.write('\n')
        
                    
        
    