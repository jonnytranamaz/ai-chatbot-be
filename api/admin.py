from django.contrib import admin
from api.models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'content', 'timestamp', 'message_type']

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'created_at']

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['telephone', 'fullname', 'age']

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Message, MessageAdmin)

admin.site.register(Conversation, ConversationAdmin)

