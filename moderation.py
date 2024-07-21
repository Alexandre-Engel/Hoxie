import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands import MissingPermissions, has_permissions
from discord import Embed
import connectDB
from bson.objectid import ObjectId


class ConfirmView(View):
    def __init__(self, ctx, message):
        super().__init__()
        self.ctx = ctx
        self.message = message
        self.value = None

    @discord.ui.button(label="Oui", style=discord.ButtonStyle.green, emoji="✔")
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            return  # Check if the person interacting is the one who invoked the command
        self.value = True
        await self.message.delete() # Supprimer le message d'origine
        await interaction.response.send_message("Suppression effectuée.", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Non", style=discord.ButtonStyle.red, emoji="❌")
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.ctx.author:
            return  # Vérifier si la personne interagissant est celle qui a invoqué la commande
        self.value = False
        await self.message.delete() # Supprimer le message d'origine
        await interaction.response.send_message("Suppression annulée.", ephemeral=True)
        self.stop()

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    async def yes_callback(self, interaction):
        # Indiquer que le bot travaille sur la réponse
        await interaction.response.defer(ephemeral=True)
        # Suppression des messages
        messages = [message async for message in interaction.channel.history(limit=self.nb_message + 1)]
        await interaction.channel.delete_messages(messages)
        # Utiliser followup.send au lieu de response.send_message après defer
        embed = Embed(title="Suppression de messages", description=f"{len(messages)-1} messages supprimés.", color=0x00ff00)
        # Utiliser followup.send avec un Embed
        await interaction.followup.send(embed=embed, ephemeral=True)
    async def no_callback(self, interaction):
        messages = [message async for message in interaction.channel.history(limit=1)]
        await interaction.channel.delete_messages(messages)
        # Annulation de la suppression
        await interaction.response.send_message("Suppression annulée.", ephemeral=True)
        
    @commands.hybrid_command()
    @commands.has_role("Leader Gungan (Admin)")
    async def delete(self, ctx, nb_message: commands.Range[int, 1, 50]) -> None:
        self.nb_message = nb_message  # Stocker le nombre de messages à supprimer
        messages = [message async for message in ctx.channel.history(limit=nb_message + 1)]
        if messages:
            # Création des boutons
            yes_button = Button(label="Oui", style=discord.ButtonStyle.green)
            no_button = Button(label="Non", style=discord.ButtonStyle.red)
            
            # Associer les callbacks
            yes_button.callback = self.yes_callback
            no_button.callback = self.no_callback
            
            # Création de la vue contenant les boutons
            view = View()
            view.add_item(yes_button)
            view.add_item(no_button)

            # Message de confirmation
            embed = Embed(title="Suppression du message", description=f"Voulez vous vraiment supprimer tous les "
                                                                        f"messages depuis "
                                                                        f"\"{messages[-2].content}\" inclus ?") # -2 car le premier message est la commande
            await ctx.send(embed=embed, view=view)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title='Permissions',
                description=f"Tu n'as pas la permission d'effectuer cette commande",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title='Erreur',
                description=f"Une erreur s'est produite {error}",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            
            
        
    @commands.hybrid_command(name='ban')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if member.id == 463463057268539402:
            embed = Embed(
                title='Bannissement',
                description=f"{member} a été banni pour la raison : {reason}",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title='Bannissement',
                description=f"{member} a été banni pour la raison : {reason}",
                colour=discord.Colour.red()
            )

            await ctx.send(embed=embed)
            await ctx.guild.ban(member, reason=reason, delete_message_days=0)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title='Ahah bien tenté !',
                description=f"Mais tu n'as pas les permissions de ban",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title='Erreur',
                description=f"Le bannissement n'a pas pu avoir lieu, surement un coup de Fulcrum ! ",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


    @commands.hybrid_command(name='kick')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = Embed(
            title='Explusion',
            description=f"{member} a été expulsé pour la raison : {reason}",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
        await ctx.guild.kick(member, reason=reason)


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title='Ahah bien tenté ! ',
                description="Mais tu n'as pas les permissions de kick",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)  
        else:
            embed = Embed(
                title='Erreur',
                description="L'expulsion n'a pas pu avoir lieu, surement un coup de Fulcrum !",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed) 


    @commands.hybrid_command(name='mute')
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        embed = Embed(
            title='Muet',
            description=f"{member} a été rendu muet pour la raison : {reason}",
            colour=discord.Colour.red()
        )
        clown_de_rue = ctx.guild.get_role(512003660058722324)
        await member.add_roles(clown_de_rue)
        await ctx.send(embed=embed)
        await member.send(f"Tu as été rendu muet pour la raison : {reason}")
        


    @mute.error
    async def mute_error(self, error, ctx):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title='Ahah bien tenté ! ',
                description=f"Mais tu n'as pas les permissions de kick",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title='Erreur',
                description=f"L'expulsion n'a pas pu avoir lieu, surement un coup de Fulcrum ! ",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


    @commands.hybrid_command(name='userinfo')
    async def userinfo(self, ctx,  member: discord.Member = None):
        if member is None:
            member = ctx.author
        dbname = connectDB.get_database()
        member_db = dbname["members"]
        member_details = member_db.find_one({"member_id": member.id})
        embed = Embed(
            title=f"{member.name}",
            colour=discord.Colour.purple()
        )
        embed.set_footer(text=f"Information sur {member.name}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Identifiant", value=member.id, inline=False)
        embed.add_field(name="A rejoint discord", value=member.created_at.strftime("%d %B %Y"), inline=True)
        embed.add_field(name="A rejoint le serveur", value=member.joined_at.strftime("%d %B %Y"), inline=True)
        embed.add_field(name="Meilleure distinction", value=member.top_role.mention, inline=False)
        embed.set_author(name=member,
                        icon_url=member.avatar.url)

        embed.add_field(name="Crédits", value=member_details["credits"], inline=True)
        embed.add_field(name="Richesse", value=member_details["richesse"], inline=True)
        perso = dbname["characters"].find({"owner": ObjectId(member_details["_id"])})

        # Initialisation d'une liste pour stocker les noms des personnages
        personnages = []

        # Itération sur le curseur pour accéder à chaque document
        for document in perso:
            # Construction du nom complet du personnage
            nom_complet = f"{document['character_surname']} {document['character_name']}"
            # Ajout du nom complet à la liste des personnages
            personnages.append(nom_complet)

        print(personnages)
        if personnages:
            embed.add_field(name="Personnage(s) dans le rp", value="\n".join(personnages), inline=False)
        else:
            embed.add_field(name="Personnage(s) dans le rp", value="Pas de personnage rp", inline=False)
        try:
            embed.add_field(name="Anniversaire", value=member_details["birthday"], inline=False)
        except:
            embed.add_field(name="Anniversaire", value="non renseigné", inline=False)
        await ctx.send(embed=embed)


    @userinfo.error
    async def userinfo_error(self, ctx, error):
        general_channel = self.bot.get_channel(550597813809971220)
        await general_channel.send(error)
        embed = Embed(
            title='Erreur',
            description=f"Je crains ne pas pouvoir accéder à votre requête {error}",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)
        
        
    @commands.hybrid_command()
    @commands.has_role("Cénariste (MJ)")
    async def removehrp(self, ctx):
        embed = discord.Embed(title="Suppression du message",
                            description="Voulez-vous vraiment supprimer tous les "
                                        "commentaires de ce salon RP ?")
        message = await ctx.send(embed=embed)
        view = ConfirmView(ctx, message)
        await message.edit(view=view)
        await view.wait()

        if view.value is None:
            return  
        elif view.value:
            message = [message async for message in ctx.channel.history(limit=50)]
            for each_message in message:
                if each_message.content.startswith('(') and each_message.content.endswith(')'):
                    await each_message.delete()
            
# appelé au chargement de l'extension par le bot
async def setup(bot):
    await bot.add_cog(Moderation(bot))