import os
import math
import json
if __name__ == "__main__":
    offset = 0
    num_file  = 55393
    num_tokens = 0
    invert_invert_index = {}
    f1 = open("partial_index"+os.path.sep+"inverted_index1.txt",'r')
    f2 = open("partial_index"+os.path.sep+"inverted_index2.txt",'r')
    f3 = open("partial_index"+os.path.sep+"inverted_index3.txt",'r')
       
    f_merge = open("inverted_index.txt","w")
    merge_list = []
    line1 = f1.readline()
    line2 = f2.readline()
    line3 = f3.readline()
    while(line1 or line2 or line3):
        write_line = ""
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
        num_tokens+=1
        len_postinglist = len(postinglist)
        write_line+=token+':'+str(len_postinglist)+":"
        for posting in postinglist:
            write_line+=(posting+' '+str(round(int(posting.split(' ')[1])*math.log(num_file/len_postinglist),2))+'\t')
        write_line+='\n'
        f_merge.write(write_line)
        invert_invert_index[token] = offset
        offset += len(write_line)
    with open("invert_invert_index.txt",'w') as outfile:
        json.dump(invert_invert_index,outfile)
    print(num_tokens)
    
    
