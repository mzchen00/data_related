import CYKParse
import Tree

requestInfo = {
        'name': '',
        'time': '',
        'location': '',
        'name2': '',
        'time2': '',
        'location2': '',

}
haveGreeted = False
comparison=False
# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):

    #for k, v in T.items():
        #print(k,v)
    # print('getSentenceParse', { k:v for k,v in T.items() })
    sentenceTrees = { k:v for k,v in T.items() if k.startswith('S/0') }
    completeSentenceTree = max(sentenceTrees.keys())

    return T[completeSentenceTree]


# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global comparison
    global requestInfo
    lookingForLocation = False
    lookingForName = False
    for leaf in Tr.getLeaves():
        #print(leaf)
        if leaf[1]=="will":
            comparison=True

        if leaf[0] == 'Adverb':
            #print(leaf[0],leaf[1])
            if requestInfo['time']!='' and comparison:
                requestInfo['time2'] = leaf[1]
            else:
                requestInfo['time'] = leaf[1]
        if lookingForLocation and leaf[0] == 'Name':
            requestInfo['location'] = leaf[1]
        if leaf[0] == 'Preposition' and leaf[1] == 'in':
            lookingForLocation = True
        else:
            lookingForLocation = False

        if leaf[0] == 'Noun' and leaf[1] == 'name':
            lookingForName = True
        if lookingForName and leaf[0] == 'Name':
            requestInfo['name'] = leaf[1]

# This function contains the data known by our simple chatbot
def getTemperature(location, time):
    if location == 'Pasadena':
        if time == 'now':
            return '90'
        elif time == 'tomorrow':
            return '45'
        elif time == 'yesterday':
            return '111'
    elif location == 'Tustin':
        if time == 'now':
            return '100'
        elif time == 'tomorrow':
            return '10'
        elif time == 'yesterday':
            return '101'

    elif location == 'Irvine':
        if time == 'now':
            return '68'
        elif time == 'tomorrow':
            return '70'
        elif time == 'yesterday':
            return '105'
    else:
        return 'unknown'

# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo
    global haveGreeted
    global comparison
    if not haveGreeted and requestInfo['name'] != '':
        print("Hello", requestInfo['name'] + '.')
        haveGreeted = True
        return

    time = 'now' # the default


    if requestInfo['time'] != '':
        time = requestInfo['time']
    salutation = ''
    if requestInfo['name'] != '':
        salutation = requestInfo['name'] + ', '

    if comparison:
        a= getTemperature(requestInfo['location'], requestInfo['time'])
        b= getTemperature(requestInfo['location'],requestInfo['time2'])
        print(a,requestInfo['time'])
        print(b, requestInfo['time2'])

        if (int(a)>int(b)):

            print(salutation + requestInfo['time'] +"'s temperature is hotter than " + requestInfo['time2'])
        elif (int(a)==int(b)):
            print(salutation + " , these two days are same temperature")
        elif a=="unkown":
            print("sorry cannot compare unknown")
        else:
            print(salutation + requestInfo['time2'] + "'s temperature is hotter than " + requestInfo['time'])

    else:
        print(salutation + 'the temperature in ' + requestInfo['location'] + ' ' +
            time + ' is ' + getTemperature(requestInfo['location'], time) + '.')

# A simple hard-coded proof of concept.
def main():

    global requestInfo
    ask = "hi my name is peter"
    print(ask)
    ask= ask.split(" ")
    print(ask)
    T, P = CYKParse.CYKParse(ask, CYKParse.getGrammarWeather())
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()




    "what is the temperature in Tustin yesterday"
    # print("type something")
    # a=input()
    # print(a.split(" "))
    # T, P = CYKParse.CYKParse(a.split(" "), CYKParse.getGrammarWeather())
    # sentenceTree = getSentenceParse(T)
    # updateRequestInfo(sentenceTree)
    # reply()
    # #
    # T,P =  CYKParse.CYKParse(['what','is','your','name'], CYKParse.getGrammarWeather())
    #
    #
    # sentenceTree = getSentenceParse(T)
    #
    # updateRequestInfo(sentenceTree)
    # reply()

main()