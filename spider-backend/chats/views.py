from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    APIException,
)
from chats.serializers import (
    ChatMessageDetailSerializer,
    ChatMessageListSerializer,
    ChatRoomDetailSerializer,
    ChatRoomListSerializer,
)
from chats.tasks import process_ai_response
from common.utils import make_new_line
from .models import ChatRooms, ChatMessages
from django.conf import settings
from django.db.models import Max
from llms.apps import chain


class ChatRoomView(APIView):

    def get(self, request):
        chat_rooms = ChatRooms.objects.filter(
            is_deleted=False,
        ).order_by("-chat_room_id")
        serializer = ChatRoomListSerializer(
            chat_rooms,
            many=True,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatRoomDetailSerializer(data=request.data)

        if serializer.is_valid():
            try:
                chat_room = serializer.save()
                serializer = ChatRoomDetailSerializer(chat_room)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                raise APIException(detail=str(e))
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChatRoomDetailView(APIView):

    def get_object(self, chat_room_id):
        try:
            return ChatRooms.objects.get(chat_room_id=chat_room_id, is_deleted=False)
        except ChatRooms.DoesNotExist:
            raise NotFound(detail="chat room not found")

    def get(self, request, chat_room_id):
        chat_room = self.get_object(chat_room_id)

        serializer = ChatRoomDetailSerializer(chat_room)
        return Response(
            data={"result": serializer.data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, chat_room_id):
        chat_room = self.get_object(chat_room_id)
        task = request.data.get("task")

        if not task:
            raise ParseError(detail="task is required")
        else:
            if task not in ("memorizing", "naming"):
                raise ParseError(detail="task must be memorizing or naming")

        serializer = ChatRoomDetailSerializer(
            chat_room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():

            if task == "naming":
                ## 최근 1턴의 대화를 가져옴
                history_messages = chat_room.chatmessages.order_by("-message_id")[:2]
                new_line = make_new_line(history_messages)
                room_name = chain.naming(new_line)
                chat_room.chat_room_name = room_name

            elif task == "memorizing":
                summary = chat_room.chat_summary
                now_summary_cnt = chat_room.chat_summary_cnt
                history_messages = chat_room.chatmessages.filter(
                    message_id__gt=now_summary_cnt
                ).order_by("-message_id")

                # 현재 요약보다 3턴(6개의 메시지) 더 대화를 한 경우에 요약 진행
                if history_messages.count() >= 6:
                    new_line = make_new_line(history_messages)

                    history_summary = chain.summary(summary=summary, new_line=new_line)
                    chat_room.chat_summary = history_summary
                    chat_room.chat_summary_cnt = now_summary_cnt + 6

            try:
                chat_room.save()
            except Exception as e:
                raise APIException(detail=str(e))

            return Response(
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, chat_room_id):
        # 삭제 여부 업데이트 -> is_deleted
        chat_room = self.get_object(chat_room_id)

        serializer = ChatRoomDetailSerializer(
            chat_room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            chat_room.is_deleted = True
            try:
                chat_room.save()
            except Exception as e:
                raise APIException(detail=str(e))

            return Response(
                data={"result": "success"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={"detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChatMessagesView(APIView):

    def get_object(self, chat_room_id):
        try:
            return ChatRooms.objects.get(chat_room_id=chat_room_id, is_deleted=False)
        except ChatRooms.DoesNotExist:
            raise NotFound(detail="chat room not found")

    def get(self, request, chat_room_id):

        chat_room = self.get_object(chat_room_id)

        try:
            num = request.query_params.get("num", 1)
            num = int(num)
        except ValueError:
            num = 1

        window_size = settings.CHAT_MESSAGE_WINDOW_SIZE
        start = (num - 1) * window_size
        end = start + window_size

        serializer = ChatMessageListSerializer(
            chat_room.chatmessages.all()[start:end],
            many=True,
        )

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, chat_room_id):
        chat_room = self.get_object(chat_room_id)
        content = request.data.get("content")

        if content is None:
            raise ParseError(
                detail="content is required",
                code=status.HTTP_400_BAD_REQUEST,
            )

        # Human message 저장
        serializer = ChatMessageDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                role=ChatMessages.MessageRoleChoices.HUMAN,
                chat_room_id=chat_room,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        task_result = process_ai_response.delay(chat_room_id, content)
        return Response(
            {"status": "success", "task_id": task_result.id},
            status=status.HTTP_201_CREATED,
        )


class TaskStatusView(APIView):
    def get(self, request, task_id):

        try:
            task_result = AsyncResult(task_id)

            if task_result.state == "SUCCESS":
                return Response(
                    {"status": "SUCCESS", "result": task_result.result["generation"]}
                )
            elif task_result.state == "FAILURE":
                return Response(
                    {"status": "FAILURE", "result": "오류가 발생했습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            else:
                return Response({"status": task_result.state})
        except Exception as e:
            raise APIException(detail=str(e))
