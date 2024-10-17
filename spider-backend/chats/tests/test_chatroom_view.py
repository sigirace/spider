from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from chats.models import ChatRooms
from users.models import Users


class ChatRoomViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            user_id="testuser@example.com", password="password123", name="Test User"
        )
        self.url = reverse("chatRoom")

    def test_get_chat_rooms(self):
        """GET 요청으로 모든 채팅방을 조회"""
        ChatRooms.objects.create(user_id=self.user, chat_room_name="Test Room 1")
        ChatRooms.objects.create(user_id=self.user, chat_room_name="Test Room 2")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_chat_room(self):
        """POST 요청으로 새로운 채팅방을 생성"""
        data = {"user_id": self.user.user_id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRooms.objects.count(), 1)
        self.assertEqual(ChatRooms.objects.get().chat_room_name, None)

    def test_create_chat_room_invalid_data(self):
        """유효하지 않은 데이터로 POST 요청"""
        data = {
            "chat_room_id": 10,
            "chat_room_name": "New Chat Room",
            "chat_summary": 10,
            "chat_summary_cnt": 10,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertNotEqual(response.data["chat_room_id"], data["chat_room_id"])
        self.assertNotEqual(response.data["chat_room_name"], data["chat_room_name"])
        self.assertNotEqual(response.data["chat_summary"], data["chat_summary"])
        self.assertNotEqual(response.data["chat_summary_cnt"], data["chat_summary_cnt"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
