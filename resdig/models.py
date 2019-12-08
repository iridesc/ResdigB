from django.db import models
import time
# from django.core.mail import send_mail
from django.conf import settings
# Create your models here.
from django.db import models

class Res(models.Model):
    link = models.CharField(max_length=800)
    web = models.CharField(max_length=300)
    type = models.CharField(max_length=10)
    filename = models.CharField(max_length=200, null=True)
    filesize = models.FloatField(default=0)


class Keyword(models.Model):
    keyword = models.CharField(max_length=90, primary_key=True, db_index=True)
    # 豆瓣电影id
    dbId = models.CharField(max_length=50, default=None)
    # 挖掘的次数
    digTimes = models.IntegerField(default=1)
    lastDigTime = models.FloatField(default=0)
    # 将资源作为外键
    ress = models.ForeignKey(Res,  on_delete=models.CASCADE,)

    def hotPlus(self):
        self.hot = self.hot+1
        self.save()




class Engine(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    system = models.CharField(max_length=30)
    model = models.CharField(max_length=20, default='')
    position = models.CharField(max_length=50)
    provider = models.CharField(default='', max_length=20)


class Feedback(models.Model):
    time = models.FloatField(default=time.time())
    info = models.CharField(max_length=200)


class Msg(models.Model):
    time = models.FloatField(default=time.time())
    info = models.CharField(max_length=200)


class Cast(models.Model):
    online = models.BooleanField(default=True)
    info = models.CharField(max_length=1000)


class Donate(models.Model):
    time = models.FloatField(default=time.time(), primary_key=True)
    donator = models.CharField(max_length=20)
    info = models.CharField(max_length=100, default='Money')
    msg = models.CharField(max_length=100, default='这位是个低调的捐献者!')
