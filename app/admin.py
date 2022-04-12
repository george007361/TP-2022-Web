from django.contrib import admin

# Register your models here.all


from app.models import *


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
# admin.site.register(Rating)
admin.site.register(Tag)