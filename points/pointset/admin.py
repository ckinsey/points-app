from django.contrib import admin

from pointset.models import PointSet

# Register your models here.
class PointSetAdmin(admin.ModelAdmin):
    pass

admin.site.register(PointSet, PointSetAdmin)