import json
from collections import defaultdict
from twimg.twi_api_auth import TwiApiAuth
from urllib import request


class GetTwJson(object):
    """Get Tweet ID from Query."""
    def __init__(self, query, auth):
        self.q = query
        self.auth = auth
        self.json_for = defaultdict(list)

        self.success = []
        self.fail = []

    def from_query(self):
        """Classify Query."""
        if ".com" in self.q or "t.co" in self.q:
            # a permanent link
            self._from_permanent(self.q)
        elif "/" in self.q:
            # list of files
            with open(self.q, 'r') as q:
                links = q.readlines()
            for link in links:
                self._from_permanent(link.strip())
        else:
            # keyword
            self._from_keyword(count=20)

    def _from_keyword(self, count):
        _url = 'https://api.twitter.com/1.1/search/tweets.json'
        try:
            _api = TwiApiAuth(self.auth)
            _r = _api.get_response(_url, params={'q': self.q, 'count': count, 'include_entities': 'true'})
            _r_text = json.loads(_r.text)
            for tweet in _r_text['statuses']:
                self.json_for[self.q].append(tweet)
            self.success.append(self.q)
        except:
            self.fail.append(self.q)

    def _from_permanent(self, plink):
        _url = 'https://api.twitter.com/1.1/statuses/show.json'

        if "//t.co/" in plink:
            plink = request.urlopen(plink).geturl()
        tid = plink.split(r'/status/')[-1].split(r'/photo/')[0]
        try:
            _api = TwiApiAuth(self.auth)
            _r = _api.get_response(_url, params={'id': tid, 'include_entities': 'true'})
            self.json_for[plink].append(_r.json())
            self.success.append(plink)
        except:
            self.fail.append(plink)
