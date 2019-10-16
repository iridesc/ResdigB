from django.contrib import admin
from .models import Etable, Keywordtable, Errotable, Feedbacktable, Messagetable, Appversiontable, Broadcasttable, Donatetable, Resourcetable

# Register your models here.
@admin.register(Etable)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'Model', 'system', 'engineposition',
                    'engineposition', 'provider')


@admin.register(Keywordtable)
class keywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'hot', 'cantfind', 'lastdigtime')


@admin.register(Resourcetable)
class ResAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'type', 'filename', 'filesize', 'link', 'web')


@admin.register(Messagetable)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('time', 'message', 'messagefrom')


@admin.register(Feedbacktable)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('time', 'message', 'messagefrom', 'mail', 'phone')


@admin.register(Appversiontable)
class AppversionAdmin(admin.ModelAdmin):
    list_display = ('updatetime', 'versioncode',
                    'versionname', 'describe', 'downloadlink')


@admin.register(Broadcasttable)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('casttime', 'servicestatus', 'message')


@admin.register(Donatetable)
class DonatetAdmin(admin.ModelAdmin):
    list_display = ('donatetime', 'donator',
                    'donatetype', 'describe', 'message')
