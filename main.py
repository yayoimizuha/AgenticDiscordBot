import os
import discord
from discord import app_commands, InteractionResponse, Client
from discord.ext.commands import Cog, Bot
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True

bot = Bot(command_prefix="/", intents=intents)


@bot.tree.command(name="hello", description="挨拶をします")
async def hello_command(interaction: discord.Interaction):
    user_name = interaction.user.display_name
    # noinspection PyTypeChecker
    resp: InteractionResponse[Client] = interaction.response
    await resp.send_message(f"こんにちは{user_name}さん！")


class TestCog(Cog):
    def __init__(self, _bot: Bot):
        self.client = _bot

    @app_commands.command(name="ping")
    async def send_ping(self, interaction: discord.Interaction[Client]):
        latency = self.client.latency
        # noinspection PyTypeChecker
        resp: InteractionResponse[Client] = interaction.response
        await resp.send_message(f"{latency}ms")


@bot.event
async def setup_hook():
    await bot.add_cog(TestCog(bot))
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')
    print('Bot is ready!')


bot.run(os.environ['DISCORD_BOT_TOKEN'])
