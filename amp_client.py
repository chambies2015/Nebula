import asyncio
import json
import aiohttp
import requests
import tokens
from ampapi.ampapi import AMPAPI
import discord
from config import AMP_BASE_URL, URL_LOGIN, URL_GET_INSTANCE, URL_START, URL_STOP, URL_RESTART

API = AMPAPI(AMP_BASE_URL)

token = None


async def login():
    global token
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


async def get_instance_status(instance_id):
    await login()
    data = {
        "InstanceId": instance_id,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    response = requests.post(URL_GET_INSTANCE, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_content = response.content.decode()
        json_response = json.loads(response_content)
        running_status = json_response.get("Running")
        return running_status, response.status_code
    return None, response.status_code


def build_info_embed(game_config, running_status):
    info_config = game_config["info"]
    embed = discord.Embed(title=info_config["embed_title"], color=discord.Color.blue())
    
    embed.add_field(name='Server IP', value=info_config["ip"], inline=False)
    embed.add_field(name='Server Port', value=info_config["port"], inline=False)
    
    if "name" in info_config:
        embed.add_field(name='Server Name', value=info_config["name"], inline=False)
    if "password" in info_config:
        embed.add_field(name='Server Password', value=info_config["password"], inline=False)
    if "mod_list" in info_config:
        embed.add_field(name='Mod List', value=info_config["mod_list"], inline=False)
    
    status_template = info_config["status_template"]
    if "unable to get status" in status_template:
        game_name = status_template.split(" server is currently")[0].replace("The ", "")
        status_text = f'The {game_name} server is currently {"running" if running_status else "not running or unable to get status"}.'
    else:
        game_name = status_template.split(" server is currently")[0].replace("The ", "")
        status_text = f'The {game_name} server is currently {"running" if running_status else "not running"}.'
    
    embed.add_field(name='Server Status', value=status_text, inline=False)
    
    return embed


async def start_instance(instance_name):
    await login()
    data = {
        "InstanceName": instance_name,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    response = requests.post(URL_START, data=json.dumps(data), headers=headers)
    return response.status_code == 200, response.status_code


async def stop_instance(instance_name):
    await login()
    data = {
        "InstanceName": instance_name,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    response = requests.post(URL_STOP, data=json.dumps(data), headers=headers)
    return response.status_code == 200, response.status_code


async def restart_instance(instance_name):
    await login()
    data = {
        "InstanceName": instance_name,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    response = requests.post(URL_RESTART, data=json.dumps(data), headers=headers)
    return response.status_code == 200, response.status_code
