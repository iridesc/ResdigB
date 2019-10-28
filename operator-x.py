import requests
import base64
import json
import traceback
import time
import sys
import os
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



class RawRes:
    def __init__(self, keyword, reslink, weblink, restype):
        self.reslink = reslink
        self.weblink = weblink
        self.type = restype
        self.keyword = keyword
        self.filename = None
        self.filesize = 0

    def reslinkparser(self):
        def base64decode(link):
            link = link.split('//')[1]
            example = base64.b64decode(link)
            for i in ['utf-8', 'gbk', 'ascii', 'gb2312', 'GB18030', 'iso8859-1', 'utf-16', ]:
                try:
                    example = example.decode(encoding=i)[2:][:-2]
                    return example
                except:
                    pass

        parselink = parse.unquote(self.reslink)
        t = parselink.split(':')[0]
        filename = None
        size = 0
        try:
            if t == 'http':
                filename = parselink.split('/')[-1].split('?')[0]
            elif t == 'ftp':
                filename = parselink.split('/')[-1]
            elif t == 'magnet':
                if '&amp;' in parselink:
                    infolist = parselink.split('&amp;')
                else:
                    infolist = parselink.split('&')
                for info in infolist:
                    if info.split('=')[0] == 'dn':
                        filename = info.split('=')[1]
                    elif info.split('=')[0] == 'xl':
                        size = int(info.split('=')[1])
            elif t == 'ed2k':
                infolist = parselink.split('|')
                filename = infolist[2]
                size = int(infolist[3])
            elif t == 'thunder':
                filename, size = reslinkparser(base64decode(parselink))
            else:
                makelog('Unknow Res Type:{}'.format(t))

        except:
            pass
        self.filename = filename
        self.filesize = size / 1024 ** 2



Ress = Resourcetable.objects.filter(
                type__in=['thunder','ed2k','magnet'],
                filesize=0
            )


readylist = []
total=Ress.count()
t = 0
n = 0
for res in Ress:
    rawres = RawRes(res.keyword, res.link, res.web, res.type)
    rawres.reslinkparser()
    res.filename = rawres.filename
    res.filesize = rawres.filesize
    readylist.append(res)    

    n+=1
    now = time.time()
    
    if now - t > 3:
        Resourcetable.objects.bulk_update(readylist, ('filename', 'filesize'))
        readylist=[]
        print(round(n*100/total,3),'% ',n,'/',total)
        t = now

Resourcetable.objects.bulk_update(readylist, ('filename', 'filesize'))
print('Done!')