import discord
from discord.ext import commands
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
import random
from random import randint
from discord import FFmpegPCMAudio
from webbrowser import get
from discord.utils import get

client = commands.Bot(command_prefix = "/", description = "Bot de Titouan")
slash = SlashCommand(client, sync_commands=True)
client.remove_command('help')
date_format = "%a, %b %d, %Y @ %I:%M %p" 

@client.event
async def on_ready():
    print("Ready ! (to use the bot, use /help Gamemaster")

emoji = [':thinking_face:', ':eyes:', ':smile:', ':sparkles:']
emote = random.choice(emoji)

@client.command()
async def help(ctx, objects):

    if objects == "Gamemaster":
        embed = discord.Embed(
            title=f"OK, voici ce que tu peux réaliser avec le Gamemaster {emote} :",
            description=":broom:   **/clear** : retire tout les messages \n \n" +
                        ":x: **/delete** (nombre de ligne) : retire le nombre de message en fonction du nombre de ligne spécifié \n\n" +
                        ":pencil2:   **/who** : le bot te donneras quelques informations sur toi \n\n" +
                        ":question:   **/help** : le bot te montrera comment l'utiliser \n\n" +
                        ":game_die:   **/change_name** (nouveau nom) : te donne un nouveau nom \n\n" +
                        ":video_game:   **/start game** : utilise-le pour lancer un jeu de rôle avec le Gamemaster, \ntapez **game** (avec le /help) pour plus d'info\n\n" +
                        ":relieved:   **/theme** : declenche une musique dans le salon vocal\n\n" +
                        ":game_die:   **/random** (range number) : te donne un nombre un nombre aléatoire en fonction du nombre choisis \n\n" +
                        ":monkey:   **/quiz** : Petit quizz qui vous indiquera quel personnage vous êtes \n\n" +
                        ":shushing_face:   **/choix** : Un énorme dilème vous attend en entrant cette commande \n\n" +
                        ":skull:   **/dead** : déconnecte le bot \n\n",
            color=0xFFFFFF
        )
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, tts=True)

    if objects == "game":
        embed = discord.Embed(
            title=f"OK, voici comment jouer avec le Gamemaster {emote} :",
            description="répond aux questions qui te seront posé pour découvrir ce qui t'attends, \n \n" +
                        f"si tu t'es trompé tu peut utiliser **return**, et **reset** pour recommencer. {emote}",
            color=0xFF0000 
        )
        embed.set_author(name=ctx.author.name,
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, tts=True)

    if objects != "Gamemaster" and objects != "game":
        await ctx.send(f':raised_hand::angry: ERREUR !! l\'objet (**{objects}**) n\'a pas été trouvé ')


@client.command()
async def who(ctx):
    embed = discord.Embed(
        title=f"Tu t'appelle {ctx.author.name}",
        description=f"Date ou tu as rejoint le serveur : **{ctx.author.joined_at.strftime(date_format)}** \n Date ou tu as créer ton compte : **{ctx.author.created_at.strftime(date_format)}**\n\nAmuse-toi bien !! {emote}",
        color=0x0000ff
    )
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def choix(ctx):
    buttons = [
        create_button(
            style=ButtonStyle.blue,
            label="La balayé puis enchainer sur un crochet du droit.",
            custom_id="agressif"
        ),
        create_button(
            style=ButtonStyle.danger,
            label="Lui demandé ce qu'elle veut",
            custom_id="passif"
        )
    ]
    action_row = create_actionrow(*buttons)
    fait_choix = await ctx.send("Une grand mère approche, que fais-tu?", components=[action_row], tts=True)

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == fait_choix.id

    button_ctx = await wait_for_component(client, components=action_row, check=check)

    if button_ctx.custom_id == "agressif":
        # response = discord.Embed( title=f'Félicitation {ctx.author.name}', description='la grand mère a bien etait neutralisé, tu es sain et sauf.',color=0xFFFFFF)
        # await ctx.send(embed=response, tts=True)
        await button_ctx.send("Félicitation la grand mère a bien etait neutralisé, tu es sain et sauf.", tts=True)
    else:
        await button_ctx.send(content="Vous êtes mort... la grand mere avait etait engangé pour vous fumer la gueule, Mefiez vous de tout !", tts=True)

@client.command()
async def quiz(ctx):
    select = create_select(
        options=[
            create_select_option("ADC", value="1", emoji="🏋️‍♂️"),
            create_select_option("Support", value="2", emoji="🧙"),
            create_select_option("Midlane", value="3", emoji="🤺"),
            create_select_option("Toplane", value="4", emoji="🐘"),
            create_select_option("Jungle", value="5", emoji="🐺")
        ],
        placeholder="Choisis un rôle...",
        min_values=1,
        max_values=1
    )
    fait_choix = await ctx.send("Quel rôle souhaitez-vous choisir?", components=[create_actionrow(select)], tts=True)

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == fait_choix.id

    choice_ctx = await wait_for_component(client, components=select, check=check)

    if choice_ctx.values[0] == "1":
        await choice_ctx.send("Tu seras Ezrael !", tts=True)
    
    if choice_ctx.values[0] == "2":
        await choice_ctx.send("Tu seras Lux !", tts=True)
    
    if choice_ctx.values[0] == "3":
        await choice_ctx.send("Tu seras Talon !", tts=True)
    
    if choice_ctx.values[0] == "4":
        await choice_ctx.send("Tu seras Sett !", tts=True)
    
    if choice_ctx.values[0] == "5":
        await choice_ctx.send("Tu seras Udyr !", tts=True)


    


