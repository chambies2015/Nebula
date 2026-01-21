import asyncio
import discord
from discord.ext import commands
from typing import Optional
from config import GAME_CONFIGS, START_DELAY_SECONDS, COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER
from amp_client import login, get_instance_status, build_info_embed, start_instance, stop_instance, restart_instance
from batch_server import start_batch_server, stop_batch_server, is_server_running, force_kill_all_processes
from sensitive import AUTHORIZED_USER_ID


def create_game_group(game_key: str, game_config: dict, use_amp: bool = True):
    @commands.group(name=game_key, help=game_config["group_help"], invoke_without_command=True)
    async def group(ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                if use_amp:
                    await login()
                embed = discord.Embed(
                    title=game_config["embed_title"],
                    description="These are the available commands",
                    color=discord.Color.blue()
                )
                for command in group.commands:
                    embed.add_field(name=command.name, value=command.help, inline=False)
                await ctx.send(embed=embed)
    
    return group


def create_info_command(group: commands.Group, game_key: str, game_config: dict, use_amp: bool = True):
    @group.command(name='info', help=game_config["info"]["help"])
    async def info_cmd(ctx: commands.Context) -> None:
        async with ctx.typing():
            if use_amp:
                running_status, status_code = await get_instance_status(game_config["instance_id"])
                if running_status is not None:
                    embed = build_info_embed(game_config, running_status)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')
            else:
                running_status = is_server_running(game_key)
                info_config = game_config["info"]
                embed = discord.Embed(title=info_config["embed_title"], color=discord.Color.blue())
                embed.add_field(name='Server IP', value=info_config["ip"], inline=False)
                embed.add_field(name='Server Port', value=info_config["port"], inline=False)
                status_text = f'The {game_key.upper()} server is currently {"running" if running_status else "not running"}.'
                embed.add_field(name='Server Status', value=status_text, inline=False)
                await ctx.send(embed=embed)


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
                success, message = await start_batch_server(game_key, batch_path)
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
                success, message = await stop_batch_server(game_key)
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
                success_stop, message_stop = await stop_batch_server(game_key)
                if success_stop:
                    await asyncio.sleep(2)
                batch_path = game_config.get("batch_script_path")
                if not batch_path:
                    await ctx.send(f'Batch script path not configured. Please set {game_key}.batch_script_path in config.py')
                    return
                success_start, message_start = await start_batch_server(game_key, batch_path)
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


ark = register_game_commands("ark", GAME_CONFIGS["ark"])
terraria = register_game_commands("terraria", GAME_CONFIGS["terraria"])
necesse = register_game_commands("necesse", GAME_CONFIGS["necesse"])
icarus = register_game_commands("icarus", GAME_CONFIGS["icarus"])
minecraft = register_game_commands("minecraft", GAME_CONFIGS["minecraft"])
satisfactory = register_game_commands("satisfactory", GAME_CONFIGS["satisfactory"])
sevendaystodie = register_game_commands("sevendaystodie", GAME_CONFIGS["sevendaystodie"])
projectzomboid = register_game_commands("projectzomboid", GAME_CONFIGS["projectzomboid"])
beamng = register_game_commands("beamng", GAME_CONFIGS["beamng"])
sotf = register_game_commands("sotf", GAME_CONFIGS["sotf"])
enshrouded = register_game_commands("enshrouded", GAME_CONFIGS["enshrouded"])
palworld = register_game_commands("palworld", GAME_CONFIGS["palworld"])
atm10 = register_game_commands("atm10", GAME_CONFIGS["atm10"], use_amp=False, has_forcekill=True)
