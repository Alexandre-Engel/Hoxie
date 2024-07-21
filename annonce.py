import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions


class Annonce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name='annonce')
    @commands.has_any_role("Leader Gungan (Admin)", "Grand Cénariste (Chef-MJ)")
    async def announcement(self, ctx, titre , message):
        general_channel = self.bot.get_channel(502202133228158989) #config 503648197210537988
        embed = discord.Embed(
            title=titre,
            description=message,
            colour=discord.Colour.gold()
        )
        embed.set_footer(text="Vos Leaders Gungans")
        embed.set_image(url="https://cdn.discordapp.com/attachments/716757114147700747/859383798369091604/rdg.png")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/854720528425156639/b5e1663f0d67c8853714c41a9734f6e5.webp?size=256")
        embed.set_author(name="Hoxie",
                        icon_url="https://cdn.discordapp.com/avatars/854720528425156639/b5e1663f0d67c8853714c41a9734f6e5.webp?size=256")

        await general_channel.send("|| @everyone ||", embed=embed)
        
        
    @announcement.error
    async def announcement_error(ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(
                title='Permissions',
                description=f"Tu n'as pas la permission d'effectuer cette commande",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Erreur',
                description=f"Une erreur s'est produite",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


    

async def setup(bot):
    await bot.add_cog(Annonce(bot))
