from django.db import models
import time
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.
from django.db import models



class Resourcetable(models.Model):
    keyword = models.CharField(max_length=90,db_index=True)
    link = models.CharField(max_length=800)
    web = models.CharField(max_length=300)
    type = models.CharField(max_length=10)
    filename = models.CharField(max_length=200,null=True)
    filesize=models.FloatField(default=0)
    scantime = models.FloatField(default=time.time())


class Keywordtable(models.Model):
    keyword = models.CharField(max_length=90, primary_key=True,db_index=True)
    hot = models.IntegerField(default=1)
    cantfind = models.BooleanField(default=False)
    lastdigtime=models.FloatField(default=time.time())
    def hotplus(self):
        self.hot=self.hot+1
        self.save()

class Etable(models.Model):
    name = models.CharField(max_length=25, primary_key=True)

    system = models.CharField(max_length=30)
    Model=models.CharField(max_length=20,default='')
    engineposition=models.CharField(max_length=50)

    provider=models.CharField(default='',max_length=20)

    # cpu=models.CharField(max_length=20,default='')
    # cpufrom=models.CharField(max_length=20,default='')

    # memory=models.CharField(max_length=20,default='')
    # memoryfrom=models.CharField(max_length=20,default='')

    # storage = models.CharField(max_length=20, default='')
    # storagefrom = models.CharField(max_length=20, default='')

    # power=models.CharField(max_length=20,default='')
    # powerfrom=models.CharField(max_length=20,default='')

    # motherboard=models.CharField(max_length=20,default='')
    # motherboardfrom=models.CharField(max_length=20,default='')



class Feedbacktable(models.Model):
    time=models.FloatField(default=time.time())
    messagefrom=models.CharField(max_length=20,default='unknow')
    mail=models.EmailField(default='resdig@qq.com')
    phone=models.CharField(max_length=12,default=None)
    message=models.CharField(max_length=200)

class Messagetable(models.Model):
    time=models.FloatField(default=time.time())
    messagefrom=models.CharField(max_length=20,default='unknow')
    message=models.CharField(max_length=200)

# class Errotable(models.Model):
#     errotype = models.CharField(db_index=True,max_length=20)
#     errotime = models.FloatField(primary_key=True)
#     message = models.CharField(max_length=2000)
#     sendmail = models.BooleanField(default=False)
#     def send(self,emaliset):
#         try:
#             statu=send_mail(self.errotype,self.message,settings.DEFAULT_FROM_EMAIL, emaliset,)
#             if statu:
#                 self.sendmail=True
#                 self.save()
#             else:
#                 print('send mail erro!!')
#         except:
#             print('send mail erro!!')

class Appversiontable(models.Model):
    versioncode=models.IntegerField(default=0)
    versionname = models.FloatField(default=0)
    describe=models.CharField(max_length=500)
    updatetime=models.FloatField(default=time.time())
    downloadlink=models.CharField(max_length=100,default='')

class Broadcasttable(models.Model):
    casttime=models.FloatField(default=time.time())
    servicestatus=models.BooleanField(default=True)
    message=models.CharField(max_length=200)

class Donatetable(models.Model):
    donatetime=models.FloatField(default=time.time(),primary_key=True)
    donator=models.CharField(max_length=20)
    donatetype=models.CharField(max_length=10,default='Money')
    describe = models.CharField(max_length=50)
    message=models.CharField(max_length=100,default='这位是个低调的捐献者!')
