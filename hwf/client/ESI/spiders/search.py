import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data'))

import sys
import io
sys.path.append(dir_path)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import datetime
from multiprocessing import Process, Queue
import re

if __name__ == "__main__":
    mode = 'search'
    search_list = []
    with open('./search.txt', 'r') as f:
        for line in f.readlines():
            search_list.append(line.strip())
    with open('./main.txt', 'a') as f:
        for search in search_list:
            f.write('\n')
            f.write(str(search))
    # search_list = ['Toward Context-Aware Mobile Social Networks']
    configure_logging()
    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl('esi', search_list, mode)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
