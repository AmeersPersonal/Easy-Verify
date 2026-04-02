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
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="max-w-7xl mx-auto p-8 text-center">
        <img src="/icon.png" width={400} height={400} />
        <h1 className="text-5xl leading-tight">Access Content Below</h1>
        <br />
        <form onSubmit={handleSubmit}>
          <input
            name="name"
            placeholder="Enter your name"
            onChange={changeName}
          />{" "}
          <br />
          <button
            type="submit"
            className="rounded-lg border border-transparent px-5 py-2.5 text-base font-medium bg-[#1a1a1a] cursor-pointer transition-colors duration-[250ms] hover:border-[#646cff] focus-visible:outline focus-visible:outline-4"
          >
            Verify
          </button>
        </form>
        <h3>{clickText}</h3>
      </div>
    </div>
  );
}

export default WebSocketVerifyPage;
