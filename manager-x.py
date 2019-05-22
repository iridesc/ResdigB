import django,os,sys,time,traceback,json,base64,requests
from multiprocessing.managers import BaseManager
from urllib import parse

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ocolab.settings")
django.setup()
from resdig.models import Resourcetable,Etable,Keywordtable,Messagetable,Appversiontable,Broadcasttable,Donatetable

#linux
host='0.0.0.0'
#windows
#host='127.0.0.1'

port=23333
password=b'iridescent256938004'
deepth=10
Egap=15


def linkparser(parselink):
    def base64decode(link):
        link = link.split('//')[1]
        example = base64.b64decode(link)
        for i in ['utf-8', 'gbk', 'ascii', 'gb2312', 'GB18030', 'iso8859-1', 'utf-16', ]:
            try:
                example = example.decode(encoding=i)[2:][:-2]
                return example
            except:
                pass

    parselink = parse.unquote(parselink)
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
            filename, size = linkparser(base64decode(parselink))
            pass
    except Exception as e:
        pass
    return filename, size


class res():
    def __init__(self,Pres,keyword,):
        self.link=Pres[0]
        self.web=Pres[1]
        self.type=Pres[2]
        self.keyword=keyword
    #manager
    def Resource(self):
        filename,filesize=linkparser(self.link)
        return Resourcetable(keyword=self.keyword,link=self.link,web=self.web,type=self.type,filename=filename,filesize=filesize/1024**2)

class task():
    def __init__(self, keyword, deepth,Egap):
        self.keyword = keyword
        self.deepth=deepth
        self.Egap=Egap
        self.statu='waiting'
        self.progress = 0
        self.reslist=[]
        self.kidslist = [kid(keyword=keyword,page=i,Egap=Egap) for i in range(deepth)]
    #manager
    def sumprogress(self):
        progress=0
        for kid in self.kidslist:
            progress=progress+kid.progress
        self.progress=progress/self.deepth
    #manager
    def checkstatu(self):
        statulist=[kid.statu for kid in self.kidslist]
        if 'digging' in statulist:
            self.statu='digging'
        elif 'waiting' not in statulist and 'digging' not in statulist:
            self.statu='done'

    #engine
    def putres(self,Preslist):
        for Pres in Preslist:
            self.reslist.append(res(Pres,self.keyword))
    def getdict(self):
        return {
            'keyword':self.keyword,
            'taskstatu':self.statu,
            'progress':self.progress,
            'statu':self.statu
        }
        pass

class kid():
    def __init__(self, keyword,page,Egap):
        self.keyword=keyword
        self.page = page
        self.Egap=Egap
        self.progress = 0

        self.lastacttime=0
        self.statu='waiting'
    #engine
    def active(self):
        self.lastacttime=time.time()
    #engine
    def is_active(self):
        return time.time()-self.lastacttime<self.Egap

class engine():
    def __init__(self,enginetableobj,Egap):
        self.Egap=Egap
        self.name=enginetableobj.name
        self.system = enginetableobj.system
        self.Model = enginetableobj.Model
        self.engineposition = enginetableobj.engineposition
        self.provider = enginetableobj.provider
        self.cpu = enginetableobj.cpu
        self.cpufrom = enginetableobj.cpufrom
        self.memory = enginetableobj.memory
        self.memoryfrom = enginetableobj.memoryfrom
        self.storage = enginetableobj.storage
        self.storagefrom = enginetableobj.storagefrom
        self.power = enginetableobj.power
        self.powerfrom = enginetableobj.powerfrom
        self.motherboard = enginetableobj.motherboard
        self.motherboarefrom = enginetableobj.motherboardfrom
        self.acttime = 0
    def is_active(self):
        return time.time()-self.acttime<self.Egap
    def act(self):
        self.acttime=time.time()
    def getdict(self):
        return {
            'name': self.name,
            'system': self.system,
            'Model': self.Model,
            'engineposition': self.engineposition,
            'provider': self.provider,
            'cpu': self.cpu,
            'cpufrom': self.cpufrom,
            'memory': self.memory,
            'memoryfrom': self.memoryfrom,
            'storage': self.storage,
            'storagefrom': self.storagefrom,
            'power': self.power,
            'powerfrom': self.powerfrom,
            'motherboard': self.motherboard,
            'motherboardfrom': self.motherboarefrom,
            'is_active':self.is_active()
        }

