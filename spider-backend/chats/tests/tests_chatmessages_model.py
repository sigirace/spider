from django.test import TestCase
from chats.models import ChatRooms, ChatMessages
from users.models import Users


class ChatMessagesModelTest(TestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user = Users.objects.create_user(
            user_id="testuser@example.com", password="password123", name="Test User"
        )

        # 테스트용 채팅방 생성
        self.chat_room = ChatRooms.objects.create(
            user_id=self.user,
            chat_room_name="Test Chat Room",
            chat_summary="This is a test chat room",
            chat_summary_cnt=10,
        )

        # 테스트용 메시지 생성
        self.chat_message_ai = ChatMessages.objects.create(
            chat_room_id=self.chat_room,
            role=ChatMessages.MessageRoleChoices.AI,
            content="This is an AI message.",
        )

        self.chat_message_human = ChatMessages.objects.create(
            chat_room_id=self.chat_room,
            role=ChatMessages.MessageRoleChoices.HUMAN,
            content="This is a Human message.",
        )

    def test_message_creation(self):
        """메시지가 제대로 생성되었는지 확인"""
        self.assertEqual(self.chat_message_ai.role, "ai")
        self.assertEqual(self.chat_message_ai.content, "This is an AI message.")
        self.assertEqual(self.chat_message_ai.chat_room_id, self.chat_room)

        self.assertEqual(self.chat_message_human.role, "human")
        self.assertEqual(self.chat_message_human.content, "This is a Human message.")
        self.assertEqual(self.chat_message_human.chat_room_id, self.chat_room)

    def test_string_representation(self):
        """__str__ 메서드가 message_id를 반환하는지 확인"""
        self.assertEqual(
            str(self.chat_message_ai), str(self.chat_message_ai.message_id)
        )
        self.assertEqual(
            str(self.chat_message_human), str(self.chat_message_human.message_id)
        )

    def test_related_name(self):
        """ChatRooms 모델에서 related_name을 통해 ChatMessages에 접근하는지 확인"""
        messages = self.chat_room.chatmessages.all()
        self.assertIn(self.chat_message_ai, messages)
        self.assertIn(self.chat_message_human, messages)

    def test_message_role_choices(self):
        """MessageRoleChoices의 옵션이 올바른지 확인"""
        self.assertIn(
            "ai", [choice[0] for choice in ChatMessages.MessageRoleChoices.choices]
        )
        self.assertIn(
            "human", [choice[0] for choice in ChatMessages.MessageRoleChoices.choices]
        )
