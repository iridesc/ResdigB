import requests
import base64
import json
import traceback
import time
import sys
import os
from retry import retry
import django
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ocolab.settings")
django.setup()
from multiprocessing import Queue
from urllib import parse
from multiprocessing.managers import BaseManager
from resdig.models import Donatetable
from resdig.models import Broadcasttable
from resdig.models import Appversiontable
from resdig.models import Messagetable
from resdig.models import Keywordtable
from resdig.models import Etable
from resdig.models import Resourcetable


def makelog(log):
    print(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
        '>>>', log
    )


class RawRes:
    def __init__(self, keyword, reslink, weblink, restype):
        self.reslink = reslink
        self.weblink = weblink
        self.type = restype
        self.keyword = keyword
        self.parsedlink = reslink
        self.filename = None
        self.filesize = 0

    def reslinkparser(self):
        def base64decode():
            # 获取到被编码的部分
            link = self.parsedlink.split('/')[-1]
            # b64解码 得到byte
            example = base64.b64decode(link)
            for i in ['utf-8', 'gbk', 'ascii', 'gb2312', 'GB18030', 'iso8859-1', 'utf-16', ]:
                try:
                    example = example.decode(encoding=i)[2:][:-2]
                    self.parsedlink = example
                    break
                except:
                    pass

        # url解码
        self.parsedlink = parse.unquote(self.parsedlink)
        # 提取链接类型
        t = self.parsedlink.split(':')[0]
        try:
            if t == 'http':
                self.filename = self.parsedlink.split('/')[-1].split('?')[0]
            elif t == 'ftp':
                self.filename = self.parsedlink.split('/')[-1]
            elif t == 'magnet':
                # 提取参数字符串
                if '&amp;' in self.parsedlink:
                    infolist = self.parsedlink.split('&amp;')
                else:
                    infolist = self.parsedlink.split('&')
                # 提取文件名和文件大小
                for info in infolist:
                    if info.split('=')[0] == 'dn':
                        self.filename = info.split('=')[1]
                    elif info.split('=')[0] == 'xl':
                        self.filesize = int(info.split('=')[1])/1024**2
            elif t == 'ed2k':
                infolist = self.parsedlink.split('|')
                self.filename = infolist[2]
                self.filesize = int(infolist[3])/1024**2
            elif t == 'thunder':
                base64decode()
                self.reslinkparser()
            else:
                pass
        except Exception as e:
            pass



@retry(tries=10, delay=2)
def get(s, e=None):
    if e == None:
        return Resourcetable.objects.filter(
            type__in=['magnet', 'ed2k', 'thunder'],)[s:]
    else:
        return Resourcetable.objects.filter(type__in=['magnet', 'ed2k', 'thunder'],)[s:e]


@retry(tries=10, delay=2)
def save(readylist):
    Resourcetable.objects.bulk_update(readylist, ('filename', 'filesize'))
    # for res in readylist:
    #    res.save()


TOTAL = Resourcetable.objects.all().count()
NEW = 0
n = 0
print(TOTAL)
for i in range(int(TOTAL/10000)):
    readylist = []
    for res in get(i*10000, (i+1)*10000):
        rawres = RawRes(res.keyword, res.link, res.web, res.type)
        rawres.reslinkparser()

        if res.filename != rawres.filename or res.filesize != rawres.filesize:
            res.filename = rawres.filename
            res.filesize = rawres.filesize
            readylist.append(res)
            NEW += 1
        n += 1
        if len(readylist) >1000:
            save(readylist)
            readylist = []
        if n>1000:
            print(round(n*100/TOTAL, 4), '%', ' NEW:', NEW)
    save(readylist)


for res in get(i*10000, None):
    rawres = RawRes(res.keyword, res.link, res.web, res.type)
    rawres.reslinkparser()

    if res.filename != rawres.filename or res.filesize != rawres.filesize:
        res.filename = rawres.filename
        res.filesize = rawres.filesize
        readylist.append(res)
        NEW += 1
    n += 1
    if len(readylist) >1000:
        save(readylist)
        readylist=[]
        print(round(n*100/TOTAL, 4), '%', ' NEW:', NEW)
save(readylist)
print('Done!')
