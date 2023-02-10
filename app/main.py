import flask,requests,json,subprocess,jinja2
import psycopg2
import facebook
import tweepy
import app.twitter as twitter
import app.fb as fb


app = flask.Blueprint("app",__name__,url_prefix='/')
app.secret_key = "hello"
facebookPageID = "100090402303764"
TwitterAuth = None
TwitterApi = None
graph = None
@app.route('/')
def home():
    return flask.render_template("/index.html",profile = "yo")

@app.route("/facebookSignIn")
def facebookSignIn():
    url = fb.fbLogin()
    return flask.redirect(url)

@app.route("/facebookcallback", methods=['GET'])
def facebookAfterSignin():
    global graph
    flask.session['fb_userid'],flask.session['fb_accessToken'] = fb.fb_tokens(flask.request.url)

    pageToken = fb.setupPage(flask.session['fb_userid'],flask.session['fb_accessToken'])

    #graph = facebook.GraphAPI(pageToken)
    
    return flask.redirect("/")
    
     
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


@app.route('/postInfo', methods=["POST"])
def postInfo():
    if(flask.request.method == "POST"):
        postContent = flask.request.form.get("body")
        TwitterApi.update_status(status=postContent)

        #graph.put_object(facebookPageID, "feed", message=postContent)
        

    return flask.jsonify({'success': True})




