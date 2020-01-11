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
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ocolab.settings")
django.setup()
from resdig.models import Keyword, Res, Engine, Donor, Cast


setting(4)
port = 23333
password = 'iridescent256938004'
DEEPTH = 400
ENGINETIMEGAP = 15


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


class Task:
    def __init__(self, keyword, subtaskqueue):
        self.keyword = keyword
        self.statu = 'Initing'
        self.progress = 0
        self.subtask_done_counter = 0
        self.subtask_total_counter = 0
        self.reslist = []
        subtaskqueue.put(
            SubTask(
                task_type='ParseTask',
                keyword=keyword,
                DEEPTH=DEEPTH,
            )
        )
        self.last_active_time = time.time()
        makelog('Task inited {}'.format(self.keyword))

    def getdict(self):
        return {
            'keyword': self.keyword,
            'progress': self.progress,
            'status': self.statu
        }

    def putrawres(self, rawres_list):
        def rawres_to_res(rawres,kw:Keyword):
            return Res(
                keyword=kw,
                link=rawres.reslink,
                web=rawres.weblink,
                type=rawres.type,
                filename=rawres.filename,
                filesize=rawres.filesize
            )

        # 更新 task 最后一次活跃时间
        makelog('更新 task 最后一次活跃时间')
        self.last_active_time = time.time()
        # 更新状态和进度
        makelog('更新状态和进度')
        self.subtask_done_counter += 1
        self.progress = self.subtask_done_counter*100/self.subtask_total_counter
        if self.subtask_done_counter == self.subtask_total_counter:
            self.statu = 'Done'
        else:
            self.statu = 'Digging'
        # 收集资源实例
        if len(rawres_list)>0:
            makelog('获取关键字')
            kw = Keyword.objects.get(keyword=self.keyword)
            makelog('收集资源实例')
            for rawres in rawres_list:
                makelog('*')
                self.reslist.append(rawres_to_res(rawres,kw))
        makelog('SubTask done! {}'.format(self.keyword), 4)


