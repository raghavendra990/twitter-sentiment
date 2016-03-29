from TwitterSearch import *
import datetime
import json
from pymongo import MongoClient
from textblob import TextBlob
#        replace mysql.server with "localhost" if you are running via your own server!
#                        server       MySQL username	MySQL pass  Database name.
# conn  =MySQLdb.connect(host='localhost',user = 'root',passwd='74332626',db = 'sentiment')

# c = conn.cursor()

def tstream(track , search_time=""):

	# c.execute("TRUNCATE TABLE data;")
	search_time = datetime.datetime.utcnow()
	try:
		tso = TwitterSearchOrder() # create a TwitterSearchOrder object
		tso.set_keywords(track) # let's define all words we would like to have a look for
		tso.set_language('en') # we want to see German tweets only
		tso.set_include_entities(False) # and don't give us all those entity information

	    # it's about time to create a TwitterSearch object with our secret tokens
		ts = TwitterSearch(
			consumer_key = "FOczd9TJM1MjvO53mNLjfNUl6",
			consumer_secret = "MIkYJ10mp6zeqP9Jn94jQxkho3aZI1jY4gF5srPxAgMRPx31jz" ,
			access_token = "2996993270-YP7iqsqvB8LdVB0nzCA4ZTocuIQ60VtjBgs0gOf",
			access_token_secret = "aKcWVVz3CkEtU7uufJs5HyBZpzEzZT3g2800VQ9vijJ40"
		)
		client = MongoClient()
		client = MongoClient('localhost', 27017)

		db = client.twitter_db
		tweets = db.tweets
		
	     # this is where the fun actually starts :)
		i = 0
		for all_data in ts.search_tweets_iterable(tso):

			if i < 100:
				tweet = all_data["text"]
				print tweet
				blob = TextBlob(tweet)
				
				senti =  blob.sentiment
				time = all_data["created_at"].encode("utf-8")
				
				username = all_data["user"]["screen_name"].encode('utf-8')
				geo = ""
				if all_data["geo"] == None:
					geo = ""
				else:
					geo = str(all_data["geo"]["coordinates"])
				# c.execute("INSERT INTO data (user,time,geo, tweet) VALUES (%s,%s,%s,%s)",
				# ( username,time,geo, tweet))

				# conn.commit()
				# print(username,time,geo,tweet)
				post = {
					"track":track,
					"search_time":search_time,
					"name":username,
					"tweet":tweet,
					"sentiment":sentiment
					"geo":geo,
					"time":time

				}


				i = i +1
			else:
				break

	except TwitterSearchException as e: # take care of all those ugly errors if there are some
		print(e)


tstream(["cricket"])