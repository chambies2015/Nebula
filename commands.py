import asyncio
import discord
from discord.ext import commands
from typing import Optional
from config import GAME_CONFIGS, START_DELAY_SECONDS, COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER
from amp_client import login, get_instance_status, build_info_embed, start_instance, stop_instance, restart_instance
from batch_server import start_batch_server, stop_batch_server, is_server_running, force_kill_all_processes




@commands.group(help=GAME_CONFIGS["ark"]["group_help"])
async def ark(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["ark"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in ark.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@ark.command(name='info', help=GAME_CONFIGS["ark"]["info"]["help"])
async def ark_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["ark"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["ark"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@ark.command(name='start', help=GAME_CONFIGS["ark"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def ark_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["ark"]["instance_name"])

        if success:
            await asyncio.sleep(START_DELAY_SECONDS)
            await ctx.send(GAME_CONFIGS["ark"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@ark.command(name='stop', help=GAME_CONFIGS["ark"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def ark_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["ark"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["ark"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@ark.command(name='restart', help=GAME_CONFIGS["ark"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def ark_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["ark"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["ark"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["terraria"]["group_help"])
async def terraria(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["terraria"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in terraria.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@terraria.command(name='info', help=GAME_CONFIGS["terraria"]["info"]["help"])
async def terraria_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["terraria"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["terraria"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@terraria.command(name='start', help=GAME_CONFIGS["terraria"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def terraria_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["terraria"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["terraria"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@terraria.command(name='stop', help=GAME_CONFIGS["terraria"]["stop"]["help"])
async def terraria_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["terraria"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["terraria"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@terraria.command(name='restart', help=GAME_CONFIGS["terraria"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def terraria_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["terraria"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["terraria"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["necesse"]["group_help"])
async def necesse(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["necesse"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in necesse.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@necesse.command(name='info', help=GAME_CONFIGS["necesse"]["info"]["help"])
async def necesse_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["necesse"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["necesse"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@necesse.command(name='start', help=GAME_CONFIGS["necesse"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def necesse_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["necesse"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["necesse"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@necesse.command(name='stop', help=GAME_CONFIGS["necesse"]["stop"]["help"])
async def necesse_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["necesse"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["necesse"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@necesse.command(name='restart', help=GAME_CONFIGS["necesse"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def necesse_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["necesse"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["necesse"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["icarus"]["group_help"])
async def icarus(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["icarus"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in icarus.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@icarus.command(name='info', help=GAME_CONFIGS["icarus"]["info"]["help"])
async def icarus_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["icarus"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["icarus"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@icarus.command(name='start', help=GAME_CONFIGS["icarus"]["start"]["help"])
async def icarus_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["icarus"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["icarus"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@icarus.command(name='stop', help=GAME_CONFIGS["icarus"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def icarus_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["icarus"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["icarus"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@icarus.command(name='restart', help=GAME_CONFIGS["icarus"]["restart"]["help"])
async def icarus_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["icarus"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["icarus"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["minecraft"]["group_help"])
async def minecraft(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["minecraft"]["embed_title"],
                                  description="These are the available commands",
                                  color=discord.Color.blue())

            for command in minecraft.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@minecraft.command(name='info', help=GAME_CONFIGS["minecraft"]["info"]["help"])
async def minecraft_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["minecraft"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["minecraft"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@minecraft.command(name='start', help=GAME_CONFIGS["minecraft"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def minecraft_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["minecraft"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["minecraft"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@minecraft.command(name='stop', help=GAME_CONFIGS["minecraft"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def minecraft_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["minecraft"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["minecraft"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@minecraft.command(name='restart', help=GAME_CONFIGS["minecraft"]["restart"]["help"])
async def minecraft_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["minecraft"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["minecraft"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["satisfactory"]["group_help"])
async def satisfactory(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["satisfactory"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in satisfactory.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@satisfactory.command(name='info', help=GAME_CONFIGS["satisfactory"]["info"]["help"])
async def satisfactory_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["satisfactory"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["satisfactory"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@satisfactory.command(name='start', help=GAME_CONFIGS["satisfactory"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def satisfactory_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["satisfactory"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["satisfactory"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@satisfactory.command(name='stop', help=GAME_CONFIGS["satisfactory"]["stop"]["help"])
async def satisfactory_stop(ctx):
    async with ctx.typing():
        success = await stop_instance(GAME_CONFIGS["satisfactory"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["satisfactory"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@satisfactory.command(name='restart', help=GAME_CONFIGS["satisfactory"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def satisfactory_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["satisfactory"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["satisfactory"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["sevendaystodie"]["group_help"])
async def sevendaystodie(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["sevendaystodie"]["embed_title"],
                                  description="These are the available commands",
                                  color=discord.Color.blue())

            for command in sevendaystodie.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@sevendaystodie.command(name='info', help=GAME_CONFIGS["sevendaystodie"]["info"]["help"])
async def sevendaystodie_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["sevendaystodie"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["sevendaystodie"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@sevendaystodie.command(name='start', help=GAME_CONFIGS["sevendaystodie"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def sevendaystodie_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["sevendaystodie"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["sevendaystodie"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@sevendaystodie.command(name='stop', help=GAME_CONFIGS["sevendaystodie"]["stop"]["help"])
async def sevendaystodie_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["sevendaystodie"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["sevendaystodie"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@sevendaystodie.command(name='restart', help=GAME_CONFIGS["sevendaystodie"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def sevendaystodie_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["sevendaystodie"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["sevendaystodie"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["projectzomboid"]["group_help"])
async def projectzomboid(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["projectzomboid"]["embed_title"],
                                  description="These are the available commands",
                                  color=discord.Color.blue())

            for command in projectzomboid.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@projectzomboid.command(name='info', help=GAME_CONFIGS["projectzomboid"]["info"]["help"])
async def projectzomboid_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["projectzomboid"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["projectzomboid"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@projectzomboid.command(name='start', help=GAME_CONFIGS["projectzomboid"]["start"]["help"])
async def projectzomboid_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["projectzomboid"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["projectzomboid"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@projectzomboid.command(name='stop', help=GAME_CONFIGS["projectzomboid"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def projectzomboid_stop(ctx):
    async with ctx.typing():
        success = await stop_instance(GAME_CONFIGS["projectzomboid"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["projectzomboid"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@projectzomboid.command(name='restart',
                        help=GAME_CONFIGS["projectzomboid"]["restart"]["help"])
async def projectzomboid_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["projectzomboid"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["projectzomboid"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["beamng"]["group_help"])
async def beamng(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["beamng"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in beamng.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@beamng.command(name='info', help=GAME_CONFIGS["beamng"]["info"]["help"])
async def beamng_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["beamng"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["beamng"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@beamng.command(name='start', help=GAME_CONFIGS["beamng"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def beamng_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["beamng"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["beamng"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@beamng.command(name='stop', help=GAME_CONFIGS["beamng"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def beamng_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["beamng"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["beamng"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@beamng.command(name='restart', help=GAME_CONFIGS["beamng"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def beamng_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["beamng"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["beamng"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["sotf"]["group_help"])
async def sotf(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["sotf"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in sotf.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@sotf.command(name='info', help=GAME_CONFIGS["sotf"]["info"]["help"])
async def sotf_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["sotf"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["sotf"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@sotf.command(name='start', help=GAME_CONFIGS["sotf"]["start"]["help"])
async def sotf_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["sotf"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["sotf"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@sotf.command(name='stop', help=GAME_CONFIGS["sotf"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def sotf_stop(ctx):
    async with ctx.typing():
        success = await stop_instance(GAME_CONFIGS["sotf"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["sotf"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@sotf.command(name='restart', help=GAME_CONFIGS["sotf"]["restart"]["help"])
async def sotf_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["sotf"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["sotf"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["enshrouded"]["group_help"])
async def enshrouded(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["enshrouded"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in enshrouded.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@enshrouded.command(name='info', help=GAME_CONFIGS["enshrouded"]["info"]["help"])
async def enshrouded_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["enshrouded"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["enshrouded"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@enshrouded.command(name='start', help=GAME_CONFIGS["enshrouded"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def enshrouded_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["enshrouded"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["enshrouded"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@enshrouded.command(name='stop', help=GAME_CONFIGS["enshrouded"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def enshrouded_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["enshrouded"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["enshrouded"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@enshrouded.command(name='restart', help=GAME_CONFIGS["enshrouded"]["restart"]["help"])
async def enshrouded_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["enshrouded"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["enshrouded"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["palworld"]["group_help"])
async def palworld(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            await login()
            embed = discord.Embed(title=GAME_CONFIGS["palworld"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in palworld.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@palworld.command(name='info', help=GAME_CONFIGS["palworld"]["info"]["help"])
async def palworld_info(ctx):
    async with ctx.typing():
        running_status, status_code = await get_instance_status(GAME_CONFIGS["palworld"]["instance_id"])
        
        if running_status is not None:
            embed = build_info_embed(GAME_CONFIGS["palworld"], running_status)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Failed to get server info. HTTP status code: {status_code}')


@palworld.command(name='start', help=GAME_CONFIGS["palworld"]["start"]["help"], aliases=['s'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def palworld_start(ctx):
    async with ctx.typing():
        success, status_code = await start_instance(GAME_CONFIGS["palworld"]["instance_name"])

        if success:
            await asyncio.sleep(20)
            await ctx.send(GAME_CONFIGS["palworld"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server. HTTP status code: {status_code}')


@palworld.command(name='stop', help=GAME_CONFIGS["palworld"]["stop"]["help"])
async def palworld_stop(ctx):
    async with ctx.typing():
        success, status_code = await stop_instance(GAME_CONFIGS["palworld"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["palworld"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server. HTTP status code: {status_code}')


@palworld.command(name='restart', help=GAME_CONFIGS["palworld"]["restart"]["help"], aliases=['r'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def palworld_restart(ctx):
    async with ctx.typing():
        success, status_code = await restart_instance(GAME_CONFIGS["palworld"]["instance_name"])

        if success:
            await ctx.send(GAME_CONFIGS["palworld"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server. HTTP status code: {status_code}')


@commands.group(help=GAME_CONFIGS["atm10"]["group_help"])
async def atm10(ctx):
    if ctx.invoked_subcommand is None:
        async with ctx.typing():
            embed = discord.Embed(title=GAME_CONFIGS["atm10"]["embed_title"], description="These are the available commands",
                                  color=discord.Color.blue())

            for command in atm10.commands:
                embed.add_field(name=command.name, value=command.help, inline=False)

            await ctx.send(embed=embed)


@atm10.command(name='info', help=GAME_CONFIGS["atm10"]["info"]["help"])
async def atm10_info(ctx):
    async with ctx.typing():
        running_status = is_server_running("atm10")
        
        info_config = GAME_CONFIGS["atm10"]["info"]
        embed = discord.Embed(title=info_config["embed_title"], color=discord.Color.blue())
        
        embed.add_field(name='Server IP', value=info_config["ip"], inline=False)
        embed.add_field(name='Server Port', value=info_config["port"], inline=False)
        
        status_text = f'The ATM10 server is currently {"running" if running_status else "not running"}.'
        embed.add_field(name='Server Status', value=status_text, inline=False)
        
        await ctx.send(embed=embed)


@atm10.command(name='start', help=GAME_CONFIGS["atm10"]["start"]["help"])
async def atm10_start(ctx):
    async with ctx.typing():
        batch_path = GAME_CONFIGS["atm10"]["batch_script_path"]
        if not batch_path:
            await ctx.send('Batch script path not configured. Please set atm10.batch_script_path in config.py')
            return
        
        success, message = await start_batch_server("atm10", batch_path)

        if success:
            await ctx.send(GAME_CONFIGS["atm10"]["start"]["success_msg"])
        else:
            await ctx.send(f'Failed to start the server: {message}')


@atm10.command(name='stop', help=GAME_CONFIGS["atm10"]["stop"]["help"], aliases=['st'])
@commands.cooldown(COMMAND_COOLDOWN_RATE, COMMAND_COOLDOWN_PER, commands.BucketType.user)
async def atm10_stop(ctx):
    async with ctx.typing():
        success, message = await stop_batch_server("atm10")

        if success:
            await ctx.send(GAME_CONFIGS["atm10"]["stop"]["success_msg"])
        else:
            await ctx.send(f'Failed to stop the server: {message}')


@atm10.command(name='restart', help=GAME_CONFIGS["atm10"]["restart"]["help"])
async def atm10_restart(ctx):
    async with ctx.typing():
        success_stop, message_stop = await stop_batch_server("atm10")
        
        if success_stop:
            await asyncio.sleep(2)
        
        batch_path = GAME_CONFIGS["atm10"]["batch_script_path"]
        if not batch_path:
            await ctx.send('Batch script path not configured. Please set atm10.batch_script_path in config.py')
            return
        
        success_start, message_start = await start_batch_server("atm10", batch_path)

        if success_start:
            await ctx.send(GAME_CONFIGS["atm10"]["restart"]["success_msg"])
        else:
            await ctx.send(f'Failed to restart the server: {message_start}')


@atm10.command(name='forcekill', help="Forcefully kills all Java and cmd.exe processes related to the server.")
async def atm10_forcekill(ctx):
    from sensitive import AUTHORIZED_USER_ID
    
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send('❌ You do not have permission to use this command.')
        return
    
    async with ctx.typing():
        success, message = await force_kill_all_processes("atm10")
        
        if success:
            await ctx.send(f'✅ {message}')
        else:
            await ctx.send(f'❌ {message}')