@client.command()
async def clear(ctx):
    await ctx.channel.purge()


@ client.command()
async def random(ctx, nombre_choisis: int):
    résultat = randint(1, nombre_choisis)
    embed = discord.Embed(
        title=f"À partir du nombre ({nombre_choisis}) ",
        description=f"tu obtiens ({résultat}) ",
        color=0xFFFFFF  # Hex-coded color
    )
    embed.set_author(name=ctx.message.author.name,
                     icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed, tts=True)



@client.command()
async def dead(ctx):
    id = str(ctx.author.id)
    if id == '635740186151747584':
        await ctx.send('Le bot s\'est déconnecte', tts=True)
        await ctx.client.logout()
    else:
        await ctx.send("how dare you !", tts=True)
        await ctx.send("https://tenor.com/view/the-rock-rock-gif-21708339", tts=True)

   
@client.command()
async def change_name(ctx, *, arg):
    await ctx.author.edit(nick=arg)
    await ctx.send(f'Nickname was changed for {ctx.author.mention} ', tts=True)


@client.command()
async def create_r(ctx, r):
    colour = discord.Colour(0xffffff)
    # permissions=discord.Permissions(permissions=<>)
    guild = ctx.guild

    for role in guild.roles:
        if role.name == r:
            return

    await guild.create_role(name=r)


@client.command()
async def add_r(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="test")
    await user.add_roles(role)


@client.command()
async def create_t(ctx, *, nom_de_salon):

    for channel in client.get_all_channels():
        if nom_de_salon == channel.name:
            return

    guild = ctx.guild
    role = nom_de_salon
    autorize_role = await guild.create_role(name=role)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        autorize_role: discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel(nom_de_salon, overwrites=overwrites)
    await ctx.author.add_roles(autorize_role)


@client.command()
async def create_v(ctx, *, nom_de_salon):
    if ctx.channel.name != nom_de_salon:
        guild = ctx.guild
        role = nom_de_salon
        autorize_role = await guild.create_role(name=role)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            autorize_role: discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_voice_channel(nom_de_salon, overwrites=overwrites)
        await ctx.author.add_roles(autorize_role)

@client.command()
async def ping(ctx, role: discord.Role, *, message):

    await ctx.send(f"""
    {role.mention}
    cette personne {ctx.author.mention} a dit : {message}
    """, tts=True)


@client.command()
async def admin(ctx, *, message):
    admin = get(ctx.guild.roles, name='admin')
    await ctx.send(f"""
    {admin.mention}
    cette personne {ctx.author.mention} a dit : {message}
    """, tts=True)


@client.command()
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

    for each_message in messages:
        await each_message.delete()

@client.command(pass_context=True)
async def theme(ctx):
    if (ctx.author.voice):
        channel= ctx.message.author.voice.channel 
        voice = await channel.connect()
        source = FFmpegPCMAudio('theme.mp3')
        player = voice.play(source)
        
    else:
        await ctx.send(f'{ctx.author.mention} \n vous devez être dans un salon vocal pour utiliser cette commande', tts=True)      

class Tree:
    def __init__(self, question, key, end):
        self.question = question
        self.key = key
        self.children = []
        self.parent = None
        self.end = end

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def testChild(self, key):
        for child in self.children:
            if child.key in key:
                return child
        if key == "return":
            return self.parent
        elif key == "reset":
            return Node1
        return self

    def question_bot(self):
        return self.question




Node1 = Tree("Press game", "key", 0)

Node2 = Tree("Vous sentez vous plus du coté du bien ou du mal ? bien/mal", "game", 0)

Node3_1 = Tree("Préférez vous attaquer de loin ou voulez vous courir dans la bataille ? mélée/range", "bien", 0)

Node4_1 = Tree("Allez vous lancer des sorts ou utiliser des armes pour combattre ?", "mélée", 0)

Node5_1 = Tree("Vous aimez donc la magie... quel élément vous sied le plus ? feu/eau/terre/air/lumière", "magie", 0)

Node6_1 = Tree("elementaire de feu", "feu", 1)

Node6_2 = Tree("elementaire d'eau", "eau", 1)

Node6_3 = Tree("elementaire de terre", "terre", 1)

Node6_4 = Tree("elementaire d'air", "air", 1)

Node6_5 = Tree("elementaire de lumière", "lumière", 1)

Node5_2 = Tree("Vous êtes donc dans le coeur de la bataille ! Préférez vous vous battre corps et âme pour la beauté du combat ou apporter la foi de la lumière aux hérétique ? combat/foi", "arme", 0)

Node6_6 = Tree("guerrier", "combat", 1)

Node6_7 = Tree("paladin", "foi", 1)

Node4_2 = Tree("Vous préférez donc vous tenir loin du danger, je vois... Allez vous plus user de pouvoir magique pour tenir vos adversaires a distance ou les abattre de loin à l'aide d'arme ? magie/arme", "range", 0)

Node5_3 = Tree("Vous êtes donc un utilisateur de magie a distance ! Juste une petite question, vous aimez les animaux plus que les humains? oui/non", "magie", 0)

Node6_8 = Tree("Vous voilà donc mage, mais quel type de magie préférez vous ? feu/eau/terre/air", "non", 0)
            
