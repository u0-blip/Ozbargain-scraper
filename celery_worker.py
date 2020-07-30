import celery
import redis
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from basic_app import app
from bargin_spider.spiders.bargin_spider import bargin_spider

celery = celery.Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

import os

@celery.task(bind=True)
def get_spider_output(self, user_id):
    from scrapy.settings import Settings

    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'bargin_spider.settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')


    process = CrawlerProcess(settings)

    print('setting is', process.settings.__dict__['attributes']['ITEM_PIPELINES'])
    # 'followall' is the name of one of the spiders of the project.
    process.crawl(bargin_spider)
    process.start() # the script will block here until the crawling is finished
    print('process is done')
    return 

