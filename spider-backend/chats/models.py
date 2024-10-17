from django.db import models

from common.models import CommonModel


# Create your models here.
class ChatRooms(CommonModel):
    chat_room_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "users.Users",
        on_delete=models.SET_NULL,
        null=True,
        related_name="chatrooms",
    )
    chat_room_name = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    chat_summary = models.TextField(null=True, blank=True)
    chat_summary_cnt = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.chat_room_id}"

    class Meta:
        db_table = "TB_CHAT_ROOM"
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"


class ChatMessages(CommonModel):
    """ChatMessage Model Definition"""

    class MessageRoleChoices(models.TextChoices):
        AI = "ai", "AI"
        HUMAN = "human", "Human"

    message_id = models.AutoField(primary_key=True)
    # 모델 타입 추가
    chat_room_id = models.ForeignKey(
        ChatRooms,
        on_delete=models.SET_NULL,
        null=True,
        related_name="chatmessages",
    )
    role = models.CharField(
        max_length=10,
        choices=MessageRoleChoices.choices,
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.message_id}"

    class Meta:
        db_table = "TB_CHAT_MESSAGE"
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
