import asyncio
import discord
from discord.ext import commands
import requests
import json
import tokens
from ampapi.ampapi import AMPAPI
import aiohttp
from discord.ext.commands import check

bot_token = tokens.bot_token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

allowed_channels = ["1014955844913332334", "939660290172268583", "809544965386272790"]


def is_allowed_channel(ctx):
    return str(ctx.channel.id) in allowed_channels


bot.add_check(check(is_allowed_channel))

API = AMPAPI("http://localhost:8080/")
url_login = "http://localhost:8080/API/Core/Login"
url_start = "http://localhost:8080/API/ADSModule/StartInstance"
url_stop = "http://localhost:8080/API/ADSModule/StopInstance"
url_restart = "http://localhost:8080/API/ADSModule/RestartInstance"
url_Network_Info = "http://localhost:8080/API/ADSModule/GetInstanceNetworkInfo"
url_Instances_Status = "http://localhost:8080/API/ADSModule/GetInstanceStatuses"
url_Get_Instance = "http://localhost:8080/API/ADSModule/GetInstance"

ark_instance_id = "2033ec8f-244f-4af2-a568-4fb362448491"
terraria_instance_id = "d5275053-eafc-493e-bbba-a5658231b7fe"
necesse_instance_id = "592aa884-68c2-47ff-aaeb-cab0be49b395"
icarus_instance_id = "25bb4b25-053e-4992-b69f-3ac20ab5b105"
minecraft_instance_id = "123ffacd-896d-49db-b35a-14e76d13042a"
sevendaystodie_instance_id = "c1e805b3-d386-4de8-80e1-fae15cf1c589"
satisfactory_instance_id = "ba176a72-d8f7-4bfc-b59d-52a4e7814612"
projectzomboid_instance_id = "1c89f2a2-2586-46d2-945b-301cad9b6e08"
beamng_instance_id = "56309d72-174f-4fd6-bd29-75cdd0e3ef4e"
sotf_instance_id = "6c7417c4-34d0-45d0-abc1-37ce4ad43009"

global token
token = None


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
        async with session.post(url_login, json=login_data, headers=headers) as resp:

            if resp.headers['Content-Type'] == 'application/json':
                loginResult = await resp.json()

                if "success" in loginResult.keys() and loginResult["success"]:
                    print("Login successful")
                    API.sessionId = loginResult["sessionID"]
                    global token
                    token = loginResult['sessionID']
                    currentStatus = await API.Core_GetStatusAsync()
                    CPUUsagePercent = currentStatus["Metrics"]["CPU Usage"]["Percent"]
                    print(f"Current CPU usage is: {CPUUsagePercent}%")

                else:
                    print("Login failed")
                    print(loginResult)

            else:
                print(f"Unexpected content type: {resp.headers['Content-Type']}")
                print(await resp.text())


async def login():
    login_data = {
        "username": tokens.username,
        "password": tokens.password,
        "token": "",
        "rememberMe": "true"
    }

    async with aiohttp.ClientSession() as session:
        headers = {'Accept': 'application/json'}
        async with session.post(url_login, json=login_data, headers=headers) as resp:

            if resp.headers['Content-Type'] == 'application/json':
                loginResult = await resp.json()

                if "success" in loginResult.keys() and loginResult["success"]:
                    print("Login successful")
                    API.sessionId = loginResult["sessionID"]
                    global token
                    token = loginResult['sessionID']
                    currentStatus = await API.Core_GetStatusAsync()
                    CPUUsagePercent = currentStatus["Metrics"]["CPU Usage"]["Percent"]
                    print(f"Current CPU usage is: {CPUUsagePercent}%")

                else:
                    print("Login failed")
                    print(loginResult)

            else:
                print(f"Unexpected content type: {resp.headers['Content-Type']}")
                print(await resp.text())


