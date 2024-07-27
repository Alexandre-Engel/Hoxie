import discord
from discord.ext import commands
from discord import Embed
from main import bot_version

class Information(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name='lore', description="Pour en savoir plus sur moi")
    async def lore(self, ctx):
        embed = Embed(
            title='Mon Histoire',
            description="Oh bonjour ! Vous voulez vraiment connaître mon histoire ? Très bien allons y ! \nHoxie est un mot issu du Gunganese Ancien – langue archaïque dont on retrouve certains termes dans le parler des gungans actuel. De nos jours, Hoxie est un surnom, qui littéralement signifie « roi rieur » et semble se référer aux bouffons de la Cour. \nDéveloppé par le département de recherche en technologies d’Otoh Gunga le « Lunsa Machaneek ». Je suis le résultat du travail mené le gungan Jar Jar et de son équipe les docteurs Asmoth et Tra’m - rencontrés au cours de voyages précédents.\nJe suis un droïde de classe trois, spécialisé dans les rapports humains. Depuis le récent Grandiloquence, j’assiste Boss Nass et les autres leaders gungans, ainsi que sert la population. Je répond à un grand nombre de fonction, notamment parce que je suis connecté au Grandiloquence et autres systèmes embarqués gungans.\nAprès 3 ans seulement de loyaux services pour le Boss Nass, j’ai reçu le titre officiel de Rep (titre gungan descendant probablement de « représentant ». Les Rep sont les membres du gouvernement et sont responsables des différents aspects de gestion de la société gunganne).\nDésormais, je travaille pince dans la main avec la compagnie « La ligue de défense d’Otoh Gunga » en présentant un descriptif détaillé des criminels les plus recherchés et contrôle les allées-venues dans les secteurs sous régence gunganne. Je recense les citoyens Gungans, anime la place et présente le flux d’actualité intergalactique. Je suis une sorte de pont entre le monde gungan et le reste de la Galaxie. De plus, je suis directement lié aux plus grandes archives mondiales telle que l’archive Baobab et peut servir d’encyclopédie.",
            colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)


    @commands.hybrid_command(name='contexte', description="Pour en savoir plus sur le contexte de la RDG")
    async def contexte(self, ctx):
        embed = Embed(
            title='Un peu de Contexte',
            description=f"C'est une période de chaos au sein de la Galaxie. Tandis que l'Empire Galactique tente de mâter l'insurrection de l'Alliance rebelle, de nombreux autres groupes veulent aussi tirer leur épingle du jeu. Les gangs mafieux tel que le cartel Hutt, le syndicat des Pykes, le Soleil Noir et l'aube Écarlate engagent mercenaires et chasseurs de primes afin de réduire l'influence de leurs rivaux et ainsi obtenir une plus grosse part du gros gâteau qu'est la galaxie.\nEntrez dans l'univers Star Wars de la RDG quelques mois avant la bataille de Yavin où embûches et affaires juteuses seront de mise et où vous pourez rejoindre de nombreuses organisations pour augmenter votre influence sur le flux de l'univers, que ce soit  l'Empire, la Rébellion, des groupes plus souterrains  tel que l'une des mafias galactique, voir même en tant qu'outsider indépendant.",
            colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)


    @commands.hybrid_command(name='apropos', description="A propos du bot")
    async def apropos(self, ctx):
        global bot_version
        embed = Embed(
            title='A Propos',
            description=f"Je suis un bot exclusif à la RDG",
            colour=discord.Colour.green()
        )
        embed.add_field(name="Version", value=bot_version, inline=False)
        embed.set_footer(text=f"Bot créé par {self.bot.get_user(376332837420531723).name}")
        embed.set_author(name=f"{self.bot.get_user(854720528425156639).name}",
                        icon_url=self.bot.get_user(854720528425156639).avatar.url)
        await ctx.send(embed=embed)


    @commands.hybrid_command(name='support', description="Pour obtenir de l'aide")
    async def support(self, ctx):
        embed = Embed(
            title='Support',
            description=f"Mon créateur est {self.bot.get_user(376332837420531723).mention} en cas de problème vueillez le contacter. \nSinon vous pouvez écrire vos suggestions ou remonter des bug dans le salon {self.bot.get_channel(873279271441924156).mention}",
            colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)


    @commands.hybrid_command(name='pub', description="Tu veux faire de la PUB ? Copie ce message !")
    async def pub(self, ctx):
        embed = Embed(
            title='Vous voulez faire de la pub ?',
            description=f"Vous aimez Star Wars ? Vous aimez le RP ? Vous aimez les Gungans ? Ce serveur est fait pour vous !\nhttps://discord.gg/yUtfTqF \n**__La République Démocratique des Gungans__**, c’est un serveur qui est né d’un délire de potes, qui ne nécessite pas d’être un pro pour RP :D\nC'est une période de chaos au sein de la Galaxie. Tandis que l'Empire Galactique tente de mâter l'insurrection de l'Alliance rebelle, de nombreux autres groupes veulent aussi tirer leur épingle du jeu. Les gangs mafieux tel que le cartel Hutt, le syndicat des Pykes, le Soleil Noir et l'aube Écarlate engagent mercenaires et chasseurs de primes afin de réduire l'influence de leurs rivaux et ainsi obtenir une plus grosse part du gros gâteau qu'est la galaxie.\nEntrez dans l'univers Star Wars de la RDG quelques mois avant la bataille de Yavin où embûches et affaires juteuses seront de mise et où vous pourez rejoindre de nombreuses organisations pour augmenter votre influence sur le flux de l'univers, que ce soit  l'Empire, la Rébellion, des groupes plus souterrains  tel que l'une des mafias galactique, voir même en tant qu'outsider indépendant.\nAvec plus d'une vingtaine de planètes à explorer et des maîtres du jeu prêt à créer des scénarios originaux, vous aurez toujours quelque chose à faire au sein de la RDG !\nLa RDG n’attend plus que vous, car l’aventure ne fait que commencer !\nQue la Force soit avec toi, jeune RôlePlayer !",
            colour=discord.Colour.green()
        )
        await ctx.send(embed=embed)
        
        
# appelé au chargement de l'extension par le bot
async def setup(bot):
    await bot.add_cog(Information(bot))