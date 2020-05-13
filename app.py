import twitter, json
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter

#Please enter your credentials from twitter developer site
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

auth=twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api =twitter.Twitter(auth=auth)

#initializing flask
app=Flask(__name__)

#main webpage of app
@app.route("/")
def index():
    return render_template("index.html")

#function to add a WOEid
@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        desired_WOEid = request.form['tag']
        _trends= twitter_api.trends.place(_id = desired_WOEid)
        _trends_set = set([trend['name'] 
                        for trend in _trends[0]['trends']])
        return render_template("index.html", _trends_set= _trends_set)
    return render_template("index.html", )

#counting how frequntly was hashtag used
@app.route('/frequency', methods = ['GET','POST'])
def frequncy(): 
    if request.method == 'POST':
        q = request.form['hashtag']
        count = 100
        search_results = twitter_api.search.tweets(q=q, count=count)
        statuses = search_results['statuses']
        for _ in range(5):
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError: # No more results when next_results doesn't exist
                break

        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
    
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
        hashtags = [ hashtag['text'] 
            for status in statuses
                for hashtag in status['entities']['hashtags'] ]

        for item in [hashtags]:
            c = Counter(item)
        frequent = c.most_common()[:1]
        return render_template("index.html", frequent = frequent )
    return render_template("index.html", )

#Function to get top 10 tweets for a particular hashtag
@app.route('/query', methods = ['GET','POST'])
def query():
    if request.method == 'POST':
        q = request.form['hashtag_n']
        def twitter_search(twitter_api, q, max_results=200, **kw):
            search_results = twitter_api.search.tweets(q=q, count=100, **kw)
        
            statuses = search_results['statuses']
            max_results = min(1000, max_results)
        
            for _ in range(10): # 10*100 = 1000
                try:
                    next_results = search_results['search_metadata']['next_results']
                except KeyError: # No more results when next_results doesn't exist
                    break

                kwargs = dict([ kv.split('=') 
                                for kv in next_results[1:].split("&") ])
                
                search_results = twitter_api.search.tweets(**kwargs)
                statuses += search_results['statuses']
                
                if len(statuses) > max_results: 
                    break
                    
            return statuses
        def find_popular_tweets(twitter_api, statuses, retweet_threshold=3):
            return [ status
                for status in statuses 
                    if status['retweet_count'] > retweet_threshold ] 

        search_results = twitter_search(twitter_api, q, max_results=200)
        popular_tweets = find_popular_tweets(twitter_api, search_results)
        a=0
        tweet=None
        twit=[]
        for tweet in popular_tweets:
            if a<10:
                a=a+1
                twit.append(tweet['text'])
        return render_template("index.html",  twit= twit )
    return render_template("index.html", )


if __name__ == "__main__":
    app.debug = True
    app.run()