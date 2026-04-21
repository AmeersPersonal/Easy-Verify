## TODO:
- Clean up the websockets so the client cleanly closes the connection
- Allow for communications between the websocket thread and the user interface

## Current Limitations

- Currently, the websocket implementation uses ws://, not wss://(secure websocket),
- For now, we are using unencrypted ws:// requests to localhost (THIS IS NOT FINAL, WE ARE USING PGP FOR THE ACTUAL HANDSHAKE)
- I am presuming that if we were to deploy this application, its gonna use https and tls, so we gotta redirect the trafifc through ngrok or another tunneling service, this prevents mixed-content issues
- its gonna be kinda jank since ws -> client app is gonna have to be unencrypted, so thats why we are gonna use pgp - > aes anyway

## Here is the plan for the pgp -> aes handshake:
(Browser)
- Opens app with easy-verify:// (and sends some basic client information)
(Client)
- On Startup, we make a PGP/RSA Key (Public + Private)
- We then send the public key through ngrok to our browser
(Browser)
- We recieve this key, then we encrypt an AES key using that public key, this gets sent through ngrok back to the client app
(Client)
- Decrypt the AES key, then we use it like normal AES-GCM to send encrypted info
