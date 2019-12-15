from multiprocessing.managers import BaseManager
from django.shortcuts import render
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

from .models import Keyword, Res, Engine, Donor, Msg, Feedback, Cast
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import json
import time
import re
import sys
import os
import random
from django.conf import settings
from django.core.mail import send_mail
from loger import makelog, setting
# Create your views here.

setting(4)
BLOCKSIZE = 16
PADSTYLE = 'pkcs7'


def GetMode():
    KEY = b'q863cqfiwyug72jc'
    VI = b'1234567812345678'
    MODE = AES.MODE_CBC
    return AES.new(KEY, MODE, VI)


def Encrypto(r_data_str):
    obj = GetMode()

    # print(data)
    r_data_bytes = bytes(r_data_str, 'utf-8')
    # 补齐字节
    r_data_paded_bytes = pad(r_data_bytes, BLOCKSIZE, PADSTYLE)
    # 加密
    e_data_bytes = obj.encrypt(r_data_paded_bytes)  # .hex()
    e_data_str = str(base64.b64encode(e_data_bytes),
                     encoding='utf-8', errors="ignore")
    # print(e_data_str)
    return e_data_str


def Decrypto(e_data_str):
    obj = GetMode()

    e_data_bytes = base64.b64decode(e_data_str)
    r_data_paded_bytes = obj.decrypt(e_data_bytes)
    r_data_bytes = unpad(r_data_paded_bytes, BLOCKSIZE, PADSTYLE)
    r_data_str = str(r_data_bytes, encoding='utf-8', errors="ignore")
    print(r_data_str)
    return r_data_str


def xssClear(s):
    os = s
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace("'", '&#39;')
    s = s.replace('"', '&quot;')
    makelog('xssClear: '+os + ' -> '+s)
    return s


def modifyKeyword(keyword: str):
    while keyword[0] == ' ':
        keyword = keyword[1:]

    while keyword[-1] == ' ':
        keyword = keyword[:-1]
    while '  ' in keyword:
        keyword = keyword.replace('  ', ' ')
    return keyword


def connectCache(host:str,port:int,password:bytes):
    class CacheManager(BaseManager):
        pass
    CacheManager.register('getCache')
    cacheManager = CacheManager(address=(host,port),authkey=password)
    cacheManager.connect()
    return cacheManager.getCache()
    

def home(request):
    return HttpResponse(render(request, 'resdig_home.html'))


