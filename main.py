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
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# specify the URL endpoint for your game server
API = AMPAPI("http://localhost:8080/")
url_login = "http://localhost:8080/API/Core/Login"
url_start = "https://localhost:8080/API/ADS01/StartInstance"
url_stop = "https://localhost:8080/API/ADS01/StopInstance"

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
        async with session.post(url_login, json=login_data) as resp:
            if resp.headers['Content-Type'] == 'application/json':
                loginResult = await resp.json()

                if "success" in loginResult.keys() and loginResult["success"]:
                    print("Login successful")
                    API.sessionId = loginResult["sessionID"]

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


    # response = requests.post(url_login, data=json.dumps(login_data), headers=headers, verify=True)
    # response_data = response.json()
    #
    # # assuming the response is a JSON object that includes a 'token' key
    # global token
    # token = response_data['token']

@bot.group()
async def ark(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid Ark command passed...')

@ark.command(name='start')
async def ark_start(ctx):
    # specify your data here
    data = {
        "InstanceName": "ARKSurvivalEvolved",
        "token": API.sessionId  # include the token in your requests
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}

    response = requests.post(url_start, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully started the server!')
    else:
        await ctx.send(f'Failed to start the server. HTTP status code: {response.status_code}')


@ark.command(name='stop')
async def ark_stop(ctx):
    # specify your params here
    params = {
        "key1": "value1",
        "key2": "value2",
        "token": token  # include the token in your requests
    }

    headers = {'Accept': 'text/javascript'}

    response = requests.get(url_stop, params=params, headers=headers)

    if response.status_code == 200:
        await ctx.send('Successfully stopped the server!')
    else:
        await ctx.send(f'Failed to stop the server. HTTP status code: {response.status_code}')


# Run the bot
bot.run(bot_token)
