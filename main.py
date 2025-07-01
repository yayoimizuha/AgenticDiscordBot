from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import discord
import os

_ = load_dotenv(find_dotenv())

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Cog "{filename[:-3]}" をロードしました。')
            except Exception as e:
                print(f'Cog "{filename[:-3]}" のロードに失敗しました: {e}')


@bot.event
async def setup_hook():
    await load_cogs()


bot.run(os.environ['DISCORD_BOT_TOKEN'])
