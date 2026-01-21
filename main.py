import discord
from discord.ext import commands
from discord.ext.commands import check
import tokens
import aiohttp
from ampapi.ampapi import AMPAPI
from config import ALLOWED_CHANNELS, AMP_BASE_URL, URL_LOGIN
from amp_client import API
import commands as game_commands

bot_token = tokens.bot_token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

allowed_channels = ALLOWED_CHANNELS


def is_allowed_channel(ctx):
    return str(ctx.channel.id) in allowed_channels


bot.add_check(check(is_allowed_channel))


# @bot.command(name="getinstances")
# async def get_instances(ctx):
#     await login()
#     headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
#     data = {
#         "SESSIONID": token
#     }
#     response = requests.post(url_Instances_Status, data=json.dumps(data), headers=headers)
#     test = response.content
#     print(test)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    login_data = {
        "username": tokens.username,
        "password": tokens.password,
        "token": "",
        "rememberMe": "true"
    }

    async with aiohttp.ClientSession() as session:
        headers = {'Accept': 'application/json'}
        async with session.post(URL_LOGIN, json=login_data, headers=headers) as resp:

            if resp.headers['Content-Type'] == 'application/json':
                loginResult = await resp.json()

                if "success" in loginResult.keys() and loginResult["success"]:
                    print("Login successful")
                    API.sessionId = loginResult["sessionID"]
                    import amp_client
                    amp_client.token = loginResult['sessionID']
                    currentStatus = await API.Core_GetStatusAsync()
                    CPUUsagePercent = currentStatus["Metrics"]["CPU Usage"]["Percent"]
                    print(f"Current CPU usage is: {CPUUsagePercent}%")

                else:
                    print("Login failed")
                    print(loginResult)

            else:
                print(f"Unexpected content type: {resp.headers['Content-Type']}")
                print(await resp.text())


bot.add_command(game_commands.ark)
bot.add_command(game_commands.terraria)
bot.add_command(game_commands.necesse)
bot.add_command(game_commands.icarus)
bot.add_command(game_commands.minecraft)
bot.add_command(game_commands.satisfactory)
bot.add_command(game_commands.sevendaystodie)
bot.add_command(game_commands.projectzomboid)
bot.add_command(game_commands.beamng)
bot.add_command(game_commands.sotf)
bot.add_command(game_commands.enshrouded)
bot.add_command(game_commands.palworld)
bot.add_command(game_commands.atm10)


@bot.command(help="displays helpful commands.")
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="These are the available commands",
                          color=discord.Color.blue())

    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)


bot.run(bot_token)
