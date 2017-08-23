## reddit bot currency convert

import praw
import check
import time
import requests


# https://www.exchangerate-api.com/python-currency-api
url = 'https://v3.exchangerate-api.com/bulk/68ed6db1a6575c73fdd3f383/USD' 
#last item in the url is the currency that will have exchange rate of 1

# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)


def kgConversion(comment):
    #convert from kg to lbs
    def converttoLbs(toConvert,converted): #converted is a listof(Num, Num) representing (lbs,kgs)
        if toConvert == []:
            return converted
        else:
            converted.append([toConvert[0],round((float(toConvert[0])*2.2046226218),2)])
            return converttoLbs(toConvert[1:],converted) 
    text = (comment.body).split()
    author = comment.author
    message =""
    toConvert = []
    if 'kg' in text:
        for i in range (1,len(text)):
            if (text[i] == 'kg' or text[i] == 'kgs') and text[i-1].isdigit():
                toConvert.append(text[i-1])
                #print(toConvert) 
        
        converted =  converttoLbs(toConvert,[])
    
        #Generate message
        for i in range(len(converted)):
            message+=("{0} kg is {1} lbs \n".format(converted[i][0],converted[i][1]))    
    return(message)
  
  
def lbConversion(comment):   
    #convert from lbs to kg
    def converttoKg(toConvert,converted): #converted is a listof(Num, Num) representing (lbs,kgs)
        if toConvert == []:
            return converted
        else:
            converted.append([toConvert[0],round((float(toConvert[0])/2.2046226218),2)])
            return converttoKg(toConvert[1:],converted)
    text = (comment.body).split()
    author = comment.author
    message =""
    toConvert = []
    if 'lbs' in text or  'lb' in text:
        for i in range (1,len(text)):
            if (text[i] == 'lbs' or text[i] == 'lbs') and text[i-1].isdigit():
                toConvert.append(text[i-1])
                #print(toConvert) 
                    
        converted = converttoKg(toConvert,[])
            
        #Generate message
        for i in range(len(converted)):
            message+=("{0} lbs is {1} kg \n".format(converted[i][0],converted[i][1]))
            
    return(message)
    
 
 
def bot_login():
    currencyBot =  praw.Reddit(user_agent='Converter Bot',
                               client_id='xI2pGK6CEylHzA',
                               client_secret='XuFjA6em6VsKPCuQrmn-kDaMQ3s',
                               username='convertoBot',
                               password='t0r7ez!')
    check.expect("check authentication",currencyBot.user.me(),"convertoBot")
    return currencyBot


def run_bot(currencyBot):
    
    ##subreddit = currencyBot.subreddit('ssbm')
    subreddit = currencyBot.subreddit('all')
    comments = subreddit.comments(limit=None)
    
    for comment in comments:
        message = ""
        message+=kgConversion(comment)
        message+=lbConversion(comment)
        if message !="":
            print(message)
            ##comment.reply(message) #send message
            
    # sleeps for 10 seconds
    print("sleep 10 seconds")
    time.sleep(10)
    

##Tests                  note: cannot perform unit tests on nested functions!
#ConverttoKG
#check.expect("Convert to kg one item",converttoKg([2.2],[]),[[2.2,1]])
#check.within("Convert to kg multiple items",converttoKg([2.2,100,135,1],[]),[[2.2, 1.0], [100, 45.36], [135, 61.23], [1, 0.45]],0.001)
#ConverttoLbs
#check.expect("Convert to lbs one item",converttoLbs([1],[]),[[1 ,2.2]])
#check.within("Convert to lbs multiple items",converttoLbs([2.2,100,135,1],[]),[[2.2, 4.85], [100, 220.46], [135, 297.62], [1, 2.2]],0.001)



r = bot_login()
while True:
    run_bot(r)










