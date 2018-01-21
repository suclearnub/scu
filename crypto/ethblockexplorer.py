import discord
import requests
import asyncio
import shlex
from modules.botModule import BotModule

class ETHBlockExplorer(BotModule):
    name = 'ethblockexplorer'

    description = 'Ethereum block explorer.'

    help_text = 'Displays transactions/accounts on the Ethereum network'

    trigger_string = 'eth'

    has_background_loop = False

    module_version = '0.1.0'

    api_key = ''
    # Get an API key from Etherscan here: https://etherscan.io/myapikey

    def ethprice(self):
        html = requests.get("https://api.coinmarketcap.com/v1/ticker/ethereum")
        data = html.json()[0]
        return int(data["price_usd"].split(".")[0])

    def wei_to_eth(self, value):
        return value/1000000000000000000

    def comma_money(self, value):
        return "{:,}".format(value)

    def hex_int(self, value):
        return int(value, 16)

    txn_types = {'std': 'Standard',
                 'ctt': 'Contract'}

    async def parse_command(self, message, client):
        msg = shlex.split(message.content)
        price_one_ether = self.ethprice()
        if len(msg) > 2: # !eth <type> <hash>
            if msg[1] == 'tx':
                html = requests.get("https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash=" + msg[2] + "&apikey=" + self.api_key)
                data = html.json()["result"]
                if data["input"] == "0x":
                    data["input"] = "0x0"
                data = [dict([x, int(y,16)] for x, y in data.items())][0]
                data["from"] = "0x" + str("{0:x}".format(data["from"]))
                data["to"] = "0x" + str("{0:x}".format(data["to"]))
                if data["input"] == 0:
                    txn_type = 'std'
                else:
                    txn_type = 'ctt'
                embed = discord.Embed(title="Transaction information", description="Transaction: " + msg[2], colour=0xecf0f1)
                embed.add_field(name="Transaction type", value=self.txn_types[txn_type], inline=True)
                embed.add_field(name="In Block", value=self.comma_money(int(data["blockNumber"])), inline=True)
                embed.add_field(name="From", value=data["from"], inline=True)
                embed.add_field(name="To", value=data["to"], inline=True)
                embed.add_field(name="Value", value=self.wei_to_eth(data["value"]), inline=True)
                embed.add_field(name="Gas Consumed", value=self.comma_money(int(data["gas"])), inline=True)
                embed.add_field(name="Gas Price", value=str(data["gasPrice"]/1000000000) + " GWei", inline=True)
                embed.set_footer(text="Information provided by etherscan.io")
                await client.send_message(message.channel, embed=embed)

            elif msg[1] == 'address' or msg[1] == 'addr':
                html = requests.get("https://api.etherscan.io/api?module=account&action=balance&address=" + msg[2] + "&tag=latest&apikey=" + self.api_key)
                data = html.json()
                embed = discord.Embed(title="Address information", description="Address: " + msg[2], color=0xecf0f1)
                ether_balance = self.wei_to_eth(int(data["result"]))
                embed.add_field(name="Balance", value=str(ether_balance) + " ETH (US$ " + self.comma_money(float("{0:.2f}".format(ether_balance*price_one_ether))) + ")", inline=True)
                embed.set_footer(text="Information provided by etherscan.io")
                await client.send_message(message.channel, embed=embed)