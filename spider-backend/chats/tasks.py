# chats/tasks.py
from celery import shared_task
from chats.serializers import ChatMessageDetailSerializer
from common.utils import make_new_line, make_history_summary
from .models import ChatMessages, ChatRooms
from llms.apps import spider, chain
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_ai_response(chat_room_id, content):
    try:
        # 채팅방과 메시지를 가져옴
        chat_room = ChatRooms.objects.get(chat_room_id=chat_room_id, is_deleted=False)

        # 최근 메시지를 가져와 요약 생성
        summary = chat_room.chat_summary
        now_summary_cnt = chat_room.chat_summary_cnt
        history_messages = chat_room.chatmessages.filter(
            message_id__gt=now_summary_cnt
        ).order_by("-message_id")

        new_line = make_new_line(history_messages)
        history_summary = make_history_summary(summary, new_line)

        state = {
            "question": content,
            "history": history_summary,
        }

        # OpenAI 호출
        result = spider(state)
        generation_text = str(result["generation"])

        # AI 응답 메시지 저장
        ai_content = {
            "content": generation_text,
        }

        logger.info("-" * 100)
        logger.info(ai_content)
        logger.info("-" * 100)

        serializer = ChatMessageDetailSerializer(data=ai_content)
        if serializer.is_valid():
            serializer.save(
                role=ChatMessages.MessageRoleChoices.AI,
                chat_room_id=chat_room,
            )
        else:
            logger.error("-" * 100)
            logger.error(serializer.errors)
            logger.error("-" * 100)

        # 직렬화 가능한 데이터만 반환
        return {"generation": generation_text}

    except Exception as e:
        logger.error("-" * 100)
        logger.error("Exception occurred: %s", str(e))
        logger.error("-" * 100)
        return str(e)
