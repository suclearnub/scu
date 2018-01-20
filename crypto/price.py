import discord
import requests
import asyncio
import shlex
from modules.botModule import BotModule

class Price(BotModule):
    name = 'price'

    description = 'Price checker for cryptocurrency'

    help_text = 'Displays price and stats about that cryptocurrency.'

    trigger_string = 'price'

    has_background_loop = False

    module_version = '0.1.0'

    def price_change(self, percent, price):
        return (price)/(1+(percent/100))

    async def parse_command(self, message, client):
        msg = shlex.split(message.content)
        if len(msg) > 1:
            html = requests.get("https://api.coinmarketcap.com/v1/ticker/" + msg[1])
            data = html.json()
            embed = discord.Embed(title= data["name"] + " Information", description="#" + data["rank"] + " in terms of market capitalization")
            embed.add_field(name="Price", value="$ " + data["price_usd"] + "USD", inline=True)
            embed.add_field(name="24h Change", value=data["percent_change_24h"] + "% (" + price_change(data["percent_change_24h"], data["price_usd"]) + ")", inline=True)
            embed.add_field(name="Market Capitalization", value="US$" + "{:,}".format(data["market_cap_usd"]), inline=True)
            embed.add_field(name="24h Volume", value="US$" + "{:,}".format(data["24h_volume_usd"]), inline=True)
            embed.set_footer(text="Information provided by coinmarketcap.com")
            await client.send_message(message.channel, embed=embed)