@bot.group(help="ARK commands to start, stop, restart, and get info on the server")
async def ark(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Ark Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in ark.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@ark.command(name='info', help="Displays the server info for Ark Survival Evolved game server.")
async def ark_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": ark_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='ARK Survival Evolved Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='7777', inline=False)
            embed.add_field(name='Server Name', value='Chambies Private Server', inline=False)
            embed.add_field(name='Server Password', value='thebois', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Ark server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@ark.command(name='start', help="Starts the spooling up process for Ark Survival Evolved. Takes awhile due to large "
                                "game.")
async def ark_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "ARKSurvivalEvolved01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Ark server! This will take some time, ~15-20 minutes.')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@ark.command(name='stop', help="Sends a stop signal to the Ark Survival Evolved game server.")
async def ark_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "ARKSurvivalEvolved01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@ark.command(name='restart', help="Sends a restart signal to the Ark Survival Evolved game server, may take awhile.")
async def ark_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "ARKSurvivalEvolved01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@bot.group(help="Terraria commands to start, stop, restart, and get info on the server")
async def terraria(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Terraria Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in terraria.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@terraria.command(name='info', help="Displays the server info for the Terraria game server.")
async def terraria_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": terraria_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")  # use dict's get() method to avoid KeyError

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Terraria Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='7779', inline=False)
            embed.add_field(name='Server Password', value='thebois', inline=False)
            embed.add_field(name='Mod List', value="""
            Boss Checklist v1.4.0
            Calamity Mod v2.0.2.3
            Calamity Mod Music v2.0.2.2
            Calamity's Vanities v10.2
            Quality of Life 更好的体验 v1.6.3.3
            Magic Storage v0.5.7.10
            Max Stack Plus Extra v1.4.0.2
            Ore Excavator v0.8.4
            Recipe Browser v0.9.8
            """, inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Terraria server is currently {"running" if running_status else "not running or unable to get status"}.',
                            inline=False)

            await ctx.send(embed=embed)

        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@terraria.command(name='start', help="Starts up the Terraria game server relatively quick.")
async def terraria_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "tModLoader1401",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started the terraria server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@terraria.command(name='stop', help="Sends a stop signal to the Terraria game server.")
async def terraria_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "tModLoader1401",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully stopped the terraria server!')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@terraria.command(name='restart', help="Sends a restart signal to the Terraria game server.")
async def terraria_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "tModLoader1401",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the terraria server!')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@bot.group(help="Necesse commands to start, stop, restart, and get info on the server")
async def necesse(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Necesse Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in necesse.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@necesse.command(name='info', help="Displays the server info for the Necesse game server.")
async def necesse_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": necesse_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Necesse Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='15000', inline=False)
            embed.add_field(name='Server Password', value='thebois', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Necesse server is currently {"running" if running_status else "not running or unable to get status"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@necesse.command(name='start', help="Starts the spooling up process for Necesse.")
async def necesse_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Necesse01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Necesse server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@necesse.command(name='stop', help="Sends a stop signal to the Necesse game server.")
async def necesse_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Necesse01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@necesse.command(name='restart', help="Sends a restart signal to the Necesse game server, may take awhile.")
async def necesse_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Necesse01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent the restart signal to the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@bot.group(help="Icarus commands to start, stop, restart, and get info on the server")
async def icarus(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Icarus Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in terraria.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@icarus.command(name='info', help="Displays the server info for the Icarus game server.")
async def icarus_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": icarus_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Icarus Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='19132', inline=False)
            embed.add_field(name='Server Name', value='chambies private server', inline=False)
            embed.add_field(name='Server Password', value='thebois', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Icarus server is currently {"running" if running_status else "not running or unable to get status"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@icarus.command(name='start', help="Starts the spooling up process for Icarus.")
async def icarus_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Icarus01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Icarus server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@icarus.command(name='stop', help="Sends a stop signal to the Icarus game server.")
async def icarus_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Icarus01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@icarus.command(name='restart', help="Sends a restart signal to the Icarus game server, may take awhile.")
async def icarus_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Icarus01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent the restart signal to the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@bot.group(help="Vanilla Minecraft commands to start, stop, restart, and get info on the server")
async def minecraft(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Vanilla Minecraft Bot Commands",
                                  description="These are the available commands",
                                  color=discord.Color.blue())

            for command in minecraft.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@minecraft.command(name='info', help="Displays the server info for Vanilla Minecraft game server.")
async def minecraft_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": minecraft_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Vanilla Minecraft Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='25565', inline=False)
            embed.add_field(name='Server Name', value='The Bois Server', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Vanilla Minecraft server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@minecraft.command(name='start', help="Starts the spooling up process for Vanilla Minecraft.")
async def minecraft_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Minecraft01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Vanilla Minecraft server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@minecraft.command(name='stop', help="Sends a stop signal to the Vanilla Minecraft game server.")
async def minecraft_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Minecraft01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@minecraft.command(name='restart', help="Sends a restart signal to the Vanilla Minecraft game server, may take awhile.")
async def minecraft_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Minecraft01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {response.status_code}')


@bot.group(help="Satisfactory commands to start, stop, restart, and get info on the server")
async def satisfactory(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Satisfactory Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in satisfactory.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@satisfactory.command(name='info', help="Displays the server info for Satisfactory game server.")
async def satisfactory_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": satisfactory_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Satisfactory Server Details (NOT EXPERIMENTAL)', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='7780', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Satisfactory server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@satisfactory.command(name='start', help="Starts the spooling up process for Satisfactory.")
async def satisfactory_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Satisfactory01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Satisfactory server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@satisfactory.command(name='stop', help="Sends a stop signal to the Satisfactory game server.")
async def satisfactory_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Satisfactory01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@satisfactory.command(name='restart', help="Sends a restart signal to the Satisfactory game server, may take awhile.")
async def satisfactory_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "Satisfactory01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {response.status_code}')


@bot.group(help="Seven Days To Die commands to start, stop, restart, and get info on the server")
async def sevendaystodie(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Seven Days To Die Bot Commands",
                                  description="These are the available commands",
                                  color=discord.Color.blue())

            for command in sevendaystodie.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@sevendaystodie.command(name='info', help="Displays the server info for Seven Days To Die game server.")
async def sevendaystodie_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": sevendaystodie_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Seven Days To Die Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='27017', inline=False)
            embed.add_field(name='Server Name', value='The Bois Server', inline=False)
            embed.add_field(name='Server Password', value='thebois', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Seven Days To Die server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@sevendaystodie.command(name='start', help="Starts the spooling up process for Seven Days To Die.")
async def sevendaystodie_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "SevenDaysToDie01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Seven Days To Die server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@sevendaystodie.command(name='stop', help="Sends a stop signal to the Seven Days To Die game server.")
async def sevendaystodie_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "SevenDaysToDie01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@sevendaystodie.command(name='restart',
                        help="Sends a restart signal to the Seven Days To Die game server, may take awhile.")
async def sevendaystodie_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "SevenDaysToDie01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {response.status_code}')


@bot.group(help="Project Zomboid commands to start, stop, restart, and get info on the server")
async def projectzomboid(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Project Zomboid Bot Commands",
                                  description="These are the available commands",
                                  color=discord.Color.blue())

            for command in projectzomboid.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@projectzomboid.command(name='info', help="Displays the server info for Project Zomboid game server.")
async def projectzomboid_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": projectzomboid_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Project Zomboid Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.158.45', inline=False)
            embed.add_field(name='Server Port', value='19133', inline=False)
            embed.add_field(name='Server Name', value='The Bois Server', inline=False)
            embed.add_field(name='Server Password', value='cumbo', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Project Zomboid server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@projectzomboid.command(name='start', help="Starts the spooling up process for Project Zomboid.")
async def projectzomboid_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "ProjectZomboid01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Project Zomboid server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@projectzomboid.command(name='stop', help="Sends a stop signal to the Project Zomboid game server.")
async def projectzomboid_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "ProjectZomboid01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@projectzomboid.command(name='restart',
                        help="Sends a restart signal to the Project Zomboid game server, may take awhile.")
async def projectzomboid_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "ProjectZomboid01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {response.status_code}')


@bot.group(help="BeamNG commands to start, stop, restart, and get info on the server")
async def beamng(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="BeamNG Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in beamng.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@beamng.command(name='info', help="Displays the server info for BeamNG game server.")
async def beamng_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": beamng_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='BeamNG Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.161.61', inline=False)
            embed.add_field(name='Server Port', value='34197', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The BeamNG server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@beamng.command(name='start', help="Starts the spooling up process for BeamNG.")
async def beamng_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "BeamMP01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the BeamNG server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@beamng.command(name='stop', help="Sends a stop signal to the BeamNG game server.")
async def beamng_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "BeamMP01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@beamng.command(name='restart', help="Sends a restart signal to the BeamNG game server, may take awhile.")
async def beamng_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "BeamMP01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully restarted the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {response.status_code}')


@bot.group(help="Sons Of The Forest commands to start, stop, restart, and get info on the server")
async def sotf(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title="Sons Of The Forest Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in beamng.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@sotf.command(name='info', help="Displays the server info for Sons Of The Forest game server.")
async def sotf_info(ctx):
    async with ctx.typing():
        await login()
        data = {
            "InstanceId": sotf_instance_id,
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
        response = requests.post(url_Get_Instance, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_content = response.content.decode()
            json_response = json.loads(response_content)
            running_status = json_response.get("Running")

            # alternative check for 'Running'
            # running_status = json_response["Running"] if "Running" in json_response else None

            embed = discord.Embed(title='Sons Of The Forest Server Details', color=discord.Color.blue())
            embed.add_field(name='Server IP', value='67.4.161.61', inline=False)
            embed.add_field(name='Server Port', value='8777', inline=False)
            embed.add_field(name='Server Status',
                            value=f'The Sons Of The Forest server is currently {"running" if running_status else "not running"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@sotf.command(name='start', help="Starts the spooling up process for Sons Of The Forest.")
async def sotf_start(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "SonsOfTheForest01",
            "SESSIONID": token
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_start, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await asyncio.sleep(20)
            await ctx.send('Successfully started spooling up the Sons Of The Forest server!')
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@sotf.command(name='stop', help="Sends a stop signal to the Sons Of The Forest game server.")
async def sotf_stop(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "SonsOfTheForest01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_stop, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a stop signal to the server! Give it time to stop completely.')
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@sotf.command(name='restart', help="Sends a restart signal to the Sons Of The Forest game server, may take awhile.")
async def sotf_restart(ctx):
    async with ctx.typing():
        await login()

        data = {
            "InstanceName": "SonsOfTheForest01",
            "SESSIONID": token
        }

        headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

        response = requests.post(url_restart, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            await ctx.send('Successfully sent a restart signal to the server! This will take awhile and may fail...')
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {response.status_code}')

@bot.command(help="displays helpful commands.")
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="These are the available commands",
                          color=discord.Color.blue())

    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)


bot.run(bot_token)
