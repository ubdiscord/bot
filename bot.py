import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import colorsys
import random
import platform
from discord import Game, Embed, Color, Status, ChannelType
import os
import functools
import time
import datetime
import requests
import json
import praw
import aiohttp

prefix = os.getenv("PREFIX")
desc= os.getenv("DESCRIPTION")

Forbidden= discord.Embed(title="Permission Denied", description="1) Please check whether you have permission to perform this action or not. \n2) Please check whether my role has permission to perform this action in this channel or not. \n3) Please check my role position.", color=0x00ff00)
client = commands.Bot(description=desc,command_prefix=prefix, pm_help = True)
client.remove_command('help')

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('--------')
    print('Started Our BOT')
    print('Created by Utkarsh')

   
@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if member.bot:
            return
        if channel.name == '🎉welcome🎉':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f'Welcome {member.name} to {member.server.name}', description='Do not forget to check rules and never try to break any one of them', color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name='__Thanks for joining__', value='**Hope you will be active here.**', inline=True)
            embed.set_thumbnail(url='https://media.giphy.com/media/OkJat1YNdoD3W/giphy.gif') 
            embed.set_image(url = member.avatar_url)
            embed.add_field(name='__Join position__', value='{}'.format(str(member.server.member_count)), inline=True)
            embed.add_field(name='Time of joining', value=member.joined_at)
            await client.send_message(channel, embed=embed) 
            role = discord.utils.get(member.server.roles, name='Members')
            await asyncio.sleep(60)
            await client.add_roles(member, role)

@client.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name == '🎉welcome🎉':
            r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
            embed = discord.Embed(title=f'{member.name} just left {member.server.name}', description='Bye bye 👋! We will miss you 😢', color = discord.Color((r << 16) + (g << 8) + b))
            embed.add_field(name='__User left__', value='**Hope you will be back soon 😕.**', inline=True)
            embed.add_field(name='Your join position was', value=member.joined_at)
            embed.set_thumbnail(url=member.avatar_url)
            await client.send_message(channel, embed=embed)
    
@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def setupwelcomer(ctx):
    if ctx.message.author.bot:
      return
    else:
      server = ctx.message.server
      everyone_perms = discord.PermissionOverwrite(send_messages=False, read_messages=True)
      everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
      await client.create_channel(server, '🎉welcome🎉',everyone)

@client.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def say(ctx,*,message:str=None):
    await client.delete_message(ctx.message)
    if message is None:
        await client.say(f'Use this command like: ``{prefix}say <anything>``')
    else:
        await client.say(message)
        
@client.command(pass_context = True)
async def meme(ctx):
    colour = '0x' + '008000'
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.reddit.com/r/me_irl/random") as r:
            data = await r.json()
            embed = discord.Embed(title='Random Memes', description='from reddit', color=discord.Color(int(colour, base=16)))
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            await client.say(embed=embed)

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.startswith('m=help'):
        await client.send_message(message.channel, 'Check your DMs 📫')
        await client.send_message(message.author, f'```Commands list:```\n1)``{prefix}meme`` : For memes\n2)``{prefix}say <anything>`` : To make bot say anything(admin permission required\n3)``{prefix}setupwelcomer`` : To setup welcomer(admin permission required')
        await client.send_message(message.author, 'You can also join our support server: https://discord.gg/wdGurTV')

            
client.run(os.getenv('TOKEN'))