class cache():
    def __init__(self,deepth,Egap):
        self.deepth=deepth
        self.Egap=Egap
        self.tasklist = []
        self.enginelist = [engine(E,self.Egap) for E in Etable.objects.all()]
        self.resamount=0
        self.keyamount=0
        self.commentlist=[]
        self.hotkeylist=[]
        self.appversion=[]
        self.broadcast=[]
        self.donorinfo=[]

    # 操作函数
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
        return [task.getdict() for  task in  self.tasklist]
    def puttask(self,keyword):
        self.tasklist.append(task(keyword,self.deepth,self.Egap))
    def checktaskin(self,keyword):
        keywordlist=[]
        for task in self.tasklist:
            keywordlist.append(task.keyword)
        return keyword in keywordlist
    ##engine
    def activeengine(self, enginename):
        for engine in self.enginelist:
            if engine.name == enginename:
                engine.act()
    def gettask(self,enginename):
        self.activeengine(enginename)
        for task in self.tasklist:
            for kid in task.kidslist:
                if not kid.is_active() and kid.statu!='done':
                    kid.active()
                    kid.statu = 'digging'
                    return kid
    def updateprogress(self,enginename,keyword,page,progress):
        self.activeengine(enginename)
        for task in self.tasklist:
            if task.keyword==keyword:
                for kid in task.kidslist:
                    if kid.page==page:
                        kid.active()
                        kid.progress=progress
    def postres(self,enginename,keyword,page,preslist):
        self.activeengine(enginename)
        for task in self.tasklist:
            if task.keyword==keyword:
                # 缓存资源
                for pres  in  preslist:
                    task.reslist.append(res(pres,keyword))
                #标记kid完成
                for kid in task.kidslist:
                    if kid.page==page:
                        kid.statu='done'
                        kid.progress=100

    #   regular函数

    def updateresamount(self):
        self.resamount = Resourcetable.objects.all().count()

    def updatekeywordamount(self):
        self.keyamount = Keywordtable.objects.all().count()

    def updatecommentlist(self):
        self.commentlist = list(Messagetable.objects.order_by('-time')[0:200].values())

    def updatehotkeylist(self):
        self.hotkeylist=list(Keywordtable.objects.all().order_by('-hot')[0:50].values())

    def updateappversion(self):
        self.appversion= Appversiontable.objects.order_by('-id').values()[0]

    def updatebroadcast(self):
        self.broadcast = Broadcasttable.objects.order_by('-id').values()[0]

    def updatedonnateinfo(self):
        self.donorinfo=list(Donatetable.objects.all().order_by('-donatetime').values())

    def saveres(self):
        for task in self.tasklist:
            if task.statu == 'done':
                #除重
                savereslist=[]
                prelinklist = [res.link for res in Resourcetable.objects.filter(keyword=task.keyword)]
                for res in task.reslist:
                    if res.link not in prelinklist:
                        prelinklist.append(res.link)
                        savereslist.append(res.Resource())
                #储存
                Resourcetable.objects.bulk_create(savereslist)
                # 删除任务
                self.tasklist.remove(task)

    def managetask(self):
        for task in self.tasklist:
            task.checkstatu()
            if task.statu=='digging':
                task.sumprogress()

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

    #管理函数
    def reloadenginestatu(self):
        self.enginelist = [engine(E,self.Egap) for E in Etable.objects.all()]
    def operator(self):
        print('-------------Operator--------------')
        ##operator here

        ##operator done
        print('----------------OJBK---------------')

class reguler():
    def __init__(self, Fname, gap):
        self.Fname = Fname
        self.gap = gap
        self.acttime = 0

    def act(self, cache):
        nowt = time.time()
        if nowt - self.acttime > self.gap:
            self.acttime = nowt
            F = getattr(cache, self.Fname)
            F()

cacheobj=cache(deepth=deepth,Egap=Egap)
def getcache():
    return cacheobj
class cachemanager(BaseManager):
    pass
cachemanager.register('cacheobj',getcache)
manager=cachemanager(address=(host, port), authkey=password)

if __name__ == '__main__':
    try:

        manager.start()
        cache = manager.cacheobj()
        reguler_list = [
            reguler('managetask',2),
            reguler('saveres', 2),
            reguler('updatecommentlist', 2),
            reguler('updatebroadcast', 10 * 60),
            reguler('updatedonnateinfo', 10 * 60),
            reguler('updateappversion', 60 * 60),
            reguler('updatehotkeylist', 3 * 60 * 60),
            reguler('updatebackground', 24 * 60 * 60),
            reguler('updateresamount', 24 * 60 * 60),
            reguler('updatekeywordamount', 24 * 60 * 60),
        ]

        while True:
            for reguler in reguler_list:
                reguler.act(cache)
                cache.getenginelist()
            time.sleep(1)
    except Exception as e:
        with open('manager-x.log','a') as f:
            f.write('---------------------'+
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+
                    '---------------------\n'+traceback.format_exc()
                    )
