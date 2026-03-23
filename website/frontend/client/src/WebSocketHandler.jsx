import { useState } from "react";
import { useEffect } from "react";
import { useCallback } from "react";
import { useRef } from "react";

export function useWebSocket(url) {
  const attemptCountRef = useRef(0); // Ref to track the number of connection attempts
  const reconnectCountRef = useRef(0); // Ref to track the number of reconnection attempts
  const socketRef = useRef(null); //initialize the reference to hold the WebSocket instance
  const [startConnect, setStartConnect] = useState(false); // State to control when to start the WebSocket connection

  const connectWebSocket = useCallback(() => {
    console.log("Attempting to connect to WebSocket...");
    socketRef.current = new WebSocket(url);
    //connect to the WebSocket server at the specified URL and store it in a reference
    socketRef.current.onopen = () => {
      console.log("WebSocket connected");
    };

    socketRef.current.onclose = (event) => {
      console.log("WebSocket disconnected");
      if (event.code !== 1000) {
        // Check if the closure was not normal
        console.warn(
          `WebSocket closed unexpectedly: ${event.code} - ${event.reason}`,
        );

        if(reconnectCountRef.current < 5) {
          reconnectCountRef.current += 1;
          console.log("Attempting to reconnect...");
          setTimeout(connectWebSocket, 500); // Attempt to reconnect after 0.5 second
        } else {
          console.error("Failed to reconnect after multiple attempts.");
          return;
        }
      } else {
        console.log("WebSocket closed normally.");
      }
    };

    socketRef.current.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      if (event.data === "Verification complete") {
        alert("Verification successful! You can now access the content.");
        socketRef.current.close(1000, "Verification Complete"); // Close the WebSocket connection with a normal closure code and reason
      }
    };

    socketRef.current.onerror = (error) => {
      console.error("WebSocket error:", error);
      setStartConnect(false); // Stop trying to connect if there's an error
    };
  }, [socketRef, url]);

  useEffect(() => {
    if (!startConnect) return; // Only connect if startConnect is true

    connectWebSocket();
    return () => {
      // cleanup function to close the WebSocket when the component unmounts
      if (socketRef.current) {
        socketRef.current.close(1000, "Component unmounted"); // Close the WebSocket connection with a normal closure code and reason
      }
    };
  }, [connectWebSocket, url, startConnect]);

  const send = (data) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(data));
    } else {

      if(attemptCountRef.current >= 5) {
        console.error("Unable to send message after multiple attempts. Please check your connection and try again.");
        return;
      }

      console.warn(
        "WebSocket error. Unable to send message, Attempting to resend",
      );
      attemptCountRef.current += 1; // Increment the attempt count
      setTimeout(() => send(data), 500); // Attempt to resend after 0.5 second
    }
  };

  return [socketRef.current, send, setStartConnect]; // Return the reference to the WebSocket instance so it can be used in other components
}

export function sendMessage(message, socketRef) {
  if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
    socketRef.current.send(message);
  }
}
