__author__ = 'batulu'
import gzip
import datetime

from scrapy import signals
from scrapy.mail import MailSender
from scrapy.exceptions import NotConfigured
from scrapy.utils.serialize import ScrapyJSONEncoder

from collections import defaultdict

try:
    from cStringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO

def format_size(size):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)

        size /= 1024.0

class GzipCompressor(gzip.GzipFile):
    extension = '.gz'
    mimetype = 'application/gzip'

    def __init__(self):
        super(GzipCompressor, self).__init__(fileobj=PlainCompressor(), mode='w')
        self.read = self.fileobj.read

class PlainCompressor(StringIO):
    extension = ''
    mimetype = 'text/plain'

    def read(self, *args, **kwargs):
        self.seek(0)

        return StringIO.read(self, *args, **kwargs)

    @property
    def size(self):
        return len(self.getvalue())

class StatusMailer(object):
    def __init__(self, recipients, mail, compressor, crawler):
        self.recipients = recipients
        self.mail = mail
        self.encoder = ScrapyJSONEncoder(crawler=crawler)
        self.files = defaultdict(compressor)

        self.num_items = 0
        self.num_errors = 0

    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist('STATUSMAILER_RECIPIENTS')
        compression = crawler.settings.get('STATUSMAILER_COMPRESSION')

        if not compression:
            compressor = PlainCompressor
        elif compression.lower().startswith('gz'):
            compressor = GzipCompressor
        else:
            raise NotConfigured

        if not recipients:
            raise NotConfigured

        mail = MailSender.from_settings(crawler.settings)
        instance = cls(recipients, mail, compressor, crawler)

        crawler.signals.connect(instance.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(instance.spider_error, signal=signals.spider_error)
        crawler.signals.connect(instance.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(instance.request_received, signal=signals.request_received)

        return instance

    def item_scraped(self, item, response, spider):
        self.files[spider.name + '-items.json'].write(self.encoder.encode(item))
        self.num_items += 1

    def spider_error(self, failure, response, spider):
        self.files[spider.name + '.log'].write(failure.getTraceback())
        self.num_errors += 1

    def request_received(self, request, spider):
        self.files[spider.name + '.log'].write(str(request) + '\n')

    def spider_closed(self, spider, reason):
        files = []

        for name, compressed in self.files.items():
            files.append((name + compressed.extension, compressed.mimetype, compressed))

        try:
            size = self.files[spider.name + '-items.json'].size
        except KeyError:
            size = 0

        body='''Crawl statistics:

 - Spider name: {0}
 - Spider finished at: {1}
 - Number of items scraped: {2}
 - Number of errors: {3}
 - Size of scraped items: {4}'''.format(
            spider.name,
            datetime.datetime.now(),
            self.num_items,
            self.num_errors,
            format_size(size)
        )

        return self.mail.send(
            to=self.recipients,
            subject='Crawler for %s: %s' % (spider.name, reason),
            body=body,
            attachs=files
        )
