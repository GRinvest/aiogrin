# aiogrin

asyncio API v3 for grin-wallet

git clone https://github.com/GRinvest/aiogrin.git

pipenv --python 3.8

pipenv install

###### Output example:

```javascript
response of wallet init_secure_api:{'id': 1586891235, 'jsonrpc': '2.0', 'result': {'Ok': '0287a491447eed8e445ea2c75045aa458fe4bf8d8ce87608353bc5a72a2a708d2b'}}
esdh init_secure_api: 9007e72453f137bb7ba2a9f193383f286670edd95c46e4af7106baff6a5cbe6b
params for ecrypt: {'jsonrpc': '2.0', 'method': 'open_wallet', 'params': {'name': None, 'password': 'password'}, 'id': 1586891235}
encoding ciphertext: a1af15a7f0fb63a8d3dcaea345bb369c63f61d4404482820128b101f3682d56bc08c9bfd23d12f944dd5c5f28ad924ff65020feb58840e223b94d842e91e218de3501a7432373d1651a118f0900cabb4a56ddea67a68c0b5b7cfd7a2dd790463684bc97cc6
nonce: 66802c9ad4613fbe76217757
open_wallet response: {'error': {'code': -32002, 'message': 'Decryption error: EncryptedBody Dec: Decryption Failed (is key correct?)'}, 'id': 1, 'jsonrpc': '2.0'}
```
