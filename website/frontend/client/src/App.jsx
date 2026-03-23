import "./App.css";
import { useState } from "react";
import { useWebSocket } from "./WebSocketHandler";

function App() {
  const [clickText, setClickText] = useState("");
  const [name, setName] = useState("");
  const [socket, send, setStartConnect] = useWebSocket("ws://localhost:8765"); // Use the custom hook to establish a WebSocket connection to the specified URL and get the reference to the WebSocket instance

  const startVerify = () => {
    setClickText("Verifying...");
    window.open("easy-verify://verifyDemoClient");
    setStartConnect(true); // Start the WebSocket connection when the user initiates verification
    setTimeout(() => send(name), 1000); // Send the name through the WebSocket connection using the sendMessage function
    setClickText(
      "Verification request sent! Please check your Easy Verify app.",
    );
  };

  function changeName(event) {
    console.log("Name input changed:", event.target.value);
    setName(event.target.value);
  }

  return (
    <>
      <div>
        <img src="/icon.png" width={400} height={400} />
        <h1>Access Content Below</h1> <br />
        <form action={startVerify}>
          <input
            name="name"
            placeholder="Enter your name"
            onChange={changeName}
          />{" "}
          <br />
          <button type="submit">Verify</button>
        </form>
        <h3>{clickText}</h3>
      </div>
    </>
  );
}

export default App;
