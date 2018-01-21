import requests
from namehash import namehash
import binascii

def data(nh):
    b = binascii.b2a_hex(namehash(nh))
    return '0x3b3b57de' + b.decode("unicode_escape")

def ENSLookup(address):
    html = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_call&to=0x5FfC014343cd971B7eb70732021E26C35B744cc4&data="
                        + data(address) + "&tag=latest&apikey=YourApiKeyToken")
    print(html.json()["result"])
    return html.json()["result"]

ENSLookup('emmypony.eth')