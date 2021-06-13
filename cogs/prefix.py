from sys import prefix
from typing import Collection
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://vikranth:test123@cluster0.fjemn.mongodb.net/discord?retryWrites=true&w=majority")
db = cluster['discord']
collection = db['prefixes']

def get_prefix(client, message):
    guild = collection.find({"_id" : f"{message.guild.id}"})
    for i in guild:
        return i["prefix"]

class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Prefix Cog is ready")
    
    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        guildId = guild.id
        prefix = "bb"

        post = {"_id" : f"{guildId}", "prefix" : f"{prefix}"}
        collection.insert_one(post)
        print("Done")
    
    @commands.command()
    async def changeprefix(self,ctx, prefix):
        # results = collection.find({"_id": ctx.guild.id})
        # if results:
        collection.update_one({"_id": f"{ctx.guild.id}"}, {"$set":{"prefix" : f"{prefix}"}})
        await ctx.send(f"Prefix changed to ``{prefix}``")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            guild = collection.find_one({"_id" : f"{message.guild.id}"})
            prefix = guild["prefix"]
            emb = discord.Embed(description=f"Hi, I currently respond to\n```Prefix: {prefix}```", color=0x009aff)
            await message.channel.send(embed=emb)

def setup(client):
    client.add_cog(Prefix(client))