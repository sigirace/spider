import { useOutletContext } from "react-router-dom";
import Sender from "../screens/Sender";
import { VStack, Text, Box } from "@chakra-ui/react";
import { motion } from "framer-motion";
import { createChatRoom } from "../../api";

interface OutletContext {
  onClickEvent: (selectedChatRoomId: number) => void;
}

export default function Home() {
  const { onClickEvent } = useOutletContext<OutletContext>();

  const handleSendMessage = (input: string) => {
    createChatRoom().then((res) => {
      onClickEvent(res.chatRoomId);
      localStorage.setItem(res.chatRoomId.toString(), input);
    });
  };

  const MotionText = motion.create(Text as any);

  return (
    <VStack h="calc(100vh - 60px)" align="stretch" flex="1" justify="center">
      <Box
        textAlign="center"
        display="flex"
        flexDirection="column"
        justifyContent="center"
        alignItems="center"
        w="100%"
        mb={8}
      >
        <MotionText
          w="50%"
          fontSize="4xl"
          fontWeight="bold"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 3 }}
          mb={8}
        >
          무엇을 도와드릴까요?
        </MotionText>
        <Box w="60%">
          <Sender onSendMessage={handleSendMessage} isLoading={false} />
        </Box>
      </Box>
    </VStack>
  );
}
