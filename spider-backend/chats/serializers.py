from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import ChatRooms, ChatMessages
from users.serializers import TinyUserSerializers


class ChatRoomListSerializer(ModelSerializer):

    class Meta:
        model = ChatRooms
        fields = (
            "chat_room_id",
            "chat_room_name",
            "chat_summary",
            "created_at",
        )


class ChatRoomDetailSerializer(ModelSerializer):

    class Meta:
        model = ChatRooms
        exclude = ["is_deleted"]
        read_only_fields = [
            "chat_room_name",
            "chat_summary",
            "chat_summary_cnt",
        ]


class ChatMessageListSerializer(ModelSerializer):
    sender_id = SerializerMethodField()

    class Meta:
        model = ChatMessages
        fields = (
            "message_id",
            "role",
            "content",
            "sender_id",
            "created_at",
        )

    def get_sender_id(self, obj):
        if obj.role == "human":
            return str(obj.chat_room_id.user_id)
        else:
            return str(obj.role)


class ChatMessageDetailSerializer(ModelSerializer):

    chat_room_id = ChatRoomListSerializer(read_only=True)

    class Meta:
        model = ChatMessages
        fields = "__all__"
        read_only_fields = [
            "role",
        ]
