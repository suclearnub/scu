import discord
import requests
import asyncio
import shlex
from modules.botModule import *
from modules.crypto.utils import *

class Mining(BotModule):
    name = 'mining'

    description = 'MiningPoolHub Stats'

    help_text = 'Shows stats from MiningPoolHub.\n' \
                '!mining id poolid apikey - Updates your API keys for the bot to use\n' \
                '!mining hashrate coin - Checks your hashrate for a particular coin' \

    trigger_string = 'mining'

    has_background_loop = False # True

    module_version = '0.1.0'

    api_key = ''

    top_mining_results = 5

    units = {'bitcoin-gold': 'Sol/s',
             'zclassic': 'Sol/s',
             'zcash': 'Sol/s',
             'zencash': 'Sol/s',
             }

    # Divide by how many to get 'sensible' number
    factor = {'bitcoin-gold': 0.001,
             'zclassic': 0.001,
             'zcash': 0.00,
             'zencash': 0.001,
             }

    mining_speed = {'ethash': 84,
                    'groest': 63.9,
                    'x11gost': 20.1,
                    'cryptonight': 2190,
                    'equihash': 870,
                    'lyra2rev2': 14700,
                    'neoscrypt': 1950,
                    'lbry': 315,
                    'blake2b': 3450,
                    'blake14r': 5910,
                    'pascal': 2100,
                    'skunkhash': 54,
                    'nist5': 57
                    }

    mining_units = {'ethash': 'MH-day',
                    'groest': 'MH-day',
                    'x11gost': 'MH-day',
                    'cryptonight': 'H-day',
                    'equihash': 'H-day',
                    'lyra2rev2': 'KH-day',
                    'neoscrypt': 'KH-day',
                    'lbry': 'MH-day',
                    'blake2b': 'MH-day',
                    'blake14r': 'MH-day',
                    'pascal': 'MH-day',
                    'skunkhash': 'MH-day',
                    'nist5': 'MH-day'
    }
    def prettify_hashrate(self, raw_hashrate, coin):
        try:
            return str(self.comma_money(raw_hashrate/self.factor[coin])) + ' ' + self.units[coin]
        except KeyError:
            return str(self.comma_money(raw_hashrate)) + ' H/s'

    def comma_money(self, value):
        return "{:,}".format(value)

    async def parse_command(self, message, client):
        target_user = Query()
        msg = shlex.split(message.content)
        if len(msg) > 1: # !mining <addid/hashrate/rank> ...
            if msg[1] == 'profit':
                if len(msg) < 3:
                    msg[2] = 'equihash'
                html = requests.get("http://whattomine.com/coins.json")
                data = html.json()["coins"]
                filtered_coins = [[key, float(data[key]["btc_revenue24"])*get_price('bitcoin')/self.mining_speed[data[key]["algorithm"].lower()]] for key in data if data[key]["algorithm"].lower() == msg[2].lower()]
                filtered_coins.sort(key=lambda x: x[1], reverse=True)
                embed = discord.Embed(title="Mining Profitability", description="On algorithm " + msg[2])
                count = 1
                for entry in filtered_coins:
                    if count <= 5:
                        embed.add_field(name="#" + str(count) + ": " + str(entry[0]), value="US$ " + str(entry[1]) + " " + self.mining_units[msg[2]])
                        count += 1;
                    else:
                        break
                embed.set_footer(text="Information provided by http://whattomine.com/")
                await client.send_message(message.channel, embed=embed)
            elif msg[1] == 'id':
                if len(msg) < 4:
                    msg = '[!] No ID found.'
                    await client.send_message(message.channel, msg)
                else:
                    if self.module_db.get(target_user.userid == message.author.id) is None:
                        self.module_db.insert({'userid': message.author.id, 'poolid': msg[2], 'api': msg[3]})
                    else:
                        self.module_db.update({'userid': message.author.id, 'poolid': msg[2], 'api': msg[3]})
                    msg = '[:ok_hand:] Successfully set Pool ID and API.'
                    await client.send_message(message.channel, msg)
            elif msg[1] == 'hashrate':
                if len(msg) < 2:
                    msg = '[!] No coin specified.'
                    await client.send_message(message.channel, msg)
                elif self.module_db.get(target_user.userid == message.author.id)['poolid'] is None or self.module_db.get(target_user.userid == message.author.id)['api'] is None:
                    msg = '[!] No API setup. See !help mining for more information'
                    await client.send_message(message.channel, msg)
                else:
                    user_id = self.module_db.get(target_user.userid == message.author.id)['poolid']
                    user_api = self.module_db.get(target_user.userid == message.author.id)['api']
                    html = requests.get("https://" + msg[2] + ".miningpoolhub.com/index.php?page=api&action=getuserhashrate&api_key=" + user_api + "&id=" + user_id)
                    data = html.json()["getuserhashrate"]
                    embed = discord.Embed(title="Hashrate Information", description="On coin " + msg[2], color=0xb75853)
                    embed.add_field(name="Hashrate", value=self.prettify_hashrate(float(data["data"]), msg[2]), inline=True)
                    embed.set_footer(text="Mining on https://miningpoolhub.com | Refreshes every 5 minutes")
                    await client.send_message(message.channel, embed=embed)
            elif msg[1] == 'rank':
                pass
                # TODO: Use API to get a hashrate ranking
