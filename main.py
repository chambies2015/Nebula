import discord
from discord.ext import commands
import requests
import json
import tokens
from ampapi.ampapi import AMPAPI
import aiohttp

# The bot token from Discord Developer Portal
bot_token = tokens.bot_token

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# specify the URL endpoint for your game server
API = AMPAPI("http://localhost:8080/")
url_login = "http://localhost:8080/API/Core/Login"
url_start = "http://localhost:8080/API/ADSModule/StartInstance"
url_stop = "http://localhost:8080/API/ADSModule/StopInstance"
url_restart = "http://localhost:8080/API/ADSModule/RestartInstance"

# global variable to store the token
global token
token = None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Login on startup
    login_data = {
        "username": "admin",
        "password": "CrimsonS0lstice0657^",
        "token": "",
        "rememberMe": "true"
    }

    async with aiohttp.ClientSession() as session:
        headers = {'Accept': 'application/json'}
        async with session.post(url_login, json=login_data, headers=headers) as resp:
            # rest of your code

            if resp.headers['Content-Type'] == 'application/json':
                loginResult = await resp.json()

                if "success" in loginResult.keys() and loginResult["success"]:
                    print("Login successful")
                    API.sessionId = loginResult["sessionID"]
                    global token
                    token = loginResult['sessionID']

                    await API.Core_SendConsoleMessageAsync("say Hello Everyone, this message was sent from the Python API!")
                    currentStatus = await API.Core_GetStatusAsync()
                    CPUUsagePercent = currentStatus["Metrics"]["CPU Usage"]["Percent"]
                    print(f"Current CPU usage is: {CPUUsagePercent}%")

                else:
                    print("Login failed")
                    print(loginResult)

            else:
                print(f"Unexpected content type: {resp.headers['Content-Type']}")
                print(await resp.text())



@bot.group()
async def ark(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid Ark command passed...')

@ark.command(name='start')
async def ark_start(ctx):

    # specify your data here
    data = {
        "InstanceName": "ARKSurvivalEvolved01",
        "SESSIONID": token  # include the token in your requests
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_start, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully started the Ark server!')
    else:
        await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@ark.command(name='stop')
async def ark_stop(ctx):
    # specify your params here
    data = {
        "InstanceName": "ARKSurvivalEvolved01",
        "SESSIONID": token  # include the token in your requests
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_stop, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully stopped the server!')
    else:
        await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')

@ark.command(name='restart')
async def ark_restart(ctx):
    # specify your params here
    data = {
        "InstanceName": "ARKSurvivalEvolved01",
        "SESSIONID": token  # include the token in your requests
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_restart, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully restarted the server!')
    else:
        await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


@bot.group()
async def terraria(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid terraria command passed...')

@terraria.command(name='start')
async def terraria_start(ctx):
    # specify your data here
    data = {
        "InstanceName": "tModLoader1401",
        "SESSIONID": token  # include the token in your requests
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_start, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully started the terraria server!')
    else:
        await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@terraria.command(name='stop')
async def terraria_stop(ctx):
    # specify your params here
    data = {
        "InstanceName": "tModLoader1401",
        "SESSIONID": token  # include the token in your requests
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_stop, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully stopped the terraria server!')
    else:
        await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')

@terraria.command(name='restart')
async def terraria_restart(ctx):
    # specify your params here
    data = {
        "InstanceName": "tModLoader1401",
        "SESSIONID": token  # include the token in your requests
    }

    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_restart, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully restarted the terraria server!')
    else:
        await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')

# Run the bot
bot.run(bot_token)
