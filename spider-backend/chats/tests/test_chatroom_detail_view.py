from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from chats.models import ChatMessages, ChatRooms
from users.models import Users


class ChatRoomDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Users.objects.create_user(
            user_id="testuser@example.com", password="password123", name="Test User"
        )
        self.chat_room = ChatRooms.objects.create(
            user_id=self.user,
        )
        self.message_human = ChatMessages.objects.create(
            chat_room_id=self.chat_room, content="Hello AI", role="human"
        )
        self.message_ai = ChatMessages.objects.create(
            chat_room_id=self.chat_room, content="Hello Human", role="ai"
        )
        self.url = reverse("chatRoomDetail", args=[self.chat_room.chat_room_id])

    def test_get_chat_room_detail(self):
        """GET 요청으로 모든 채팅방 조회"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_chat_room_name(self):
        """PUT 요청으로 채팅방 이름 변경"""
        data = {"task": "naming", "chat_room_name": "Updated Room Name"}

        # 채팅방에 메세지가 존재하는지 확인
        self.assertTrue(self.message_human.content)
        self.assertTrue(self.message_ai.content)

        response = self.client.put(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.chat_room.refresh_from_db()
        self.assertTrue(self.chat_room.chat_room_name)

    def test_delete_chat_room(self):
        """DELETE 요청으로 채팅방 삭제"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.chat_room.refresh_from_db()
        self.assertTrue(self.chat_room.is_deleted)

    def test_get_nonexistent_chat_room(self):
        """존재하지 않는 채팅방을 조회할 때 NotFound 오류 발생"""
        url = reverse("chatRoomDetail", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
