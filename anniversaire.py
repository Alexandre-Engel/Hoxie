import discord
from discord.ext import commands, tasks
import connectDB
import datetime



class Anniversaire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.anniv.start() 
        
    @commands.hybrid_command(name='addanniv')
    async def addanniv(self, ctx, member: discord.Member, jour: int, mois: int):
        dbname = connectDB.get_database()
        member_db = dbname["members"]
        member_details = member_db.find_one({"member_id": member.id})
        if member_details:
            member_db.update_one({"member_id": member.id}, {"$set": {"birthday": str(jour) + '/' + str(mois)}})
            embed = discord.Embed(
                title="Anniversaire mis à jour",
                description=f"Nous souhaiterons un très joyeux anniversaire à {member.name} le jour venu ! ",
                colour=discord.Colour.gold()
            )
        else:
            embed = discord.Embed(
                title="Erreur",
                description=f"Le membre n'existe pas",
                colour=discord.Colour.gold()
            )
        await ctx.channel.send(member.mention, embed=embed)
        
    @addanniv.error
    async def addanniv_error(self, ctx, error):
        general_channel = self.bot.get_channel(550597813809971220)
        await general_channel.send(error)
        embed = discord.Embed(
            title='Erreur',
            description=f"Je crains ne pas pouvoir accéder à votre requête {error}",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
        
        
    @tasks.loop(minutes=4)
    async def anniv(self):
        date = datetime.datetime.now()
        if date.hour == 9 and date.minute in range(0, 5):
            today = str(date.day) + '/' + str(date.month)
            dbname = connectDB.get_database()
            member_db = dbname["members"]
            member_details = member_db.find_one({"birthday": today})
            if member_details:
                embed = discord.Embed(
                    title="JOYEUX ANNIVERSAIRE",
                    description=f"Nous souhaitons un très joyeux anniversaire à {member_details['pseudo']} ! ",
                    colour=discord.Colour.gold()
                )
                embed.set_footer(text="Vos Leader Gungan favoris")
                embed.set_image(
                    url="https://media.discordapp.net/attachments/573260699170766849/860538087704363059/unknown.png?width=1205&height=676")
                embed.set_author(name="Bot de la RDG",
                                icon_url="https://cdn.discordapp.com/avatars/854720528425156639/b5e1663f0d67c8853714c41a9734f6e5.webp?size=256")
                general_channel = self.bot.get_channel(502202133228158989) # 503148462565490718
                await general_channel.send(embed=embed)
                
    @anniv.before_loop
    async def before_anniv(self):
        await self.bot.wait_until_ready()


    

async def setup(bot):
    await bot.add_cog(Anniversaire(bot))
