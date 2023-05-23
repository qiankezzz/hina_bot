from crawler.error import RequestConfigurationError


__all__ = ('Request', 'SleepTask')


class Request(object):
    def __init__(self, tag=None, url=None, callback=None, meta=None,
                 timeout=10):
        self.url = url
        if tag is not None and callback is not None:
            raise RequestConfigurationError('Only one of tag and callback '
                                            'arguments should be specified')
        self.callback = callback
        self.tag = tag
        if meta is None:
            self.meta = {}
        else:
            self.meta = meta
        self.timeout = timeout


class SleepTask(object):
    def __init__(self, delay):
        assert isinstance(delay, (int, float))
        self.delay = delay
