import os
import discord
from discord import Client
from discord.ext.commands import Bot

from cogs.simple_agent import SimpleAgentCog
from cogs.test import TestCog

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix="/", intents=intents)


@bot.command("test_text")
async def test_text(interaction: discord.Interaction[Client], *args):
    print(args)


@bot.event
async def setup_hook():
    await bot.add_cog(TestCog(bot))
    await bot.add_cog(SimpleAgentCog(bot))
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready!')


if __name__ == '__main__':
    bot.run(os.environ['DISCORD_BOT_TOKEN'])
