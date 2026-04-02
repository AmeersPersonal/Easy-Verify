import { useState } from "react";
import { useVerification } from "../features/wsVerification/Verification";

function WebSocketVerifyPage() {
  const [name, setName] = useState("");
  const { clickText, startVerify } = useVerification();

  function changeName(event) {
    console.log("Name input changed:", event.target.value);
    setName(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    startVerify(name);
  }

  return (
    <>
      <div>
        <img src="/icon.png" width={400} height={400} />
        <h1>Access Content Below</h1> <br />
        <form onSubmit={handleSubmit}>
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

export default WebSocketVerifyPage;
