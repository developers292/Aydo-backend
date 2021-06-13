from django.contrib import admin
from .models import Province, City



@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(City)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'province']
    