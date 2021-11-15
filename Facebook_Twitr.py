# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 09:42:17 2021

@author: Ng Yixiang
"""
dir_name = 'C:/Users/Ng Yixiang/Desktop/Projects/[MinLaw]/Scraping FB Twitr data/'

#%% facebook-sdk api ###
import facebook
token = 'EAAOxgKgOKJQBAGDAxtqgX6ZCIssKesT8x589jR2HBdnOgbbbRPQtQM0MATH53lrSUrHR1RhM70WAyuEK4G25WBb2ZACcjZA7bDdiT79iMH721iY4dKduv39OGV0n3JpgPLvA2YRDTqhZAq4jjeI2ZCy6V5sZCZBJt0mXdAjV5tUiKZBrZAFvnZB8FF5am9dHi2F40ZD'
graph = facebook.GraphAPI(access_token=token)
events = graph.request('/search?q=Poetry&type=event&limit=10000')

#%% facebook_scraper: Get posts from a page ###
from facebook_scraper import get_posts
import pandas as pd

#scrape FB, can search 'group' or 'page'
cookies_file = dir_name + 'cookies.txt'
post_df_full = pd.DataFrame()
for post in get_posts(group='sgopposition',cookies=cookies_file,extra_info=True,pages=10,options={"comments":False}):
    post_entry = post
    fb_post_df = pd.DataFrame.from_dict(post_entry,orient='index')
    fb_post_df = fb_post_df.transpose()
    post_df_full = post_df_full.append(fb_post_df)
    print (post['post_id']+'get')

post_df_full.columns
post_df_full.info()
post_df_full.to_csv(dir_name + 'FB_Sample_SGOpposition.csv',index=False)

#read csv and converting reactions JSON to columns
post_df_full = pd.read_csv(dir_name + 'FB_Sample_SGOpposition.csv')
post_df_full['reactions'] = post_df_full['reactions'].apply(lambda x: dict(eval(x)))
post_df_full_reactions = post_df_full['reactions'].apply(pd.Series)
df_final = pd.concat([post_df_full,post_df_full_reactions],axis=1).drop('reactions',axis=1)

#%% Tweepy ####
# Bearer token: AAAAAAAAAAAAAAAAAAAAACIxVwEAAAAAd4Jq1%2FMcYljM29aBp5%2FPf4tNsJc%3DL7duOYaVFQKYkstYhnLZEnXPqeLYO82rflMCwUY9I9C7ZDuomJ

import tweepy
import pandas as pd

access_token = '1458722337663041540-LZHCbQoVehu0AOlT8ajFSPnYggml8A'
access_token_secret = 'jH851pgxcof5N6BoKHSH8ZQTm1fHiMZvs1fKRAhprfnyJ'
consumer_key = 'Cwy65x0Yu2Vwq6WCA8V3ReO5D'
consumer_secret = 'BfV3iW7tWKCOK8ZWSjqcOr1pjOBiuwkLBrTjO8Q0YrGUjT5i04'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


"""if you don't add since= as one of the parameters, Twitter will sample the last 7 days worth of data depending
on how many total tweets there are with the specific hashtag, keyword, or key phrase that you are looking for. You can
manually add in the number of items (or tweets) you want to get back in the items() section."""

"""Don't forget that these are just a few of the fields that you can pull from the REST API. There are many more fields, such as
mentions and hashtags which you can get directly from the API. Alternatively you can pull these out using various Regex commands in Pandas"""

tweets = []
count = 1

#There is a 7 day search limit. No tweets will be found for a date older than one week.
for tweet in tweepy.Cursor(api.search_tweets, q="#singapore since:2021-11-10 until:2021-11-12", count=450).items(50000):
	
	print(count)
	count += 1

	try: 
		data = [tweet.created_at, tweet.id, tweet.text, tweet.user._json['screen_name'], tweet.user._json['name'], tweet.user._json['created_at'], tweet.entities['urls'], tweet.retweet_count, tweet.favorite_count, tweet.geo, tweet.place]
		data = tuple(data)
		tweets.append(data)

	except tweepy.TweepError as e:
		print(e.reason)
		continue

	except StopIteration:
		break

df = pd.DataFrame(tweets, columns = ['created_at','tweet_id', 'tweet_text', 'screen_name', 'name', 'account_creation_date', 'urls','No_retweets','No_favourites','Geo','Place'])

df.to_csv(dir_name + 'SampleTweets.csv', index=False) 









