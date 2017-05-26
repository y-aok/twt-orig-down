class GetImg(object):
    def __init__(self):
        self.imgs = []

    def from_json(self, _json):
        try:
            imgs = []
            ms = _json['extended_entities']['media']
            for m in ms:
                l = m['media_url']
                l = l + ":orig"
                imgs.append(l)
                self.imgs += imgs
            return imgs
        except:
            raise Exception('failed to find media_link')
