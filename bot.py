from webbrowser import get
import discord 
from discord.ext import commands
from discord.utils import get
bot=commands.Bot(command_prefix="$")

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
            return Node1
        return self

    def question_bot(self):
        return self.question




Node1 = story("start", "key", 0)

Node2 = story("bien/mal", "start", 0)

Node3_1 = story("mélée/range", "bien", 0)

Node4_1 = story("magie/arme", "mélée", 0)

Node5_1 = story("element", "magie", 0)

Node6_1 = story("elementaire de feu", "feu", 1)

Node6_2 = story("elementaire d'eau", "eau", 1)

Node6_3 = story("elementaire de terre", "terre", 1)

Node6_4 = story("elementaire d'air", "air", 1)

Node6_5 = story("elementaire de lumière", "lumière", 1)

Node5_2 = story("defense/attaque", "arme", 0)

Node6_6 = story("guerrier", "defense", 1)

Node6_7 = story("Paladin", "attaque", 1)

Node4_2 = story("magie/arme", "range", 0)

Node5_3 = story("taper/non", "magie", 0)

Node6_8 = story("element", "taper", 0)
            
Node7_1 = story("mage de feu", "feu", 1)

Node7_2 = story("mage d'eau", "eau", 1)

Node7_3 = story("mage de terre", "terre", 1)

Node7_4 = story("mage d'air", "air", 1)

Node6_9 = story("Druide", "non", 1)

Node5_4 = story("taper/non", "arme", 0)

Node6_10 = story("archer", "taper", 1)

Node6_11 = story("Barde", "non", 1)

Node3_2 = story("mélée/range", "mal", 0)

Node4_3 = story("magie/arme", "mélée", 0)

Node5_5 = story("element", "magie", 0)

Node6_12 = story("elementaire de poison", "poison", 1)

Node6_13 = story("elementaire de sang", "sang", 1)

Node6_14 = story("elementaire de tenèbre", "tenèbre", 1)

Node5_6 = story("defense/attaque", "arme", 0)

Node6_15 = story("Troll", "defense", 1)

Node6_16 = story("Orc", "attaque", 1)

Node4_4 = story("magie/arme", "range", 0)

Node5_7 = story("taper/non", "magie", 0)

Node6_17 = story("element", "taper", 0)

Node7_5 = story("mage de poison", "poison", 1)

Node7_6 = story("mage de sang", "sang", 1)

Node7_7 = story("mage de tenèbre", "tenèbre", 1)

Node6_18 = story("necromentien", "non", 1)

Node5_8 = story("Chasseur", "range", 1)


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

Node4_4.add_child(Node5_7)

Node5_7.add_child(Node6_17)

Node6_17.add_child(Node7_5)

Node6_17.add_child(Node7_6)

Node6_17.add_child(Node7_7)

Node5_7.add_child(Node6_18)

Node4_4.add_child(Node5_8)




@bot.command()
async def mj(ctx, arg):
    def check(m):
        return int(m.author.id) == int(ctx.message.author.id) and int(m.channel.id) == int(ctx.message.channel.id)
    reponse = Node1.testChild(arg)
    level = Node2
    if reponse != Node1:
        await ctx.send(f"{reponse.question_bot()}")
        while reponse.end == 0:
            msg = await bot.wait_for("message", check=check)
            reponse = reponse.testChild(msg.content)
            if level == reponse:
                await ctx.send(f"je ne comprend pas, veuillez rééssayer")
            else:
                await ctx.send(f"{reponse.question_bot()}")
                level = reponse
    else:
        await ctx.send(f"je ne comprend pas, veuillez réessayer")



@bot.command()
async def change_name(ctx, *, arg):
    await ctx.author.edit(nick=arg)
    await ctx.send(f'Nickname was changed for {ctx.author.mention} ' , tts=True)


@bot.command()
async def create_r(ctx,r):
    colour=discord.Colour(0xffffff)
    # permissions=discord.Permissions(permissions=<>)
    guild = ctx.guild

    for role in guild.roles:
        if role.name == r:
            return

    await guild.create_role( name=r)

@bot.command()
async def add_r(ctx):
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="test")
    await user.add_roles(role)

@bot.command()
async def create_t(ctx, *, nom_de_salon):

    for channel in bot.get_all_channels():
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

@bot.command()
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


@bot.command(name='del')
async def delete(ctx, number_of_messages: int):
    messages = await ctx.channel.history(limit=number_of_messages + 1).flatten()

    for each_message in messages:
        await each_message.delete()


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.command()
async def ping(ctx, role: discord.Role, *, message):

    await ctx.send(f"""
    {role.mention}
    cette personne {ctx.author.mention} a dit : {message}
    """)

@bot.command()
async def admin(ctx,*, message):
    admin = get(ctx.guild.roles,name='admin') 
    await ctx.send(f"""
    {admin.mention}
    cette personne {ctx.author.mention} a dit : {message}
    """)


# faire le bot

bot.run("OTc4MjI5MzgxNjQ0MzE2NzEy.GrSDPk.7vgtGIoQlb2voSUzwN4UNh1KxbCJvK0V1Kpozk")