Node7_1 = Tree("mage de feu", "feu", 1)

Node7_2 = Tree("mage d'eau", "eau", 1)

Node7_3 = Tree("mage de terre", "terre", 1)

Node7_4 = Tree("mage d'air", "air", 1)

Node6_9 = Tree("druide", "oui", 1)

Node5_4 = Tree("Vous avez donc une préférence pour les armes bien réelle contrairement aux mages et leurs petits sors de pacotille ! Allez vous fêter votre victoire en musique ? oui/non", "arme", 0)

Node6_10 = Tree("archer", "non", 1)

Node6_11 = Tree("barde", "oui", 1)

Node3_2 = Tree("Vous êtes donc un soldat du mal, vous aimez la mort, et de toute façon la vie c'est trop nul... ( ah lala, les jeunes émo-gothique, tous les mêmes...). Bref je divague, allez vous observer vos ennemis perir de loin ou plutôt les achever de vos main ? mélée/range", "mal", 0)

Node4_3 = Tree("Vous voulez donc avoir vos main couverte du sang impur de vos ennemis, je vois... Allez vous vous lancer dans la bataille avec dans vos mains une arme sanglante ou bien alez vous vous renforcer a l'aide de magie interdite ? magie/arme", "mélée", 0)

Node5_5 = Tree("Vous vous transformez donc en élémentaire, un être fait de magie mais de quelle magie impure êtes vous fait au pus profond de votre âme déchainée ? poison/sang/tenèbre", "magie", 0)

Node6_12 = Tree("elementaire de poison", "poison", 1)

Node6_13 = Tree("elementaire de sang", "sang", 1)

Node6_14 = Tree("elementaire de tenèbre", "tenèbre", 1)

Node5_6 = Tree("Vous courez donc dans la bataille, la bave aux lèvres près a taper sur tout ce qui bouge autour de vous ! Mais après réflexion, allez vous taper puis courir ou bien courir puis taper ? taper/courir", "arme", 0)

Node6_15 = Tree("troll", "taper", 1)

Node6_16 = Tree("orc", "courir", 1)

Node4_4 = Tree("Vous vous tenez donc au bord du combat près a répandre mort de destruction sur le monde entier mais pour cela allez vous utiliser une magie toute droit venu des enfers ou allez vous prendre votre plaisir dans le fait de regarder des pouvoirs impurs souiller le monde ? enfers, impurs", "range", 0)

Node6_17 = Tree("Vous aimez donc les pouvoirs impurs... Non m'approchez pas répondez juste à mes questions de loin, vous préférez quoi comme éléments ? poison/sang/tenèbre", "impurs", 0)

Node7_5 = Tree("mage de poison", "poison", 1)

Node7_6 = Tree("mage de sang", "sang", 1)

Node7_7 = Tree("mage de tenèbre", "tenèbre", 1)

Node6_18 = Tree("necromentien", "enfers", 1)


Node1.add_child(Node2)

Node2.add_child(Node3_1)

Node3_1.add_child(Node4_1)

Node4_1.add_child(Node5_1)

Node5_1.add_child(Node6_1)

Node5_1.add_child(Node6_2)

Node5_1.add_child(Node6_3)

Node5_1.add_child(Node6_4)

Node5_1.add_child(Node6_5)

Node4_1.add_child(Node5_2)

Node5_2.add_child(Node6_6)

Node5_2.add_child(Node6_7)

Node3_1.add_child(Node4_2)

Node4_2.add_child(Node5_3)

Node5_3.add_child(Node6_8)

Node6_8.add_child(Node7_1)

Node6_8.add_child(Node7_2)

Node6_8.add_child(Node7_3)

Node6_8.add_child(Node7_4)

Node5_3.add_child(Node6_9)

Node4_2.add_child(Node5_4)

Node5_4.add_child(Node6_10)

Node5_4.add_child(Node6_11)

Node2.add_child(Node3_2)

Node3_2.add_child(Node4_3)

Node4_3.add_child(Node5_5)

Node5_5.add_child(Node6_12)

Node5_5.add_child(Node6_13)

Node5_5.add_child(Node6_14)

Node4_3.add_child(Node5_6)

Node5_6.add_child(Node6_15)

Node5_6.add_child(Node6_16)

Node3_2.add_child(Node4_4)

Node4_4.add_child(Node6_17)

Node6_17.add_child(Node7_5)

Node6_17.add_child(Node7_6)

Node6_17.add_child(Node7_7)

Node4_4.add_child(Node6_18)


class story:
    def __init__(self, question, key, end):
        self.question = question
        self.key = key
        self.children = []
        self.parent = None
        self.end = end

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def testChild(self, key):
        for child in self.children:
            if child.key in key:
                return child
        if key == "return":
            return self.parent
        elif key == "reset":
            return Node_story_1
        return self

    def question_bot(self):
        return self.question


Node_story_1 = story("start", "key", 0)

Node_story_2 = story(
    "Vous devez choisir entre Élementaire / Mage / Guerrier / Paladin / Druide / Archer / Barde / Troll / Orc / Nécromancien / Chasseur", "start", 0)

Node_story_3_1 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Élementaire", 0)

Node_story_3_2 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Mage", 0)

Node_story_3_3 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Guerrier", 0)

Node_story_3_4 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Paladin", 0)

Node_story_3_5 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Druide", 0)

Node_story_3_6 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Archer", 0)

Node_story_3_7 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Barde", 0)

