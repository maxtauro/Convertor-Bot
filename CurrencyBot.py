## reddit bot currency convert

import praw
import check
import time

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
        text = comment.body
        author = comment.author
        if 'fox' in text:
            
            #Generate message
            message = "Congrats Max ur siccc"
            ##comment.reply(message) #send message
            print("replied to {0} in {1}".format(comment.author,comment.submission.title))  
            
    # sleeps for 10 seconds
    print("sleep 10 seconds")
    time.sleep(10)
    


r = bot_login()
while True:
    run_bot(r)







