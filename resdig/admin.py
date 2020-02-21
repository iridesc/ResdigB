from django.contrib import admin
from .models import Keyword, Res, Engine, Donor, Cast
# Register your models here.
@admin.register(Engine)
class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'system', 'position',
                    'provider')


@admin.register(Keyword)
class keywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'showInRec','digTimes', 'lastDigTime')


@admin.register(Res)
class ResAdmin(admin.ModelAdmin):
    list_display = ('type', 'filename', 'filesize', 'link', 'web')


@admin.register(Cast)
class castAdmin(admin.ModelAdmin):
    list_display = ('online', 'info')


@admin.register(Donor)
class donorAdmin(admin.ModelAdmin):
    list_display = ('time', 'name','info','msg')
