from django.contrib import admin
from api.models import *

# Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email']


# class ProfileAdmin(admin.ModelAdmin):
#     list_editable = ['verified']
#     list_display = ['user', 'full_name' ,'verified']

# class TodoAdmin(admin.ModelAdmin):
#     list_editable = ['completed']
#     list_display = ['user', 'title' ,'completed', 'date']
# admin.site.register(User, UserAdmin)
# admin.site.register( Profile,ProfileAdmin)
# admin.site.register( Todo,TodoAdmin)

class ChatMessageAdmin(admin.ModelAdmin):
    # list_editable = ['is_read', 'message']
    # list_display = ['user','sender', 'reciever', 'is_read', 'message']
    list_editable = ['message','sender','room']
    list_display = ['date', 'message','sender', 'room']

class RoomAdmin(admin.ModelAdmin):
    # list_editable = ['room_name']
    list_display = ['room_name']
    # list_display_links = ['room_name']

admin.site.register(ChatMessage,ChatMessageAdmin)

admin.site.register(Room, RoomAdmin)
