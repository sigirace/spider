from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from chats.models import ChatRooms, ChatMessages
from users.models import Users
from django.conf import settings


class ChatMessagesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            user_id="testuser@example.com", password="password123", name="Test User"
        )
        self.chat_room = ChatRooms.objects.create(
            user_id=self.user, chat_room_name="Test Room"
        )
        self.url = reverse("chatMessages", args=[self.chat_room.chat_room_id])

    def test_get_chat_messages(self):
        """GET 요청으로 특정 채팅방의 메시지 조회"""
        ChatMessages.objects.create(
            chat_room_id=self.chat_room, role="human", content="Hello!"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_human_message(self):
        """POST 요청으로 사람의 메시지를 채팅방에 추가"""
        data = {"content": "Hello, AI!"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(ChatMessages.objects.count(), 1)

    def test_post_message_without_content(self):
        """빈 content로 POST 요청하면 오류 반환"""
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_messages_pagination(self):
        """메시지 pagination 테스트"""
        window_size = settings.CHAT_MESSAGE_WINDOW_SIZE

        for i in range(window_size * 2):
            ChatMessages.objects.create(
                chat_room_id=self.chat_room, role="human", content=f"Message {i+1}"
            )
        # 첫 페이지 메시지 조회
        response = self.client.get(f"{self.url}?num=1")
        self.assertEqual(len(response.data), window_size)

        # 두 번째 페이지 메시지 조회
        response = self.client.get(f"{self.url}?num=2")
        self.assertEqual(len(response.data), window_size)
