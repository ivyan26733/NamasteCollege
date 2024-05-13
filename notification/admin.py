from django.contrib import admin
from .models import Notification, DComment, DPost, Notif

admin.site.register(Notification)
admin.site.register(DComment)
admin.site.register(DPost)
admin.site.register(Notif)


