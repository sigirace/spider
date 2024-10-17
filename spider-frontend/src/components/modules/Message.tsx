import { HStack, Text, Box, useColorModeValue } from "@chakra-ui/react";
import { FaRobot } from "react-icons/fa";
import { IMessage } from "../../types";
import { CgGirl } from "react-icons/cg";

export default function Message({ messageId, role, content }: IMessage) {
  const humanChatTextColor = useColorModeValue("inherit", "inherit");
  const aiChatTextColor = useColorModeValue("black", "white");
  const humanChatBoxColor = useColorModeValue("inherit", "inherit");
  const aiChatBoxColor = useColorModeValue("gray.300", "gray.700");

  return (
    <Box
      bg={role === "human" ? humanChatBoxColor : aiChatBoxColor}
      color={role === "human" ? humanChatTextColor : aiChatTextColor}
      px={"5"}
      py={"3"}
      borderRadius="md"
      w="100%"
      whiteSpace="pre-wrap"
    >
      <HStack key={messageId} spacing="3" align={"flex-start"}>
        {role === "ai" && <FaRobot size="40px" color="teal" />}
        {role === "human" && <CgGirl size="40px" color="gray" />}
        <Text px={"3"} py={"1"} flex="1">
          {content}
        </Text>
      </HStack>
    </Box>
  );
}
