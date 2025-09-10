from django.contrib import admin

# Register your models here.
from .models import CampUser, TeamProfile, PointRecord, CommentBoard

class CampUserAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__','role')
class TeamProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__','user','current_points')
class PointRecordAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__','team','change','reason')
class CommentBoardAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__','user','comment','pos')

# Register your models here.
admin.site.register(CampUser,CampUserAdmin)
admin.site.register(TeamProfile,TeamProfileAdmin)
admin.site.register(PointRecord,PointRecordAdmin)
admin.site.register(CommentBoard,CommentBoardAdmin)