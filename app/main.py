import flask,requests,json,subprocess,jinja2
import psycopg2
import tweepy
import facebook


eApp = flask.Blueprint("eApp",__name__,url_prefix='/')
eApp.secret_key = "hello"

twitter_auth_keys = {
        "consumer_key"        : "tRxNoZMhrpHsIwVOgsGDMbtUW",
        "consumer_secret"     : "PY2jAn1XdJirSOChFLqpd7liYAkq8JbEQpCc6xcB56Fjcv01Do",
        "access_token"        : "1421147694593048581-4we6TPNJL3bNXadk0EQMEqFQf7kv5Y",
        "access_token_secret" : "0vjBGHdoQL7iiAT8jEaZaYv7IC6rsTIaQZNULZz73qpUa"
    }


@eApp.route('/')
def home():
    return flask.render_template("/index.html",profile = "yo")

def twitterAuthenticate():
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)

    return api

def facebookAuthenticate(post):
    page_access_token = "EAAKZA6tGacmEBAL6ZBM5QX8CoRKzEMwjSf1oMtoi2JcTRRZCzUHaPzNb1YNkYW9v7LKHZAUsZBa8mK4DZC87mQs5pdJ40d8kqorfIFvDRIAZBnCRyWYvtJwfcvdpsXEnSj4n0B2qXp3Mi11XfeUZAxsosg3mYGRwoXt0nGp6096ElIpGKZAsvyD8w"
    graph = facebook.GraphAPI(page_access_token)

    
    #facebook_page_id = "fernando.depaz.10"
    graph.put_object("100002672706017", "feed", message=post)


@eApp.route('/postInfo', methods=["POST"])
def postInfo():
    if(flask.request.method == "POST"):
        postContent = flask.request.form.get("body")
        api = twitterAuthenticate()

        
##        media = api.media_upload("william_gibson.jpg")
## 
##        # Post tweet with image
##        tweet = "Great scifi author or greatest scifi author? #williamgibson"
        post_result = api.update_status(status=postContent)#, media_ids=[media.media_id])
        facebookAuthenticate(postContent)
##        
##        
##        bucket = flask.request.form.get("bucket")
##        action = flask.request.form.get("action")
    return flask.jsonify({'success': True})




@eApp.route('/orderupdate', methods=["POST"])
def getOrder():
    return flask.render_template("/index.html")


@eApp.route('/getMembershipsTable')
def getMembershipsTable():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode='require')
    cur = conn.cursor()
    conn.close()
    return flask.render_template("/index.html")





@eApp.route('/<studentURLHandle>')
def fetchStudent(studentURLHandle):
    return flask.render_template("/index.html")


