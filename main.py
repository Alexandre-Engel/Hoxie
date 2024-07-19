import os
import discord
from discord.ext import commands

class Hoxie(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.tree.sync() # Pour gérer les commandes slash

    async def on_ready(self) -> None:
        print("Allumage du bot...")

bot = Hoxie()

if __name__ == "__main__":
    bot.run(os.getenv('DISCORDTOKEN'))
