import { Box, VStack, Spinner } from "@chakra-ui/react";
import { IChatRoom } from "../../types";
import ChatRoom from "../modules/ChatRoom";

interface ChatRoomListProps {
  onChatRoomClick: (chatRoomId: number) => void;
  onDeleteChatRoom: (chatRoomId: number) => void;
  chatRooms: IChatRoom[];
  isLoading: boolean;
}

export default function ChatRoomList({
  onChatRoomClick,
  onDeleteChatRoom,
  isLoading,
  chatRooms,
}: ChatRoomListProps) {
  return (
    <Box w="100%" h="calc(100vh - 60px)" overflowY="auto">
      <VStack py="1" px="4" align="stretch" spacing="3">
        {isLoading ? (
          <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            height="100%"
          >
            <Spinner size="lg" />
          </Box>
        ) : (
          chatRooms
            ?.sort((a, b) => b.chatRoomId - a.chatRoomId)
            .map((chatroom) => (
              <ChatRoom
                key={chatroom.chatRoomId}
                chatRoomId={chatroom.chatRoomId}
                chatRoomName={chatroom.chatRoomName}
                createdAt={chatroom.createdAt}
                onChatRoomClick={onChatRoomClick}
                onDeleteChatRoom={onDeleteChatRoom}
              />
            ))
        )}
      </VStack>
    </Box>
  );
}
