//Message
export interface IMessage {
  messageId: number;
  role: string;
  content: string;
}

export interface IChatRoom {
  chatRoomId: number;
  chatRoomName: string | null;
  createdAt: string;
}
