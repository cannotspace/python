# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
# os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data'))

import sys
# import io
# sys.path.append(dir_path)
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import datetime
from multiprocessing import Process, Queue


class run_spider:

    def __init__(self, search_list, mode):
        self.search_list = search_list
        self.mode = mode
        self.q = Queue()

    def start_spider(self):
        configure_logging()
        runner = CrawlerRunner(get_project_settings())
        d = runner.crawl('esi', self.search_list, self.mode)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def start_spiders(self):
        p = Process(target=self.select_spider, args=())
        p.start()
        p.join()

    def select_spider(self):
        try:
            configure_logging()
            runner = CrawlerRunner(get_project_settings())
            if self.mode == 'search':
                deferred = runner.crawl('esi', self.search_list, self.mode)
            elif self.mode == 'update':
                # runner.crawl('incites')
                # runner.crawl('esi', self.search_list, self.mode)
                # deferred = runner.join()
                deferred = runner.crawl('esi', self.search_list, self.mode)
            else:
                if self.mode == 'update_incites':
                    deferred = runner.crawl('incites')
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            self.q.put(None)
        except Exception as e:
            self.q.put(e)
