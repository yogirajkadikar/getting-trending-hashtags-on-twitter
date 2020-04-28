import twitter, json
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter


ACCESS_TOKEN = "1254297025845137408-XcNl4aA5NKRbJyisYNzLkLLh9UhSQf"
ACCESS_TOKEN_SECRET = "7YK2hRFDmHQIqxM8Ra53vWpvqHS2dIEW8ki6E0ccgUNth"
CONSUMER_KEY = "Y9Rc4DVewa7XcD2kxJfq4SsBR"
CONSUMER_SECRET = "yYjv6GaX2kKqwe9zRjKeMgCKXgIOVIvLtnPZMFLkm7oCa0eud3"

auth=twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api =twitter.Twitter(auth=auth)
#print(twitter_api)

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE-URI']='postgresql://postgres:yogikadikar@localhost/trending_hastags'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        desired_WOEid = request.form['tag']
        _trends= twitter_api.trends.place(_id = desired_WOEid)
        _trends_set = set([trend['name'] 
                        for trend in _trends[0]['trends']])
        return render_template("index.html", _trends_set= _trends_set)
    return render_template("index.html", )

@app.route('/frequency', methods = ['GET','POST'])
def frequncy(): #counting how frequntly was hashtag used
    if request.method == 'POST':
        q = request.form['hashtag']
        count = 100
        search_results = twitter_api.search.tweets(q=q, count=count)
        statuses = search_results['statuses']
        for _ in range(5):
            #print ("Length of statuses", len(statuses))
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError: # No more results when next_results doesn't exist
                break
        
    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
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



if __name__ == "__main__":
    app.debug = True
    app.run()