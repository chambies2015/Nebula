import discord
from discord.ext import commands
from discord.ext.commands import check, CommandOnCooldown, MissingPermissions, CheckFailure
import tokens
from config import ALLOWED_CHANNELS
from amp_client import API, login, get_instance_statuses
import commands as game_commands
from exceptions import AMPAPIError, AuthenticationError
from logger import setup_logger
from sensitive import AUTHORIZED_USER_ID

logger = setup_logger("main")

bot_token = tokens.bot_token
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

allowed_channels = ALLOWED_CHANNELS


def is_allowed_channel(ctx):
    return str(ctx.channel.id) in allowed_channels


bot.add_check(check(is_allowed_channel))


@bot.command(name="getinstances", help="Get status of all AMP instances (authorized users only)")
async def get_instances(ctx):
    if ctx.author.id != AUTHORIZED_USER_ID:
        await ctx.send('❌ You do not have permission to use this command.')
        return
    
    async with ctx.typing():
        result, status_code = await get_instance_statuses()
        if result is not None:
            import json
            formatted_json = json.dumps(result, indent=2)
            if len(formatted_json) > 2000:
                await ctx.send(f'```json\n{formatted_json[:1900]}...\n```')
            else:
                await ctx.send(f'```json\n{formatted_json}\n```')
        else:
            await ctx.send(f'❌ Failed to get instance statuses. HTTP status code: {status_code}')


@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    
    success = await login()
    if not success:
        logger.warning("Initial login failed. Bot may not function correctly.")


bot.add_command(game_commands.ark)
bot.add_command(game_commands.terraria)
bot.add_command(game_commands.necesse)
bot.add_command(game_commands.icarus)
bot.add_command(game_commands.minecraft)
bot.add_command(game_commands.satisfactory)
bot.add_command(game_commands.sevendaystodie)
bot.add_command(game_commands.projectzomboid)
bot.add_command(game_commands.beamng)
bot.add_command(game_commands.sotf)
bot.add_command(game_commands.enshrouded)
bot.add_command(game_commands.palworld)
bot.add_command(game_commands.atm10)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(f'⏳ This command is on cooldown. Try again in {error.retry_after:.1f} seconds.')
    elif isinstance(error, MissingPermissions):
        await ctx.send('❌ You do not have permission to use this command.')
    elif isinstance(error, CheckFailure):
        await ctx.send('❌ This command cannot be used in this channel.')
    elif isinstance(error, AMPAPIError):
        await ctx.send(f'❌ API Error: {str(error)}')
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        logger.error(f"Unhandled error in command {ctx.command}: {error}", exc_info=True)
        await ctx.send('❌ An unexpected error occurred. Please try again later.')


@bot.command(help="displays helpful commands.", aliases=['h', 'commands'])
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Use `$<game> <command>` to control servers. Aliases: `s`=start, `st`=stop, `r`=restart",
        color=discord.Color.blue()
    )
    
    game_groups = {}
    other_commands = []
    
    for command in bot.commands:
        if isinstance(command, commands.Group):
            game_groups[command.name] = command
        else:
            other_commands.append(command)
    
    if game_groups:
        games_text = ", ".join(sorted(game_groups.keys()))
        embed.add_field(name="Available Games", value=games_text, inline=False)
        embed.add_field(
            name="Game Commands",
            value="Each game supports: `info`, `start` (alias: `s`), `stop` (alias: `st`), `restart` (alias: `r`)",
            inline=False
        )
    
    if other_commands:
        for cmd in other_commands:
            aliases_text = f" (aliases: {', '.join(cmd.aliases)})" if cmd.aliases else ""
            embed.add_field(name=f"${cmd.name}{aliases_text}", value=cmd.help or "No description", inline=False)
    
    embed.set_footer(text="Commands have a 3 uses per 60 seconds cooldown per user")
    await ctx.send(embed=embed)


bot.run(bot_token)
