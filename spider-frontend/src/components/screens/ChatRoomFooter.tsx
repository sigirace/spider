import { HStack, Text, Box, Avatar } from "@chakra-ui/react";

export default function ChatRoomFooter() {
  return (
    <Box w="100%" h="calc(60px)">
      <HStack padding="4" justifyContent="space-between">
        <Avatar size="sm" />
        <Text fontWeight="bold" flex={1} textAlign="center">
          Admin User
        </Text>
      </HStack>
    </Box>
  );
}
