import asyncio
from time import time

import aiohttp
import json
from coincurve import PrivateKey # https://pypi.org/project/coincurve/
from Crypto.Cipher import AES # https://pycryptodome.readthedocs.io/en/latest/src/introduction.html
from yaml import safe_load

with open('config/settings.yaml') as f:
    CONFIG = safe_load(f)["NODE"]

AUTH = aiohttp.BasicAuth(
    CONFIG["USERNAME"],
    password=CONFIG["PASSWORD_OWNER"]
)

def encrypt_AES_GCM(msg, secretKey):
    encrypt_text = []
    aesCipher = AES.new(bytes.fromhex(secretKey), AES.MODE_GCM)
    ciphertext = aesCipher.encrypt_and_digest(msg.encode("utf8"))
    for item in ciphertext:
        encrypt_text.append(item.hex())
    print(f"msg: {encrypt_text}")
    print(f"nonce: {aesCipher.nonce.hex()}")
    return {
        'nonce': aesCipher.nonce.hex(),
        'body_enc': encrypt_text[0],
    }

async def init_secure_api(session: aiohttp.ClientSession):
    private_key = PrivateKey.from_int(2)
    public_key = private_key.public_key.format(True).hex()
    params = {
        "jsonrpc": "2.0",
        "method": "init_secure_api",
        "params": {
            "ecdh_pubkey": public_key
        },
        "id": int(time())
    }
    async with session.post(
            CONFIG["URL_OWNER"],
            auth=AUTH,
            json=params) as response:
        res = await response.json()
    return private_key.ecdh(bytes.fromhex(res["result"]["Ok"])).hex()


async def open_wallet(session: aiohttp.ClientSession, shared_key):
    private_key = PrivateKey.from_int(2)
    public_key = private_key.public_key.format(True).hex()
    id_res = int(time())
    params_decrypt = {
        "jsonrpc": "2.0",
        "method": "open_wallet",
        "params": {
            "name": None,
            "password": "password"
        },
        "id": id_res
    }
    params_encrypt = encrypt_AES_GCM(json.dumps(params_decrypt), shared_key)
    params = {
        "jsonrpc": "2.0",
        "method": "encrypted_request_v3",
        "params": params_encrypt,
        "id": id_res
    }
    async with session.post(
            CONFIG["URL_OWNER"],
            auth=AUTH,
            json=params) as response:
        res = await response.json()
    return res


async def main():
    async with aiohttp.ClientSession() as session:
        res = await init_secure_api(session)
        print(f"init_secure_api: {res}")
        res = await open_wallet(session, res)
        print(f"open_wallet: {res}")

if __name__ == '__main__':
    asyncio.run(main())
