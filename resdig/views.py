from multiprocessing.managers import BaseManager
from  django.shortcuts import render
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from .models import Resourcetable,Etable,Keywordtable,Feedbacktable,Messagetable,Appversiontable
from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed,HttpResponseBadRequest
import json,time,re,sys,os,random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


#erro
#Contains illegal characters 1002
#Illegal length of string    1001
#No history found for re     1003
#No such api                 1004
#unknow erro                 2222

BLOCKSIZE=16
PADSTYLE='pkcs7'

def GetMode():
    KEY=b'q863cqfiwyug72jc'
    VI=b'1234567812345678'
    MODE=AES.MODE_CBC
    return AES.new(KEY,MODE,VI)
    
def Encrypto(r_data_str):
    obj=GetMode()

    # print(data)
    r_data_bytes=bytes(r_data_str,'utf-8')
    #补齐字节
    r_data_paded_bytes= pad(r_data_bytes,BLOCKSIZE,PADSTYLE)
    #加密
    e_data_bytes = obj.encrypt(r_data_paded_bytes)#.hex()
    e_data_str=str(base64.b64encode(e_data_bytes),encoding='utf-8',errors="ignore")
    # print(e_data_str)
    return e_data_str

def Decrypto(e_data_str):
    obj=GetMode()
    
    e_data_bytes= base64.b64decode(e_data_str)
    r_data_paded_bytes=obj.decrypt(e_data_bytes)
    r_data_bytes=unpad(r_data_paded_bytes,BLOCKSIZE,PADSTYLE)
    r_data_str=str(r_data_bytes,encoding='utf-8',errors="ignore")
    print(r_data_str)
    return r_data_str

def xxsclear(s):
    s=s.replace('&', '&amp;')
    s=s.replace('<', '&lt;')
    s=s.replace('>', '&gt;')
    s=s.replace("'", '&#39;')
    s=s.replace('"', '&quot;')
    return s

def home(request):
    return HttpResponse(render(request, 'resdig_home.html'))
    
