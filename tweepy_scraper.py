# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:43:26 2020

@author: nites
"""

# Import libraries
from tweepy import OAuthHandler
import tweepy
import csv
import pandas as pd
import time

# Twitter credentials
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''

# Pass your twitter credentials to tweepy via its OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

def scrapedtweets(query,date_since,max_tweets,numRuns):
    db_tweets = pd.DataFrame(columns = ['username', 'acctdesc', 'is_verified', 'location', 'following', 'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts', 'retweetcount', 'listed_count', 'favourites_count', 'text', 'is_retweet', 'hashtags','profile_image','default_profile_image'])
    #db_tweets = pd.DataFrame()
    
    for i in range(numRuns):
        searched_tweets = []
        last_id = -1
        while len(searched_tweets) < max_tweets:
            count = max_tweets - len(searched_tweets)
            try:
                new_tweets = api.search(q=query, tweet_mode='extended', include_rts = True, since=date_since, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break
                searched_tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # depending on TweepError.code, one may want to retry or wait
                # to keep things simple, we will give up on an error
                break
        
        noTweets=0
        for tweet in searched_tweets:
            username = tweet.user.screen_name
            username = username.replace('\n',' ')
            username = username.replace('\r',' ')
            acctdesc = tweet.user.description
            acctdesc = acctdesc.replace('\n',' ')
            acctdesc = acctdesc.replace('\r',' ')
            verified = tweet.user.verified
            if verified:
                is_verified = 1
            else:
                is_verified = 0
            loc = tweet.user.location
            loc=loc.replace('\n',' ')
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            usercreatedts = tweet.user.created_at
            tweetcreatedts = tweet.created_at
            retweetcount = tweet.retweet_count
            listed_count = tweet.user.listed_count
            favourites_count = tweet.user.favourites_count
            hashtags = tweet.entities['hashtags']
            lst=[]
            for h in hashtags:
                hsh = h['text']
                hsh = hsh.replace('\n',' ')
                hsh = hsh.replace('\r',' ')
                lst.append(hsh)
            is_retweet = 0
            try:
                text = tweet.retweeted_status.full_text
                is_retweet = 1
            except AttributeError:  # Not a Retweet
                text = tweet.full_text
            text = text.replace('\n',' ')
            image = tweet.user.profile_image_url_https
            image = image.replace('_normal','')
            profile_image = tweet.user.default_profile_image
            if profile_image:
                default_profile_image = 1
            else:
                default_profile_image = 0
                    
            itweet = [username,acctdesc,is_verified,loc,following,followers,totaltweets,usercreatedts,tweetcreatedts,retweetcount,listed_count,favourites_count,text,is_retweet,lst,image,default_profile_image]
            db_tweets.loc[len(db_tweets)] = itweet
            noTweets+=1
            print(noTweets,itweet)
        
        print('no. of tweets scraped for run {} is {}'.format(i + 1, noTweets))
        #if i+1 != numRuns:
            #time.sleep(920)
            
        filename = "tweets.csv"
        # Store dataframe in csv with creation date timestamp
        db_tweets.to_csv(filename, mode='a', index = False)
    
# Hashtags for scraping data from twitter    
#CongressForIndia OR #ArrestArnab
#HumModiKeSathHain OR #WhyBJPhatesDelhi
#NarendraModi OR #NaMo OR #BJPIndia OR #bjpindia OR #AmitShah OR #ArvindKejriwal OR #BJP
#IndianPolitics OR #IForIndia OR #ISupportSudhirChoudhary
#RiyazNaikoo OR #CleanKashmir
#WeStandWithSambitPatra OR #ArrestSambitPatra OR OR #PMCareFraud

program_start = time.time()
query = ['#RiyazNaikoo OR #CleanKashmir','#Aurangabad','#CongressForIndia OR #ArrestArnab','#NarendraModi OR #NaMo OR #BJPIndia OR #bjpindia OR #AmitShah OR #ArvindKejriwal OR #BJP','#HumModiKeSathHain OR #WhyBJPhatesDelhi','#IndianPolitics OR #IForIndia','#RahulFightsForIndia OR #UddhavMustAnswers','#isupportSudhirchaudhary OR #ISupportSudhirChoudhary','#IndiaWithZee OR #IndiaIsNotWithZeeNews']
for q in query:
    max_tweets = 2500
    date_since = "2020-05-02"
    #date_until = "2020-05-02"
    numRuns = 10
    program_start = time.time()
    scrapedtweets(q,date_since,max_tweets,numRuns)
program_end = time.time()
print('Scraping has completed!')
print('Total time taken to scrap is {} minutes.'.format(round(program_end - program_start)/60, 2))
