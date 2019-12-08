from multiprocessing.managers import BaseManager
from django.shortcuts import render
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

from .models import Keyword,Res,Engine,Donate,Msg,Feedback,Cast
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import json
import time
import re
import sys
import os
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


# erro
# Contains illegal characters 1002
# Illegal length of string    1001
# No history found for re     1003
# No such api                 1004
# unknow erro                 2222

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


def xxsclear(s):
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace("'", '&#39;')
    s = s.replace('"', '&quot;')
    return s


def home(request):
    return HttpResponse(render(request, 'resdig_home.html'))


def api(request):
    if request.method == 'POST':
        try:
            # 请求的获取与解析
            e_data_str = str(request.body, encoding='utf-8', errors="ignore")
            r_data_str = Decrypto(e_data_str)
            postdata = json.loads(r_data_str)
            reason = postdata['reason']

            class cachemanager(BaseManager):
                pass
            # 链接到缓存
            cachemanager.register('cacheobj')
            m = cachemanager(address=('127.0.0.1', 23333),
                             authkey=b'iridescent256938004')
            m.connect()
            cache = m.cacheobj()
            # 获取操作
            if reason == 'getElist':
                data = {
                    'statu': 'getElist',
                    'Elist': cache.getenginelist()
                }

            elif reason == 'getTasks':
                data = {
                    'tasklist': cache.gettasklist()
                }

            elif reason == 'checkKeyword':
                keyword = postdata['keyword']
                nowtime = time.time()
                data = {

                }
                # 检查是否在任务列表
                if checktaskin(keyword):
                    data['status'] = 'digging'
                else:
                    # 检查是否有记录
                    if Keywordtable.objects.get(keyword=keyword):
                        data['status'] = 'recoded'
                        # 检查资源数量
                        data['resAmount'] = 11
                        # 最后一次检查时间
                        data['lastDigTime'] = 123
                        # 挖掘次数
                        data['digTimes'] = 456
                    else:
                        data['status'] = 'notRecod'

            elif reason == 'getRes':
                keyword = xxsclear(postdata['keyword'])
                try:
                    # 获取到关键字
                    key = Keywordtable.objects.get(keyword=keyword)
                    # 热度增加
                    key.hotplus()
                    # 获取资源
                    data = {
                        'ress': []
                    }
                except:
                    data = {
                        'ress': []
                    }
            elif reason == 'dig':
                keyword = postdata['keyword']

                # 判断表单合法
                if len(keyword) > 0 and len(keyword) <= 50:
                    # 检查是否有记录
                    if Keywordtable.objects.get(keyword=keyword):
                        lastDigTime = 56
                        
                        # 检查记录是否超过时间锁
                        if nowtime - lastDigTime > 24 * 60 * 60:
                            # 加入任务列表
                            cache.puttask(keyword)
                            data = {
                                'suc':True
                            }
                        else:
                            data = {
                                'suc': False,
                                'reason':'timeLock'
                            }
                    else:
                        cache.puttask(keyword)
                        data = {
                            'suc':True
                        }
                else:
                    data = {
                        'suc': False,
                        'reson': 'keywordInvalid'
                    }

            # 获取热词
            elif reason == 'getHots':
                data = {
                    'statu': 'hotkeylist',
                    'hotkeylist': cache.hotkeylist
                }

            elif reason == 'getAmount':
                data = {
                    'statu': 'getamount',
                    'resamount': cache.getresamount(),
                    'keyamount': cache.getkeyamount(),
                }

            elif reason == 'getMsg':
                data = {
                    'statu': 'getmessage',
                    'messagelist': cache.getcommentlist()
                }

            elif reason == 'getAnc':
                data = {
                    'statu': 'getbroadcast',
                    'data': cache.getbroadcast()
                }

            elif reason == 'getDonators':
                data = {
                    'statu': 'getdonateinfo',
                    'donatelist': cache.getdonorinfo()
                }

            elif reason == 'sendFeedback':
                message = xxsclear(postdata['message'])
                messagefrom = xxsclear(postdata['messagefrom'])  # web:0 app:1
                phone = xxsclear(postdata['phone'])
                mail = xxsclear(postdata['mail'])

                if 0 < len(message) and len(message) <= 200:
                    try:
                        Feedbacktable(time=time.time(), phone=phone, mail=mail, messagefrom=messagefrom,
                                      message=message).save()
                        data = {'statu': 'feedback'}
                    except:
                        data = {'statu': 'erro',
                                'data': 'unknow erro',
                                'code': 2222}
                else:
                    data = {
                        'statu': 'erro',
                        'data': 'Illegal length of string',
                        'code': 1001
                    }

            elif reason == 'sendMsg':
                message = xxsclear(postdata['message'])
                messagefrom = xxsclear(postdata['messagefrom'])
                if 0 < len(message) and len(message) <= 200:
                    try:
                        Messagetable(
                            time=time.time(), messagefrom=messagefrom, message=message).save()
                        data = {'statu': 'leavemessage'}
                    except:
                        data = {'statu': 'erro',
                                'data': 'unknow erro',
                                'code': 2222}
                else:
                    data = {'statu': 'erro',
                            'data': 'Illegal length of string',
                            'code': 1001}

            else:
                data = {'statu': 'erro',
                        'data': 'No such api',
                        'code': 1004
                        }

            data = Encrypto(json.dumps(data))
            return HttpResponse(data)

        except Exception as E:
            print('Erro:\napi exception', str(E))
            try:
                print('try reading....')
                e_data_str = str(
                    request.body, encoding='utf-8', errors="ignore")
                print(e_data_str)
                r_data_str = Decrypto(e_data_str)
                print(r_data_str)
            except Exception as e:
                print('Reading erro:', str(e))
                print(request.body)

            return HttpResponseBadRequest()
    else:
        print('Erro:\nwrong method!')
        try:
            print('try reading....')
            e_data_str = str(request.body, encoding='utf-8', errors="ignore")
            print(e_data_str)
            r_data_str = Decrypto(e_data_str)
            print(r_data_str)
        except Exception as e:
            print('Reading erro:', str(e))
            print(request.body)
        return HttpResponseBadRequest()
