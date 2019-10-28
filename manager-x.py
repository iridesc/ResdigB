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
from multiprocessing.managers import BaseManager
from resdig.models import Donatetable
from resdig.models import Broadcasttable
from resdig.models import Appversiontable
from resdig.models import Messagetable
from resdig.models import Keywordtable
from resdig.models import Etable
from resdig.models import Resourcetable

host = '0.0.0.0'
port = 23333
password = b'iridescent256938004'
DEEPTH = 10
ENGINETIMEGAP = 15


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


class Task:
    def __init__(self, keyword, subtaskqueue):
        self.keyword = keyword
        self.statu = 'waiting'
        self.progress = 0
        self.subtask_done_counter = 0
        self.subtask_total_counter = 0
        self.reslist = []
        for page in range(DEEPTH):
            subtaskqueue.put(
                SubTask(
                    task_type='ParseTask',
                    keyword=keyword,
                    page=page
                )
            )
        self.last_active_time=time.time()
        makelog('Task inited {}'.format(self.keyword))

    def getdict(self):
        return {
            'keyword': self.keyword,
            'taskstatu': self.statu,
            'progress': self.progress,
            'statu': self.statu
        }

    def putrawres(self, rawres_list):
        def rawres_to_res(rawres):
            return Resourcetable(
                keyword=rawres.keyword,
                link=rawres.reslink,
                web=rawres.weblink,
                type=rawres.type,
                filename=rawres.filename,
                filesize=rawres.filesize
            )

        # 更新 task 最后一次活跃时间
        self.last_active_time = time.time()
        # 更新状态和进度
        self.subtask_done_counter += 1
        self.progress = self.subtask_done_counter*100/self.subtask_total_counter
        if self.subtask_done_counter == self.subtask_total_counter:
            self.statu = 'done'
        else:
            self.statu = 'digging'
        for rawres in rawres_list:
            self.reslist.append(rawres_to_res(rawres))
        # makelog('SubTask done! {}'.format(self.keyword))


class SubTask:
    def __init__(self, task_type: str, keyword: str, page: int, weblink=None):
        self.task_type = task_type
        self.keyword = keyword
        self.page = page
        if weblink == None and task_type == 'ParseTask':
            self.link = 'http://www.baidu.com/s?'
        elif task_type == 'MiniTask':
            self.link = weblink
        else:
            makelog('Task type error!')
            raise
        # makelog('SubTask inited:{}'.format(self.task_type))

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
                'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
                'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
                'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
                'User-Agent, Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            ]

            head = {
                'User-Agent': random.choice(UA)
            }
            r = requests.get(
                link,
                headers=head,
                timeout=5,
                params=params,
                allow_redirects=allow_redirects
            )
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
            # st=time.time()
            sourcecode = get_source_code()
            rawres_list = get_rawres(sourcecode)
            # 找到任务并放入rawres
            CACHE.rawres_upload(self.keyword, rawres_list)
            # now_time=time.time()
            # makelog('MiniTask Done!  {} con_time:{} total_time:{}'.format(self.keyword,now_time-t,now_time-st,))

        def parsetask():
            def get_tags():
                params = {'wd': self.keyword+' 下载',
                          'process_number': int(self.page) * 50, 'rn': 50}

                try:
                    r = net(self.link, params=params)
                    r.encoding = r.apparent_encoding
                    tags = BeautifulSoup(r.text, 'html.parser').find_all(
                        'h3', class_="t")
                except:
                    makelog(traceback.format_exc())
                    tags = []

                return tags

            # 获取标签
            tags = get_tags()
            # 获取链接
            self.weblinklist = [BeautifulSoup(
                str(n), "html.parser").a['href'] for n in tags]
            # 上传SubTask
            CACHE.subtaskqueue_puts(
                self.keyword,
                [
                    SubTask(
                        task_type='MiniTask',
                        keyword=self.keyword,
                        page=self.page,
                        weblink=weblink
                    ) for weblink in self.weblinklist
                ]
            )

        # makelog('{} Start!'.format(self.task_type))

        if self.task_type == 'MiniTask':
            minitask()
        elif self.task_type == 'ParseTask':
            parsetask()
        else:
            makelog('Error unknow task{}'.format(self.task_type))




def makelog(log):
    print(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
        '>>>',log
    )

class Engine:
    def __init__(self, enginetableobj):
        self.name = enginetableobj.name
        self.system = enginetableobj.system
        self.Model = enginetableobj.Model
        self.engineposition = enginetableobj.engineposition
        self.provider = enginetableobj.provider
        self.acttime = 0

    def is_active(self):
        return time.time()-self.acttime < ENGINETIMEGAP

    def act(self):
        self.acttime = time.time()

    def getdict(self):
        return {
            'name': self.name,
            'system': self.system,
            'Model': self.Model,
            'engineposition': self.engineposition,
            'provider': self.provider,
            'cpu': '',
            'cpufrom': '',
            'memory': '',
            'memoryfrom': '',
            'storage': '',
            'storagefrom': '',
            'power': '',
            'powerfrom': '',
            'motherboard': '',
            'motherboardfrom':'',
            'is_active': self.is_active()
        }


