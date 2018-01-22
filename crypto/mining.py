import discord
import requests
import asyncio
import shlex
from modules.botModule import *

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
        if len(msg) == 1: # !mining
            pass
            # TODO: Mining profitability
        elif len(msg) > 1: # !mining <addid/hashrate/rank> ...
            if msg[1] == 'id':
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
