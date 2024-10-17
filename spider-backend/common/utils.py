import os
import json
from typing import List, Dict, Any

from chats.models import ChatMessages

APP_PATH = os.path.dirname(__file__)


def read_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def url_format(host, port, protocol=None):
    base_url = str(host) + ":" + str(port)
    if not protocol:
        return base_url
    elif protocol == "http":
        return "http://" + base_url
    elif protocol == "https":
        return "https://" + base_url


def make_new_line(conversation_queryset: List[ChatMessages]):
    try:
        new_line = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in conversation_queryset]
        )
        return new_line
    except Exception as e:
        print(e)
        return ""


def make_history_summary(conversation_summary: str, new_line: str):

    history_summary = ""
    if conversation_summary:
        history_summary += f"과거 대화 내역 요약: {conversation_summary}\n\n"
    if new_line:
        history_summary += f"최근 대화 내역: {new_line}\n\n"

    return history_summary
