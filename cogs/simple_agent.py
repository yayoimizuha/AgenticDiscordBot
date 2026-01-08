import discord
from pydantic_ai import Agent
from discord import app_commands, Client

from discord.ext.commands import Cog, Bot

from bot_util import send_message


class SimpleAgentCog(Cog):
    def __init__(self, _bot: Bot):
        self.client = _bot
        self._simple_agent = Agent(model="openrouter:openrouter/polaris-alpha")

    @app_commands.command(name="log")
    async def log(self, interaction: discord.Interaction[Client], args: str):
        print(args)
        await send_message(interaction, args)

    @app_commands.command(name="begin_thread")
    async def begin_thread(self, interaction: discord.Interaction[Client]):
        channel = interaction.channel
        thread = await channel.create_thread(
            name=f"{interaction.user.display_name} - {interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        )
        await thread.add_user(interaction.user)
        await send_message(interaction, f"スレッドを開始しました。\n{thread.jump_url}")
