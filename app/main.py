import flask,requests,json,subprocess,jinja2
import psycopg2
import facebook
import tweepy
import app.twitter as twitter


app = flask.Blueprint("app",__name__,url_prefix='/')
app.secret_key = "hello"

TwitterAuth = None

TwitterApi = None

@app.route('/')
def home():
    return flask.render_template("/index.html",profile = "yo")


@app.route("/twitterSignIn")
def twitterSignIn():
    resource = twitter.twitter_get_oauth_request_token()
    flask.session['ro_key'] = resource[0]
    flask.session['ro_secret'] = resource[1]
    return flask.redirect(twitter.getURL(resource[0]))

@app.route("/callback", methods=['GET'])
def twitterAfterSignIn():
    global TwitterAuth, TwitterApi
    oauth_token = flask.request.args.get('oauth_token')
    oauth_verifier = flask.request.args.get('oauth_verifier')
    flask.session['oauth_token'] = oauth_token
    flask.session['oauth_verifier'] = oauth_verifier

    access_token_list = twitter.twitter_get_oauth_token(flask.session["ro_key"],flask.session["ro_secret"],flask.session["oauth_verifier"])
    accessTokens = twitter.twitter_get_access_token(access_token_list)

    
    TwitterAuth = tweepy.OAuth1UserHandler(accessTokens[0],
                                           accessTokens[1],
                                           accessTokens[2],
                                           accessTokens[3]
                                           )
    TwitterApi = tweepy.API(TwitterAuth)
    
    
    return flask.redirect("/")

    



def facebookAuthenticate(post):
    page_access_token = "EAAKZA6tGacmEBAL6ZBM5QX8CoRKzEMwjSf1oMtoi2JcTRRZCzUHaPzNb1YNkYW9v7LKHZAUsZBa8mK4DZC87mQs5pdJ40d8kqorfIFvDRIAZBnCRyWYvtJwfcvdpsXEnSj4n0B2qXp3Mi11XfeUZAxsosg3mYGRwoXt0nGp6096ElIpGKZAsvyD8w"
    graph = facebook.GraphAPI(page_access_token)

    
    #facebook_page_id = "fernando.depaz.10"
    graph.put_object("100002672706017", "feed", message=post)


@app.route('/postInfo', methods=["POST"])
def postInfo():
    if(flask.request.method == "POST"):
        postContent = flask.request.form.get("body")
        TwitterApi.update_status(status=postContent)
        

    return flask.jsonify({'success': True})