class SubTask:
    def __init__(self, task_type: str, keyword: str, weblink=None, DEEPTH=None):
        self.task_type = task_type
        self.keyword = keyword

        if DEEPTH != None and task_type == 'ParseTask':
            self.DEEPTH = DEEPTH

        elif task_type == 'MiniTask':
            self.link = weblink
        else:
            makelog('Task type error!', 1)
            raise
        makelog('SubTask inited:{}'.format(self.task_type), 4)

    def do(self):
        @retry(tries=2)
        def net(link, params=None, allow_redirects=True):
            UA = [
                'User-Agent,Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                'User-Agent,Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                'User-Agent,Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
                'User-Agent, Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1    ',
                'User-Agent,Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
                'User-Agent, Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            ]

            r = requests.get(
                link,
                headers={
                    'User-Agent': random.choice(UA)
                },
                timeout=5,
                params=params,
                allow_redirects=allow_redirects
            )
            # print(r.request.url)
            r.raise_for_status()
            return r

        def minitask():
            def get_source_code():
                sourcecode = ''
                try:
                    n = 0
                    status_code = 302
                    while status_code in [302, 301] and n < 3:
                        r = net(self.link, allow_redirects=False)
                        status_code = r.status_code
                        if status_code in [301, 302]:
                            self.link = r.headers['location']
                            n = n + 1
                        else:
                            r.encoding = r.apparent_encoding
                            # 收集网页源码
                            sourcecode = r.text
                except:
                    pass

                return sourcecode

            def get_rawres(sourcecode):
                # 匹配表达式
                th_r = re.compile(
                    r'''thunder://[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=]+''')
                ed_r = re.compile(r'''ed2k://[\s\S]+?(?:[/])''')
                magnet_r = re.compile(
                    r'''magnet:\?\S+?(?=['"“”‘’《》<>$()（）：])''')

                # 匹配资源
                rawres_list = []
                for res_container in [
                    [th_r.findall(sourcecode), 'thunder'],
                    [ed_r.findall(sourcecode), 'ed2k'],
                    [magnet_r.findall(sourcecode), 'magnet'],
                ]:
                    for reslink in res_container[0]:
                        if len(reslink) < 800:
                            raw_res = RawRes(
                                self.keyword,
                                reslink,
                                self.link,
                                res_container[1]
                            )
                            # 补全信息
                            raw_res.reslinkparser()
                            # 加入列表
                            rawres_list.append(
                                raw_res
                            )
                return rawres_list

            # print('---------------------------')
            sourcecode = get_source_code()
            rawres_list = get_rawres(sourcecode)
            # 找到任务并放入rawres
            CACHE.rawres_upload(self.keyword, rawres_list)
            makelog('MiniTask Done!', 4)

        def parsetask():

            sengine = Bing(keyWord=self.keyword+' 下载', amount=self.DEEPTH)
            makelog('search engine start', 3)
            results = sengine.Search()
            self.weblinklist = [res['link'] for res in results]

            # 上传SubTask
            CACHE.subtaskqueue_puts(
                self.keyword,
                [
                    SubTask(
                        task_type='MiniTask',
                        keyword=self.keyword,
                        weblink=weblink
                    ) for weblink in self.weblinklist
                ]
            )

        makelog('{} Start!'.format(self.task_type), 3)

        if self.task_type == 'MiniTask':
            minitask()
        elif self.task_type == 'ParseTask':
            parsetask()
        else:
            makelog('Error unknow task{}'.format(self.task_type), 1)


class Enginer:
    acttime = 0

    def __init__(self, enginetableobj):
        self.name = enginetableobj.name
        self.system = enginetableobj.system
        self.model = enginetableobj.model
        self.position = enginetableobj.position
        self.provider = enginetableobj.provider

    def isActive(self):
        return time.time()-self.acttime < ENGINETIMEGAP

    def act(self):
        self.acttime = time.time()

    def getDict(self):
        return {
            'name': self.name,
            'system': self.system,
            'model': self.model,
            'position': self.position,
            'provider': self.provider,
            'isActive': self.isActive()
        }


class reguler():
    acttime = 0

    def __init__(self, Fname, gap, obj):
        self.Fname = Fname
        self.gap = gap
        self.obj = obj

    def act(self):
        nowt = time.time()
        if nowt - self.acttime > self.gap:
            self.acttime = nowt
            F = getattr(self.obj, self.Fname)
            F()
            # makelog(self.Fname+' Done!', 4)


class Cache:
    # 主任务
    tasks = []
    # 子任务队列
    subtaskQueue = Queue()
    # 挖掘深度
    deepth = DEEPTH

    engines = [Enginer(E) for E in Engine.objects.all()]
    resAmount = 0
    keyAmount = 0
    hots = []
    donors = []
    casts=[]

    # api
    def puttask(self, keyword):
        self.tasks.append(Task(keyword, self.subtaskQueue))
        return True

    def checkTaskIn(self, keyword):
        keywordlist = []
        for task in self.tasks:
            keywordlist.append(task.keyword)
        return keyword in keywordlist

    def getDynamicData(self):
        return {
            'engines': [engine.getDict() for engine in self.engines],
            'tasks': [task.getdict() for task in self.tasks]
        }

    def getStaticData(self):
        return {
            'resAmount': self.resAmount,
            'keywordAmount': self.keyAmount,
            'casts': self.casts,
            'donors': self.donors,
            'hots': self.hots
        }

    # engine

    def subtaskqueue_empty(self):
        return self.subtaskQueue.empty()

    def subtaskqueue_get(self):
        return self.subtaskQueue.get()

    def subtaskqueue_puts(self, keyword, subtask_list):
        for task in self.tasks:
            if task.keyword == keyword:
                task.subtask_total_counter += len(subtask_list)
                task.statu = 'Waiting'
        for subtak in subtask_list:
            self.subtaskQueue.put(subtak)

    def rawres_upload(self, keyword, rawres_list):
        for task in self.tasks:
            if task.keyword == keyword:
                task.putrawres(rawres_list)
                break

    def activeengine(self, engineName):
        for engine in self.engines:
            if engine.name == engineName:
                engine.act()

    #   regular函数

    def udResAmount(self):
        self.resAmount = Res.objects.all().count()

    def udKeywordAmount(self):
        self.keyAmount = Keyword.objects.all().count()


    def udHots(self):
        try:
            self.hots = list(
                Keyword.objects.filter(showInRec='True').order_by('-digTimes')[0:50].values()
            )
        except Exception as e:
            makelog('Error in udhotkeylist!\n'+str(e), 1)

    def udCasts(self):
        try:
            self.casts = list(Cast.objects.order_by('-id').values())
        except Exception as e:
            makelog('Error in udCasts!\n' + str(e), 1)

    def udDonors(self):
        try:
            self.donors = list(
                Donor.objects.all().order_by('-time').values())
        except Exception as e:
            makelog('Error in uddonnateinfo!\n' + str(e), 1)

    def saveRes(self):
        for task in self.tasks:
            if task.statu == 'Done' or (task.statu == 'Digging' and time.time() - task.last_active_time > 20):
                # 除重
                savereslist = []
                prelinklist = [
                    res.link for res in Res.objects.filter(keyword=task.keyword)
                ]
                for res in task.reslist:
                    if res.link not in prelinklist:
                        savereslist.append(res)
                    else:
                        prelinklist.append(res.link)
                # 储存
                Res.objects.bulk_create(savereslist)
                # 删除任务
                self.tasks.remove(task)

if __name__ == '__main__':
    while True:
        makelog('Manager-x 2.0 start!', 2)
        try:
            # 启动服务
            cache = initManager(isManager=True,obj=Cache(),port=port,password=password)

            reguler_list = [
                reguler('saveRes', 2, cache),
                reguler('udCasts', 10 * 60, cache),
                reguler('udDonors', 10 * 60, cache),
                reguler('udHots', 3 * 60 * 60, cache),
                reguler('udResAmount', 24 * 60 * 60, cache),
                reguler('udKeywordAmount', 24 * 60 * 60, cache),
            ]
            makelog('cache start sscuessed !', 2)
            while True:
                for reguler in reguler_list:
                    reguler.act()
                time.sleep(1)
        except Exception as e:
            makelog('Error in main process! Reboot after 2s !\n{}'.format(
                traceback.format_exc()), 1)
            time.sleep(2)
