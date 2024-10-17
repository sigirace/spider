from django.contrib import admin
from .models import ChatRooms, ChatMessages


@admin.register(ChatRooms)
class ChatRoomsAdmin(admin.ModelAdmin):
    list_display = ("chat_room_id", "chat_room_name", "is_deleted", "chat_summary")
    search_fields = ("chat_room_name",)
    list_filter = ("is_deleted",)


@admin.register(ChatMessages)
class ChatMessagesAdmin(admin.ModelAdmin):
    list_display = ("message_id", "chat_room_id", "role", "content")
    search_fields = ("content",)
    list_filter = ("role",)