Node_story_3_8 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Troll", 0)

Node_story_3_9 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Orc", 0)

Node_story_3_10 = story("vous voulez mourir ou vivre?(mourir/vivre)",
                 "Nécromancien", 0)

Node_story_3_11 = story("vous voulez mourir ou vivre?(mourir/vivre)", "Chasseur", 0)


Node_story_4_1_2 = story("vous êtes mort ", "mourir", 1)

Node_story_4_2_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_3_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_4_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_5_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_6_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_7_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_8_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_9_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_10_2 = story("vous êtes mort", "mourir", 1)

Node_story_4_11_2 = story("vous êtes mort", "mourir", 1)


Node_story_4_1_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_2_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_3_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_4_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_5_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_6_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_7_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_8_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_9_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_10_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)

Node_story_4_11_1 = story(
    "vous avez survécu, une vielle dame apparaît que faites-vous ? **(l'aide/tuer)**", "vivre", 0)


Node_story_5_1_2 = story(
    "La vielle dame vous a tuer, vous êtes mort", "l'aide", 1)

Node_story_5_2_2 = story(
    "Vous avez osé tuer une pauvre vielle dame...?\nles mages n'ont aucune limite quand il s'agit d'être lamentable, la prison vous attends", "tuer", 1)

Node_story_5_3_2 = story(
    "La vielle dame vous a tuer, vous êtes mort et pitoyable", "l'aide", 1)

Node_story_5_4_2 = story(
    "quel mauvais Paladin vous êtes partie en prison", "tuer", 1)

Node_story_5_5_2 = story(
    "quel mauvais Druide vous êtes partie en prison", "tuer", 1)

Node_story_5_6_2 = story("La grand mere vous a tuer , vous êtes mort", "l'aide", 1)

Node_story_5_7_2 = story(
    "quel mauvais Barde vous êtes partie en prison", "tuer", 1)

Node_story_5_8_2 = story("La grand mere vous a tuer , vous etes mort", "l'aide", 1)

Node_story_5_9_2 = story("La grand mere vous a tuer , vous etes mort", "l'aide", 1)

Node_story_5_10_2 = story(
    "quel mauvais necromentien vous etes partie en prison", "tuer", 1)

Node_story_5_11_2 = story(
    "quel mauvais Chasseur vous etes partie en prison", "tuer", 1)


Node_story_5_1_1 = story(
    "Félicitation la grand mère a bien été neutralisé, tu es sain et sauf. Mais son fils apprend la nouvelle est veut votre mort que voulez vous faire ? **(le tuer / le console)**", "tuer", 0)

Node_story_5_2_1 = story(
    "Quel gentleman/lady vous êtes, la vielle dame vous offre une friandise.\n son fils veut vous donner une potion l'acceptez-vous  ? (non / oui)", "l'aide", 0)

Node_story_5_3_1 = story(
    "Félicitation ! l'ancêtre a bien été neutralisé, vous êtes sain et sauf. \nMais son fils apprend l'effroyable nouvelle et veut votre tête, que comptez-vous faire ? **(le tuer / le console)**", "tuer", 0)

Node_story_5_4_1 = story(
    "Quel gentleman/lady vous êtes, la vielle dame vous offre une friandise.\n son fils veut vous donner une potion l'acceptez-vous  ? **(non / oui)**", "l'aide", 0)

Node_story_5_5_1 = story(
    "Quel gentleman/lady vous êtes, la vielle dame vous offre une friandise.\n son fils veut vous donner une potion l'acceptez-vous  ? **(non / oui)**", "l'aide", 0)

Node_story_5_6_1 = story(
    "Félicitation ! l'ancêtre a bien été neutralisé, vous êtes sain et sauf. \nMais son fils apprend l'effroyable nouvelle et veut votre tête, que comptez-vous faire ? **(le tuer / le console)**", "tuer", 0)

Node_story_5_7_1 = story(
    "Quel gentleman/lady vous êtes, la vielle dame vous offre une friandise.\n son fils veut vous donner une potion l'acceptez-vous  ? (non / oui)", "l'aide", 0)

Node_story_5_8_1 = story(
    "Félicitation ! l'ancêtre a bien été neutralisé, vous êtes sain et sauf. \nMais son fils apprend l'effroyable nouvelle et veut votre tête, que comptez-vous faire ? **(le tuer / le console)**", "tuer", 0)

Node_story_5_9_1 = story(
    "Félicitation ! l'ancêtre a bien été neutralisé, vous êtes sain et sauf. \nMais son fils apprend l'effroyable nouvelle et veut votre tête, que comptez-vous faire ? **(le tuer / le console)**", "tuer", 0)

Node_story_5_10_1 = story(
    "Quel gentleman/lady vous êtes, la vielle dame vous offre une friandise.\n son fils veut vous donner une potion l'acceptez-vous  ? **(non / oui)**", "l'aide", 0)

Node_story_5_11_1 = story(
    "Quel gentleman/lady vous êtes, la vielle dame vous offre une friandise.\n son fils veut vous donner une potion l'acceptez-vous  ? **(non / oui)**", "l'aide", 0)


Node_story_6_1_2 = story(
    "Son fantome vous a maudit ! vous agonisez dans les mort 24 heures qui suivent", "le tuer", 1)

Node_story_6_2_2 = story(
    "vous étiez en réalité souffrant d'un cancer appelé 'scénario' vous succombez donc à vos blessures ", "non", 1)

