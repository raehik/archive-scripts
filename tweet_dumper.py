#!/usr/bin/env python2
# encoding: utf-8
#
# Download all the tweets of a given Twitter user.
#
# By yanofsky, https://gist.github.com/yanofsky/5436496

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "zs4Ok2mUwJT3u4oyqZnQqf46t"
consumer_secret = "W5tacMrtLR2m6qOh6PgNipWiIERBVar83mexwSeVi5QTfAEjEp"
access_key = "2703511004-nffa7Ee2ftmJy5XxA05Qsj0DjRVEw5T1vcJf3Hl"
access_secret = "8dF199YjeHyUtXLffIT2Rit3VvKAi1YLO5MUxEFa8wOaK"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("raehik")
