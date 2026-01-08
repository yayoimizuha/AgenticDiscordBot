import discord
from discord import InteractionResponse, Client
from typing import Any


async def send_message(interaction: discord.Interaction[Client], content: Any):
    # noinspection PyTypeChecker
    resp: InteractionResponse[Client] = interaction.response
    await resp.send_message(content=content)
