from django.contrib import admin
from .models import Keyword, Res, Engine, Donate, Msg, Feedback, Cast
# Register your models here.
@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'system', 'position',
                    'provider')


@admin.register(Keyword)
class keywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'dbId', 'digTimes', 'lastDigTime')


@admin.register(Res)
class ResAdmin(admin.ModelAdmin):
    list_display = ('type', 'filename', 'filesize', 'link', 'web')


@admin.register(Msg)
class MsgAdmin(admin.ModelAdmin):
    list_display = ('time', 'info')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('time', 'info')


@admin.register(Cast)
class BroadcastAdmin(admin.ModelAdmin):
    list_display = ('online', 'info')


@admin.register(Donate)
class DonatetAdmin(admin.ModelAdmin):
    list_display = ('time', 'donator','info','msg')
