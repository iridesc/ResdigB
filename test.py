import os
import sys
import json
import time
import base64
import django
import requests
import traceback
from multiprocessing import Queue
from loger import makelog, setting
from initManager import initManager

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ocolab.settings")
django.setup()
from resdig.models import Keyword, Res, Engine, Donor, Cast

setting(2)

from AesEverywhere import aes256

PASSWORD = "q863cqfiwyug72jc"

data = {
    # 静态数据请求
    # "reason": "getStaticData",
    # 'reason': 'getCasts',
    # 'reason': 'getHots',
    # 'reason': 'getDonors',
    # 'reason': 'getAmount',
    # 动态数据请求
    # "reason": "getDynamicData"
    # 'reason': 'getEngines'
    # 'reason': 'getMsgs',
    # 'reason': 'getTasks',
    # 即时数据请求
    # 'reason': 'checkKeyword',
    # 'keyword': 'batman1',
    'reason': 'getRess',
    # 'keyword': 'batmanisdgf',
    # 'reason': 'dig',
    'keyword': '机械师',
    # 'reason': 'sendFeedback',
    # 'info':'hahahha'
    # 'reason': 'sendMsg',
    # 'info':'hahahhaisdg\>>'
}

# encryption
# encrypted = aes256.encrypt("TEXT", "PASSWORD")
# print(encrypted)

# # decryption
# print(aes256.decrypt(encrypted, "PASSWORD"))


r = requests.post('https://resdig.net/api/', data=aes256.encrypt(json.dumps(data),PASSWORD))
print(r.status_code)
print(aes256.decrypt(r.content,PASSWORD))
# # 测试加密解密
# a=json.dumps({})

# # encryption
# encrypted = aes256.encrypt(a, PASSWORD)
# print(encrypted)
# # decryption
# print(aes256.decrypt(encrypted, 'PASSWORD'))


# e=encrypto(a)
# print(e)
# print('************************')
# d=decrypto(e)
# print(d)
# amount=Keyword.objects.all().count()
# n=0
# for kw in Keyword.objects.all():
#     kw.visitTimes=kw.digTimes
#     kw.lastVisitTime=kw.lastDigTime
#     kw.save()
#     n+=1
#     if n%500==0:
#         print(round(n*100/amount),'%')