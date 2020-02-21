from django.db import models
import time

# from django.core.mail import send_mail
from django.conf import settings

# Create your models here.
from django.db import models



class Keyword(models.Model):
    keyword = models.CharField(max_length=90, primary_key=True, db_index=True)

    # rec contro
    showInRec = models.BooleanField(default=True)

    # 挖掘的次数
    digTimes = models.IntegerField(default=0)
    lastDigTime = models.FloatField(default=time.time())

    # visit static
    visitTimes = models.IntegerField(default=0)
    lastVisitTime = models.FloatField(default=time.time())

    def udVisitTimeAndTimes(self):
        self.lastVisitTime = time.time()
        self.visitTimes = self.visitTimes + 1
        self.save()

    def udDigTimeAndTimes(self):
        self.lastDigTime = time.time()
        self.digTimes = self.digTimes + 1
        self.save()

class Res(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, db_index=True)
    link = models.CharField(max_length=800)
    web = models.CharField(max_length=300)
    type = models.CharField(max_length=10)
    filename = models.CharField(max_length=200, null=True)
    filesize = models.FloatField(default=0)


class Engine(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    system = models.CharField(max_length=30)
    model = models.CharField(max_length=20, default="")
    position = models.CharField(max_length=50)
    provider = models.CharField(default="", max_length=20)


class Cast(models.Model):
    online = models.BooleanField(default=True)
    info = models.CharField(max_length=1000)


class Donor(models.Model):
    time = models.FloatField(default=time.time(), primary_key=True)
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100, default="Money")
    msg = models.CharField(max_length=100, default="这位是个低调的捐献者!")
