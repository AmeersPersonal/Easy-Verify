import { useState, useEffect, useCallback, useRef } from "react";
import { JSEncrypt } from "jsencrypt";

export function useWebSocket(easyVerifyUrl, apiUrl) {
  const webSocket = useRef(null); //This ref will contain the websocket instance
  const [isSocketOpen, setSocketOpen] = useState(false);
  const [startConnect, setStartConnect] = useState(false);
  const [verifyStatus, setVerifyStatus] = useState(false);
  const verifyState = useRef("Not Started");

  /**
   * the states it can be in:
   * Await Public Key
   * Verifying
   * Finish
   *
   */

  const sendMessage = useCallback((message) => {
    try {
      webSocket.current.send(message);
    } catch (error) {
      console.error("Error" + error);
    }
  }, []);

  const connect = useCallback(() => {
    const getAPIInfo = () => {
      console.log(apiUrl);
    };

    console.log("started connection");
    //the hooks that connect everything together
    try {
      webSocket.current = new WebSocket(easyVerifyUrl);
    } catch (error) {
      console.error(error);
    }

    webSocket.current.onopen = () => {
      getAPIInfo();
      console.log("socket open");
      setSocketOpen(true);
      verifyState.current = "Await Public Key";
    };
    webSocket.current.onerror = (error) => {
      console.error("WebSocket error:", error);
      setSocketOpen(false);
    };

    webSocket.current.onclose = (event) => {
      console.log("WebSocket disconnected");

      if (event.code !== 1000) {
        // Check if the closure was not normal
        console.warn(
          `WebSocket closed unexpectedly: ${event.code} - ${event.reason}`,
        );

        if (verifyState.current === "Not Started") {
          setTimeout(() => connect(), 2000); // call again after failed initial connection
        } else {
          alert("Connection error");
        }
      } else {
        console.log("WebSocket closed normally.");
      }
      setStartConnect(false);
      setSocketOpen(false);
    };

    webSocket.current.onmessage = (event) => {
      console.log(verifyState.current);
      switch (verifyState.current) {
        case "Await Public Key":
          var encrypt = new JSEncrypt();
          var publicKey = JSON.parse(event.data);
          encrypt.setPublicKey(publicKey);
          var encryptedData = encrypt.encrypt("Encryption Test");
          sendMessage(encryptedData);
          verifyState.current = "Verifying";
          break;
        case "Verifying":
          if (event.data === "Verification complete") {
            if (!verifyStatus) setVerifyStatus(true);
            verifyState.current = "Complete";
            webSocket.current.close(1000, "Verification Complete"); // Close the WebSocket connection with a normal closure code and reason
          } else {
            console.log(event.data);
          }
          break;
        default:
          console.log("Invalid State, Closing socket");
          console.log(verifyState.current);
          console.log(event.data);
          webSocket.current.close();
          break;
      }
    };
  }, [easyVerifyUrl, sendMessage, verifyStatus, setVerifyStatus, apiUrl]);

  useEffect(() => {
    if (!startConnect) {
      return;
    } else {
      connect(easyVerifyUrl);
      return () => {
        // cleanup function to close the WebSocket when the component unmounts
        if (webSocket.current) {
          webSocket.current.close(1000, "Component unmounted"); // Close the WebSocket connection with a normal closure code and reason
        }
      };
    }
  }, [connect, easyVerifyUrl, startConnect]);

  return [isSocketOpen, setStartConnect, verifyStatus];
}
