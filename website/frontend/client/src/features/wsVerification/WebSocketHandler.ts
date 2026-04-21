// import { JSEncrypt } from "jsencrypt";
import JSEncrypt from "jsencrypt";
import type { ClientToApp, ServerToClient, CurrentState } from "./states";
import { responsiveFontSizes } from "@mui/material/styles";

/**
 * The websocket handler won't really contain much of the back and forth from the handshake, this will be done in verification.ts
 *
 */

/**
 * for each response type in ServerToClient, we add a function to it that takes in a response, and returns a void
 */
type PayloadType = ((payload: {
  response: string;
}) => void);
/**
 * map every possible response type that the server can give into a map that accociates it with a function that returns a void
 * this type type that we construct is then going to be used in a variable in the class
 * basically, we store each function that we call for its corresponding ServerToClient state
 */
type HandlersMapType = {
  [K in keyof ServerToClient]?: PayloadType;
};
//type StateHandler = (state: CurrentState) => void; //a type that defines a function that takes in a variable of one of the connection states and returns a void

export class useWebSocket {
  private attemptCount: number = 0;

  private webSocket: WebSocket | null = null; //object containing the websocket
  private easyVerifyUrl: string;
  private handlersMap: HandlersMapType = {}; // Stores all of our handlers for each server to client call

  constructor(easyVerifyUrl: string) {
    this.easyVerifyUrl = easyVerifyUrl;
  }

  private reconnect() {
    if (this.attemptCount >= 10) {
      console.log("Max retries reached");
      throw new Error("Max retries");
    }

    const delay = this.delay(this.attemptCount);
    console.log(`Reconnecting in ${delay}ms...`);

    this.attemptCount++;

    setTimeout(() => {
      this.connect();
    }, delay);
  }

  private delay = (attempts: number): number => {
    let delay = 300 * attempts;

    const rand = Math.random() * delay * 0.3; // 0–30% jitter
    delay = delay - rand;

    return Math.floor(delay);
  }

  connect() {
    this.webSocket = new WebSocket(this.easyVerifyUrl);
    //instead of using the .on functions, we use addEventListener to be more flexible
    this.webSocket.addEventListener("open", this.onOpen);
    this.webSocket.addEventListener("message", this.onMessage);
    this.webSocket.addEventListener("close", this.onClose);
    this.webSocket.addEventListener("error", this.onError);
  }
  //handler functions
  private onOpen = (): void => {
    console.log("Open");
  };
  /**
   * We have to check the message for a json that looks like this
   * {
   *  responseType: ServerToClient Type in string
   *  response: Also string
   * }
   * @param messageEvent
   */
  private onMessage = (messageEvent: MessageEvent): void => {
    try {
      const msg = JSON.parse(messageEvent.data)
      console.log(msg);
      let responseType : string = msg.responseType;
      let responseData : string = msg.response;
      if (typeof responseType === "string" && responseType in this.handlersMap) {
        if (typeof responseData === "string") {
          this.handlersMap[responseType as keyof ServerToClient]?.({ response: responseData });
        }
        else {
          throw new Error("bad response data");
        }
      } else {
        throw new Error("Invalid Response type");
      }

    } catch (error) {
      console.log(error);
      console.error(messageEvent.data)
      throw new Error("Error recieving message");
    }
  };

  /**
   * assign a function to whatever state the server is in at this moment
   * @param handler
   * handler: one of the server to client states
   * function
   */
  on<K extends keyof ServerToClient>(type: K,
    func?: PayloadType
  ) {
    this.handlersMap[type] = func;
  }
  off<K extends keyof ServerToClient>(type: K) {
    delete this.handlersMap[type];
  }

  private onClose = (event: CloseEvent): void => {
    console.log(event.reason);
    //normal closure
    if (event.code === 1000) {
      console.log("normal closure");
    }
    console.log("Event code:" + event.code);
    if (!event.wasClean) {
      console.error("socket didn't close properly :(");
      this.reconnect();
    }
    console.log();
    console.log("Close");
  };

  private onError = (error: Event): void => {
    console.error("Error");
    console.error(error);
    throw new Error("Websocket Error");

  };

  send<K extends keyof ClientToApp>(type: K, message: string) {
    if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
      throw new Error("Cannot send");
    }
    console.log(JSON.stringify({ type, message}));
    this.webSocket.send(JSON.stringify({ type, message }));
  }

  disconnect() {
    this.webSocket?.close();
    this.webSocket = null;
    console.log("websocket client closed and socket disconencted");
  }
}
