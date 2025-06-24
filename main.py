import asyncio

from dotenv import load_dotenv, find_dotenv
from loguru import logger
from discord.ext import commands
import discord
import os

_ = load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


class AgentCog(commands.Cog):
    def __init__(self, _bot: commands.Bot):
        self.bot = _bot

    @commands.command(name="hello", description="こんにちは！")
    async def send_hello(self, ctx: commands.Context):
        await ctx.send(f"こんにちは！、{ctx.author.display_name}")


@bot.event
async def on_ready():
    logger.info(f"{bot.user} log inned!")
    await bot.add_cog(AgentCog(bot))
    await asyncio.gather(*[bot.tree.sync(guild=guild) for guild in bot.guilds])


bot.run(os.environ["DISCORD_BOT_TOKEN"])