class cache:
    def __init__(self, deepth, Egap):
        self.deepth = deepth
        # 主任务
        self.tasklist = []
        # 子任务
        self.subtaskqueue = Queue()

        self.enginelist = [Engine(E) for E in Etable.objects.all()]
        self.resamount = 0
        self.keyamount = 0
        self.commentlist = []
        self.hotkeylist = []
        self.appversion = []
        self.broadcast = []
        self.donorinfo = []

    # 操作函数
    def puttask(self, keyword):
        self.tasklist.append(Task(keyword, self.subtaskqueue))

    def subtaskqueue_empty(self):
        return self.subtaskqueue.empty()

    def subtaskqueue_get(self):
        return self.subtaskqueue.get()

    def subtaskqueue_puts(self, keyword, subtask_list):
        for task in self.tasklist:
            if task.keyword == keyword:
                task.subtask_total_counter+=len(subtask_list)
        for subtak in subtask_list:
            self.subtaskqueue.put(subtak)

    def getresamount(self):
        return self.resamount

    def getkeyamount(self):
        return self.keyamount

    def getenginelist(self):
        return [engine.getdict() for engine in self.enginelist]

    def getcommentlist(self):
        return self.commentlist

    def gethotkeylist(self):
        return self.hotkeylist

    def getappversion(self):
        return self.appversion

    def getbroadcast(self):
        return self.broadcast

    def getdonorinfo(self):
        return self.donorinfo


    
    def gettasklist(self):
        return [task.getdict() for task in self.tasklist]

    def checktaskin(self, keyword):
        keywordlist = []
        for task in self.tasklist:
            keywordlist.append(task.keyword)
        return keyword in keywordlist
    
    def rawres_upload(self,keyword,rawres_list):
        for task in self.tasklist:
            if task.keyword == keyword:
                task.putrawres(rawres_list)
                break        



    # engine

    def activeengine(self, enginename):
        for engine in self.enginelist:
            if engine.name == enginename:
                engine.act()

    #   regular函数

    def updateresamount(self):
        self.resamount = Resourcetable.objects.all().count()

    def updatekeywordamount(self):
        self.keyamount = Keywordtable.objects.all().count()

    def updatecommentlist(self):
        self.commentlist = list(
            Messagetable.objects.order_by('-time')[0:200].values())

    def updatehotkeylist(self):
        self.hotkeylist = list(
            Keywordtable.objects.all().order_by('-hot')[0:50].values())

    def updateappversion(self):
        self.appversion = Appversiontable.objects.order_by('-id').values()[0]

    def updatebroadcast(self):
        self.broadcast = Broadcasttable.objects.order_by('-id').values()[0]

    def updatedonnateinfo(self):
        self.donorinfo = list(
            Donatetable.objects.all().order_by('-donatetime').values())

    def saveres(self):
        # makelog('Save Res:')
        for task in self.tasklist:
            if task.statu == 'done' or (task.statu == 'digging' and time.time() - task.last_active_time >20):
                # 除重
                savereslist = []
                prelinklist = [
                    res.link for res in Resourcetable.objects.filter(keyword=task.keyword)
                    ]
                for res in task.reslist:
                    if res.link not in prelinklist:
                        savereslist.append(res)
                # 储存
                Resourcetable.objects.bulk_create(savereslist)
                # 删除任务
                self.tasklist.remove(task)

    def updatebackground(self):
        imagepath = './static/resdig/background.jpg'
        url = 'https://cn.bing.com/HPImageArchive.aspx'
        data = {
            'n': 1,
            'format': 'js'
        }
        baselink = requests.get(url, data).json()['images'][0]['url']
        link = 'https://cn.bing.com' + baselink
        image = requests.get(link, )
        with open(imagepath, 'wb') as fd:
            fd.write(image.content)

    # 管理函数
    def reloadenginestatu(self):
        self.enginelist = [Engine(E) for E in Etable.objects.all()]

    def operator(self):
        print('-------------Operator--------------')
        # operator here

        # operator done
        print('----------------OJBK---------------')


class reguler():
    def __init__(self, Fname, gap):
        global CACHE
        self.Fname = Fname
        self.gap = gap
        self.acttime = 0

    def act(self):
        nowt = time.time()
        if nowt - self.acttime > self.gap:
            self.acttime = nowt
            F = getattr(CACHE, self.Fname)
            F()





def getcache():
    return cacheobj


class cachemanager(BaseManager):
    pass




if __name__ == '__main__':
    while True:
        makelog('Manager-x 2.0 start!')
        try:
            cacheobj = cache(deepth=DEEPTH, Egap=ENGINETIMEGAP)
            cachemanager.register('cacheobj', getcache)
            manager = cachemanager(address=(host, port), authkey=password)
            manager.start()
            CACHE = manager.cacheobj()
            reguler_list = [
                reguler('saveres', 2),
                reguler('updatecommentlist', 2),
                reguler('updatebroadcast', 10 * 60),
                reguler('updatedonnateinfo', 10 * 60),
                reguler('updateappversion', 60 * 60),
                reguler('updatehotkeylist', 3 * 60 * 60),
                # reguler('updatebackground', 24 * 60 * 60),
                reguler('updateresamount', 24 * 60 * 60),
                reguler('updatekeywordamount', 24 * 60 * 60),
            ]
            makelog('CACHE start sscuessed !')
            while True:
                for reguler in reguler_list:
                    reguler.act()
                    CACHE.getenginelist()
                time.sleep(1)
        except Exception as e:
            makelog('Error in main process! Reboot after 2s !\n{}'.format(traceback.format_exc()))
            time.sleep(2)
