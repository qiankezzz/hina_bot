# coding: utf-8
from unittest import TestCase

from crawler import Response


class ResponseTestCase(TestCase):
    def test_absolute_url(self):
        res = Response(body='', url='http://example.com')
        self.assertEquals('http://example.com', res.absolute_url(''))
        self.assertEquals('http://example.com/', res.absolute_url('/'))
        self.assertEquals('http://example.com', res.absolute_url())
        self.assertEquals('http://example.com/foo', res.absolute_url('/foo'))
        self.assertEquals('http://example.com/foo?1=2',
                          res.absolute_url('/foo?1=2'))
        self.assertEquals('http://domain.com/foo',
                          res.absolute_url('http://domain.com/foo'))
