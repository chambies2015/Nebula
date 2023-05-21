import asyncio
import time

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

global token
token = None


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
            login()
            embed = discord.Embed(title="Ark Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in ark.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@ark.command(name='info', help="Displays the server info for Ark Survival Evolved game server.")
async def ark_info(ctx):
    async with ctx.typing():
        login()
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
                            value=f'The Ark server is currently {"running" if running_status else "not running or unable to get status"}.',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {response.status_code}')


@ark.command(name='start', help="Starts the spooling up process for Ark Survival Evolved. Takes awhile due to large "
                                "game.")
async def ark_start(ctx):
    async with ctx.typing():
        login()

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
        login()

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
        login()

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
            login()
            embed = discord.Embed(title="Terraria Bot Commands", description="These are the available commands",
                                  color=discord.Color.blue())

            for command in terraria.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@terraria.command(name='info', help="Displays the server info for the Terraria game server.")
async def terraria_info(ctx):
    async with ctx.typing():
        login()
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
        login()

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
        login()

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
        login()

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


@bot.command(help="displays helpful commands.")
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="These are the available commands",
                          color=discord.Color.blue())

    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help, inline=False)

    await ctx.send(embed=embed)


bot.run(bot_token)
