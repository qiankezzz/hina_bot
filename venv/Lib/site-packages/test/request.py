# coding: utf-8
from unittest import TestCase
from test_server import TestServer

from crawler import Crawler, Request
from crawler.error import RequestConfigurationError


class RequestTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = TestServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.server.reset()

    def test_constructor_arguments(self):
        req = Request()
        self.assertEqual(req.tag, None)
        self.assertEqual(req.url, None)
        self.assertEqual(req.callback, None)

        req = Request('TAG')
        self.assertEqual(req.tag, 'TAG')
        self.assertEqual(req.url, None)

        req = Request('TAG', 'URL')
        self.assertEqual(req.tag, 'TAG')
        self.assertEqual(req.url, 'URL')

        req = Request(url='URL', tag='TAG')
        self.assertEqual(req.tag, 'TAG')
        self.assertEqual(req.url, 'URL')

    def test_constructor_meta_argument(self):
        req = Request()
        self.assertEqual(req.meta, {})
        req = Request(meta=1)
        self.assertEqual(req.meta, 1)
        req = Request(meta={'place': 'hell'})
        self.assertEqual(req.meta, {'place': 'hell'})

    def test_callback_argument(self):

        server = self.server

        class SimpleCrawler(Crawler):
            def prepare(self):
                self.points = []

            def task_generator(self):
                yield Request(url=server.get_url(), callback=self.handler_test)

            def handler_test(self, req, res):
                self.points.append(1)

        bot = SimpleCrawler()
        bot.run()
        self.assertEqual(bot.points, [1])

    def test_callback_and_tag_arguments_conflict(self):

        server = self.server

        class SimpleCrawler(Crawler):
            def task_generator(self):
                yield Request('test', url=server.get_url(),
                              callback=self.handler_test)

            def handler_test(self, req, res):
                pass

        bot = SimpleCrawler()
        self.assertRaises(RequestConfigurationError, bot.run)
