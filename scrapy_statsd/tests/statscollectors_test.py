from twisted.trial import unittest
import mock
from scrapy.settings import Settings

from scrapy_statsd.statscollectors import StatsDStatsCollector

class StatsDStatsCollectorTest(unittest.TestCase):
    """
    To run these tests it's better to use Twisted Trial runner.
    http://twistedmatrix.com/trac/wiki/TwistedTrial

    Also, to verify the stats are actually being sent to the server a Statsd
    server must be running. Otherwise, the UDP packets go into thin air.
    """
    def __init__(self, *args, **kwargs):
        super(StatsDStatsCollectorTest, self).__init__(*args, **kwargs)
        self._crawler_mock = mock.MagicMock()
        self._crawler_mock.settings = Settings({'STATS_DUMP': True})

        self._spider_mock = mock.MagicMock()
        self._spider_mock.name = 'test_spider'

    def setUp(self):
        self._statsd_collector = StatsDStatsCollector(self._crawler_mock)

    def tearDown(self):
        self._statsd_collector = None

    def test_set_value(self):
        return self._statsd_collector.set_value(
              'meow/meow',
              1,
              self._spider_mock)

    def test_set_value_non_numeric(self):
        key = 'this/wont/go'
        value = 'not_numeric'
        self._statsd_collector.set_value(key, value, self._spider_mock)
        self.assertEqual(self._statsd_collector.get_value(key), value)

    def test_inc_value(self):
        return self._statsd_collector.inc_value(
            'test/inc/me',
            1,
            self._spider_mock)

    def test_max_value(self):
        key = 'this/is/a/max/value'

        first_value = 1
        self._statsd_collector.max_value(key, first_value, self._spider_mock)
        self.assertEqual(
            self._statsd_collector.get_value(key),
            first_value)

        second_value = 2
        deferred = self._statsd_collector.max_value(
              key,
              second_value,
              self._spider_mock)
        self.assertEqual(
            self._statsd_collector.get_value(key),
            second_value)

        third_value = 0
        self._statsd_collector.max_value(key, third_value, self._spider_mock)
        self.assertEqual(
            self._statsd_collector.get_value(key),
            second_value)

        return deferred

    def test_min_value(self):
        key = 'this/is/a/min/value'

        first_value = 3
        self._statsd_collector.min_value(key, first_value, self._spider_mock)
        self.assertEqual(
            self._statsd_collector.get_value(key),
            first_value)

        second_value = 2
        deferred = self._statsd_collector.min_value(
              key,
              second_value,
              self._spider_mock)
        self.assertEqual(
            self._statsd_collector.get_value(key),
            second_value)

        third_value = 4
        self._statsd_collector.min_value(key, third_value, self._spider_mock)
        self.assertEqual(
            self._statsd_collector.get_value(key),
            second_value)

        return deferred


