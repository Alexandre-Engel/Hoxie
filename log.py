import discord
from discord.ext import commands


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = discord.Embed(title="[❌] Message supprimé.",
                                description=f"{message.author.display_name} a supprimé un message dans le salon {message.channel.mention}.",
                                color=message.author.color)
            fields = [("Message:", message.content, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
                embed.set_thumbnail(url=message.author.avatar.url)
                embed.set_footer(text="Ce message a été supprimé")

            channel = self.bot.get_channel(550597813809971220)
            await channel.send(embed=embed)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        message = before
        if not message.author.bot:
            embed = discord.Embed(title="[✏️] Message modifié.",
                                description=f"{message.author.display_name} a modifié un message dans le salon {message.channel.mention}.",
                                color=message.author.color)
            embed.add_field(name="Avant", value=before.content, inline=False)
            embed.add_field(name="Après", value=after.content, inline=False)
            embed.set_thumbnail(url=message.author.avatar.url)
            embed.set_footer(text="Ce message a été modifié")
            channel = self.bot.get_channel(550597813809971220)
            await channel.send(embed=embed)


    

async def setup(bot):
    await bot.add_cog(Log(bot))
