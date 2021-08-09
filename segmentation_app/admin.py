from django.contrib import admin

# Register your models here.
from . models import UploadModel,HCModel
admin.site.register(UploadModel)
admin.site.register(HCModel)