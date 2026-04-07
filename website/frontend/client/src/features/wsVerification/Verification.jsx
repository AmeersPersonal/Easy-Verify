import { useState } from "react";
import { useWebSocket } from "./WebSocketHandler";

export function useVerification(url = "ws://localhost:8765") {
  const [, send, setStartConnect] = useWebSocket(url);
  const [clickText, setClickText] = useState("");

  const startVerify = (name) => {
    setClickText("Verifying...");
    window.open("easy-verify://verifyDemoClient");
    setStartConnect(true);
    setTimeout(() => send(name), 1000);
    setClickText(
      "Verification request sent! Please check your Easy Verify app.",
    );
  };

  return {
    clickText,
    startVerify,
  };
} 
