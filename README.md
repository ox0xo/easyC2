# easyC2
```
                                         $$$$$$\   $$$$$$\  
                                        $$  __$$\ $$  __$$\ 
 $$$$$$\   $$$$$$\   $$$$$$$\ $$\   $$\ $$ /  \__|\__/  $$ |
$$  __$$\  \____$$\ $$  _____|$$ |  $$ |$$ |       $$$$$$  |
$$$$$$$$ | $$$$$$$ |\$$$$$$\  $$ |  $$ |$$ |      $$  ____/ 
$$   ____|$$  __$$ | \____$$\ $$ |  $$ |$$ |  $$\ $$ |      
\$$$$$$$\ \$$$$$$$ |$$$$$$$  |\$$$$$$$ |\$$$$$$  |$$$$$$$$\ 
 \_______| \_______|\_______/  \____$$ | \______/ \________|
                              $$\   $$ |                    
                              \$$$$$$  |                    
                               \______/                     
```

## How to install

```
pip install pycryptodome
pip install requests
```

## How to setup

Generate an RSA private key (private.pem) and a public key (public.pem) and place them in the same folder as `server.py`. Note that encrypted keys with passphrase cannot be used.

This key is used to encrypt the message exchange between you and the victim. Please be aware that any leaks will increase the likelihood of detection by the security personnel of the victim's organization. We recommend that you recreate the key every time you start a campaign.

Other customizable items are as follows.

#### `server.py`

- KEEPALIVE
Specifies the agent heartbeat interval in seconds.
- ENTRYPOINT_BEACON
You can specify the name of the endpoint that will receive agent heartbeats.
- ENTRYPOINT_RESPONSE
You can specify the name of the endpoint that will receive the leaked information from the agent.
- app.run(host="0.0.0.0", port=8080, debug=True)
You can specify the listening IP and port of the C2 server.

#### `agent.py`

- server
Specify the IP of the C2 server to connect to.
- port
Specify the Port of the C2 server to connect to.
- user_agent
User agent name can be specified.

## How to use

Start `server.py` and then run `agent.py` on the victim's terminal.

`agent.py` sends a beacon to `server.py` at each interval specified by KEEPALIVE.

If a command is set in `server.py`, it replies to the beacon with the command. This command can be set by passing `http://server:port/command/?command=this_is_specify_command` on the local host of `server.py`.

When `agent.py` receives the command, it calls a sub-process to execute it and sends the result back to `server.py`.

This cycle continues until the command KILL is sent from `server.py` to `agent.py`.
