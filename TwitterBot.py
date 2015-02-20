#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, ConfigParser, json, tweepy
import DocToPDF as Docs
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

config = ConfigParser.ConfigParser()
config.read('.twitter.sample')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
account_screen_name = config.get('app','account_screen_name')
account_user_id = config.get('app','account_user_id')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)

class ReplyToTweet(StreamListener):
	def on_data(self,data):
		#process stream data here
		print data
		tweet = json.loads(data.strip())

		retweeted = tweet.get('retweeted')
		from_self = tweet.get('user',{}).get('id_str','') == account_user_id

		if retweeted is not None and not retweeted and not from_self:

			tweetId = tweet.get('id_str')
			screenName = tweet.get('user',{}).get('screen_name')
			tweetText = tweet.get('text')

			chatResponse = Docs.transformation(tweetText.split('@PDFbot ')[-1])

			replyText = '@' + screenName + ' ' + chatResponse

			if len(replyText) > 140:
				replyText = replyText[0:137] + '...'

			print('Tweet ID: ' + tweetId)
			print('From: ' + screenName)
			print('Tweet Text: ' + tweetText.split('@PDFbot ')[-1])
			print('Reply Text: ' + replyText)

			twitterApi.update_status(status=replyText)

	def on_error(self,status):
		print status




if __name__ == '__main__':
	StreamListener = ReplyToTweet()
	twitterStream = Stream(auth, StreamListener)
	twitterStream.userstream(_with='user')