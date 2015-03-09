from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy import log

class CustomRetryMiddleware(RetryMiddleware):

    def _retry(self, request, reason, spider):
        #retries = request.meta.get('retry_times', 0) + 1
        retries = 20
        if retries <= self.max_retry_times:
            log.msg(format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            # do something with the request: inspect request.meta, look at request.url...
            log.msg(format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)