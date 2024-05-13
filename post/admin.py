from django.contrib import admin
from post.models import Post, Tag, Follow, Events, Stream, Feedback, Professor, Placement, Notes, Events, Alumni, Student_Placed, Report

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Professor)
admin.site.register(Placement)
admin.site.register(Notes)
admin.site.register(Events)
admin.site.register(Alumni)


admin.site.register(Feedback)
admin.site.register(Student_Placed)
admin.site.register(Report)





