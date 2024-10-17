import { Textarea } from "@chakra-ui/react";
import { useState } from "react";

interface ISenderProps {
  onSendMessage: (input: string) => void;
  isLoading: boolean;
}

export default function Sender({ onSendMessage, isLoading }: ISenderProps) {
  const [input, setInput] = useState<string>("");
  const [isComposing, setIsComposing] = useState(false);

  const handleKeyPress = async (
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (!isComposing && e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (input.trim()) {
        onSendMessage(input);
        setInput("");
        const target = e.target as HTMLTextAreaElement;
        target.style.height = "30px";
      }
    }
  };

  return (
    <Textarea
      placeholder={isLoading ? "답변 생성중..." : "ChatGPT에게 메세지 쓰기"}
      isDisabled={isLoading}
      value={input}
      onChange={(e) => {
        setInput(e.target.value);
        const target = e.target as HTMLTextAreaElement;
        target.style.height = `${target.scrollHeight}px`; // 새로운 높이 설정
        if (e.target.value === "") {
          target.style.height = "42px";
        }
      }}
      onKeyDown={handleKeyPress}
      onCompositionStart={() => setIsComposing(true)}
      onCompositionEnd={() => setIsComposing(false)}
      borderRadius="30px"
      border="3px solid lightgray"
      minHeight="42px"
      maxHeight="120px"
      resize="none"
      overflowY="auto"
      sx={{
        scrollbarGutter: "stable",
        "&::-webkit-scrollbar": {
          display: "none",
        },
      }}
    />
  );
}
