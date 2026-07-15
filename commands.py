import asyncio
from pathlib import Path

import discord
from discord.ext import commands
from config import GAME_CONFIGS, START_DELAY_SECONDS, COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER
from amp_client import get_instance_status, build_info_embed, start_instance, stop_instance, restart_instance
from batch_server import start_batch_server, stop_batch_server, is_server_running, force_kill_all_processes
from palworld_api import is_configured as rest_api_is_configured, save_and_shutdown
from sensitive import AUTHORIZED_USER_ID


def create_game_group(game_key: str, game_config: dict, use_amp: bool = True):
    @commands.group(name=game_key, help=game_config["group_help"], invoke_without_command=True)
    async def group(ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                embed = discord.Embed(
                    title=game_config["embed_title"],
                    description="These are the available commands",
                    color=discord.Color.blue()
                )
                for command in group.commands:
                    embed.add_field(name=command.name, value=command.help, inline=False)
                await ctx.send(embed=embed)
    
    return group


async def stop_batch_game(game_key: str, game_config: dict):
    rest_api_config = game_config.get("rest_api")
    if rest_api_is_configured(rest_api_config):
        return await save_and_shutdown(rest_api_config)

    return await stop_batch_server(
        game_key,
        game_config.get("process_match_terms"),
    )


async def wait_for_batch_server_stop(game_key: str, game_config: dict) -> bool:
    rest_api_config = game_config.get("rest_api") or {}
    timeout_seconds = rest_api_config.get("shutdown_wait_seconds", 0) + 45

    for _ in range(timeout_seconds):
        if not is_server_running(game_key, game_config.get("process_match_terms")):
            return True
        await asyncio.sleep(1)
    return False


async def send_info_embed(ctx: commands.Context, embed: discord.Embed, info_config: dict) -> None:
    package_path = info_config.get("mod_package_path")
    if package_path and Path(package_path).is_file():
        await ctx.send(
            embed=embed,
            file=discord.File(
                package_path,
                filename=info_config.get("mod_package_filename") or Path(package_path).name,
            ),
        )
        return

    await ctx.send(embed=embed)


def create_info_command(group: commands.Group, game_key: str, game_config: dict, use_amp: bool = True):
    @group.command(name='info', help=game_config["info"]["help"])
    async def info_cmd(ctx: commands.Context) -> None:
        async with ctx.typing():
            if use_amp:
                running_status, status_code = await get_instance_status(game_config["instance_id"])
                if running_status is not None:
                    embed = build_info_embed(game_config, running_status)
                    await send_info_embed(ctx, embed, game_config["info"])
                else:
                    await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')
            else:
                running_status = is_server_running(
                    game_key,
                    game_config.get("process_match_terms"),
                )
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
                status_text = f'The {game_key.upper()} server is currently {"running" if running_status else "not running"}.'
                embed.add_field(name='Server Status', value=status_text, inline=False)
                await send_info_embed(ctx, embed, info_config)


def create_start_command(group: commands.Group, game_key: str, game_config: dict, use_amp: bool = True):
    @group.command(name='start', help=game_config["start"]["help"], aliases=['s'])
    @commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
    async def start_cmd(ctx: commands.Context) -> None:
        async with ctx.typing():
            if use_amp:
                success, status_code = await start_instance(game_config["instance_name"])
                if success:
                    await asyncio.sleep(START_DELAY_SECONDS)
                    await ctx.send(game_config["start"]["success_msg"])
                else:
                    await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')
            else:
                batch_path = game_config.get("batch_script_path")
                if not batch_path:
                    await ctx.send(f'Batch script path not configured. Please set {game_key}.batch_script_path in config.py')
                    return
                success, message = await start_batch_server(
                    game_key,
                    batch_path,
                    game_config.get("process_match_terms"),
                    game_config.get("keep_console_open", True),
                )
                if success:
                    await ctx.send(game_config["start"]["success_msg"])
                else:
                    await ctx.send(f'Failed to start the server: {message}')


def create_stop_command(group: commands.Group, game_key: str, game_config: dict, use_amp: bool = True):
    @group.command(name='stop', help=game_config["stop"]["help"], aliases=['st'])
    @commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
    async def stop_cmd(ctx: commands.Context) -> None:
        async with ctx.typing():
            if use_amp:
                success, status_code = await stop_instance(game_config["instance_name"])
                if success:
                    await ctx.send(game_config["stop"]["success_msg"])
                else:
                    await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')
            else:
                success, message = await stop_batch_game(game_key, game_config)
                if success:
                    await ctx.send(game_config["stop"]["success_msg"])
                else:
                    await ctx.send(f'Failed to stop the server: {message}')


def create_restart_command(group: commands.Group, game_key: str, game_config: dict, use_amp: bool = True):
    @group.command(name='restart', help=game_config["restart"]["help"], aliases=['r'])
    @commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
    async def restart_cmd(ctx: commands.Context) -> None:
        async with ctx.typing():
            if use_amp:
                success, status_code = await restart_instance(game_config["instance_name"])
                if success:
                    await ctx.send(game_config["restart"]["success_msg"])
                else:
                    await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')
            else:
                success_stop, message_stop = await stop_batch_game(game_key, game_config)
                if not success_stop:
                    await ctx.send(f'Failed to restart the server: {message_stop}')
                    return

                if not await wait_for_batch_server_stop(game_key, game_config):
                    await ctx.send('Failed to restart the server: server did not stop before the timeout.')
                    return

                batch_path = game_config.get("batch_script_path")
                if not batch_path:
                    await ctx.send(f'Batch script path not configured. Please set {game_key}.batch_script_path in config.py')
                    return
                success_start, message_start = await start_batch_server(
                    game_key,
                    batch_path,
                    game_config.get("process_match_terms"),
                    game_config.get("keep_console_open", True),
                )
                if success_start:
                    await ctx.send(game_config["restart"]["success_msg"])
                else:
                    await ctx.send(f'Failed to restart the server: {message_start}')


def create_forcekill_command(group: commands.Group, game_key: str):
    @group.command(name='forcekill', help="Forcefully kills all Java and cmd.exe processes related to the server.")
    async def forcekill_cmd(ctx: commands.Context) -> None:
        if ctx.author.id != AUTHORIZED_USER_ID:
            await ctx.send('❌ You do not have permission to use this command.')
            return
        
        async with ctx.typing():
            success, message = await force_kill_all_processes(game_key)
            if success:
                await ctx.send(f'✅ {message}')
            else:
                await ctx.send(f'❌ {message}')


def register_game_commands(game_key: str, game_config: dict, use_amp: bool = True, has_forcekill: bool = False) -> commands.Group:
    group = create_game_group(game_key, game_config, use_amp)
    create_info_command(group, game_key, game_config, use_amp)
    create_start_command(group, game_key, game_config, use_amp)
    create_stop_command(group, game_key, game_config, use_amp)
    create_restart_command(group, game_key, game_config, use_amp)
    
    if has_forcekill:
        create_forcekill_command(group, game_key)
    
    return group


def uses_amp(game_config: dict) -> bool:
    return game_config.get("use_amp", "instance_id" in game_config and "instance_name" in game_config)


def has_forcekill(game_key: str, game_config: dict) -> bool:
    return game_config.get("has_forcekill", game_key == "atm10")


GAME_COMMANDS = {
    game_key: register_game_commands(
        game_key,
        game_config,
        use_amp=uses_amp(game_config),
        has_forcekill=has_forcekill(game_key, game_config),
    )
    for game_key, game_config in GAME_CONFIGS.items()
}

globals().update(GAME_COMMANDS)
