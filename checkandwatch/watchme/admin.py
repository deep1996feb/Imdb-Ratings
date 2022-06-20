from django.contrib import admin
from .models import Review, Watch_List, StreamPlatform, Review
# Register your models here.

admin.site.register(Watch_List)
admin.site.register(StreamPlatform)
admin.site.register(Review)
