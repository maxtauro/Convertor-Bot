## reddit bot currency convert

import praw

currencyBot =  praw.Reddit(user_agent='CurrencyBot v0.1',
                           client_id='POmsiu3RKBxEKg',
                           client_secret='0QEu3wMvD95ygr5plnx3RrH28fo',
                           username='ConvertCurrencyBot',
                           password='t0r7ez!')
print(currencyBot.user.me())
subreddit = currencyBot.subreddit('bottesting')
##subreddit = currencyBot.subreddit('all')
comments = subreddit.stream.comments()


for comment in comments:
    text = comment.body
    author = comment.author
    if '!ConversionTestMax' in text:
        print("got one")
        #Generate message
        message = "Congrats Max ur siccc"
        comment.reply(message) #send message
        print("replied to {0}".format(comment.author))
