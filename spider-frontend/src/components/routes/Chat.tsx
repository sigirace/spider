import { Box, VStack } from "@chakra-ui/react";
import MessageList from "../screens/MessageList";
import Sender from "../screens/Sender";
import { IMessage } from "../../types";
import { QueryClient, useQuery, useQueryClient } from "@tanstack/react-query";
import { useOutletContext, useParams } from "react-router-dom";
import {
  conversation,
  getConversationStatus,
  getMessages,
  setChatRoomProperty,
} from "../../api";
import { useState } from "react";

export default function Chat() {
  const { chatRoomId } = useParams();
  const { roomUpdate } = useOutletContext<any>();
  const [isLoading, setIsLoading] = useState(false);

  const queryClient = useQueryClient();

  const { isLoading: isMessageLoading, data: messages } = useQuery({
    queryKey: ["messages", Number(chatRoomId)],
    queryFn: async () => {
      let messageList: IMessage[] = [];
      const storedMessage = localStorage.getItem(chatRoomId!.toString());

      if (storedMessage) {
        const humanMessage = {
          messageId: Date.now(),
          role: "human",
          content: storedMessage,
        } as IMessage;

        messageList.push(humanMessage);
        localStorage.removeItem(chatRoomId!.toString());

        setIsLoading(true);
        const taskId = await conversation(Number(chatRoomId), storedMessage);
        checkTaskStatus(
          taskId,
          Number(chatRoomId),
          setIsLoading,
          queryClient,
          true,
          roomUpdate
        );
      } else {
        messageList = await getMessages(Number(chatRoomId));
      }

      return messageList;
    },
    enabled: !queryClient.getQueryData(["messages", Number(chatRoomId)]),
  });

  const handleSendMessage = async (input: string) => {
    const humanMessage = {
      messageId: Date.now(),
      role: "human",
      content: input,
    } as IMessage;

    setIsLoading(true);

    queryClient.setQueryData(
      ["messages", Number(chatRoomId)],
      (prevMessages: any) => [...(prevMessages || []), humanMessage]
    );

    const taskId = await conversation(Number(chatRoomId), input);
    checkTaskStatus(
      taskId,
      Number(chatRoomId),
      setIsLoading,
      queryClient,
      false,
      roomUpdate
    );
  };

  return (
    <VStack h="calc(100vh - 80px)" flex="1" justify="center">
      <Box
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        w="100%"
        h="100%"
        pt="2"
        pb="2"
      >
        <Box flex="1" overflow="hidden" w="65%" h="80vh">
          <MessageList messages={messages || []} isLoading={isMessageLoading} />
        </Box>
        <Box pt="1" w="60%" flex="none">
          <Sender onSendMessage={handleSendMessage} isLoading={isLoading} />
        </Box>
      </Box>
    </VStack>
  );
}

const checkTaskStatus = async (
  taskId: string,
  roomId: number,
  setIsLoading: any,
  queryClient: QueryClient,
  isFirst: boolean,
  roomUpdate: any
) => {
  const interval = setInterval(async () => {
    try {
      const response = await getConversationStatus(taskId);

      if (response) {
        clearInterval(interval);
        queryClient.setQueryData(["messages", roomId], (prevMessages: any) => [
          ...(prevMessages || []),
          response,
        ]);
        setIsLoading(false);

        if (isFirst) {
          await setChatRoomProperty(roomId, "naming");
          roomUpdate.mutate();
        } else {
          setChatRoomProperty(roomId, "memorizing");
        }
      } else {
        console.log("task is not finished yet");
      }
    } catch (error) {
      console.error("Error fetching chat rooms:", error);
      clearInterval(interval);
      setIsLoading(false);
      throw error;
    }
  }, 2000);
};
