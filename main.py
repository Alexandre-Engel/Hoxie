import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

bot_version = "2.0"

class Hoxie(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await bot.load_extension("ficheRP")
        await bot.load_extension("log")
        await bot.load_extension("accueil")
        await bot.load_extension("annonce")
        await bot.load_extension("anniversaire")
        await bot.load_extension("moderation")
        await bot.load_extension("information")
        await self.tree.sync() # Pour gérer les commandes slash

    async def on_ready(self) -> None:
        print("Allumage du bot...")

bot = Hoxie()
    
if __name__ == "__main__":
    bot.run(os.getenv('DISCORDTOKEN'))
