import discord
from discord.ext import commands
from discord import Spotify
import requests

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun Cog ready!")
    
    @commands.command()
    async def spotify(self,ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
            pass
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = discord.Embed(
                        title=f"{user.name}'s Spotify",
                        description="Listening to {}".format(activity.title),
                        color=activity.colour)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text="Song started at {}".format(
                        activity.created_at.strftime("%H:%M")))
                    await ctx.send(embed=embed)
        else:
            await ctx.send("user is not listening to any song ")
    
    @commands.command()
    async def joke(self,ctx):
        req = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = req.json()
        embed = discord.Embed(
            title="{}".format(joke['setup']),
            description="{}".format(joke['punchline']),
            color=0xFF5733)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def insult(ctx, user: discord.Member = None):
        if user == None:
            await ctx.send("No u cant insult yourself,Tag someone")
        else:
            req = requests.get(
                "https://evilinsult.com/generate_insult.php?lang=en&type=json")
            insult = req.json()
            embed = discord.Embed(title="{}".format(user.display_name),
                                description="{}".format(insult['insult']),
                                color=0xFF5733)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def createavatar(ctx, a=None):
        if a == None:
            await ctx.send("please enter a random text to generate your avatar")
        else:
            req = requests.get(
                f'https://robohash.org/{a}.png?set=set{random.randint(1,3)}')
            img = req.url
            embed = discord.Embed(title="your avatar",
                                description=f"Here is your random avatar genrated by your text {a}",
                                color=0xFF5733)
            embed.set_image(url=img)
            embed.set_footer(text="created by https://robohash.org/")
            await ctx.send(embed=embed)
    
    @commands.command()
    async def av(ctx, user: discord.User = None):

        emb = discord.Embed(title="Avatar")

        if user == None:
            emb.set_image(url=ctx.author.avatar_url)

        else:
            emb.set_image(url=user.avatar_url)

        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)


    @av.error
    async def av_error(ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send("Hmm 🤔, I had a hard time finding the user, you sure that user exits❓ it got a bit chilly right now 👻")

        else:
            await ctx.send("Hmm somethings wrong, plz inform the developers")

def setup(client):
    client.add_cog(Fun(client))
