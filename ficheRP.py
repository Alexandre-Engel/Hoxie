import discord
from discord.ext import commands
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions, has_role
# import pymysql.cursors
from discord.utils import get
from logger import writeLogCommand
import re
import connectDB




class CommandeRP(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name='fiche', description="Permet d'afficher la fiche du personnage")
    @writeLogCommand
    async def viewFiche(self, ctx, *, name=None):
        args = name.split() if name else []
        if len(args) == 0 or len(args) > 2:
            embed = discord.Embed(
                title='Erreur',
                description="Le personnage demandé n'existe pas.",
                colour=discord.Colour.red()
            )
            embed.add_field(name='Conseil', value="Tape la commande de cette manière : !fiche <prénom> <nom>", inline=True)
        else:
            dbname = connectDB.get_database()
            character = dbname["characters"]
            if len(args) == 2:
                surname_char = args[0]
                name_char = args[1]
                character_details = character.find_one({"character_surname": re.compile(surname_char, re.IGNORECASE),
                                                        "character_name": re.compile(name_char, re.IGNORECASE)})
            elif len(args) == 1:
                unknown_char = args[0]

                if character.find_one({"character_surname": re.compile(unknown_char, re.IGNORECASE)}):
                    character_details = character.find_one({"character_surname": re.compile(unknown_char, re.IGNORECASE)})
                elif character.find_one({"character_name": re.compile(unknown_char, re.IGNORECASE)}):
                    character_details = character.find_one({"character_name": re.compile(unknown_char, re.IGNORECASE)})
                else:
                    character_details = None

            if character_details:
                embed = discord.Embed(
                    title='Fiche',
                    description=character_details["character_surname"] + ' ' + character_details["character_name"],
                    colour=discord.Colour.blue()
                )

                embed.set_footer(text='Command by ' + ctx.message.author.name)
                embed.set_image(url=character_details["picture"])

                member = dbname["members"]
                member_details = member.find_one({"_id": character_details["owner"]})
                # user = get(bot.get_all_members(), id=member_details["member_id"])
                if member_details:
                    user = get(self.bot.get_all_members(), id=member_details["member_id"])
                    embed.set_author(name=user, icon_url=user.avatar.url)
                else:
                    embed.set_author(name="?",
                                     icon_url='https://www.cdiscount.com/pdt2/1/9/3/1/700x700/shl6911524070193/rw/shlk-peluche-jouet-prank-props-coussin-poupee-e.jpg')
                embed.add_field(name='Nom', value=character_details["character_name"], inline=True)
                embed.add_field(name='Prénom', value=character_details["character_surname"], inline=True)
                embed.add_field(name='Espèce', value=character_details["species"], inline=True)
                embed.add_field(name='Age', value=character_details["age"], inline=True)
                embed.add_field(name='Faction', value=character_details["faction"], inline=True)
                embed.add_field(name='Vaisseaux', value=character_details["vessel"], inline=True)
            else:
                embed = discord.Embed(
                    title='Erreur',
                    description="Le personnage demandé n'existe pas.",
                    colour=discord.Colour.red()
                )
                embed.add_field(name='Conseil', value="Tape la commande de cette manière : !fiche <prénom> <nom>",
                                inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name='addfiche', description="Ajoute une fiche de personnage")
    @writeLogCommand
    @commands.has_role("Cénariste (MJ)")
    async def addFiche(self, ctx, character_surname, character_name, species: discord.Role, age, faction, vessel, picture, owner: discord.Member):
        ownerID = owner.id#(owner.replace("<", "").replace("@", "").replace(">", "").replace("!", ""))
        dbname = connectDB.get_database()
        character = dbname["characters"]
        member = dbname["members"]

        member_details = member.find_one({"member_id": int(ownerID)})
        if not member_details:
            uCreate = {
                "member_id": int(ownerID),
                "pseudo": ctx.message.author.name,
                "credits": 200,
                "birthday": None
            }
            member.insert_one(uCreate)
        member_details = member.find_one({"member_id": int(ownerID)})
        character_details = character.find_one({"character_surname": re.compile(character_surname, re.IGNORECASE),
                                                "character_name": re.compile(character_name, re.IGNORECASE)})
        if not character_details:
            characterToAdd = {
                "character_surname": character_surname,
                "character_name": character_name,
                "species": species.name,
                "age": age,
                "faction": faction,
                "vessel": vessel,
                "picture": picture,
                "owner": member_details["_id"]
            }
            await owner.add_roles(species)
            character.insert_one(characterToAdd)
            await self.viewFiche(ctx, name=character_surname + ' ' + character_name)
        else:
            embed = discord.Embed(
                title='Erreur',
                description='Le personnage existe déjà.',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

    @addFiche.error
    @writeLogCommand
    async def addFiche_error(self, ctx, error):
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
                description=f"Une erreur s'est produite : {error}",
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name='removefiche', description="Supprime une fiche de personnage")
    @commands.has_role("Cénariste (MJ)")
    @writeLogCommand
    async def removeFiche(self, ctx, character_surname, character_name):
        dbname = connectDB.get_database()
        character = dbname["characters"]
        character.delete_one({"character_surname": re.compile(character_surname, re.IGNORECASE),
                              "character_name": re.compile(character_name, re.IGNORECASE)})
        embed = discord.Embed(
            title='Succès !',
            description=f"La fiche du personnage {character_surname} {character_name} a bien été supprimée !",
            colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)

    @removeFiche.error
    @writeLogCommand
    async def removeFiche_error(ctx, error):
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

    @commands.hybrid_command(name='addprime', description="Ajoute une prime sur une tête")
    @commands.has_role("Cénariste (MJ)")
    @writeLogCommand
    async def addPrime(ctx, identity, sex, wanted_by, certified, characteristic, grade, wanted, appearance, reward):
        dbname = connectDB.get_database()
        bounty = dbname["bountys"]
        print(bounty)
        bounty_details = bounty.find_one({"character_surname": re.compile(identity, re.IGNORECASE)})
        if not bounty_details:
            bountyToAdd = {
                "identity": identity,
                "sex": sex,
                "wanted_by": wanted_by,
                "certified": certified,
                "characteristic": characteristic,
                "grade": grade,
                "wanted": wanted,
                "appearance": appearance,
                "reward": reward
            }
            bounty.insert_one(bountyToAdd)
            embed = discord.Embed(
                title='Ajout effectué',
                description='La tête a été mise à prix !',
                colour=discord.Colour.orange()
            )
        else:
            embed = discord.Embed(
                title='Erreur',
                description='La tête de est déjà mise à prix !',
                colour=discord.Colour.red()
            )
        await ctx.send(embed=embed)

    @addPrime.error
    @writeLogCommand
    async def addPrime_error(ctx, error):
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

    @commands.hybrid_command(name='removeprime', description="Supprime une prime sur une tête")
    @commands.has_role("Cénariste (MJ)")
    @writeLogCommand
    async def removePrime(ctx, identity):
        dbname = connectDB.get_database()
        prime = dbname["prime"]
        prime.delete_one({"identity": re.compile(identity, re.IGNORECASE)})

    @removePrime.error
    @writeLogCommand
    async def removePrime_error(ctx, error):
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

    @commands.hybrid_command(name='prime')
    @writeLogCommand
    async def viewPrime(ctx, identity):
        dbname = connectDB.get_database()
        bounty = dbname["bountys"]
        bounty_details = bounty.find_one({"identity": re.compile(identity, re.IGNORECASE)})
        if bounty_details:
            embed = discord.Embed(
                title='Fiche',
                description=bounty_details["identity"],
                colour=discord.Colour.blue()
            )

            embed.set_footer(text='Command by ' + ctx.message.author.name)
            embed.set_image(url=bounty_details["appearance"])
            embed.add_field(name='Identité', value=bounty_details["identity"], inline=True)
            embed.add_field(name='Sexe', value=bounty_details["sex"], inline=True)
            embed.add_field(name='Recherché par', value=bounty_details["wanted_by"], inline=True)
            embed.add_field(name='Agréé', value=bounty_details["certified"], inline=True)
            embed.add_field(name='Cible', value=bounty_details["grade"], inline=True)
            embed.add_field(name='Recherché', value=bounty_details["wanted"], inline=True)
            embed.add_field(name='Récompense', value=bounty_details["reward"], inline=True)
        else:
            embed = discord.Embed(
                title='Erreur',
                description="Le personnage demandé n'existe pas.",
                colour=discord.Colour.red()
            )
            embed.add_field(name='Conseil', value="Tape la commande de cette manière : !fiche <prénom> <nom>",
                            inline=True)
        await ctx.send(embed=embed)

    @viewPrime.error
    @writeLogCommand
    async def viewPrime_error(self, ctx, error):
        general_channel = self.bot.get_channel(550597813809971220)
        await general_channel.send(error)
        embed = discord.Embed(
            title='Erreur',
            description=f"Je suis désolé, je n'arrive pas à accéder à votre requète",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=embed)


