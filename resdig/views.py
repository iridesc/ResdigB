from django.shortcuts import render
from .models import Keyword

# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
from AesEverywhere import aes256
import base64
from initManager import initManager
from .models import Keyword, Res, Engine, Donor, Cast
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
)
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import time
import re
import sys
import os, traceback
import random
from django.conf import settings
from django.core.mail import send_mail
from loger import makelog, setting

# Create your views here.
setting(2)
PASSWORD = "q863cqfiwyug72jc"


def xssClear(s):
    os = s
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace("'", "&#39;")
    s = s.replace('"', "&quot;")
    makelog("xssClear: " + os + " -> " + s)
    return s


def modifyKeyword(keyword: str):
    return re.sub(r"(^\s)|(\s$)", "", re.sub(r"\s+", " ", keyword))


def home(request, movieName="Resdig"):
    # server render
    recs = list(
        Keyword.objects.filter(showInRec="True")
        .filter(visitTimes__gt=1)
        .order_by("?")[0:500]
        .values()
    )

    return HttpResponse(
        render(request, "index.html", {"keyword": movieName, "recs": recs})
    )


def api(request):
    if request.method == "POST":
        try:
            # 请求的获取与解析
            byte = aes256.decrypt(request.body, PASSWORD)
            postdata = json.loads(str(byte, encoding="utf-8", errors="ignore"))
            makelog(str(postdata))

            # 获取reason
            reason = postdata["reason"]
            # 链接到缓存
            cache = initManager(password="iridescent256938004")
            # 动态数据请求
            if reason == "getDynamicData":
                data = cache.getDynamicData()

            # 静态数据请求
            elif reason == "getStaticData":
                data = cache.getStaticData()
                # makelog(str(data),2)

            # 检查关键字的状态（digging，recorded->getRess/dig，notRecord->dig）
            elif reason == "checkKeyword":
                keyword = postdata["keyword"]
                # makelog(keyword)
                # 检查是否在任务列表
                if cache.checkTaskIn(keyword):
                    data = {"status": "digging"}
                else:
                    # 检查是否有记录
                    try:
                        KW = Keyword.objects.get(keyword=keyword)
                        data = {}
                        data["status"] = "recorded"
                        # 检查资源数量
                        data["resAmount"] = KW.res_set.all().count()
                        # 最后一次检查时间
                        data["lastDigTime"] = KW.lastDigTime
                        # 挖掘次数
                        data["digTimes"] = KW.digTimes
                    except Exception as e:
                        makelog(str(e))
                        data = {"status": "notRecord"}

            # 获取关键字资源
            elif reason == "getRess":
                keyword = postdata["keyword"]
                try:
                    # 获取到关键字
                    KW = Keyword.objects.get(keyword=keyword)
                    # 热度增加
                    KW.udVisitTimeAndTimes()
                    # 获取资源
                    data = {"suc": True, "ress": list(KW.res_set.all().values())}
                except:
                    data = {"suc": False}
            # 挖掘
            elif reason == "dig":

                def checkRecordedAndTimelock(keyword):
                    # 检查是否有记录
                    try:
                        KW = Keyword.objects.get(keyword=keyword)
                        makelog(str(KW.lastDigTime))
                        return True, time.time() - KW.lastDigTime < 24 * 3600, KW
                    except Exception as e:
                        makelog(str(e), 1)
                        print(type(e))
                        return False, False, None

                keyword = modifyKeyword(xssClear(postdata["keyword"]))
                # 判断关键字是否合法
                makelog("判断关键字是否合法")
                if len(keyword) > 0 and len(keyword) <= 50:
                    # 检查是否在任务列表
                    makelog("检查是否在任务列表")

                    if cache.checkTaskIn(keyword):
                        data = {"suc": False, "reason": "inTasks"}
                        makelog("Task in!", 4)
                    else:
                        recorded, timelock, KW = checkRecordedAndTimelock(keyword)
                        makelog("检查是否有记录")
                        if recorded:
                            makelog("检查时间锁")
                            if timelock:
                                data = {
                                    "suc": False,
                                    "reason": "timeLocked",
                                    "lastDigTime": KW.lastDigTime,
                                }
                                makelog("locked")
                            else:
                                cache.puttask(keyword)
                                # 更新搜索时间
                                KW.udDigTimeAndTimes()

                                data = {"suc": True}
                                makelog("Not lock", 4)

                        else:
                            cache.puttask(keyword)
                            # 更新搜索时间
                            KW = Keyword(keyword=keyword)
                            KW.udDigTimeAndTimes()

                            data = {"suc": True}
                            makelog("Not recorde!", 4)
                else:
                    data = {"suc": False, "reson": "keywordInvalid"}
                    makelog("keywordInvalid", 4)

            # elif reason == "sendFeedback":
            #     info = xssClear(postdata["info"])
            #     makelog("检查信息是否合法")
            #     if 0 < len(info) and len(info) <= 500:
            #         try:
            #             Feedback(time=time.time(), info=info).save()
            #             data = {"suc": True}
            #             makelog("save suc!")
            #         except Exception as e:
            #             data = {
            #                 "suc": False,
            #             }
            #             makelog("save faile!\n" + str(e), 1)
            #     else:
            #         data = {"suc": False, "reason": "lenInvalid"}
            #         makelog("信息非法！")

            # elif reason == "sendMsg":
            #     info = xssClear(postdata["info"])
            #     makelog("检查信息是否合法")
            #     if 0 < len(info) and len(info) <= 200:
            #         try:
            #             Msg(time=time.time(), info=info).save()
            #             data = {"suc": True}
            #             makelog("save suc!")
            #         except Exception as e:
            #             data = {
            #                 "suc": False,
            #             }
            #             makelog("save faile!\n" + str(e), 1)
            #     else:
            #         data = {"suc": False, "reason": "lenInvalid"}
            #         makelog("信息非法！")

            else:
                data = {"suc": False}
                makelog("unknow reason", 1)

            data = aes256.encrypt(json.dumps(data), PASSWORD)
            return HttpResponse(data)
        except Exception as E:
            makelog("Main error in api\n" + str(E), 1)
            makelog(traceback.format_exc())
            e_data_str = str(request.body, encoding="utf-8", errors="ignore")
            makelog(e_data_str)

            return HttpResponseBadRequest()
    else:
        makelog("wrong method!", 1)
        e_data_str = str(request.body, encoding="utf-8", errors="ignore")
        makelog(e_data_str,)
        return HttpResponseBadRequest()
