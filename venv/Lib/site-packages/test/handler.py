# coding: utf-8
from unittest import TestCase
from test_server import TestServer

from crawler import Crawler, Request


class HandlerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.reset()

    def test_handler_generator(self):

        server = self.server

        class SimpleCrawler(Crawler):
            points = list()

            def task_generator(self):
                yield Request('test', url=server.get_url(), meta={'id': 1})

            def handler_test(self, req, res):
                self.points.append(req.meta['id'])
                yield Request('test2', url=server.get_url(), meta={'id': 2})
                yield Request('test3', url=server.get_url(), meta={'id': 3})

            def handler_test2(self, req, res):
                self.points.append(req.meta['id'])
                yield Request('test3', url=server.get_url(), meta={'id': 3})

            def handler_test3(self, req, res):
                self.points.append(req.meta['id'])

        bot = SimpleCrawler()
        bot.run()
        self.assertEquals([1, 2, 3, 3], sorted(bot.points))

    def test_handler_simple_function(self):

        server = self.server

        class SimpleCrawler(Crawler):
            points = list()

            def task_generator(self):
                yield Request('test', url=server.get_url(), meta={'id': 1})

            def handler_test(self, req, res):
                self.points.append(req.meta['id'])

        bot = SimpleCrawler()
        bot.run()
        self.assertEquals([1], sorted(bot.points))
