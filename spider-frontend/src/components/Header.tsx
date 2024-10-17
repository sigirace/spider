import {
  Box,
  HStack,
  IconButton,
  Stack,
  useColorMode,
  useColorModeValue,
} from "@chakra-ui/react";
import { FaMoon, FaSun, FaSpider } from "react-icons/fa";
import { Link } from "react-router-dom";

export default function Header() {
  const { toggleColorMode } = useColorMode();
  const logoColor = useColorModeValue("yellow.600", "yellow.200");
  const Icon = useColorModeValue(FaMoon, FaSun);

  return (
    <Stack
      justifyContent={"space-between"}
      alignItems="center"
      py={1}
      px={10}
      direction={"row"}
      height="50px"
      borderBottomWidth={1}
    >
      <Box color={logoColor}>
        <Link to={"/"}>
          <FaSpider size={"24"} />
        </Link>
      </Box>
      <HStack spacing={2}>
        <IconButton
          onClick={toggleColorMode}
          variant={"ghost"}
          aria-label="Toggle dark mode"
          icon={<Icon />}
        />
      </HStack>
    </Stack>
  );
}