def api(request):
    if request.method == 'POST':
        try:
            # 请求的获取与解析
            e_data_str = str(request.body, encoding='utf-8', errors="ignore")
            # r_data_str = Decrypto(e_data_str)
            postdata = json.loads(e_data_str)
            makelog(str(postdata))
            reason = postdata['reason']

            # 链接到缓存
            cache = connectCache('127.0.0.1', 23333,b'iridescent256938004')

            # 获取引擎状态
            if reason == 'getEngines':
                data = {

                    'engines': cache.getEngines()
                }
            # 获取任务列表
            elif reason == 'getTasks':
                data = {
                    'tasks': cache.getTasks()
                }
            # 检查关键字的状态（digging，recoded->getRess/dig，notRecode->dig）
            elif reason == 'checkKeyword':
                keyword = postdata['keyword']
                # 检查是否在任务列表
                if cache.checkTaskIn(keyword):
                    data = {'status': 'digging'}
                else:
                    # 检查是否有记录
                    try:
                        KW = Keyword.objects.get(keyword=keyword)
                        data = {}
                        data['status'] = 'recoded'
                        # 检查资源数量

                        data['resAmount'] = KW.res_set.all().count()
                        # 最后一次检查时间
                        data['lastDigTime'] = KW.lastDigTime
                        # 挖掘次数
                        data['digTimes'] = KW.digTimes
                    except Exception as e:
                        makelog(str(e))
                        data = {'status': 'notRecod'}
            # 获取关键字资源
            elif reason == 'getRess':
                keyword = postdata['keyword']
                try:
                    # 获取到关键字
                    KW = Keyword.objects.get(keyword=keyword)
                    # 热度增加
                    KW.hotPlus()
                    # 获取资源
                    data = {
                        'ress': list(KW.res_set.all().values())
                    }
                except:
                    data = {'ress': []}
            # 挖掘
            elif reason == 'dig':
                def checkRecodedAndTimelock(keyword):
                    # 检查是否有记录
                    try:
                        KW = Keyword.objects.get(keyword=keyword)
                        makelog(str(KW.lastDigTime))
                        return True, time.time() - KW.lastDigTime < 24 * 3600, KW
                    except Exception as e:
                        makelog(str(e), 1)
                        print(type(e))
                        return False, False, None

                keyword =  modifyKeyword(xssClear(postdata['keyword']))
                # 判断关键字是否合法
                makelog('判断关键字是否合法')
                if len(keyword) > 0 and len(keyword) <= 50:
                    # 检查是否在任务列表
                    makelog('检查是否在任务列表')
                    recoded, timelock, KW = checkRecodedAndTimelock(keyword)
                    if cache.checkTaskIn(keyword):
                        data = {
                            'suc': False,
                            'reason': 'inTasks'
                        }
                        makelog('Task in!')
                    else:
                        makelog('检查是否有记录')
                        if recoded:
                            makelog('检查时间锁')
                            if timelock:
                                data = {
                                    'suc': False,
                                    'reason': 'timeLocked',
                                    'lastDigTime': KW.lastDigTime
                                }
                                makelog('locked')
                            else:
                                cache.puttask(keyword)
                                data = {
                                    'suc': True
                                }
                                makelog('Not lock')
                        else:
                            cache.puttask(keyword)
                            data = {
                                'suc': True
                            }
                            makelog('Not recode!')
                else:
                    data = {
                        'suc': False,
                        'reson': 'keywordInvalid'
                    }
                    makelog('keywordInvalid')

            elif reason == 'getHots':
                data = {
                    'hots': cache.getHots()
                }

            elif reason == 'getAmount':
                data = cache.getAmount()

            elif reason == 'getMsgs':
                data = {
                    'msgs': cache.getMsgs()
                }

            elif reason == 'getCasts':
                data = {
                    'casts': cache.getCasts()
                }

            elif reason == 'getDonors':
                data = {
                    'donors': cache.getDonors()
                }

            elif reason == 'sendFeedback':
                info = xssClear(postdata['info'])
                makelog('检查信息是否合法')
                if 0 < len(info) and len(info) <= 500:
                    try:
                        Feedback(
                            time=time.time(),
                            info=info
                        ).save()
                        data = {'suc': True}
                        makelog('save suc!')
                    except Exception as e:
                        data = {'suc': False, }
                        makelog('save faile!\n'+str(e), 1)
                else:
                    data = {
                        'suc': False,
                        'reason': 'lenInvalid'
                    }
                    makelog('信息非法！')

            elif reason == 'sendMsg':
                info = xssClear(postdata['info'])
                makelog('检查信息是否合法')
                if 0 < len(info) and len(info) <= 200:
                    try:
                        Msg(time=time.time(), info=info).save()
                        data = {'suc': True}
                        makelog('save suc!')
                    except Exception as e:
                        data = {'suc': False, }
                        makelog('save faile!\n'+str(e), 1)
                else:
                    data = {
                        'suc': False,
                        'reason': 'lenInvalid'
                    }
                    makelog('信息非法！')

            else:
                data = {'suc': False}

            # data = Encrypto(json.dumps(data))
            # return HttpResponse(data)
            return JsonResponse(data)

        except Exception as E:
            makelog('Main error in api\n'+str(E),1)
            e_data_str = str(request.body, encoding='utf-8', errors="ignore")
            makelog(e_data_str,1)
            return HttpResponseBadRequest()
    else:
        makelog('wrong method!', 1)
        e_data_str = str(request.body, encoding='utf-8', errors="ignore")
        makelog(e_data_str, 1)
        return HttpResponseBadRequest()
