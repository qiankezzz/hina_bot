from urllib.parse import urljoin


__all__ = ('Response',)


class Response(object):
    def __init__(self, body, url):
        self.body = body
        self.url = url

    def absolute_url(self, url=None):
        if url is None:
            return self.url
        else:
            return urljoin(self.url, url)
