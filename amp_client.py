import asyncio
import json
import aiohttp
import time
import tokens
from ampapi.ampapi import AMPAPI
import discord
from config import AMP_BASE_URL, URL_LOGIN, URL_GET_INSTANCE, URL_START, URL_STOP, URL_RESTART
from typing import Optional, Tuple
from logger import setup_logger

logger = setup_logger("amp_client")

API = AMPAPI(AMP_BASE_URL)

token: Optional[str] = None
token_expiry: float = 0
SESSION_TIMEOUT = 30 * 60
_session: Optional[aiohttp.ClientSession] = None


async def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


async def ensure_authenticated() -> bool:
    global token, token_expiry
    current_time = time.time()
    
    if token is None or current_time >= token_expiry:
        return await login()
    return True


async def login() -> bool:
    global token, token_expiry
    login_data = {
        "username": tokens.username,
        "password": tokens.password,
        "token": "",
        "rememberMe": "true"
    }

    session = await get_session()
    headers = {'Accept': 'application/json'}
    
    try:
        async with session.post(URL_LOGIN, json=login_data, headers=headers) as resp:
            if resp.headers.get('Content-Type', '').startswith('application/json'):
                loginResult = await resp.json()

                if "success" in loginResult.keys() and loginResult["success"]:
                    logger.info("Login successful")
                    API.sessionId = loginResult["sessionID"]
                    token = loginResult['sessionID']
                    token_expiry = time.time() + SESSION_TIMEOUT
                    
                    try:
                        currentStatus = await API.Core_GetStatusAsync()
                        CPUUsagePercent = currentStatus["Metrics"]["CPU Usage"]["Percent"]
                        logger.info(f"Current CPU usage is: {CPUUsagePercent}%")
                    except Exception as e:
                        logger.warning(f"Failed to get CPU usage: {e}")
                    
                    return True
                else:
                    logger.error(f"Login failed: {loginResult}")
                    return False
            else:
                content_type = resp.headers.get('Content-Type', 'unknown')
                logger.error(f"Unexpected content type: {content_type}")
                text = await resp.text()
                logger.error(f"Response text: {text}")
                return False
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        return False


async def get_instance_status(instance_id: str) -> Tuple[Optional[bool], int]:
    if not await ensure_authenticated():
        return None, 401
    
    data = {
        "InstanceId": instance_id,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    
    session = await get_session()
    try:
        async with session.post(URL_GET_INSTANCE, data=json.dumps(data), headers=headers) as resp:
            if resp.status == 200:
                response_content = await resp.text()
                json_response = json.loads(response_content)
                running_status = json_response.get("Running")
                return running_status, resp.status
            return None, resp.status
    except Exception as e:
        logger.error(f"Error getting instance status: {e}", exc_info=True)
        return None, 500


def build_info_embed(game_config: dict, running_status: bool) -> discord.Embed:
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


async def start_instance(instance_name: str) -> Tuple[bool, int]:
    if not await ensure_authenticated():
        return False, 401
    
    data = {
        "InstanceName": instance_name,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    
    session = await get_session()
    try:
        async with session.post(URL_START, data=json.dumps(data), headers=headers) as resp:
            return resp.status == 200, resp.status
    except Exception as e:
        logger.error(f"Error starting instance: {e}", exc_info=True)
        return False, 500


async def stop_instance(instance_name: str) -> Tuple[bool, int]:
    if not await ensure_authenticated():
        return False, 401
    
    data = {
        "InstanceName": instance_name,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    
    session = await get_session()
    try:
        async with session.post(URL_STOP, data=json.dumps(data), headers=headers) as resp:
            return resp.status == 200, resp.status
    except Exception as e:
        logger.error(f"Error stopping instance: {e}", exc_info=True)
        return False, 500


async def restart_instance(instance_name: str) -> Tuple[bool, int]:
    if not await ensure_authenticated():
        return False, 401
    
    data = {
        "InstanceName": instance_name,
        "SESSIONID": token
    }
    headers = {'Content-type': 'application/json', 'Accept': 'text/javascript'}
    
    session = await get_session()
    try:
        async with session.post(URL_RESTART, data=json.dumps(data), headers=headers) as resp:
            return resp.status == 200, resp.status
    except Exception as e:
        logger.error(f"Error restarting instance: {e}", exc_info=True)
        return False, 500
