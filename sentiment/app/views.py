from django.shortcuts import render

# Create your views here.
from django.conf import settings 
from django.http import HttpResponse
import time as tm
from TwitterSearch import *
import datetime
import json
from pymongo import MongoClient
from textblob import TextBlob
from textblob import Word
search_time = ""
track = []	
import numpy
import re
from collections import Counter
import pandas as pd


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.twitter_db
tweets = db.tweets

def tstream(track, tweets = tweets):

	# c.execute("TRUNCATE TABLE data;")
	search_time = str(datetime.datetime.utcnow())
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
		
	    # this is where the fun actually starts :)
		i = 0
		for all_data in ts.search_tweets_iterable(tso):

			if i < 300:	
				tweet = all_data["text"]
				time = tm.strftime('%Y-%m-%d %H:%M:%S', tm.strptime(all_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
				
				blob = TextBlob(tweet)
				
				senti =  blob.sentiment

				username = all_data["user"]["screen_name"].encode('utf-8')
				geo = ""
				if all_data["geo"] == None:
					geo = ""
				else:
					geo = str(all_data["geo"]["coordinates"])
				# c.execute("INSERT INTO data (user,time,geo, tweet) VALUES (%s,%s,%s,%s)",
				# ( username,time,geo, tweet))

				# conn.commit()
				#print(username,time,geo,tweet)
				post = {
					"track":track,
					"search_time":search_time,
					"name":username,
					"polarity": senti.polarity,
					"subjectivity": senti.subjectivity,
					"tweet":str(tweet.encode('utf-8')),
					"geo":geo,
					"time":time

				}

				#print post
				tweets.insert_many([post])
				i = i +1
			else:
				break
		#print tweets.find_one({"track":track})

		return search_time
	except TwitterSearchException as e: # take care of all those ugly errors if there are some
		print(e)
	


def index(request, search_time_=search_time, tweets = tweets , track=track):
	
	track_ = ""

	if request.method == 'POST':

		if request.POST.get("search_box") is not None :
			track_ = request.POST.get("search_box")
			client = MongoClient()
			client = MongoClient('localhost', 27017)

			db = client.twitter_db
			tweets = db.tweets

			track_ = str(request.POST.get("search_box")).split(" ")
			print track_
			search_time = tstream(track_)
			# global track
			# global search_time
			track  = " ".join(track_)
			

			a = list(tweets.find({"search_time":search_time ,"track":track},{"time":1,"tweet":1 ,"polarity":1,"subjectivity":1,"_id":0}))
			
			# data = [{ "key":"series",
			# 		"values":[]

			# }
			# ]


			# length = len(a)
			# for i in range(length):
			# 	time_ = datetime.datetime.strptime(a[i]["time"], "%Y-%m-%d %H:%M:%S")
			# 	time_ = tm.mktime(time_.timetuple())
			# 	c = [time_ , a[i]['polarity']]
			# 	data[0]["values"].append(c)

			# data = [ ['Task', 'Hours per Day']]

			# length_a = len(a)
			# positive  = 0
			# negative = 0

			# neutral = 0


			# for i in range(length_a):
			# 	if a[i]["polarity"] >0:
			# 		positive += 1
			# 	elif a[i]["polarity"] == 0:
			# 		neutral += 1
			# 	else: 
			# 		negative += 1

			# data.append(["positive",positive])
			# data.append(["negative",negative])
			# data.append(["neutral",neutral])


			# search_time = "2016-01-19 07:11:49.584101"	
			# track = "india"

			# dist = numpy.unique(word_pos)
			

			# dist_count = []
			# for c in dist:
			# 	temp = {"text":"","size":0}
			# 	count = 
			context = { "scatter":json.dumps(a) , "search_time":search_time , "track":track}
			return render(request, 'app/scatter.html', context )

		elif request.POST.get("name") == "scatter":
			search_time  = str(request.POST.get("search_time"))
			track = request.POST.get("track")
			a = list(tweets.find({"search_time":search_time ,"track":track },{"polarity":1,"subjectivity":1 ,"_id":0}))
			context = {"scatter": json.dumps(a) , "search_time": search_time , "track":track}
			return render(request, 'app/scatter.html' , context )

		elif request.POST.get("name") == "donat":
			search_time  = str(request.POST.get("search_time"))
			track = request.POST.get("track")
			a = list(tweets.find({"search_time":search_time ,"track":track },{"polarity":1 ,"_id":0}))

			data = [ ['Task', 'Hours per Day']]

			length_a = len(a)
			positive  = 0
			negative = 0

			neutral = 0


			for i in range(length_a):
				if a[i]["polarity"] >0:
					positive += 1
				elif a[i]["polarity"] == 0:
					neutral += 1
				else: 
					negative += 1

			data.append(["positive",positive])
			data.append(["negative",negative])
			data.append(["neutral",neutral])


			context = {"donat": json.dumps(data) , "search_time": search_time , "track":track}
			return render(request, 'app/donat.html' , context )

		elif request.POST.get("name") == "table":
			search_time  = str(request.POST.get("search_time"))
			track = request.POST.get("track")
			pd.set_option('display.max_colwidth', -1)
			a = pd.DataFrame(list(tweets.find({"search_time":search_time ,"track":track },{"_id":0,"name":1,"polarity":1,"subjectivity":1,"tweet":1,"time":1  })))
			print list(tweets.find({"search_time":search_time ,"track":track },{"_id":0,"name":1,"polarity":1,"subjectivity":1,"tweet":1,"time":1  }))
			context = {"table": a.to_html(index= False).replace('class="dataframe"','id="example1" class="table table-striped table-bordered"') , "search_time": search_time , "track":track}
			return render(request, 'app/table.html' , context )

	
	return render(request, 'app/index.html', context = {})






# client = MongoClient()
# client = MongoClient('localhost', 27017)

# db = client.twitter_db
# tweets = db.tweets



#2016-01-19 07:11:49.584101
# 2016-01-18 14:27:52.500655





