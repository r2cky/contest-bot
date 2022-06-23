import random
import requests
import discord
import time
import os
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
from discord.ext import commands
from bs4 import BeautifulSoup as bsp

client = commands.Bot(command_prefix='waimai~~', help_command=None)
ch=939525785008615484
bot_talk = 977200316586008606
channel = client.get_channel(ch)
name = "waimai" #bot name
st = "Count down"
stop = 1
ok = 0 #0 not started 1 joining 2 start_contest

#db['update log'].append(["v1.01","Fix the initialize bug"])

@client.event
async def on_message(msg):
    global stop
    if(msg.channel.id == bot_talk):
      l = msg.content.split(",")
      if(l[0].strip() == "stop"):
        stop = 1
      if(l[0].strip() == "c_d" or l[0].strip() == "r_u"):      
        if(stop == 1):
          stop = 0
          await count(l[1])  
      

@client.event
async def count(x):
    global bot_talk, stop
    s = client.get_channel(bot_talk)
    cnt = int(x)
    for i in range (int(x)-1):
      time.sleep(60)
      cnt -= 1
      if(stop == 1):
        stop = 0
        return
      await s.send("r_u,"+str(cnt))
    time.sleep(60)
    await s.send("e_c")
    stop = 1
      
@client.event
async def on_ready():
    global channel
    global st
    game = discord.Game(st)
    await client.change_presence(status=discord.Status.online, activity=game)

keep_alive()
try:
  client.run(db['token'])
except:
  os.system("kill 1")

