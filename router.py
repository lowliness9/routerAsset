# -*- coding:utf-8 -*-
import requests
import Queue
import sys
import threading
import time
import argparse
reload(sys)
sys.setdefaultencoding('utf-8')
requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Connection':'close',
    'Referer':'http://www.baidu.com/spider.html'
}

def task_run():
    while not task_queue.empty():
        ip = task_queue.get()
        try:
            p = requests.get('http://'+ip,headers=headers,timeout=args.timeout,verify=False)
            header_ok = True
            try:
                req_resp_header = str(p.headers['Server'])
                for respheader_banner in respheader_banners:
                    router = respheader_banner.split('|')[0]
                    flag = respheader_banner.split('|')[1]
                    if flag in req_resp_header:
                        lock.acquire()
                        logs('Find A Router')
                        with open(res_name, 'a+') as f:
                            try:
                                header_ok = False
                                f.write(router + '|' + ip + '\n')
                                f.close()
                            except:
                                f.close()
                        lock.release()
                        break
            except:
                pass
            if header_ok:
                for respbody_banner in respbody_banners:
                    router = respbody_banner.split('|')[0]
                    flag = respbody_banner.split('|')[1]
                    if flag in p.text or flag in p.content:
                        lock.acquire()
                        logs('Find A Router')
                        with open(res_name,'a+') as f:
                            try:
                                f.write(router + '|' + ip + '\n')
                                f.close()
                            except:
                                f.close()
                        lock.release()
                        break
        except:
           pass

def parse_rule():
    respbody_banners = []
    respheader_banners = []
    for line in open('rule.ini','r+').readlines():
        line = line.strip()
        if line != '':
            if line.startswith('#'):
                continue
            else:
                rule = eval(line)
                if rule['type'] == 'respbody_banner':
                    respbody_banners.append(rule['routerName'] + '|' + rule['feature'])
                elif rule['type'] == 'respheader_server':
                    respheader_banners.append(rule['routerName'] + '|' + rule['feature'])
                else:
                    pass
        else:
            pass
    return respheader_banners,respbody_banners

def remain():
    while not task_queue.empty():
        lock.acquire()
        logs('Remaining: {} task'.format(task_queue.qsize()))
        lock.release()
        time.sleep(10)

def logs(msg):
    print '[+]',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(' ')[1],msg

def msg():
    msg = '''
usage: router.py [-h] [-f FILE] [-t TIMEOUT] [-c COUNT]

routerAsset v1.0

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Scan from file discover router
  -t TIMEOUT, --timeout TIMEOUT
                        Request timeout , default 3
  -c COUNT, --count COUNT
                        Scan thread num , default 100
'''
    print msg
    sys.exit(-1)

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="routerAsset v1.0")
    parse.add_argument('-f', '--file', type=str, help='Scan from file discover router')
    parse.add_argument('-t', '--timeout', type=int, help='Request timeout , default 3',default=3)
    parse.add_argument('-c', '--count', type=int, help='Scan thread num , default 100', default=100)
    args = parse.parse_args()

    if args.file:
        pass
    else:
        msg()

    respheader_banners,respbody_banners = parse_rule()
    lock = threading.Lock()
    task_queue = Queue.Queue()
    all_thread = []
    res_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_res.txt'

    logs('Body  规则数量: {}'.format(len(respbody_banners)))
    logs('Header规则数量: {}'.format(len(respheader_banners)))
    time.sleep(1)

    for ip in open(args.file,'r+').readlines():
        ip = ip.strip()
        if ip != '':
            task_queue.put(ip)

    logs('Task Count: {}'.format(task_queue.qsize()))

    for _ in range(args.count):
        t = threading.Thread(target=task_run,args=())
        t.start()
        all_thread.append(t)

    t = threading.Thread(target=remain,args=())
    t.start()
    all_thread.append(t)
    for t in all_thread:
        t.join()
    logs('Task Finish OK')

