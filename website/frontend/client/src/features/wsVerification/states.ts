
/**
 * Whatever this frontend is sending to the app
 */
export type ClientToApp = {
  request_key: string
  encrypted_string: string;
};

/**
 * All types here must follow the same format in order for them to map properly to the handlers map
 */
export type ServerToClient = {
  public_key: { response: string };
  verifyStatus: { response: string } // either OK: or FAIL
};


export type CurrentState = 'keyWait' | 'verificationWait' | 'done' | 'fail' | 'error'
/**
 * Authentication Outline:
 * Company Backend -> User Info + Updating DB
 * FE -> This, gets info from server, encrypts it, passes it to app
 * ClientApp - >
 *
 *
  * We have to check the message for a json that looks like this
  * {
  *  responseType: ServerToClient Type in string
  *  response: Also string
  * }
 */