def api(request):
    if request.method == 'POST':
        try:
            e_data_str=str(request.body,encoding='utf-8',errors="ignore")
    
            r_data_str=Decrypto(e_data_str)
            postdata = json.loads(r_data_str)
            reason=postdata['reason']
            class cachemanager(BaseManager):
                pass

            cachemanager.register('cacheobj')
            m = cachemanager(address=('127.0.0.1', 23333), authkey=b'iridescent256938004')
            m.connect()
            cache = m.cacheobj()

            if reason=='getElist':
                data = {
                    'statu': 'getElist',
                    'Elist': cache.getenginelist()
                }

            elif reason=='getres':
                keyword = postdata['keyword']
                data={
                    'statu': 'getres',
                    'reslist': list(Resourcetable.objects.filter(keyword=keyword).values())
                }

            elif reason=='gettasklist':
                data = {
                    'statu': 'gettasklist',
                    'tasklist': cache.gettasklist()
                }

            elif reason=='recheek':
                keyword=postdata['keyword']
                nowtime = time.time()

                try:
                    key = Keywordtable.objects.get(keyword=keyword)
                    if nowtime-key.lastdigtime >24*60*60:
                        #更新最后搜索时间
                        key.lastdigtime=nowtime
                        key.save()
                        if not cache.checktaskin(keyword):
                            cache.puttask(keyword)

                        data = {
                            'statu': 'digging',
                            'tasklist': cache.gettasklist()
                        }

                    else:
                        data={
                        'statu':'timelock',
                        'lasttime':key.lastdigtime
                    }
                except:
                    data={'statu':'erro',
                          'data':'No history found for re',
                          'code':1003}

            elif reason=='gethotkey':
                data = {
                    'statu': 'hotkeylist',
                    'hotkeylist': cache.hotkeylist
                }

            elif reason=='getamount':
                data = {
                    'statu': 'getamount',
                    'resamount': cache.getresamount(),
                    'keyamount': cache.getkeyamount(),
                }

            elif reason=='getmessage':
                data = {
                    'statu': 'getmessage',
                    'messagelist': cache.getcommentlist()
                }

            elif reason=='cheekappversion':
                data ={
                    'statu':'cheekappversion',
                    'data': cache.getappversion()
                }

            elif reason=='getbroadcast':
                data = {
                    'statu': 'getbroadcast',
                    'data': cache.getbroadcast()
                }

            elif reason=='getdonateinfo':
                data = {
                    'statu': 'getdonateinfo',
                    'donatelist': cache.getdonorinfo()
                }

            elif reason=='cheekkey':

                keyword=xxsclear(postdata['keyword'])
                # 判断表单合法
                if len(keyword)>0 and len(keyword)<=50:
                    #是否搜索过
                    try:
                        key = Keywordtable.objects.get(keyword=keyword)
                        # 热度增加
                        key.hotplus()
                        #正在搜索
                        if cache.checktaskin(keyword):
                            data = {
                                'statu': 'digging',
                                'tasklist': cache.gettasklist()
                            }
                        #没有搜索
                        else:
                            #没有资源
                            if key.cantfind:
                                # 最后搜索时间
                                nowtime=time.time()
                                lasttime = key.lastdigtime
                                # 超过时间锁
                                if nowtime-lasttime > 24*60*60:
                                    #加入搜索列表
                                    cachedata=cache.puttask(keyword)
                                    #更新最后搜索时间
                                    key.lastdigtime=nowtime
                                    key.save()
                                    data = {
                                        'statu': 'digging',
                                        'tasklist': cache.gettasklist(keyword)
                                    }
                                #未超过时间锁
                                else:
                                    data={
                                        'statu':'cantfind',
                                        'lastdigtime':lasttime
                                    }
                            #有资源
                            else:
                                data={
                                    'statu':'haveres',
                                    'reslist':list(Resourcetable.objects.filter(keyword=keyword).values()),
                                }
                    #未搜索过
                    except:
                        Keywordtable(keyword=keyword).save()
                        #添加任务
                        cache.puttask(keyword)
                        data = {
                            'statu': 'digging',
                            'tasklist': cache.gettasklist()
                        }
                else:
                    data = {'statu': 'erro',
                            'data':'Illegal length of string',
                            'code':1001}

            elif reason == 'feedback':
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
                    data = {'statu': 'erro',
                            'data': 'Illegal length of string',
                            'code': 1001}

            elif reason == 'leavemessage':
                message = xxsclear(postdata['message'])
                messagefrom = xxsclear(postdata['messagefrom'])
                if 0 < len(message) and len(message) <= 200:
                    try:
                        Messagetable(time=time.time(), messagefrom=messagefrom, message=message).save()
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
                data={'statu':'erro',
                       'data':'No such api',
                      'code':1004
                      }
            
            data = Encrypto(json.dumps(data))
            return HttpResponse(data)

        except Exception as E:
            print('Erro:\napi exception',str(E))
            try:
                print('try reading....')
                e_data_str=str(request.body,encoding='utf-8',errors="ignore")
                print(e_data_str)
                r_data_str=Decrypto(e_data_str)
                print(r_data_str)
            except Exception as e:
                print('Reading erro:',str(e))
                print(request.body)

            return HttpResponseBadRequest()
    else:
        print('Erro:\nwrong method!')
        try:
            print('try reading....')
            e_data_str=str(request.body,encoding='utf-8',errors="ignore")
            print(e_data_str)
            r_data_str=Decrypto(e_data_str)
            print(r_data_str)
        except Exception as e:
            print('Reading erro:', str(e))
            print(request.body)
        return HttpResponseBadRequest()

def operator(requests):
    allow=True
    if allow:
        pass
    else:
        return HttpResponse('not allowed')
