import requests
from modules.crypto.namehash import namehash
import binascii

ens_registry = "0x314159265dD8dbb310642f98f50C066173C1259b"

def data_registrar(addr):
    b = binascii.b2a_hex(namehash(addr))
    return '0x0178b8bf' + b.decode("unicode_escape")

def data_resolver(addr):
    b = binascii.b2a_hex(namehash(addr))
    return '0x3b3b57de' + b.decode("unicode_escape")

def ENSLookup(address):
    resolver_address = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_call&to=" + ens_registry + "&data="
                        + data_registrar(address) + "&tag=latest&apikey=YourApiKeyToken").json()["result"]
    resolver_address = '0x' + resolver_address[26:]
    html = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_call&to=" + resolver_address + "&data="
                        + data_resolver(address) + "&tag=latest&apikey=YourApiKeyToken")
    return html.json()["result"]