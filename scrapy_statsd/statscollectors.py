from twisted.internet.threads import deferToThread
import scrapy.statscollectors
import statsd

class StatsDStatsCollector(scrapy.statscollectors.MemoryStatsCollector):
    """
    Send all the stats to the statsd server in a thread. This is to ensure
    the UDP packet which is sent doesn't hold up the main thread. Note that the
    StatsD client is the UDP version therefore sending from multiple threads
    should be safe.

    Note, for calls like set_value, max_value, min_value the values can
    be strings, datetimes, or any other Python objects which isn't suitable for
    stats.

    Note for incr_value the start parameter is ignored because the model for
    statsd is very different. It's not possible to find out if a value was
    ever set.
    """

    NUMERIC_TYPES = [
        int,
        float,
        long
    ]

    def __init__(self, crawler):
        super(StatsDStatsCollector, self).__init__(crawler)

        self._statsd_client = statsd.StatsClient(
            host=crawler.settings.get('STATSD_HOST', 'localhost'),
            port=crawler.settings.getint('STATSD_PORT', 8125))

    @classmethod
    def _is_numeric_type(cls, value):
        return type(value) in cls.NUMERIC_TYPES

    def _dotted_key(self, key, spider):
        new_key = key.replace('/', '.')
        return '%s.%s' % (spider.name, new_key) if spider is not None else new_key

    def _set_value_thread(self, key, value, spider):
        self._statsd_client.gauge(self._dotted_key(key, spider), value)

    def set_value(self, key, value, spider=None):
        super(StatsDStatsCollector, self).set_value(key, value, spider)
        if self._is_numeric_type(value):
            return deferToThread(self._set_value_thread, key, value, spider)

    def _inc_value_thread(self, key, count, start, spider):
        self._statsd_client.incr(self._dotted_key(key, spider), count)

    def inc_value(self, key, count=1, start=0, spider=None):
        super(StatsDStatsCollector, self).inc_value(key, count, start, spider)
        return deferToThread(
            self._inc_value_thread,
            key,
            count,
            start,
            spider)

    def _get_set_value(self, key, spider):
        value = self.get_value(key, spider)
        if self._is_numeric_type(value):
            return deferToThread(self._set_value_thread, key, value, spider)

    def max_value(self, key, value, spider=None):
        super(StatsDStatsCollector, self).max_value(key, value, spider)
        return self._get_set_value(key, spider)

    def min_value(self, key, value, spider=None):
        super(StatsDStatsCollector, self).min_value(key, value, spider)
        return self._get_set_value(key, spider)