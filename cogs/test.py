import discord
from discord.ext import commands
from discord import app_commands


class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.qualified_name} Cog is ready.')

    @app_commands.command(name="hello", description="ボットが挨拶します。")
    async def hello_command(self, interaction: discord.Interaction):
        await interaction.response().send_message(f'こんにちは！ {interaction.user.display_name}さん！')

    @app_commands.command(name="ping", description="ボットのレイテンシを表示します。")
    async def ping_command(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response().send_message(f'Pong! {latency_ms}ms')


async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCommands(bot))
