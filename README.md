# getting-trending-hashtags-on-twitter

A web app to do some data mining from twitter using flask

# Usage

It is used for getting location specific trending hashtags, counting their occurence 
and displaying top 10 tweets that used the hashtag.

Yahoo's WhereOnEarth id is used for getting location.
http://developer.yahoo.com/geo/geoplanet/




#development 
1. Twitter's developer key and tokens are required for mining the data on twitter.
    http://dev.twitter.com/apps/new
    
    See https://dev.twitter.com/docs/auth/oauth for more information 
    on Twitter's OAuth implementation.


2. Need to install flask:
   $ pip install flask
   
3. Need to install sql alchecmy: 
   $ pip install FlaskSQLAlchemy
  
4. Need to install twitter module:
   $ pip install twitter
   
5. Create a virtual environment:
   $ python3 -m venv virtual
   
6.  Run the code app.py in venv
