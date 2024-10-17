import { Outlet, useNavigate, useParams } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { HStack, VStack } from "@chakra-ui/react";
import ChatRoomFooter from "./screens/ChatRoomFooter";
import ChatRoomHeader from "./screens/ChatRoomHeader";
import ChatRoomList from "./screens/ChatRoomList";
import { deleteChatRoom, getChatRooms } from "../api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export default function Root() {
  const { chatRoomId } = useParams();
  const navigator = useNavigate();
  const queryClient = useQueryClient();

  const { isLoading: isChatRoomLoading, data: chatRooms } = useQuery({
    queryKey: ["chatRooms"],
    queryFn: getChatRooms,
  });

  const chatRoomMutation = useMutation({
    mutationFn: getChatRooms,
    onSuccess: () => {
      queryClient.refetchQueries({ queryKey: ["chatRooms"] });
    },
  });

  const handleChatRoomClick = (selectedChatRoomId: number) => {
    if (selectedChatRoomId === 0) {
      navigator("");
    } else {
      chatRoomMutation.mutate();
      navigator(selectedChatRoomId.toString());
    }
  };

  const handleDeleteChatRoom = (deletedChatRoomId: number) => {
    deleteChatRoom(deletedChatRoomId);
    chatRoomMutation.mutate();
    if (chatRoomId === deletedChatRoomId.toString()) {
      navigator("");
    }
  };

  return (
    <div>
      <Header />
      <HStack align="stretch" h="calc(100vh - 80px)" spacing="0">
        <VStack w="300px" align="stretch" spacing="0">
          <ChatRoomHeader onChatRoomClick={handleChatRoomClick} />
          <ChatRoomList
            onChatRoomClick={handleChatRoomClick}
            onDeleteChatRoom={handleDeleteChatRoom}
            chatRooms={chatRooms || []}
            isLoading={isChatRoomLoading}
          />
          <ChatRoomFooter />
        </VStack>
        <Outlet
          context={{
            onClickEvent: handleChatRoomClick,
            roomUpdate: chatRoomMutation,
          }}
        />
      </HStack>
      <Footer />
      <ReactQueryDevtools />
    </div>
  );
}
