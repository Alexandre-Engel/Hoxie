import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.ext.commands import MissingPermissions
from discord import Embed

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
            embed = discord.Embed(
                title='Permissions',
                description=f"Tu n'as pas la permission d'effectuer cette commande",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Erreur',
                description=f"Une erreur s'est produite {error}",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)
            
# appelé au chargement de l'extension par le bot
async def setup(bot):
    await bot.add_cog(Moderation(bot))