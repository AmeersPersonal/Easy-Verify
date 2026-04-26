import { useWebSocket } from "./WebSocketHandler";
import JSEncrypt from "jsencrypt";

import { CurrentState } from "./states";
// TODO: add listeners for UI

type User = {
  email?: string;
  callback_url?: string;
};

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) {
    return false;
  }
  // a record is basically an empty pair of a key, and an uknown
  const v = value as Record<string, unknown>;

  //**
  // just checking if every attribute of the object that you pass in is either undefined or a string
  //
  // */
  return (
    (v.email === undefined || typeof v.callback_url === "string") &&
    (v.callback_url === undefined || typeof v.callback_url === "string")
  );
}

type Listener = (state: CurrentState) => void;
export class Verifier {
  currentUser: User;
  socket: useWebSocket;
  state: CurrentState = "keyWait";
  private listeners = new Set<Listener>();

  constructor(
    url: string = "ws://localhost:8765",
    newUser?: User,
  ) {
    this.currentUser = isUser(newUser)
      ? (newUser as User)
      : {
        email: "example.com",
        callback_url: "TEST"
      };
    this.setState("keyWait");
    this.socket = new useWebSocket(url);

    //setting up handlers for the socket, rn we are just sending a response
    this.socket.on("public_key", (data) => {
      if (this.state !== "keyWait") {
        throw new Error("Invalid State");
      }
      const encrypt: JSEncrypt = new JSEncrypt();
      const publicKey: string = data["response"];
      encrypt.setPublicKey(publicKey);

      const encryptedData: string | false = encrypt.encrypt(
        JSON.stringify(this.currentUser),
      );
      if (encryptedData === false) {
        throw new Error("Encryption Error");
      }
      this.setState("verificationWait")

      this.socket.send("encrypted_string", encryptedData);
    });

    this.socket.on("verifyStatus", (response) => {
      if (this.state !== "verificationWait") {
        throw new Error("verifystatus error");
      }
      const status: string = response["response"];
      console.log(status);
      this.setState(status === "OK" ? "done" : status === "FAIL" ? "fail" : "error");
    });

  }

  //just tracking updates for the current state so the UI updates to match
  setState(newState: CurrentState) {
    this.state = newState;
    this.listeners.forEach((listener) => listener(this.state));   
  }

  getState() {
    return this.state;
  }

  subscribe(listener: Listener) {
    this.listeners.add(listener);
    listener(this.state);
    console.log(listener);
    return () => {this.listeners.delete(listener)};
  }

  startConnect() {
    this.socket.connect();
  }
}
