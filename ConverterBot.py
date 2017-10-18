## reddit bot convert

import praw
import check
import time
import requests


CurrencyTypes = ['USD', 'AED', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'BBD', 'BDT', 
                 'BGN', 'BHD', 'BRL', 'BSD', 'BWP', 'BYN', 'CAD', 'CHF', 'CLP', 
                 'CNY', 'COP', 'CZK', 'DKK', 'DOP', 'EEK', 'EGP', 'ETB', 'EUR', 
                 'FJD', 'GBP', 'GHS', 'GTQ', 'HKD', 'HNL', 'HRK', 'HUF', 'IDR', 
                 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 
                 'KHR', 'KRW', 'KWD', 'KZT', 'LAK', 'LBP', 'LKR', 'LTL', 'LVL', 
                 'MAD', 'MKD', 'MMK', 'MUR', 'MXN', 'MYR', 'NAD', 'NGN', 'NOK', 
                 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 
                 'QAR', 'RON', 'RSD', 'RUB', 'SAR', 'SCR', 'SEK', 'SGD', 'THB', 
                 'TJS', 'TND', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UYU', 'UZS', 
                 'VEF', 'VND', 'XAF', 'XCD', 'XOF', 'XPF', 'ZAR', 'ZMW']

CurrencySymbols = { '$' : 'USD',
                    '£' : 'GBP',
                    '€' : 'EUR',
                    '¥' : 'JPY' }



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
    if 'kg' in text:  # here we're checking if we need to convert from kg to lb and if the value is before or after kg
        for i in range (1,len(text)):
            if (text[i] == 'kg' or text[i] == 'kgs') and text[i-1].isdigit():
                toConvert.append(text[i-1])
    else:
        for i in range(len(text)):
            if 'kg' in text[i] or  'kgs' in text[i]:
                j = text[i].find('kg')
                if text[i][j].isdigit():
                    toConvert.append(text[i][j])
                    
    converted =  converttoLbs(toConvert,[])  #sends values to be converted to lbs
                                             #and gets a list of converted values
                       
    #Generate message
    if converted != []: #checks if any values have been converted
        for i in range(len(converted)):
            message+=("{0} kgs is {1} lbs \n\n".format(converted[i][0],converted[i][1]))    
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
    if 'lbs' in text or  'lb' in text:  # here we're checking if we need to convert from lb to kg and if the value is before or after lb
        for i in range (1,len(text)):
            if (text[i] == 'lbs' or text[i] == 'lbs') and text[i-1].isdigit():
                toConvert.append(text[i-1])       
    else:
        for i in range(len(text)):
            if 'lbs' in text[i] or  'lb' in text[i]:
                if text[i][:text[i].find('lb')].isdigit():
                    toConvert.append(text[i][:text[i].find('lb')])
                    
    converted = converttoKg(toConvert,[])
                       
    #Generate message
    if converted != []:
        for i in range(len(converted)):
            message+=("{0} lbs is {1} kg \n\n".format(converted[i][0],converted[i][1]))    
    return(message)

def CurrencyConversion(comment):
    def convertCurrency(toConvert, converted):
        if toConvert == []:
            return converted 
        else:
            _converted = []
            rate = toConvert[0][1] #rate is what we are converting from
            valueToConvert = float(toConvert[0][0])
            url = 'https://v3.exchangerate-api.com/bulk/68ed6db1a6575c73fdd3f383/{0}'.format(rate)
            response = requests.get(url)
            data = response.json()   # Json response gives values to facilitate currency exchange
            
            if rate != 'USD': #convert to usd
                exchange = data['rates']['USD']             
                _converted = [valueToConvert,rate,round(valueToConvert*exchange,2),'USD']
            else: #convert to Euros 
                exchange = data['rates']['EUR']
                _converted = [valueToConvert, rate,round(valueToConvert*exchange,2),'EUR']

            converted.append(_converted)
            return convertCurrency(toConvert[1:],converted)
        
    def getSymbol(currency): #determines which symbol to print based on currency rate
        return(next(key for key, value in CurrencySymbols.items() if value == currency))
       
        
    text = (comment.body).split()
    author = comment.author
    text =(comment.body).split()
    toConvert = []
    for i in range(len(text)):
        for key in CurrencySymbols:
            text[i] = text[i].replace(",","") # eliminates commas in large numbers
            
            if text[i]!="" and (text[i][-1] == '.' or ','):
                text[i] = text[i][-1]
            if key in text[i]:
                rateToConvertFrom = CurrencySymbols[key]
                conValA = text[i][text[i].find(key)+1:] # these values are needed to deal with $10 vs 10$
                conValB = text[i][:text[i].find(key)]

                if conValA.isdigit(): #check if amount is before or after currency symbol
                    if text[min(i+1,len(text)-1)] in CurrencyTypes:
                        rateToConvertFrom = text[min(i+1,len(text)-1)]    
                    toConvert.append([conValA,rateToConvertFrom])
                elif conValB.isdigit():
                    if text[min(i+1,len(text)-1)] in CurrencyTypes:
                        rateToConvertFrom = text[min(i+1,len(text)-1)]
                    toConvert.append([conValB,rateToConvertFrom])
                
   
    converted = convertCurrency(toConvert,[])
                     
    #Generate message
    message = ''
    if converted != []:
        for i in range(len(converted)):
            oldSymbol = getSymbol(converted[i][1]) # these lines get the currency symbol to be used in the message
            newSymbol =  getSymbol(converted[i][3])
            message+=("{0}{1} {2} is {3}{4} {5} \n\n".format(oldSymbol,converted[i][0],converted[i][1],newSymbol,converted[i][2],converted[i][3]))    
    return(message)

def bot_login():
    currencyBot =  praw.Reddit(user_agent='Converter Bot',
                               client_id='xI2pGK6CEylHzA',
                               client_secret='XuFjA6em6VsKPCuQrmn-kDaMQ3s',
                               username='convertoBot',
                               password='t0r7ez!')
    check.expect("check authentication",currencyBot.user.me(),"convertoBot") #checks if login in succesful
    return currencyBot


def run_bot(currencyBot):
    _replied = open('replies.txt','r+')
    replied = _replied.readlines()
    subreddit = currencyBot.subreddit('all') #the subreddit the bot browses and comments too
    comments = subreddit.comments(limit=None)#there will be no limit on the number of comments checked
    
    for comment in comments:
        author = comment.author
        if author != 'convertoBot' and not(comment.id +'\n' in replied): #prevents bot from replying to itself and replying twice
            message = ""
            message+=kgConversion(comment)
            message+=lbConversion(comment)
            message+=CurrencyConversion(comment)
            if message !="":
                print("replying to " + comment.body + "with ")
                print(message)
                print("--------------------")
                try:
                    #print(comment.id)
                    _replied.write(comment.id + '\n') # comment id is added to txt file containing any comments that have already been replied to
                    comment.reply(message) #send message
                    
                except praw.exceptions.APIException as e:  #the frequency the bot is allowed to reply is based on karma
                    e = str(e).split()                     #less karma means 
                    # sleeps for duration of wait seconds
                    print("ratelimit exceeded waiting {0} minutes".format(e[10]))
                    time.sleep(int(e[10])*60)                
                
    
    _replied.close()        
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
while True:     #login the bot and then run the bot
    run_bot(r)

        


