import {
  Text,
  Box,
  useColorModeValue,
  Button,
  Spinner,
} from "@chakra-ui/react";
import { useState, useEffect, useRef } from "react";
import { FaTrash } from "react-icons/fa";
import { IChatRoom } from "../../types";

interface IChatRoomProps extends IChatRoom {
  onChatRoomClick: (id: number) => void;
  onDeleteChatRoom: (id: number) => void;
}

export default function ChatRoom({
  chatRoomId,
  chatRoomName,
  createdAt,
  onChatRoomClick,
  onDeleteChatRoom,
}: IChatRoomProps) {
  const bgColor = useColorModeValue("gray.300", "gray.700");
  const [showMenu, setShowMenu] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
  const menuRef = useRef<HTMLDivElement>(null);

  const handleContextMenu = (e: React.MouseEvent) => {
    e.preventDefault();
    setShowMenu(true);
    setMenuPosition({ x: e.clientX, y: e.clientY });
  };

  const handleDelete = () => {
    onDeleteChatRoom(chatRoomId);
    setShowMenu(false);
  };

  const handleClickOutside = (e: MouseEvent) => {
    if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
      setShowMenu(false);
    }
  };

  useEffect(() => {
    if (showMenu) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showMenu]);

  return (
    <>
      <Box
        key={chatRoomId}
        as="button"
        padding="3"
        borderRadius="md"
        bg={bgColor}
        _hover={{ bg: "gray.600" }}
        onContextMenu={handleContextMenu}
        onClick={() => onChatRoomClick(chatRoomId)}
      >
        {chatRoomName === null ? (
          <Spinner size="sm" />
        ) : (
          <Text align="left" fontSize="sm" fontWeight="bold" isTruncated>
            {chatRoomName}
          </Text>
        )}
        <Text align="right" fontSize="xs">
          {createdAt}
        </Text>
      </Box>

      {showMenu && (
        <Box
          ref={menuRef}
          position="absolute"
          top={`${menuPosition.y}px`}
          left={`${menuPosition.x}px`}
        >
          <Button size="sm" colorScheme="red" onClick={handleDelete}>
            <FaTrash />
          </Button>
        </Box>
      )}
    </>
  );
}