Node_story_6_3_2 = story(
    "Le jeune homme vous tue par vengance, logique vous aviez tout de même tué sa seule famille", "le console", 1)

Node_story_6_4_2 = story(
    "Bravo ! vous êtes mort, la potion contenait un poison ", "oui", 1)

Node_story_6_5_2 = story(
    "vous étiez en réalité souffrant d'un cancer appelé 'scénario' vous succombez donc à vos blessures", "non", 1)

Node_story_6_6_2 = story(
    "Son fantome vous a maudit ! vous agonisez dans les 24 heures qui suivent", "le tuer", 1)

Node_story_6_7_2 = story(
    "vous étiez en réalité souffrant d'un cancer appelé 'scénario' vous succombez donc à vos blessures", "non", 1)

Node_story_6_8_2 = story(
    "Le jeune homme vous tue par vengance, logique vous aviez tout de même tué sa seule famille", "le console", 1)

Node_story_6_9_2 = story(
    "Le jeune homme vous tue par vengance, logique vous aviez tout de même tué sa seule famille", "le console", 1)

Node_story_6_10_2 = story(
    "Bravo ! vous êtes mort, la potion contenait un poison ", "oui", 1)

Node_story_6_11_2 = story(
    "Bravo ! vous êtes mort, la potion contenait un poison ", "oui", 1)


Node_story_6_1_1 = story(
    "Le jeune homme se calme, car il se souvenu qu'il détestait sa grand mère mais vous conseil de fuir . Voulez vous fuir ? **(non / oui)** ", "le console", 0)

Node_story_6_2_1 = story(
    "vous étiez gravement blessé la potion vous a soigner, \nle fils s'avérait être en realité un grand chevalier, et vous propose de le rejoindre dans l'armée du roi, acceptez_vous ? **(non / oui)**", "oui", 0)

Node_story_6_3_1 = story(
    "Vous aviez bien fait, si vous ne l'aviez pas fait vous seriez mort, \nmais quelques minutes plus tard des soldats au service du petit fils de la vielle dame vous ont entendu, \nqu'allez-vous faire ? **(les combattre / se rendre)**", "le tuer", 0)

Node_story_6_4_1 = story(
    "elle était empoissonné vous avez bien fait, voulez-vous vous venger ? **(non / oui)**", "non", 0)

Node_story_6_5_1 = story(
    "vous étiez gravement blessé la potion vous a soigner, \nle fils s'avérait être en realité un grand chevalier, et vous propose de le rejoindre dans l'armée du roi, acceptez_vous ? **(non / oui)**", "oui", 0)

Node_story_6_6_1 = story(
    "Le jeune homme se calme, car il se souvenu qu'il détestait sa grand mère mais vous conseil de fuir . Voulez vous fuir ? **(non / oui)**", "le console", 0)

Node_story_6_7_1 = story(
    "vous étiez gravement blessé la potion vous a soigner, \nle fils s'avérait être en realité un grand chevalier, et vous propose de le rejoindre dans l'armée du roi, acceptez_vous ? **(non / oui)** ", "oui", 0)

Node_story_6_8_1 = story(
    "Vous aviez bien fait, si vous ne l'aviez pas fait vous seriez mort \nmais quelques minutes plus tard des soldats au service du petit fils de la vielle dame vous ont entendu, \nqu'allez-vous faire ? **(se rendre / se battre)**", "le tuer", 0)

Node_story_6_9_1 = story(
    "Vous aviez bien fait, si vous ne l'aviez pas fait vous seriez mort \nmais quelques minutes plus tard des soldats au service du petit fils de la vielle dame vous ont entendu, \nqu'allez-vous faire ? **(se rendre / se battre)**", "le tuer", 0)

Node_story_6_10_1 = story(
    "elle était empoissonné vous avez bien fait, voulez-vous vous venger ? (non / oui)", "non", 0)

Node_story_6_11_1 = story(
    "elle était empoissonné vous avez bien fait, voulez-vous vous venger ? (non / oui)", "non", 0)


Node_story_7_1_2 = story(
    "le fils s'avérait être en realité un grand chevalier, et voue tue sans difficulté", "non", 1)

Node_story_7_2_2 = story(
    "c'était une embuscade , vous êtes mort  ", "oui", 1)

Node_story_7_3_2 = story(
    "vous êtes trop faible pour vous battre contre ces soldats ,vous êtes donc logiquement mort", "les combattre", 1)

Node_story_7_4_2 = story(
    "trop clément, il vous on tuer ", "oui", 1)

Node_story_7_5_2 = story(
    "Déçu de votre refus, le chevalier estime que vous ne méritez pas de vivre", "non", 1)

Node_story_7_6_2 = story(
    "vous avez trebucher chute fatal vous etes mort ", "oui", 1)

Node_story_7_7_2 = story(
    "Déçu de votre refus, le chevalier estime que vous ne méritez pas de vivre ", "non", 1)

Node_story_7_8_2 = story(
    "ils étaient sans pitié et vous ont tuer", "se rendre ", 1)

Node_story_7_9_2 = story(
    "vous êtes trop faible contre eux , vous êtes mort ", "se battre", 1)

Node_story_7_10_2 = story(
    "2 contre 1 !? parce-que vous penseriez avoir le niveau ? ridicule ! vous êtes MORT... ", "oui", 1)

Node_story_7_11_2 = story(
    "2 contre 1 !? parce-que vous penseriez avoir le niveau ? ridicule ! vous êtes MORT... ", "oui", 1)


