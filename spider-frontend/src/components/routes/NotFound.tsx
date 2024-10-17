import { Button, Heading, Text, VStack } from "@chakra-ui/react";
import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <VStack justifyContent={"center"} minH="100vh">
      <Heading>Page not found.</Heading>
      <Text>The page you are looking for does not exist.</Text>
      <Link to="/">
        <Button colorScheme="red" variant={"solid"}>
          Go home
        </Button>
      </Link>
    </VStack>
  );
}
