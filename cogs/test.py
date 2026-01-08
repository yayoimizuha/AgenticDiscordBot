import discord
from discord import app_commands, Client
from discord.ext.commands import Cog, Bot
from bot_util import send_message


class TestCog(Cog):
    def __init__(self, _bot: Bot):
        self.client = _bot

    @app_commands.command(name="ping")
    async def send_ping(self, interaction: discord.Interaction[Client]):
        latency = self.client.latency
        await send_message(interaction, f"{latency}ms")

    @app_commands.command(name="hello")
    async def say_hello(self, interaction: discord.Interaction[Client]):
        user_name = interaction.user.display_name
        await send_message(interaction, f"こんにちは{user_name}さん！")