Node_story_7_1_1 = story(
    "Grâce à votre grande vitesse vous aviez survécu, félicitation ! mais la culpabilité vous ronge... voulez-vous vous suicider ? **(non / oui)** ", "oui", 0)

Node_story_7_2_1 = story(
    "C'était un test, et vous l'aviez reussi !!! \nils voudraient vous marier a sa soeur, acceptez-vous  ? **(non / oui)** ", "non", 0)

Node_story_7_3_1 = story(
    "Ému par votre sens de l'honneur, il vous demande de les rejoindre, vous voulez accepter ? **(non / oui)**", "se rendre", 0)

Node_story_7_4_1 = story(
    "Leur chatiment est merité, les tentatives d'assasinat doivent être puni, mais l'armée vous veut vous arrêter, qu'aller-vous faire ? **(se battre / s'expliquer)**", "non", 0)


Node_story_7_5_1 = story(
    "Si fière de vous avoir recruter, ils veulent faire la fête en votre compagnie,  accepter-vous ? **(non / oui)**", "oui", 0)

Node_story_7_6_1 = story(
    "Ému par votre sens de l'honneur, il vous demande de les rejoindre, vous voulez accepter ? **(non / oui)**", "non", 0)

Node_story_7_7_1 = story(
    "Si fière de vous avoir recruté, ils veulent faire la fête en votre compagnie, vous accepter ? **(non / oui)**", "oui", 0)

Node_story_7_8_1 = story(
    "Votre force les impresionne, et veulent faire de vous un mercenaire, acceptez-vous ? **(non / oui)**", "se battre", 0)

Node_story_7_9_1 = story(
    "Ému par votre sens de l'honneur, il vous demande de devenir mercenaire voulez vous acrcepte ? **(non / oui)**", "se rendre", 0)

Node_story_7_10_1 = story(
    "Ému par votre clémence, ils vous donne leurs richesses, acceptez-vous ? **(non / oui)**", "non", 0)

Node_story_7_11_1 = story(
    "Ému par votre clémence, ils vous donne leurs richesses, acceptez-vous ? **(non / oui)**", "non", 0)


Node_story_8_1_2 = story(
    "le fils vous rattrape vous êtes mort.", "non", 1)

Node_story_8_2_2 = story(
    "c'était une tueuse en série vous êtes mort célibataire.", "oui", 1)

Node_story_8_3_2 = story(
    "il n'avaient pas le choix, vous aviez tout de même commis des crimes, vous êtes mort.", "non", 1)

Node_story_8_4_2 = story(
    "énervé il vous tue.", "se battre", 1)

Node_story_8_5_2 = story(
    "Vous ne supportez pas l'alcool, vous mourrez d'ivresse.", "oui", 1)

Node_story_8_6_2 = story(
    "vous pensiez vraiment avoir chance de rentrer à l'armée ? ne rêver pas, vous êtes mort", "oui", 1)

Node_story_8_7_2 = story(
    "accablé par votre manque de respect, il vous tue.", "non", 1)

Node_story_8_8_2 = story(
    "accablé par votre culot, il vous tue.", "oui ", 1)

Node_story_8_9_2 = story(
    "ils étaient trop énervé pour vous épargner, donc il vous ont donc tuer.", "non", 1)

Node_story_8_10_2 = story(
    "c'était évidemment un piège, vous êtes mort.", "oui", 1)

Node_story_8_11_2 = story(
    "Vous leurs avez manqués de respect, ils s'énervent et vous tue.", "non", 1)


Node_story_8_1_1 = story(
    "le fils vous rattrape et vous sauve, félicitation ! vous avez survecu !", "oui", 1)

Node_story_8_2_1 = story(
    "votre chasteté vous a sauvé ! felicitation vous avez survécu ! ", "non", 1)

Node_story_8_3_1 = story(
    "vous avez rejoint l'armée, félicitation vous avez survecu !", "oui", 1)

Node_story_8_4_1 = story(
    "vos arguments et votre motivation les touches, on vous libère, félicitation vous avez survécu !", "s'expliquer", 1)

Node_story_8_5_1 = story(
    "votre sérieux les rends admiratif,  félicitation vous avez survécu !", "non", 1)

Node_story_8_6_1 = story(
    "accepte votre décicion, et decide de vous libérer, félicitation vous avez survécu", "non", 1)

Node_story_8_7_1 = story(
    "Vous faite la fête avec l'armée, félicitation vous avez survécu !", "oui", 1)

Node_story_8_8_1 = story(
    "Impréssionné par votre courage, on vous libère, félicitation vous avez survécu !", "non", 1)

Node_story_8_9_1 = story(
    "vous finissez par rejoindre l'armée, félicitation vous avez survécu", "oui", 1)

Node_story_8_10_1 = story(
    "votre clémence est légendaire, ils vous suivront même en enfer, félicitation vous avez survécu !", "non", 1)

Node_story_8_11_1 = story(
    "vous êtes riche, libre et surtout vivant ! félicitation vous avez survécu ?", "oui", 1)


Node_story_1.add_child(Node_story_2)

Node_story_2.add_child(Node_story_3_1)

Node_story_2.add_child(Node_story_3_2)

Node_story_2.add_child(Node_story_3_3)

Node_story_2.add_child(Node_story_3_4)

Node_story_2.add_child(Node_story_3_5)

