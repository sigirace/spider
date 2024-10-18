import { IChatRoom, IMessage } from "./types";
import axios from "axios";

const apiBaseURL =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000/api/v1/"
    : `http://${window.location.hostname}:8000/api/v1/`;

const instance = axios.create({
  baseURL: apiBaseURL,
  headers: {
    "Content-type": "application/json",
  },
  withCredentials: true,
});

export const getChatRooms = async () => {
  try {
    console.log("[api] getRooms start");
    const response = await instance.get("chat/room");
    return response.data.map((res: any) => ({
      chatRoomId: res.chat_room_id,
      chatRoomName: res.chat_room_name || null,
      createdAt: res.created_at.split("T")[0],
    })) as IChatRoom[];
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};

export const getMessages = async (chatRoomId: number) => {
  try {
    console.log("[api] getMessages start", chatRoomId);
    const response = await instance.get(`chat/messages/${chatRoomId}`);
    return response.data.map((res: any) => ({
      messageId: res.message_id,
      role: res.role,
      content: res.content,
    })) as IMessage[];
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};

export const createChatRoom = async () => {
  try {
    console.log("[api] createRoom start");
    const response = await instance.post("chat/room");
    return {
      chatRoomId: response.data.chat_room_id,
      chatRoomName: response.data.caht_room_name || null,
      createdAt: response.data.created_at.split("T")[0],
    } as IChatRoom;
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};

export const conversation = async (chatRoomId: number, content: string) => {
  try {
    console.log("[api] conversation start");
    const response = await instance.post(`chat/messages/${chatRoomId}`, {
      chat_room_id: chatRoomId,
      content: content,
    });

    return response.data.task_id;
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};

export const getConversationStatus = async (
  taskId: string
): Promise<IMessage | null> => {
  // 수정: 반환 타입 명시
  try {
    console.log("[api] getConversationStatus start", taskId);
    const res = await instance.get(`chat/status/${taskId}`);
    if (res.data.result) {
      const aiMessage = {
        messageId: Date.now(),
        role: "ai",
        content: res.data.result,
      } as IMessage;
      return aiMessage; // aiMessage 반환
    }

    return null; // 결과가 없을 경우 null 반환
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};
export const setChatRoomProperty = async (chatRoomId: number, task: string) => {
  try {
    console.log("[api] setChatRoomProperty start", task);
    await instance.put(`chat/room/${chatRoomId}`, {
      task: task,
    });
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};

export const deleteChatRoom = async (chatRoomId: number) => {
  try {
    console.log("[api] deleteChatRoom start", chatRoomId);
    await instance.delete(`chat/room/${chatRoomId}`);
  } catch (error) {
    console.error("Error fetching chat rooms:", error);
    throw error;
  }
};
