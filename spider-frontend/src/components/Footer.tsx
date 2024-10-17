import { Stack, Link, HStack, Text } from "@chakra-ui/react";
import { FaGithub, FaGithubAlt } from "react-icons/fa";

export default function Footer() {
  return (
    <Stack
      justifyContent={"space-between"}
      alignItems="center"
      py={3}
      px={10}
      direction={"row"}
      borderTopWidth={1}
      borderColor={"grey.500"}
      height="30px"
    >
      <Text color={"gray.500"}>created by sigirace</Text>
      <HStack>
        <Link
          href="https://sigirace.github.io"
          isExternal
          display="flex"
          alignItems="center"
          mr={30}
        >
          <FaGithub size={15} />
        </Link>
        <Link
          href="https://github.com/sigirace"
          isExternal
          display="flex"
          alignItems="center"
          mr={2}
        >
          <FaGithubAlt size={15} />
        </Link>
      </HStack>
    </Stack>
  );
}
