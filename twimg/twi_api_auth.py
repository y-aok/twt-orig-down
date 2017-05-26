import datetime
import time
from requests_oauthlib import OAuth1Session


class TwiApiAuth(object):
    def __init__(self, auth):
        self._ck, self._cs, self._at, self._as = auth
        try:
            self._session = OAuth1Session(self._ck, self._cs, self._at, self._as)
        except:
            raise

    def _header(self, res):
        self.access_allowed = res.headers['X-Rate-Limit-Remaining']  # アクセス可能回数
        self.reset_time = res.headers['X-Rate-Limit-Reset']  # リセット時間
        self.reset_sec = int(res.headers['X-Rate-Limit-Reset']) - \
                         time.mktime(datetime.datetime.now().timetuple())  # リセット時間 (残り秒数に換算)

    def get_response(self, url, params):
        res = self._session.get(url, params=params)
        # self._header(res)

        if res.status_code != 200:
            raise Exception('Twitter API Error: {}'.format(res.status_code))
        else:
            return res
