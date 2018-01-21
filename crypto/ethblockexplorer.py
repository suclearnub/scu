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

    async def parse_command(self, message, client):
        msg = shlex.split(message.content)
        price_one_ether = self.ethprice()
        if len(msg) > 2: # !eth <type> <hash>
            if msg[1] == 'tx':
                # TODO: Add tx
                pass
            elif msg[1] == 'address' or msg[1] == 'addr':
                html = requests.get("https://api.etherscan.io/api?module=account&action=balance&address=" + msg[2] + "&tag=latest&apikey=" + self.api_key)
                data = html.json()
                embed = discord.Embed(title="Address information", description="Address: " + msg[2], color=0xecf0f1)
                ether_balance = self.wei_to_eth(int(data["result"]))
                embed.add_field(name="Balance", value=str(ether_balance) + " ETH (US$ " + self.comma_money(float("{0:.2f}".format(ether_balance*price_one_ether))) + ")", inline=True)
                embed.set_footer(text="Powered by etherscan.io")
                await client.send_message(message.channel, embed=embed)