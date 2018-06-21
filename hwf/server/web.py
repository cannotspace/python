# -*- coding: utf-8 -*-
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.join(dir_path, 'data'))
from bottle import *
import json
import re
import bottle
import datetime
from paste import httpserver
from gevent import monkey
monkey.patch_all()
import gevent
from multiprocessing import Process
import match

@route('/search', method=['POST'])
def search():
    response.set_header('Access-Control-Allow-Origin', '*')
    search_list = request.POST.get('search_list')
    search = json.loads(search_list)
    cited = []
    with open('./esi.txt', 'r') as f:
        for line in f.readlines():
            cited.append(eval(line))
    with open('./search.txt', 'w') as f:
        for index, value in enumerate(search):
            f.write(str(value))
            if index < len(search) - 1:
                f.write('\n')
    data = {'data': 'success', 'status': 1}
    return json.dumps(data)



@route('/approach', method=['POST'])
def approach():
    response.set_header('Access-Control-Allow-Origin', '*')
    search = request.POST.get('search')
    print(search)
    cited = []
    with open('./esi.txt', 'r') as f:
        for line in f.readlines():
            cited.append(eval(line))
    m = match.match(search, cited)
    match_result = m.similar()
    data = {'data': match_result, 'status': 1}
    return json.dumps(data)

@route('/show', method=['POST'])
def show():
    response.set_header('Access-Control-Allow-Origin', '*')
    order_type = request.POST.get('order_type')
    # order_type = request.GET.get('order_type')
    request_type = request.POST.get('request_type')
    # request_type = request.GET.get('request_type')
    print(order_type)
    print(request_type)
    # 读取展示的内容
    search = []
    if request_type == 'search':
        with open('./search.txt', 'r') as f:
            for line in f.readlines():
                search.append(line.strip())
    elif request_type == 'main':
        with open('./main.txt', 'r') as f:
            for line in f.readlines():
                search.append(line.strip())
    else:
        print('没有进行搜索操作！！！')
    # print(len(search))
    # 读取incites.txt
    highly_cited_threshold = {}
    with open('./incites.txt', 'r') as f:
        for line in f.readlines():
            tem_list = line.strip().split(':')
            highly_cited_threshold[tem_list[0]] = tem_list[1]
    # 读取esi.txt
    cited = []
    with open('./esi.txt', 'r') as f:
        for line in f.readlines():
            if eval(line)['year'] != datetime.datetime.now().strftime('%Y'):
                cited.append(eval(line))
    for index, value in enumerate(cited):
        year = value['year']
        for k, v in highly_cited_threshold.items():
            if k == year:
                value['cited_2'] = v
                break
    results = []
    for value_1 in search:
        for value_2 in cited:
            if value_1 == value_2['search'] or value_1 == value_2['title']:
                results.append(value_2)
                break
    #处理作者显示
    for index_1,value_1 in enumerate(results):
        author = re.findall(r'\([^)]*\)', value_1['author'])
        str_author = ''
        for index_2,value_2 in enumerate(author):
            value_2 = value_2.replace('(','').replace(')','')
            tem = value_2.split(',')
            str_author += tem[-1]
            for index,value in enumerate(tem):
                str_author += ' '
                str_author += value
                if index == len(tem)-2:
                    break
            if index_2 == len(author)-1:
                break
            str_author += ', '
        value_1['author'] = str_author
    # print(results)
    # print(len(results))
    # exit()
    # 1.按完成百分比排序;2.相差次数倒序;3.发表时间排序;4.按照姓氏排序
    if int(order_type) == 1:
        results_by_order = sorted(results, key=lambda r: int(r['cited']) / int(r['cited_2']), reverse=True)
    elif int(order_type) == 2:
        results_by_order = sorted(results, key=lambda r: abs(int(r['cited']) - int(r['cited_2'])), reverse=True)
    elif int(order_type) == 3:
        results_by_order = sorted(results, key=lambda r: int(r['year']), reverse=True)
    else:
        all_author = []
        for index_1,value_1 in enumerate(results):
            author = value_1['author'].split(', ')
            list_author = []
            for index_2,value_2 in enumerate(author):
                tem = value_2.split(' ')
                str_author = ''
                str_author += tem[-1]
                for index,value in enumerate(tem):
                    str_author += ' '
                    str_author += value
                    if index == len(tem)-2:
                        break
                list_author.append(str_author)
                #将作者名字写入list中
                if len(all_author) == 0:
                    all_author.append(str_author)
                else:
                    for index_3,value_3 in enumerate(all_author):
                        if value_3 == str_author:
                            break
                        if index_3 == len(all_author)-1:
                            all_author.append(str_author)
            value_1['author'] = list_author
        # print(results[0]['author'])
        # print(all_author)
        all_author_sort = sorted(all_author)
        # print(all_author_sort)
        results_by_order = {}
        for index_1,value_1 in enumerate(all_author_sort):
            tem = []
            sum = 0
            for index_2,value_2 in enumerate(results):
                for value_3 in value_2['author']:
                    if value_3 == value_1:
                        tem.append(value_2)
                        sum += 1
                        break
            tem.append(sum)
            results_by_order[value_1] = tem
    # print(results_by_order)
    print('success')
    if int(order_type) == 4:
        data = {'data': results_by_order, 'status': 4}
    else:
        data = {'data': results_by_order, 'status': 1}
    return json.dumps(data)

# run(server='paste', host='127.0.0.1', port=8080, debug=True)
run(host='127.0.0.1', port=8080, debug=True, server='gevent')
# p = Process(target=run(host='127.0.0.1', port=8080, debug=True, server='gevent'))
# p.start()
# p.join()
