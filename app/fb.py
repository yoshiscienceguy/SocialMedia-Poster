from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix# Credentials you get from registering a new application
import requests
client_id = '2168819056633750'
client_secret = '839156d3079c82e75630176d7551b206'
authorization_base_url = 'https://www.facebook.com/dialog/oauth'
token_url = 'https://graph.facebook.com/oauth/access_token'
redirect_uri = 'https://localhost:8040/facebookcallback'     # Should match Site URL
facebook = None

def fbLogin():
    # OAuth endpoints given in the Facebook API documentation
    global facebook
    facebook = OAuth2Session(client_id, redirect_uri=redirect_uri)
    facebook = facebook_compliance_fix(facebook)

    # Redirect user to Facebook for authorization
    authorization_url, state = facebook.authorization_url(authorization_base_url)

    return authorization_url

def fb_tokens(redirect_response):

    # Fetch the access token
    response = facebook.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)
   
    # Fetch a protected resource, i.e. user profile
    r = facebook.get('https://graph.facebook.com/me?')
 
    return (r.json()["id"],response["access_token"])

def setupPage(uID,accessToken):
    url = "https://graph.facebook.com/"+uID+"/accounts?fields=name,access_token&access_token="+accessToken
    response = facebook.get(url)
    print(response.json())
    return response.json()
   
