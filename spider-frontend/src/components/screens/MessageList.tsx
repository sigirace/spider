import { VStack, Box, Spinner } from "@chakra-ui/react";
import { FaRobot } from "react-icons/fa";
import { useRef, useEffect } from "react";
import React from "react";
import { IMessage } from "../../types";
import Message from "../modules/Message";

interface MessageListProps {
  messages: IMessage[];
  isLoading: boolean;
}

function MessageList({ messages, isLoading }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <VStack
      spacing={3}
      overflowY="auto"
      maxHeight="100%"
      w="100%"
      sx={{
        scrollbarGutter: "stable",
        "&::-webkit-scrollbar": {
          display: "none",
        },
      }}
    >
      {isLoading ? (
        <Box display="flex" justifyContent="center" alignItems="center">
          <Spinner size="xl" />
        </Box>
      ) : messages?.length === 0 ? (
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          pt="250"
        >
          <FaRobot size="100px" />
        </Box>
      ) : (
        messages?.map((msg) => (
          <Message
            key={msg.messageId}
            messageId={msg.messageId}
            content={msg.content}
            role={msg.role}
          />
        ))
      )}
      <Box ref={bottomRef} />
    </VStack>
  );
}

export default React.memo(MessageList);
