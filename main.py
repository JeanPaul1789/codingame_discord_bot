import asyncio
import codingame
import discord
import json
from discord.colour import Color
from discord.ext import commands

with open("./config/config.json", "r") as cjson:
    config = json.load(cjson)
with open("./config/db.json", "r") as dbjson:
    db = json.load(dbjson)
bot = commands.Bot(command_prefix=config["prefix"])
client = codingame.Client()

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")

@bot.event
async def on_ready():
    print('Le bot est pret')
    await bot.change_presence(activity=discord.Game(name="!help"))

@bot.command(name="unlink", description="Unlink you from your actual profil")
async def unlink(ctx):
    with open("./config/db.json", "r+") as file:
        file_data = json.load(file)
        try:
            if not file_data[str(ctx.author.id)]["user"]:
                await ctx.send("You are not linked, use !link to link your codingame profile")
            else:
                tmp = file_data[str(ctx.author.id)]["user"]
                file_data[str(ctx.author.id)]["user"] = ""
                await ctx.send("Succesfully unlinked from " + tmp)
        except KeyError:
            await ctx.send("You are not linked, use !link to link your codingame profile")
        with open("./config/db.json", "w+") as fp:
            json.dump(file_data, fp, sort_keys=True, indent=4)

@bot.command(name="link", description="link you to a codingame profil")
async def link(ctx, arg):
    with open("./config/db.json", "r+") as file:
        file_data = json.load(file)
        try:
            if not file_data[str(ctx.author.id)]["user"]:
                file_data[str(ctx.author.id)]["user"] = arg
                await ctx.send("Succesfully linked to " + arg)
            else:
                await ctx.send("You are already linked, use !unlink to reset your link")
        except KeyError:
            file_data[str(ctx.author.id)] = {"user": arg}
            await ctx.send("Succesfully linked to " + arg)
        with open("./config/db.json", "w+") as fp:
            json.dump(file_data, fp, sort_keys=True, indent=4)

@bot.command(name="profil", description="See an user profil from codingame")
async def profil(ctx, arg=None):
    if not arg:
        file = open("./config/db.json", "r+")
        file_data = json.load(file)
        if not file_data[str(ctx.author.id)]["user"]:
            await ctx.send("This command required an argument or to be linked")
            return(84)
        else:
            codingamer = client.get_codingamer(file_data[str(ctx.author.id)]["user"])
    else:
        codingamer = client.get_codingamer(arg)
    embed = discord.Embed(title=codingamer.pseudo, url="https://www.codingame.com/profile/" + codingamer.public_handle, color=Color.orange())
    embed.add_field(name="Clash Of Code Global rank:", value=str(codingamer.get_clash_of_code_rank()) + " ème", inline=True)
    embed.add_field(name="Global Rank", value=str(codingamer.rank) + " ème", inline=True)
    embed.add_field(name="Level:", value=str(codingamer.level), inline=False)
    embed.set_thumbnail(url=codingamer.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="game", description="Join the actual game of  clash of code")
async def game(ctx):
    coc = client.get_pending_clash_of_code()
    embed = discord.Embed(title="Click to join", url=coc.join_url, description="**Players online:**", color=Color.blue())
    embed.set_thumbnail(url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png")
    for player in coc.players:
        embed.add_field(name=player.pseudo, value="[See profil](https://www.codingame.com/profile/" + player.public_handle + ")")
    embed.set_footer(text="Time before start: " + str(coc.time_before_start.seconds) + "s")
    await ctx.send(embed=embed)

@bot.command(name="next", description="Join the next game of clash of code")
async def next(ctx):
    coc = client.get_pending_clash_of_code()
    next_battle = coc.time_before_start.seconds
    await ctx.send("Next battle in " + str(next_battle) + "s ~")
    while next_battle > 5:
        coc = client.get_pending_clash_of_code()
        next_battle = coc.time_before_start.seconds
        await asyncio.sleep(5)
    await asyncio.sleep(next_battle + 5)
    await ctx.send(ctx.author.mention)
    coc = client.get_pending_clash_of_code()
    while not coc:
        coc = client.get_pending_clash_of_code()
        asyncio.sleep(1)
    embed = discord.Embed(title="Click to join", url=coc.join_url, description="**Players online:**", color=Color.blue())
    embed.set_thumbnail(url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png")
    for player in coc.players:
        embed.add_field(name=player.pseudo, value="https://www.codingame.com/profile/" + player.public_handle)
    embed.set_footer(text="Time before start: " + str(coc.time_before_start))
    await ctx.send(embed=embed)

bot.run(config["token"])