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
from selenium import webdriver
from scrapy.http import Request,FormRequest,HtmlResponse  
from scrapy.selector import Selector
import re
import json

class IncitesSpider(scrapy.Spider):
	name = 'incites'
	#allowed_domains = ['esi.incites.thomsonreuters.com']
	#start_urls = ['http://esi.incites.thomsonreuters.com/ThresholdsAction.action']
	custom_settings = {
		'COOKIES_ENABLED': False,
	}
	def __init__(self):
		self.headers = {
			'Accept': '*/*',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Connection': 'keep-alive',
			#'Cookie': 'PSSID="H3-YZWPb5x2FYVGx2BMM9owZYDdh4F5yJoSpK6s-18x2dA7Ox2F2IofavXXs0XqhOfBNgx3Dx3Dx2BPRH2XReb4zRwcRzdO2kPQx3Dx3D-9vvmzcndpRgQCGPd1c2qPQx3Dx3D-wx2BJQh9GKVmtdJw3700KssQx3Dx3D"; CUSTOMER_NAME="FUZHOU UNIV"; E_GROUP_NAME="IC2 Platform"; SUBSCRIPTION_GROUP_ID="242368"; SUBSCRIPTION_GROUP_NAME="FUZHOU UNIV_20150123616_1"; CUSTOMER_GROUP_ID="242364"; IP_SET_ID_NAME="FUZHOU UNIV"; ROAMING_DISABLED="true"; ACCESS_METHOD="IP"; esi.isLocalStorageCleared=true; esi.Show=; esi.Type=; esi.FilterValue=; esi.GroupBy=; esi.FilterBy=; esi.authorsList=; esi.frontList=; esi.fieldsList=; esi.instList=; esi.journalList=; esi.terriList=; esi.titleList=; JSESSIONID=7EFF23F01ACC9183FD363ECD8F61575D; _ga=GA1.2.1847634004.1524138582; _gid=GA1.2.1377071393.1524138582; _gat=1',
			#'Host': 'esi.incites.thomsonreuters.com',
			'Referer': 'http://esi.incites.thomsonreuters.com/Thresh21oldsAction.action',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest',
		}
	def start_requests(self):
		fireFoxOptions = webdriver.FirefoxOptions()
		fireFoxOptions.set_headless()
		brower = webdriver.Firefox(firefox_options=fireFoxOptions)

		brower.get('http://esi.incites.thomsonreuters.com/ThresholdsAction.action')
		brower.implicitly_wait(1)
		#print(brower.get_cookies())
		tem = ''
		for index,value in enumerate(brower.get_cookies()):
			tem += value['name']+'='+value['value']
			if index < len(brower.get_cookies())-1:
				tem += '; '
		#print(tem)
		brower.quit()
		self.headers['Cookie'] = tem
		yield Request('http://esi.incites.thomsonreuters.com/ThresholdsDataAction.action?_dc=1523892398413&type=thresholdsHighlyCited',
			#meta=self.meta,
			headers=self.headers,
			dont_filter=True,
			callback=self.get_json
	)
	def get_json(self,response):
		highly_cited_thresholds = json.loads(response.body)
		#highly_cited_threshold = []
		tem = {}
		for x in highly_cited_thresholds['data']:
			if x['FIELD'] == 'COMPUTER SCIENCE':
				tem = x
				break
		highly_cited_threshold = sorted(tem.items())[:-1]
		file_name = './incites.txt'
		with open(file_name,'w') as f:
			for index,value in enumerate(highly_cited_threshold):
				f.write(value[0]+':'+value[1])
				if index == len(highly_cited_threshold)-1:
					break
				f.write('\n')