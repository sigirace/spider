import { HStack, Text, IconButton, Box } from "@chakra-ui/react";
import { FaPlus } from "react-icons/fa";

interface IChatRoomHeaderProps {
  onChatRoomClick: (id: number) => void;
}

export default function ChatRoomHeader({
  onChatRoomClick,
}: IChatRoomHeaderProps) {
  const handleChatRoomClick = (id: number) => {
    onChatRoomClick(id);
  };

  return (
    <Box w="100%" h="calc(60px)">
      <HStack padding="4" justifyContent="space-between">
        <Text fontSize="lg" fontWeight="bold" align="center">
          Chat Rooms
        </Text>
        <IconButton
          aria-label="Add room"
          size="sm"
          onClick={() => {
            handleChatRoomClick(0);
          }}
          icon={<FaPlus />}
        />
      </HStack>
    </Box>
  );
}
