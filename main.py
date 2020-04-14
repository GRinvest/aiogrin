import asyncio
import ujson
from time import time

import aiohttp
from coincurve import PrivateKey  # https://pypi.org/project/coincurve/
# https://pycryptodome.readthedocs.io/en/latest/src/introduction.html
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from yaml import safe_load

with open('config/settings.yaml') as f:
    CONFIG = safe_load(f)["NODE"]

AUTH = aiohttp.BasicAuth(
    CONFIG["USERNAME"],
    password=CONFIG["PASSWORD_OWNER"]
)


def encrypt_AES_GCM(params, secretKey):
    """
    encryption using AES-256-GCM see doc https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html
    """
    nonce = get_random_bytes(12)  # generate random byte nonce
    aesCipher = AES.new(bytes.fromhex(secretKey), AES.MODE_GCM, nonce)
    # encrypt params transferred by a json to string and converted for encryption into bytes
    ciphertext = aesCipher.encrypt(params.encode("utf8"))

    print(f"ciphertext: {ciphertext.hex()}")
    print(f"nonce: {nonce.hex()}")
    return {
        'nonce': nonce.hex(),
        # ciphertext in bytes convert to a hex for sending to a wallet ????? right or not not clear
        'body_enc': ciphertext.hex(),
    }


async def init_secure_api(session: aiohttp.ClientSession):
    """
    initialize wallet with ecdh curve secp256k1 see doc https://pypi.org/project/coincurve/
    """
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
        print(f"response of wallet init_secure_api: {res}")
    # I encrypt the answer from the wallet esdh
    return private_key.ecdh(bytes.fromhex(res["result"]["Ok"])).hex()


async def open_wallet(session: aiohttp.ClientSession, shared_key):
    id_res = int(time())
    data = {
        "jsonrpc": "2.0",
        "method": "open_wallet",
        "params": {
            "name": None,
            "password": "password"
        },
        "id": id_res
    }
    print(f"params for ecrypt: {data}")
    params_encrypt = encrypt_AES_GCM(ujson.dumps(data), shared_key) # encrypt params for sent wallet
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
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        res = await init_secure_api(session)
        print(f"esdh init_secure_api: {res}")
        res = await open_wallet(session, res)
        print(f"open_wallet response: {res}")

if __name__ == '__main__':
    asyncio.run(main())
