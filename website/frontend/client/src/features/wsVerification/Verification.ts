import { useWebSocket } from "./WebSocketHandler";
import JSEncrypt from "jsencrypt";

import { ClientToApp, ServerToClient, CurrentState } from "./states";
import { JSXElementConstructor } from "react";
// TODO: add listeners for UI

type User = {
  first_name?: string;
  last_name?: string;
  oAuthToken?: string;
  callback_url?: string;
  client_id?: string;
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
    (v.first_name === undefined || typeof v.first_name === "string") &&
    (v.last_name === undefined || typeof v.last_name === "string") &&
    (v.oAuthToken === undefined || typeof v.oAuthToken === "string") &&
    (v.callback_url === undefined || typeof v.callback_url === "string") &&
    (v.client_id === undefined || typeof v.client_id === "string")
  );
}


export class Verifier {
  currentUser: User;
  socket: useWebSocket;
  state: CurrentState = "keyWait";

  constructor(
    url: string = "ws://localhost:8765",
    apiUrl = "TEST",
    newUser?: User,
  ) {
    this.currentUser = isUser(newUser)
      ? (newUser as User)
      : {
          first_name: "John",
          last_name: "Doe",
          oAuthToken: "TEST",
          callback_url: apiUrl,
          client_id: "TEST",
        };

    this.socket = new useWebSocket(url);

    //setting up handlers for the socket, rn we are just sending a response
    this.socket.on("public_key", (data) => {
      if (this.state !== "keyWait") {
        throw new Error("Invalid State");
      }
      let encrypt: JSEncrypt = new JSEncrypt();
      let publicKey: string = data["response"];
      encrypt.setPublicKey(publicKey);

      let encryptedData: string | false = encrypt.encrypt(
        JSON.stringify(this.currentUser),
      );
      if (encryptedData === false) {
        throw new Error("Encryption Error");
      }
      this.state = "verificationWait";

      this.socket.send("encrypted_string", encryptedData);
    });

    this.socket.on("verifyStatus", (response) => {
      if (this.state !== "verificationWait") {
        throw new Error("verifystatus error");
      }
      let status: string = response["response"];
      console.log(status);
      this.state = status === "OK" ? "done" : status === "FAIL" ? "fail" : "error";
    });
  }
  startConnect() {
    this.socket.connect();
  }
}
