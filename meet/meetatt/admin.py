from django.contrib import admin
from .models import  Postpdf,Folder,Class,Contact
# Register your models here.
@admin.register(Postpdf)
class PostpdfAdmin(admin.ModelAdmin):
    pass
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact)
admin.site.register(Folder)