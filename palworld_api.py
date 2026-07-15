import asyncio

import aiohttp

from logger import setup_logger

logger = setup_logger("palworld_api")


def is_configured(rest_api_config):
    return bool(
        rest_api_config
        and rest_api_config.get("base_url")
        and rest_api_config.get("username")
        and rest_api_config.get("password")
    )


async def _request(rest_api_config, method, endpoint, payload=None):
    if not is_configured(rest_api_config):
        return False, None, "Palworld REST API credentials are not configured"

    url = f"{rest_api_config['base_url'].rstrip('/')}/{endpoint.lstrip('/')}"
    auth = aiohttp.BasicAuth(
        rest_api_config["username"],
        rest_api_config["password"],
    )
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with aiohttp.ClientSession(auth=auth, timeout=timeout) as session:
            async with session.request(method, url, json=payload) as response:
                if response.status != 200:
                    return False, None, f"HTTP status code: {response.status}"

                if response.content_type == "application/json":
                    return True, await response.json(), ""
                return True, None, ""
    except (aiohttp.ClientError, asyncio.TimeoutError) as error:
        logger.error(f"Palworld REST API request failed: {error}")
        return False, None, str(error)


async def get_server_info(rest_api_config):
    return await _request(rest_api_config, "GET", "info")


async def save_and_shutdown(rest_api_config):
    saved, _, save_message = await _request(rest_api_config, "POST", "save")
    if not saved:
        return False, f"Could not save the world: {save_message}"

    wait_seconds = rest_api_config.get("shutdown_wait_seconds", 15)
    payload = {
        "waittime": wait_seconds,
        "message": "The Palworld server is shutting down for maintenance.",
    }
    shutdown, _, shutdown_message = await _request(rest_api_config, "POST", "shutdown", payload)
    if not shutdown:
        return False, f"Could not request shutdown: {shutdown_message}"
    return True, f"Server shutdown requested; waiting {wait_seconds} seconds."