Node_story_2.add_child(Node_story_3_6)

Node_story_2.add_child(Node_story_3_7)

Node_story_2.add_child(Node_story_3_8)

Node_story_2.add_child(Node_story_3_9)

Node_story_2.add_child(Node_story_3_10)

Node_story_2.add_child(Node_story_3_11)

Node_story_3_1.add_child(Node_story_4_1_1)

Node_story_3_1.add_child(Node_story_4_1_2)

Node_story_3_2.add_child(Node_story_4_2_1)

Node_story_3_2.add_child(Node_story_4_2_2)

Node_story_3_3.add_child(Node_story_4_3_1)

Node_story_3_3.add_child(Node_story_4_3_2)

Node_story_3_4.add_child(Node_story_4_4_1)

Node_story_3_4.add_child(Node_story_4_4_2)

Node_story_3_5.add_child(Node_story_4_5_1)

Node_story_3_5.add_child(Node_story_4_5_2)

Node_story_3_6.add_child(Node_story_4_6_1)

Node_story_3_6.add_child(Node_story_4_6_2)

Node_story_3_7.add_child(Node_story_4_7_1)

Node_story_3_7.add_child(Node_story_4_7_2)

Node_story_3_8.add_child(Node_story_4_8_1)

Node_story_3_8.add_child(Node_story_4_8_2)

Node_story_3_9.add_child(Node_story_4_9_1)

Node_story_3_9.add_child(Node_story_4_9_2)

Node_story_3_10.add_child(Node_story_4_10_1)

Node_story_3_10.add_child(Node_story_4_10_2)

Node_story_3_11.add_child(Node_story_4_11_1)

Node_story_3_11.add_child(Node_story_4_11_2)

Node_story_4_1_1.add_child(Node_story_5_1_1)

Node_story_4_1_1.add_child(Node_story_5_1_2)

Node_story_4_2_1.add_child(Node_story_5_2_1)

Node_story_4_2_1.add_child(Node_story_5_2_2)

Node_story_4_3_1.add_child(Node_story_5_3_1)

Node_story_4_3_1.add_child(Node_story_5_3_2)

Node_story_4_4_1.add_child(Node_story_5_4_1)

Node_story_4_4_1.add_child(Node_story_5_4_2)

Node_story_4_5_1.add_child(Node_story_5_5_1)

Node_story_4_5_1.add_child(Node_story_5_5_2)

Node_story_4_6_1.add_child(Node_story_5_6_1)

Node_story_4_6_1.add_child(Node_story_5_6_2)

Node_story_4_7_1.add_child(Node_story_5_7_1)

Node_story_4_7_1.add_child(Node_story_5_7_2)

Node_story_4_8_1.add_child(Node_story_5_8_1)

Node_story_4_8_1.add_child(Node_story_5_8_2)

Node_story_4_9_1.add_child(Node_story_5_9_1)

Node_story_4_9_1.add_child(Node_story_5_9_2)

Node_story_4_10_1.add_child(Node_story_5_10_1)

Node_story_4_10_1.add_child(Node_story_5_10_2)

Node_story_4_11_1.add_child(Node_story_5_11_1)

Node_story_4_11_1.add_child(Node_story_5_11_2)

Node_story_5_1_1.add_child(Node_story_6_1_1)

Node_story_5_1_1.add_child(Node_story_6_1_2)

Node_story_5_2_1.add_child(Node_story_6_2_1)

Node_story_5_2_1.add_child(Node_story_6_2_2)

Node_story_5_3_1.add_child(Node_story_6_3_1)

Node_story_5_3_1.add_child(Node_story_6_3_2)

Node_story_5_4_1.add_child(Node_story_6_4_1)

Node_story_5_4_1.add_child(Node_story_6_4_2)

Node_story_5_5_1.add_child(Node_story_6_5_1)

Node_story_5_5_1.add_child(Node_story_6_5_2)

Node_story_5_6_1.add_child(Node_story_6_6_1)

Node_story_5_6_1.add_child(Node_story_6_6_2)

Node_story_5_7_1.add_child(Node_story_6_7_1)

Node_story_5_7_1.add_child(Node_story_6_7_2)

Node_story_5_8_1.add_child(Node_story_6_8_1)

Node_story_5_8_1.add_child(Node_story_6_8_2)

Node_story_5_9_1.add_child(Node_story_6_9_1)

Node_story_5_9_1.add_child(Node_story_6_9_2)

Node_story_5_10_1.add_child(Node_story_6_10_1)

Node_story_5_10_1.add_child(Node_story_6_10_2)

Node_story_5_11_1.add_child(Node_story_6_11_1)

Node_story_5_11_1.add_child(Node_story_6_11_2)

Node_story_6_1_1.add_child(Node_story_7_1_1)

Node_story_6_1_1.add_child(Node_story_7_1_2)

Node_story_6_2_1.add_child(Node_story_7_2_1)

Node_story_6_2_1.add_child(Node_story_7_2_2)

Node_story_6_3_1.add_child(Node_story_7_3_1)

Node_story_6_3_1.add_child(Node_story_7_3_2)

Node_story_6_4_1.add_child(Node_story_7_4_1)

Node_story_6_4_1.add_child(Node_story_7_4_2)

Node_story_6_5_1.add_child(Node_story_7_5_1)

Node_story_6_5_1.add_child(Node_story_7_5_2)

Node_story_6_6_1.add_child(Node_story_7_6_1)

