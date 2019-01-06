# -*- coding: utf-8 -*-

# Scrapy settings for JDSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'JDSpider'

SPIDER_MODULES = ['JDSpider.spiders']
NEWSPIDER_MODULE = 'JDSpider.spiders'

# 分布式爬虫需要配置要访问的redis的主机
#REDIS_HOST = '10.11.56.63'  # 主机ip,本地写'localhost'
REDIS_HOST = '192.168.0.101'#或者写REDIS_HOST = '127.0.0.1'或者'localhost'
#部署scrapy-redis的master端，部署scrapy-redis的slave端 配置的是形如REDIS_URL = 'redis://192.168.1.112:6379'
REDIS_PORT = 6379

MONGO_URL = 'mongodb://localhost:27017'
MONGO_DB = "JDSpider_Comment"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_TIMEOUT = 2
RETRY_ENABLED = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#    'Connection': 'keep-alive',
#}
#我们想要用scrapy设置request的请求头ua是随机的，而header中其他参数是固定的。
#其实，由于scrapy局部设置优先于全局设置。所以在middleware中设置随机ua,在settings中DEFAULT_REQUEST_HEADERS设置固定部分，
#就能够实现header中ua是随机的，其他参数是固定的，也就是所middlewares.AgentMiddleware中的User-Agent会覆盖全局settingss中的ua
DEFAULT_REQUEST_HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #"Accept-Encoding":"gzip, deflate",
    "Connection":"keep-alive",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    #'Upgrade-Insecure-Requests':'1',
    #'Content-Type':'application/x-www-form-urlencoded'
    }



# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'JDSpider.middlewares.JdspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'JDSpider.middlewares.ChangeProxy': 541,
   'JDSpider.middlewares.ABProxyMiddleware': 541,
   #'JDSpider.middlewares.ProxyMiddleWare': 541,
   'JDSpider.middlewares.AgentMiddleware': 542,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'JDSpider.pipelines.JdspiderPipeline': 300,
   'scrapy_redis.pipelines.RedisPipeline':400,
   'JDSpider.pipelines.DuplicatesPipeline': 401,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'

#启用限速设置  阿布云动态ip默认是1秒钟请求5次，（可以加钱，购买多次）
#所以，当他是默认5次的时候，我需要对爬虫进行限速

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.2  # 初始下载延迟 1/5=0.2
DOWNLOAD_DELAY = 0.2  # 每次请求间隔时间