# -*- coding: utf-8 -*-
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../data'))

import sys
import io
sys.path.append(dir_path)
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

import scrapy
from scrapy.http import Request, FormRequest
import re
import datetime

import match


class Esispider(scrapy.Spider):
    """docstring for Esi"""
    name = "esi"
    allowed_domains = ['apps.webofknowledge.com']
    #start_urls = ['http://apps.webofknowledge.com/UA_GeneralSearch_input.do']
    # custom_settings = {
    #     'COOKIES_ENABLED': False,
    # }

    def __init__(self, search_list, mode):
        self.search_list = search_list
        self.mode = mode
        self.sid_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            #'Content-Length':'1393',//400
            # 'Host':'apps.webofknowledge.com',#NullSessionID
            'Upgrade-Insecure-Requests': '1',
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            #'Content-Length':'1393',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'JSESSIONID=0EE5976CFE7E14AD41CE6C84E7FC81C0; SID="6DyDemy1qpy4vDHqxFP"; CUSTOMER="Fuzhou University"; E_GROUP_NAME="Fuzhou University"; ak_bmsc=28AAD81E421B89CF49BD9FE0D58CE983B8325755037A0000C8C5D15A91058E7C~plfwO1ySu8oHjBGNVhVQKQ6zU+vItnzm71nUdBocS7ldIBxH2O+/Q3HbXPZ56v4VBkFGt6IBFjs9+Kf5wAHeTNDki0cGviiBjOUw/JC6CcisFOhufNZslDfFtSQMXLbtq9wa+EURzq1u09LKWJolgUofqOqr9YWdr42xEwvlsjlDcDao2LTziLYcw/HZ9lCVIhdAYG3fv7upkPpdBlm0bIZF4t1fqAmLTD6mKFgTmAWh2cBIo8AmZ6yOvU2ivfY7ug; bm_sv=6A47C4D1FE7F8EF777A4E58C5653D8B3~ewD9M7nbnyZno3lKV/9VFsMSzyrfC5G6Zsh2ElStw6MpBP7pfhktbVjtiwltKOHPGPW8N2HLMC6xQ4WP6Lk6EwvWGWBK0S1OczHVsCEWPdAWDb6o0lmSYAKyDI+KzOMLftbQjEZDw2BTxQ9E8TiZM6B/dX/z94YszyrkjrYUhTw=',
            'Host': 'apps.webofknowledge.com',
            #'Referer':' http://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=8FDXzGGa1sGYMmmI32T&preferencesSaved=',
            'Upgrade-Insecure-Requests': '1',
        }
        self.form_data = {
            'fieldCount': '1',
            'action': 'search',
            'product': 'UA',
            'search_mode': 'GeneralSearch',
            #'SID':'5ELgeJnB2VBz4VK9yJW',
            'max_field_count': '25',
            'max_field_notice': 'Notice: You cannot add another field.',
            'input_invalid_notice': 'Search Error: Please enter a search term.',
            'exp_notice': 'Search Error: Patent search term could be found in more than one family (unique patent number required for Expand option)',
            'input_invalid_notice_limits': '<br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field.',
            #'sa_params':'UA||5ELgeJnB2VBz4VK9yJW|http://apps.webofknowledge.com|',
            'formUpdated': 'true',
            # 'value(input1)': 'The+Emergence+of+Social+and+Community+Intelligence',
            # 'value(select1)': 'TS',
            'value(hidInput1)': '',
            'limitStatus': 'collapsed',
            'ss_lemmatization': 'On',
            'ss_spellchecking': 'Suggest',
            'SinceLastVisit_UTC': '',
            'SinceLastVisit_DATE': '',
            'period': 'Range Selection',
            'range': 'ALL',
            'startYear': '1950',
            'endYear': '2018',
            'update_back2search_link_param': 'yes',
            'ssStatus:display': 'none',
            'ss_showsuggestions': 'ON',
            'ss_query_language': 'auto',
            'ss_numDefaultGeneralSearchFields': '1',
            'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A',
        }
    # 获取sid

    def start_requests(self):
        yield Request('http://www.webofknowledge.com',
                      headers=self.sid_headers,
                      dont_filter=True,
                      callback=self.start_search,
                      )

    def start_search(self, response):
        sid = re.findall(r'SID=\w+&', response.url)
        if sid:
            sid = sid[0].replace('SID=', '').replace('&', '')
        else:
            sid = '6DCBJfj4hTtr2G3kS7l'#8DWULQG3bidF79DvusO
        jsessionid = re.findall(r'JSESSIONID=\w+;', str(response.headers))
        if not jsessionid:
            jsessionid.append('JSESSIONID=0EE5976CFE7E14AD41CE6C84E7FC81C0;')
        bm_sv = re.findall(r'bm_sv=[\s\S]*=;', str(response.headers))
        if not bm_sv:
            bm_sv.append('bm_sv=6A47C4D1FE7F8EF777A4E58C5653D8B3~ewD9M7nbnyZno3lKV/9VFsMSzyrfC5G6Zsh2ElStw6MpBP7pfhktbVjtiwltKOHPGPW8N2HLMC6xQ4WP6Lk6EwvWGWBK0S1OczHVsCEWPdAWDb6o0lmSYAKyDI+KzOMLftbQjEZDw2BTxQ9E8TiZM6B/dX/z94YszyrkjrYUhTw=')
        self.form_data['SID'] = sid
        self.form_data['sa_params'] = 'UA||' + sid + '|http://apps.webofknowledge.com|'
        self.headers['Referer'] = response.url
        self.headers['Cookie'] = jsessionid[0] + ' SID="' + sid + '"; CUSTOMER="Fuzhou University"; E_GROUP_NAME="Fuzhou University"; ak_bmsc=28AAD81E421B89CF49BD9FE0D58CE983B8325755037A0000C8C5D15A91058E7C~plfwO1ySu8oHjBGNVhVQKQ6zU+vItnzm71nUdBocS7ldIBxH2O+/Q3HbXPZ56v4VBkFGt6IBFjs9+Kf5wAHeTNDki0cGviiBjOUw/JC6CcisFOhufNZslDfFtSQMXLbtq9wa+EURzq1u09LKWJolgUofqOqr9YWdr42xEwvlsjlDcDao2LTziLYcw/HZ9lCVIhdAYG3fv7upkPpdBlm0bIZF4t1fqAmLTD6mKFgTmAWh2cBIo8AmZ6yOvU2ivfY7ug; ' + bm_sv[0]
        for value in self.search_list:
            meta = {'dont_redirect': True,  # 禁止网页重定向
                    'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
                    }
            if self.mode == 'search':
                self.form_data['value(select1)'] = 'TS'
                self.form_data['value(input1)'] = value
                meta['search'] = value
            if self.mode == 'update':
                self.form_data['value(select1)'] = 'DO'
                self.form_data['value(input1)'] = value['doi']
                meta['update'] = value

            yield FormRequest(
                url='http://apps.webofknowledge.com/UA_GeneralSearch.do',
                meta=meta,
                headers=self.headers,
                formdata=self.form_data,
                callback=self.post_search,
                dont_filter=True,
                method='POST',
            )

    def post_search(self, response):
        search_url = 'http://apps.webofknowledge.com/' + response.headers['Location'].decode('utf-8')
        meta = {}
        if self.mode == 'update':
            meta['update'] = response.meta['update']
        if self.mode == 'search':
            meta['search'] = response.meta['search']
        return Request(search_url,
                      meta=meta,
                      headers=self.headers,
                      callback=self.parse_item,
                      )

    def parse_item(self, response):
        if self.mode == 'search':
            search_contents = response.xpath('//div[@class="search-results-item"]')
            if not search_contents:
                print('not exist')
            else:
                results = []
                if 'results' in response.meta:
                    results += response.meta['results']
                for each_result in search_contents:
                    tem = {}
                    value = each_result.xpath('./div[@class="search-results-content"]/div/div/a[@class="smallV110"]/value')  # 定位到title的value（存在多个title）
                    title_list = value.xpath('string(.)').extract()
                    # 处理title的英文标题显示
                    flag = value.xpath('./@lang_id').extract()  # 定位到title的语言（为空，不存在这个属性，多个值：en...）
                    if not flag:  # 不存在这个属性
                        for index in range(len(value)):
                            if re.match('^[a-zA-Z0-9\s,.?\'\"-]*$', title_list[index]):
                                tem['title'] = title_list[index].strip("\n")
                    elif not flag[0]:  # 该属性值为空
                        tem['title'] = title_list[0].strip("\n")
                    else:  # 存在多个title
                        for index in range(len(flag)):
                            if flag[index] == 'en':
                                tem['title'] = title_list[index].strip("\n")
                    tem['cited'] = each_result.xpath('./div[@class="search-results-data"]/div[@class="search-results-data-cite"]/a/text()').extract()
                    if tem['cited']:
                        tem['cited'] = tem['cited'][0]
                    else:
                        tem['cited'] = 0

                    tem['highly_cited_paper'] = each_result.xpath('./div[@class="search-results-data"]/div[@class="search-results-data-icon"]').extract()
                    if tem['highly_cited_paper']:
                        tem['highly_cited_paper'] = 1
                    else:
                        tem['highly_cited_paper'] = 0
                    tem['detail'] = each_result.xpath('./div[@class="search-results-content"]/div/div/a[@class="smallV110"][1]/@href').extract()[0]
                    results.append(tem)
                    # print(tem)
                # print(results)
                # 下一页url
                next_url = response.xpath('//a[@class="paginationNext"]/@href').extract()
                if next_url:
                    yield Request(next_url[0],
                                  headers=self.headers,
                                  meta={'results': results,'search':response.meta['search']},
                                  callback=self.parse_item,
                                  )
                else:
                    print(results)
                    print(response.meta['search'])
                    m = match.match(response.meta['search'], results)
                    match_result = m.similar()
                    match_result['search'] = response.meta['search']
                    match_result['time'] = datetime.datetime.now().strftime('%Y%m%d')
                    print(match_result)
                    detail_split = match_result['detail'].split("?")
                    detail_url = 'http://apps.webofknowledge.com' + detail_split[0] + '?locale=en_US&' +detail_split[1]
                    yield Request(detail_url,
                                  headers=self.headers,
                                  meta={'results': match_result},
                                  callback=self.write_item,
                                  )
        if self.mode == 'update':
            result = response.meta['update']
            cited = response.xpath('//div[@class="search-results-data"]/div[@class="search-results-data-cite"]/a/text()').extract()
            if cited:
                result['cited'] = cited[0]
            else:
                result['cited'] = 0

            highly_cited_paper = response.xpath('//div[@class="search-results-data"]/div[@class="search-results-data-icon"]').extract()
            if highly_cited_paper:
                result['highly_cited_paper'] = 1
            else:
                result['highly_cited_paper'] = 0
            result['time'] = datetime.datetime.now().strftime('%Y%m%d')
            print(result)
            self.alter_item(result)

    def write_item(self, response):
        result = response.meta['results']
        # with open('./html.txt', 'w', encoding='utf-8') as f:
        #     f.write(response.body.decode('utf-8'))
        #     f.write('\n')
        # return
        # 存在多个作者
        author_tem = response.xpath('//div[@class="block-record-info"][1]/p[@class="FR_field"]')
        author = author_tem[0].xpath('string(.)').extract()[0].replace("\n", "").replace(" ", "").replace("By", "")
        filter_list = re.findall(r'\[[0-9,]+\]', author)
        for value in filter_list:
            author = author.replace(value, '')
        author = author.split(':')[1:]
        if len(author) == 1:
            result['author'] = author[0]
        else:
            for value in author:
                if re.match('^[a-zA-Z][a-zA-Z\s,();.]+', str(value)):
                    result['author'] = str(value)
                    break
        # result['author'] = result['author'].split('隐藏')[0]
        record = response.xpath('//div[@class="block-record-info block-record-info-source"]')
        # 存在多个来源标题的情况
        sourcetitle = record.xpath('./p[@class="sourceTitle"]/value/text()').extract()
        if len(sourcetitle) == 1:
            result['sourcetitle'] = sourcetitle[0]
        else:
            for value in sourcetitle:
                if re.match('[a-zA-Z\s]+$', str(value)):
                    result['sourcetitle'] = str(value)
                    break
        data = record.xpath('./div[@class="block-record-info-source-values"]')
        info = data[0].xpath('string(.)').extract()[0].replace("\n", "")
        result['info'] = info
        fr_field = record.xpath('./p[@class="FR_field"]')
        for index in range(len(fr_field)):
            information = fr_field[index].xpath('string(.)').extract()[0].replace("\n", "")
            if re.match('DOI[:]', information):
                result['doi'] = information.replace("DOI:", "")
            elif re.match('Published[:]', information):
                result['year'] = re.findall(r'[1-9]\d{3}', information)[0]
            elif re.match('Document Type[:]', information):
                result['typetitle'] = information.replace("Document Type:", "")
            else:
                continue
        result.pop('detail')
        print(result)
        print('写入文件')
        with open('./esi.txt', 'a') as f:
            f.write(str(result))
            f.write('\n')

    def alter_item(self, result):
        # 读取esi.txt
        cited = []
        with open('./esi.txt', 'r') as f:
            for line in f.readlines():
                if eval(line)['title'] != result['title']:
                    cited.append(eval(line))
        cited.append(result)
        with open('./esi.txt', 'w') as f:
            for value in cited:
                f.write(str(value))
                f.write('\n')
