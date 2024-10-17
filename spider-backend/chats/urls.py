from django.urls import path
from . import views

urlpatterns = [
    path("room", views.ChatRoomView.as_view(), name="chatRoom"),
    path(
        "room/<int:chat_room_id>",
        views.ChatRoomDetailView.as_view(),
        name="chatRoomDetail",
    ),
    path(
        "messages/<int:chat_room_id>",
        views.ChatMessagesView.as_view(),
        name="chatMessages",
    ),
    path("status/<str:task_id>", views.TaskStatusView.as_view(), name="taskStatus"),
]