Node_story_6_6_1.add_child(Node_story_7_6_2)

Node_story_6_7_1.add_child(Node_story_7_7_1)

Node_story_6_7_1.add_child(Node_story_7_7_2)

Node_story_6_8_1.add_child(Node_story_7_8_1)

Node_story_6_8_1.add_child(Node_story_7_8_2)

Node_story_6_9_1.add_child(Node_story_7_9_1)

Node_story_6_9_1.add_child(Node_story_7_9_2)

Node_story_6_10_1.add_child(Node_story_7_10_1)

Node_story_6_10_1.add_child(Node_story_7_10_2)

Node_story_6_11_1.add_child(Node_story_7_11_1)

Node_story_6_11_1.add_child(Node_story_7_11_2)

Node_story_7_1_1.add_child(Node_story_8_1_1)

Node_story_7_1_1.add_child(Node_story_8_1_2)

Node_story_7_2_1.add_child(Node_story_8_2_1)

Node_story_7_2_1.add_child(Node_story_8_2_2)

Node_story_7_3_1.add_child(Node_story_8_3_1)

Node_story_7_3_1.add_child(Node_story_8_3_2)

Node_story_7_4_1.add_child(Node_story_8_4_1)

Node_story_7_4_1.add_child(Node_story_8_4_2)

Node_story_7_5_1.add_child(Node_story_8_5_1)

Node_story_7_5_1.add_child(Node_story_8_5_2)

Node_story_7_6_1.add_child(Node_story_8_6_1)

Node_story_7_6_1.add_child(Node_story_8_6_2)

Node_story_7_7_1.add_child(Node_story_8_7_1)

Node_story_7_7_1.add_child(Node_story_8_7_2)

Node_story_7_8_1.add_child(Node_story_8_8_1)

Node_story_7_8_1.add_child(Node_story_8_8_2)

Node_story_7_9_1.add_child(Node_story_8_9_1)

Node_story_7_9_1.add_child(Node_story_8_9_2)

Node_story_7_10_1.add_child(Node_story_8_10_1)

Node_story_7_10_1.add_child(Node_story_8_10_2)

Node_story_7_11_1.add_child(Node_story_8_11_1)

Node_story_7_11_1.add_child(Node_story_8_11_2)

@client.command()
async def mj(ctx, arg):
    def check(m):
        return int(m.author.id) == int(ctx.message.author.id) and int(m.channel.id) == int(ctx.message.channel.id)
    reponse = Node_story_1.testChild(arg)
    level = Node_story_2
    if reponse != Node_story_1:
        await ctx.send(f"{ctx.author.mention} \n {reponse.question_bot()}", tts=True)
        while reponse.end == 0:
            msg = await client.wait_for("message", check=check)
            reponse = reponse.testChild(msg.content)
            if level == reponse:
                await ctx.send(f"{ctx.author.mention} \n je ne comprend pas, veuillez rééssayer  " ,tts=True)
            else:
                await ctx.send(f"{ctx.author.mention} \n {reponse.question_bot()}", tts=True)
                level = reponse
    else:
        await ctx.send(f"{ctx.author.mention} \n je ne comprend pas, veuillez réessayer ", tts=True)

@client.command()
async def start(ctx, arg):
    def check(m):
        return int(m.author.id) == int(ctx.message.author.id) and int(m.channel.id) == int(ctx.message.channel.id)
    reponse = Node1.testChild(arg)
    level = Node2
    if reponse != Node1:
        await ctx.send(f"{ctx.author.mention} \n {reponse.question_bot()}", tts=True)
        while reponse.end == 0:
            msg = await client.wait_for("message", check=check)
            reponse = reponse.testChild(msg.content)
            if level == reponse:
                await ctx.send(f"{ctx.author.mention} \n je ne comprend pas, veuillez rééssayer ", tts=True)
            elif reponse.end == 1:
                await ctx.send(f"{ctx.author.mention} \n {reponse.question_bot()} ", tts=True)
                level = reponse
                await ctx.send(f"{ctx.author.mention} \n voulez vous prendre cette classe ? ", tts=True)
                msg =await client.wait_for("message", check=check)
                if msg.content == "oui":
                    await create_t(ctx, reponse.question_bot())
                    await create_v(ctx, reponse.question_bot())
                    await add_r(ctx, reponse.question_bot())
            else:
                await ctx.send(f"{ctx.author.mention} \n {reponse.question_bot()} ", tts=True)
                level = reponse


    else:
        await ctx.send(f"{ctx.author.mention} \n je ne comprend pas, veuillez réessayer", tts=True)


async def add_r(ctx, name):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name=name)
    await user.add_roles(role)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(error, tts=True)

async def create_t(ctx, nom_de_salon):

    for channel in client.get_all_channels():
        if nom_de_salon == channel.name:
            return



    guild = ctx.guild
    role = nom_de_salon
    autorize_role = await guild.create_role(name=role)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        autorize_role: discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel(nom_de_salon, overwrites=overwrites)
    await ctx.author.add_roles(autorize_role)


async def create_v(ctx, nom_de_salon):
    if ctx.channel.name != nom_de_salon:
        guild = ctx.guild
        role = nom_de_salon
        autorize_role = await guild.create_role(name=role)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            autorize_role: discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_voice_channel(nom_de_salon, overwrites=overwrites)
        await ctx.author.add_roles(autorize_role)



client.run("bot ID here")