'''
    @commands.hybrid_command()
    @writeLogCommand
    async def baz(self, ctx):
        await ctx.send("Whatever")

    @commands.hybrid_command(name='Ahsoka')
    @writeLogCommand
    async def ahsoka(self, ctx):
        db = connect_database()
        cur = db.cursor()
        cur.execute('SELECT * FROM rdgcharacter where character_surname = \'Ahsoka\'')
        rows = cur.fetchall()
        await ctx.send(str(rows))


    def create_embed_fiche(self, data, author):
        embed = discord.Embed(
                title='Fiche',
                description=data["character_surname"] + ' ' + data["character_name"],
                colour=discord.Colour.blue()
            )

        embed.set_footer(text='Command by ' + author)
        embed.set_image(url=data["picture"])
        user = self.bot.get_user(int(data["owner"]))
        embed.set_author(name=user, icon_url=user.avatar.url)
        embed.add_field(name='Nom', value=data["character_name"], inline=True)
        embed.add_field(name='Prénom', value=data["character_surname"], inline=True)
        embed.add_field(name='Espèce', value=data["species"], inline=True)
        embed.add_field(name='Age', value=data["age"], inline=True)
        embed.add_field(name='Faction', value=data["faction"], inline=True)
        embed.add_field(name='Vaisseaux', value=data["vessel"], inline=True)
        return embed


    @commands.hybrid_command(name='perso')
    @writeLogCommand
    async def perso(self, ctx, *name):
        nom_perso = " ".join(name)

        db = connect_database()
        cur = db.cursor()
        cur.execute(f'SELECT * FROM rdgcharacter WHERE LOWER(character_surname) = LOWER(\'{nom_perso}\') OR LOWER(character_name) = LOWER(\'{nom_perso}\') OR CONCAT(LOWER(character_surname),\' \',LOWER(character_name)) = LOWER(\'{nom_perso}\') ')
        rows = cur.fetchall()

        if (len(rows) >= 1):
            await ctx.send(embed = self.create_embed_fiche(rows[0], ctx.message.author.name))
        else:
            await ctx.send(f"Le personnage \"{nom_perso}\" n'est pas dans la base de donnée")
'''


# appelé au chargement de l'extension par le bot
async def setup(bot):
    await bot.add_cog(CommandeRP(bot))
