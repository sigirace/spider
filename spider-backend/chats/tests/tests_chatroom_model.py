from django.test import TestCase
from chats.models import ChatRooms
from users.models import Users


class ChatRoomsModelTest(TestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user = Users.objects.create_user(
            user_id="testuser@example.com", password="password123", name="Test User"
        )

        # 기본 채팅방 생성
        self.chat_room = ChatRooms.objects.create(
            user_id=self.user,
            chat_room_name="Test Chat Room",
            chat_summary="This is a test chat room",
            chat_summary_cnt=10,
        )

    def test_chat_room_creation(self):
        """채팅방이 제대로 생성되었는지 확인"""
        self.assertEqual(self.chat_room.chat_room_name, "Test Chat Room")
        self.assertEqual(self.chat_room.chat_summary, "This is a test chat room")
        self.assertEqual(self.chat_room.chat_summary_cnt, 10)
        self.assertEqual(self.chat_room.is_deleted, False)
        self.assertEqual(self.chat_room.user_id, self.user)

    def test_string_representation(self):
        """__str__ 메서드가 제대로 작동하는지 확인"""
        self.assertEqual(str(self.chat_room), str(self.chat_room.chat_room_id))

    def test_soft_delete(self):
        """is_deleted 필드를 사용하여 soft delete가 제대로 작동하는지 확인"""
        self.chat_room.is_deleted = True
        self.chat_room.save()
        self.assertTrue(self.chat_room.is_deleted)

    def test_update_chat_summary(self):
        """채팅 요약 및 요약 개수를 업데이트하는 기능 확인"""
        self.chat_room.chat_summary = "Updated summary"
        self.chat_room.chat_summary_cnt = 5
        self.chat_room.save()

        self.assertEqual(self.chat_room.chat_summary, "Updated summary")
        self.assertEqual(self.chat_room.chat_summary_cnt, 5)

    def test_null_user_id(self):
        """user_id가 null일 때 제대로 처리되는지 확인"""
        chat_room = ChatRooms.objects.create(
            user_id=None,
            chat_room_name="Orphaned Chat Room",
            chat_summary="This room has no user",
            chat_summary_cnt=0,
        )
        self.assertIsNone(chat_room.user_id)
        self.assertEqual(chat_room.chat_room_name, "Orphaned Chat Room")

    def test_blank_chat_room_name(self):
        """chat_room_name이 공백일 때 동작 확인"""
        chat_room = ChatRooms.objects.create(
            user_id=self.user,
            chat_room_name="",
            chat_summary="This is a chat room with no name",
            chat_summary_cnt=1,
        )
        self.assertEqual(chat_room.chat_room_name, "")

    def test_blank_chat_summary(self):
        """chat_summary가 공백일 때 동작 확인"""
        chat_room = ChatRooms.objects.create(
            user_id=self.user,
            chat_room_name="Chat Room No Summary",
            chat_summary="",
            chat_summary_cnt=0,
        )
        self.assertEqual(chat_room.chat_summary, "")

    def test_default_chat_summary_cnt(self):
        """chat_summary_cnt의 기본값이 0인지 확인"""
        chat_room = ChatRooms.objects.create(
            user_id=self.user,
            chat_room_name="New Chat Room",
            chat_summary="Summary with default count",
        )
        self.assertEqual(chat_room.chat_summary_cnt, 0)

    def test_maximum_chat_summary_cnt(self):
        """chat_summary_cnt에 최대값을 설정하여 동작 확인"""
        chat_room = ChatRooms.objects.create(
            user_id=self.user,
            chat_room_name="Max Count Room",
            chat_summary="Summary with max count",
            chat_summary_cnt=10000,
        )
        self.assertEqual(chat_room.chat_summary_cnt, 10000)
