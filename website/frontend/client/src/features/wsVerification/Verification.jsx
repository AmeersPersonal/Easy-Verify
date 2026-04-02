import { useWebSocket } from "./WebSocketHandler";
import { useState } from "react";

const [socket, send, setStartConnect] = useWebSocket("ws://localhost:8765"); // Use the custom hook to establish a WebSocket connection to the specified URL and get the reference to the WebSocket instance

export const startVerify = (name) => {
    setClickText("Verifying...");
    window.open("easy-verify://verifyDemoClient");
    setStartConnect(true); // Start the WebSocket connection when the user initiates verification
    setTimeout(() => send(name), 1000); // Send the name through the WebSocket connection using the sendMessage function
    setClickText(
        "Verification request sent! Please check your Easy Verify app.",
    );
};
