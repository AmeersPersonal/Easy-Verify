import { useState } from "react";
import { useWebSocket } from "./WebSocketHandler";

export function useVerification(url = "ws://localhost:8765", apiUrl = "https://www.randomnumberapi.com/api/v1.0/randomstring?min=100") {

  const [isSocketOpen, setStartConnect, verifyStatus] = useWebSocket(
    url,
    apiUrl,
  );
  const [isVerifying, setIsVerifying] = useState(false);


  const startVerify = () => {
    setIsVerifying(true);
    window.location.href = "easy-verify://verifyDemoClient";
    setStartConnect(true)
  };

  return {
    startVerify,
    isSocketOpen,
    verifyStatus,
    isVerifying
  };
}
