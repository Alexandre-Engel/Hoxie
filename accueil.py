import discord
from discord.ext import commands


class Accueil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        general_channel = self.bot.get_channel(496686135368744962) #config
        embed = discord.Embed(
            title='Au revoir !',
            description=f"{member.display_name} a détruit un sous-marin de Boss Nass. Le résultat est sous "
                        f"vos yeux... ",
            colour=discord.Colour.red()
        )
        embed.set_image(url="https://media.discordapp.net/attachments/624184032418332714/735432757118894090/unknown.png")
        await general_channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        general_channel = self.bot.get_channel(496686135368744962) #config
        embed = discord.Embed(
            title='Bievenue !',
            description=f"{self.bot.get_emoji(599399019801739300)} {member.mention}, Je m'appelle Hoxie, et je suis le droïde de La RDG. Je t'invite à prendre"
                        f" connaissance des règles de ce serveur, par la suite n'hésite pas à te faire"
                        f" un personnage, sorti de ton imagination ou même prendre un personnage de la"
                        f" saga, et ainsi le poster dans {self.bot.get_channel(598744577368784916).mention} . Si tu as quelconque question les MJ"
                        f" ou le staff pourront te répondre, et nous te souhaitons tous une bonne"
                        f" expérience sur La RDG ! {self.bot.get_emoji(624185090221670411)} ",
            colour=discord.Colour.blue()
        ) #config
        embed.set_image(url="https://media.giphy.com/media/3owzWgfjON3M6BOEEM/giphy.gif")
        await general_channel.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Accueil(bot))
