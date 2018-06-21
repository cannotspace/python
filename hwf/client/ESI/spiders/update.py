import os
dir_path = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(dir_path)

import threading
import paramiko
import datetime
import run_spider

# 定时任务
config = {
    'hostname'   : '123.207.161.173',
    'username'   : 'Administrator',
    'password'   : '7317Fu350321',
    'port'       : 22,
    'update_time': 1,
    'local_path' : 'D:/py/scrapy/ESI/data',
    'ssh_path'   : 'C:/Users/Administrator/Documents',
    'upload_list': ['esi.txt','incites.txt'],
}

def timing():
    print('timing running')
    cited = []
    update_cited = []
    search_cited = []
    day = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y%m%d'), '%Y%m%d')
    file_name = os.path.join(dir_path, '../../data/esi.txt')
    with open(file_name, 'r') as f:
        for line in f.readlines():
            day_2 = datetime.datetime.strptime(eval(line)['time'], '%Y%m%d')
            if day.month != day_2.month or day.day == config['update_time']:
                if ('doi' in eval(line).keys()):
                    update_cited.append(eval(line))
                else:
                    search_cited.append(eval(line))
    print('根据DOI进行更新')
    print(update_cited)
    print('根据句子相似度进行更新')
    print(search_cited)
    file_name = os.path.join(dir_path, '../../data/incites.txt')
    with open(file_name, 'r') as f:
        highly_cited_threshold = f.read()
    print(highly_cited_threshold)
    if not highly_cited_threshold.strip() or day.day == config['update_time']:
        r = run_spider.run_spider(update_cited, 'update_incites')
        r.start_spiders()
    if update_cited or day.day == config['update_time']:
        r = run_spider.run_spider(update_cited, 'update')
        r.start_spiders()
    if search_cited or day.day == config['update_time']:
        print('暂未处理')
    if day.day == config['update_time']+1:
        t = paramiko.Transport((config['hostname'], config['port']))
        t.connect(username=config['username'], password=config['password'])
        sftp = paramiko.SFTPClient.from_transport(t)
        for file_name in config['upload_list']:
            sftp.put(os.path.join(config['local_path'],file_name), os.path.join(config['ssh_path'], file_name))
        t.close()
    global timer
    timer = threading.Timer(6, timing)
    timer.start()

if __name__ == "__main__":
    timing()
