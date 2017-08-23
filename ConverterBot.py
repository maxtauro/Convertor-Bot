## reddit bot currency convert

import praw
import check
import time


#convert from lbs to kg
def converttoKg(toConvert,converted): #converted is a listof(Num, Num) representing (lbs,kgs)
    if toConvert == []:
        return converted
    else:
        converted.append([toConvert[0],(toConvert[0]/2.2)])
        return converttoKg(toConvert[1:],converted)
    
#convert from kg to lbs
def converttoLbs(toConvert,converted): #converted is a listof(Num, Num) representing (lbs,kgs)
    if toConvert == []:
        return converted
    else:
        converted.append([toConvert[0],(toConvert[0]*2.2)])
        return converttoLbs(toConvert[1:],converted)    
    

def bot_login():
    currencyBot =  praw.Reddit(user_agent='CurrencyBot v0.1',
                               client_id='POmsiu3RKBxEKg',
                               client_secret='0QEu3wMvD95ygr5plnx3RrH28fo',
                               username='ConvertCurrencyBot',
                               password='t0r7ez!')
    check.expect("check authentication",currencyBot.user.me(),"ConvertCurrencyBot")
    return currencyBot

def run_bot(currencyBot):
    
    ##subreddit = currencyBot.subreddit('ssbm')
    subreddit = currencyBot.subreddit('all')
    comments = subreddit.comments(limit=None)
    
    for comment in comments:
        text = (comment.body).split()
        author = comment.author
        toConvert = []
        
        if 'kg' in text:
            for i in range (1,len(text)):
                if (text[i] == 'kg' or text[i] == 'kgs') and text[i-1].isdigit():
                    toConvert.append(text[i-1])
                    #print(toConvert) 
            
            #Generate message
            message = "Congrats Max ur siccc"
            ##comment.reply(message) #send message
            print("kg was brough up in {0} in {1}".format(text,comment.submission.title)) 
            print('/n')
            
        elif 'lbs' in text or  'lb' in text:
            for i in range (1,len(text)):
                if (text[i] == 'lb' or text[i] == 'lbs') and text[i-1].isdigit():
                    toConvert.append(text[i-1])
                    #print(toConvert)             
            
            #Generate message
            message = "Congrats Max ur siccc"
            ##comment.reply(message) #send message
            print("lb was brought up in {0} in {1}".format(text,comment.submission.title))  
            print('/n')
            
            #Call conversion from lb to kg
            
            
            
            
            
    # sleeps for 10 seconds
    print("sleep 10 seconds")
    time.sleep(10)
    

##Tests
    
#ConverttoKG
check.expect("Convert to kg one item",converttoKg([2.2],[]),[[2.2,1]])
check.within("Convert to kg multiple items",converttoKg([2.2,100,135,1],[]),[[2.2, 1.0], [100, 45.4545], [135, 61.363], [1, 0.4545]],0.001)

#ConverttoLbs
check.expect("Convert to lbs one item",converttoLbs([1],[]),[[1 ,2.2]])
check.within("Convert to lbs multiple items",converttoLbs([2.2,100,135,1],[]),[[2.2, 4.84], [100, 220.0], [135, 297.0], [1, 2.2]],0.001)



#r = bot_login()
#while True:
#    run_bot(r)










