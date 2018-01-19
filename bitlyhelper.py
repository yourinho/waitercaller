# We'll use this lib to correctly encode URL parameters.
import urllib
# We'll use this lib to download the data from the web.
import urllib.request as urllib2
#import urllib2
import json

TOKEN = "6011aedca04af2e406a8189b32efedbca230a207"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = urllib2.urlopen(url).read()
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            print (e)
