import random
import requests
import discord
import re
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
import time
import json
import math
import os
from bs4 import BeautifulSoup as bsp

client = commands.Bot(command_prefix='loli~', help_command=None)
chl = 939525785008615484
bot_talk = 977200316586008606
channel = client.get_channel(chl)
clock = 0
r_time = 100000
host = "0"
host_id = 0
user = []
user_name = []
user_id = []
solve_count = []
type = 0 #0: First win 1:get score/AC  2:atcoder like
rated = 0
prob = []
prob2 = []
aced = [] #checker for first
ac = []#for all 
score = []
user_score = []
user_final_time = []
fastest = []
name = "CCP match system" #bot name
st = "CCP match"
ok = 0 #0 not started 1 pending 2 joining 3 start_contest
busy = 0
for_use = 1 #0 service closed
my_ch = 977520526010482741
my_ch_1 = 977528953692639273
my_ch_2 = 977528954414051358
my_ch_3 = 977529093534924810
desc = ["This is a speedy round. That is, only the first AC can get all point from a problem.","This is a div round. That is, all participants that get AC will divide point from a problem equally, the first AC will get 10% bonus point.","This is atcoder-like round. That is, all participants can get all point from a problem."]
#db['contest_count']=0
#db['ccpcontest']={}
#db['ccprating']={}
#db['user_account']={}
#db['token']= 
#db['problem']={}
#for i in range(100,4001,100):
  #db['problem'][str(i)]=[]
#db['problem_now'] = 500


def get_problem(diff):
  return db['problem'].get(str(diff))
  
@client.event
async def on_message(msg):
    global busy, bot_talk, ok, r_time, db, user, user_name, user_id , user_score, st, my_ch, my_ch_1, user_final_time, prob, prob2, score, type, name, aced, solve_count, ac, chl, for_use, rated, r_time, host
    cha = client.get_channel(chl)
    bch = client.get_channel(bot_talk)
    if(msg.author.id==966927096033181718):return
    if(msg.channel.id != bot_talk and msg.channel.id != chl):return
    if(for_use == 0):
      await cha.send(embed = discord.Embed(title="The loli bot is currently unavailable."))
      return
    if(msg.channel.id == bot_talk):
      busy = 1
      await client.process_commands(msg)
      busy = 1
      l=msg.content.split(",")
      if(l[0]=="r_u"):
          if(r_time<=int(l[1])):
            busy = 0
            return
          r_time = int(l[1])
          if(ok == 0):
            ok = 3
            a = str(db['contest_count'])
            prob = db['ccpcontest'][a][0]
            prob2 = db['ccpcontest'][a][1]
            score = db['ccpcontest'][a][2]
            user = db['ccpcontest'][a][3]
            user_name = db['ccpcontest'][a][4]
            type = db['ccpcontest'][a][5]
            user_id = db['ccpcontest'][a][6]
            rated = db['ccpcontest'][a][7]
            host = db['ccpcontest'][a][8]
            print(db['ccpcontest'][a]);
            for i in range(0,len(prob)):
              aced.append("0")
              solve_count.append(0)

            for i in range(len(user)):
              ac.append([])
              user_score.append(0) 
              user_final_time.append(0)
              for j in range(len(prob)):
                ac[i].append(False)
          try:
            if(len(user) == 0):busy=0
            tmp = discord.Embed(title=name)
            cha = client.get_channel(my_ch)
            msg = await cha.fetch_message(my_ch_1)
            tmp.add_field(name="Remaining time", value=str(r_time)+":00 before the match ends.", inline=False)
            await msg.edit(embed = tmp)
          except:
             print("update time failed")          
          try:
            await update_status()
            busy = 0
          except:
            busy = 0
            print("update status failed") 

      if(msg.content.strip()=="unlock"):
        busy = 0
        return 
      if(msg.content.strip()=="e_c"):
        game = discord.Game(st)
        await client.change_presence(status=discord.Status.online, activity=game)
        if(ok == 0 or r_time == 0):
          busy = 0
          return
        r_time = 0
        await cha.send(embed = discord.Embed(title=name,description="The match has ended."))
        try:
          ok = 0
          tmp = discord.Embed(title=name)
          cha = client.get_channel(my_ch)
          msg = await cha.fetch_message(my_ch_1)
          tmp.add_field(name="Remaining time", value="The match has ended.", inline=False)
          await msg.edit(embed = tmp)
        except:
          print("update time failed")
        await update_status()
        if(len(user_name)==0):
          ok=busy=0
          return
        fin = []
        for i in range(len(user)):
          pi = [user_name[i],user_score[i],user_id[i],-user_final_time[i]]
          fin.append(pi)
        fin.sort(key = lambda x:(x[1],x[3]), reverse=True)
        if(rated == 1):
          await update_rating(fin)
        db['ccprank'][db['contest_count']] = fin
        cha = client.get_channel(chl)
        rank=discord.Embed(title="Final Standing")
        for i in range(len(user)):
          rank.add_field(name=str(i+1)+". "+fin[i][0], value="Score: "+str(fin[i][1]), inline=False)
          if(i+1 == len(user) or i % 20 == 19):
            await cha.send(embed = rank)
            rank=discord.Embed(title="Final Standing")
        busy = 0
      busy = 0
      return     
    if(busy==1):
      print("busy")
      return
    try:
      busy = 1
      await client.process_commands(msg)
      busy = 0
    except:
      busy = 0
    finally:
      busy = 0

#declare commands
@client.command()
async def help(ctx):
    try:
      text=discord.Embed(title=help, url="https://contest-bot.cheesechi.repl.co")
      text.add_field(name="for all command", value="loli~", inline=False)
      text.add_field(name="prepare + [command]", value="Prepare a round , author can use [prepare cancel] to cancel.\nThe command format can be seen [here](https://hackmd.io/@r1cky/Sk9a9qD_q)", inline=False)
      text.add_field(name="start", value="Start a round", inline=False)
      text.add_field(name="link + [your codeforces account]", value="Link your account so you can join the matches.", inline=False)
      text.add_field(name="join", value="Join a round", inline=False)
      text.add_field(name="past_contest + [round number]", value="Find a match in the past.", inline=False)
      text.add_field(name="my_account", value="Find your profile", inline=False)
      text.add_field(name="update_problem", value="Update the problems in the database.", inline=False)
      text.add_field(name="help", value="Show this message.", inline=False)
      await ctx.send(embed = text)
    except:
      print("err")
################################################################# 
@client.command()
async def link(ctx,arg):   
    if(ok == 3):
      await ctx.channel.send(embed = discord.Embed(title=name,description="You can't do this command during contest."))
      return
    global db
    try: 
      if(db['ccprating'].get(str(ctx.author.id)) == None):
         db['ccprating'][str(ctx.author.id)] = {}
      db['user_account'][str(ctx.author.id)] = [arg.strip()]
      print("linked")     
      await ctx.channel.send(embed = discord.Embed(title=name,description="Your account has been linked to codeforces account "+arg))
    except:
      print("err")
################################################################# 
@client.command()
async def join(ctx):
    global db, user, user_name, ok, user_score, user_id
    if(ok != 2):
       await ctx.channel.send(embed = discord.Embed(title=name,description="Exception."))
       return
    try:
      cf_name = db['user_account'].get(str(ctx.author.id))
      print(cf_name)
      if(cf_name==None):
          await ctx.channel.send(embed = discord.Embed(title=name,description="You need to set your account to your codeforces account first."))
          return
      for i in user_id:
         if(i == str(ctx.author.id)):
            await ctx.channel.send(embed = discord.Embed(title=name,description="You have joined the match "))  
            return
      user.append(ctx.author)    
      user_name.append(ctx.author.name) 
      user_id.append(str(ctx.author.id)) 
      user_score.append(0) 
      await ctx.channel.send(embed = discord.Embed(title=name,description="You have joined the match successfully."))  
      return
    except:
      await ctx.channel.send(embed = discord.Embed(title=name,description="Err"))
##########################################################
@client.command()
async def start(ctx):
  global host,channel, ok, db, host_id, prob, prob2, score, r_time, clock, user, user_name, user_id, bot_talk, ac, my_ch, my_ch_1, user_final_time, rated
  if(ok != 2):
    await ctx.channel.send(embed = discord.Embed(title=name,description="Exception occured."))
    return
  if(host_id != str(ctx.author.id)):
    await ctx.channel.send(embed = discord.Embed(title=name,description="You're not the host of the contest."))
    return
  if(len(user)<3 and rated==1):
    await ctx.send(embed = discord.Embed(title="The participant is less than three, it is not rated."))
    rated = 0
  for i in range(len(user)):
    ac.append([])
    user_final_time.append(0)
    for j in range(len(prob)):
      ac[i].append(False)
  ok = 3
  bch = client.get_channel(bot_talk)
  await bch.send("c_d,"+str(clock))
  parti = ""
  for i in user_name:
     parti+=i
     parti+=" "
  if(len(user_name)==0):parti="none"
  tmp=discord.Embed(title=name)
  tmp.add_field(name="CCP Match # "+str(db['contest_count']), value="The contest has started.", inline=False)
  tmp.add_field(name="Participants: ", value=parti, inline=False)
  tmp.add_field(name="Duration time: ", value=str(r_time)+" mins", inline=False)
  for i in range(len(prob)):
    ur="https://codeforces.com/problemset/problem/"+str(prob[i])+"/"+str(prob2[i])
    tmp.add_field(name="Question # "+str(i+1)+" : "+str(prob[i])+" "+str(prob2[i]), value="[Score: "+str(score[i])+"]("+ur+")", inline=False)
  a = [prob,prob2,score,user_name,user_name,type,user_id,rated,host]
  b = str(db['contest_count'])
  db['ccpcontest'][b] = a
  await ctx.send(embed = tmp)
  await update_status()
  tmp=discord.Embed(title=name)
  tmp.add_field(name="Remaining time", value=str(r_time)+":00 before the match ends.", inline=False)
  cha = client.get_channel(my_ch)
  msg = await cha.fetch_message(my_ch_1)
  await msg.edit(embed = tmp)
  return
#########################################################
@client.command()
async def prepare(ctx,arg):
    global name, channel, prob, prob2, clock, ok, score, aced, host, host_id, r_time, user,user_id,user_name, user_score, type, rated, ac, solve_count, desc, user_final_time
    if(ok == 2 and str(ctx.author.id) == host_id):
      if(arg.strip()=="cancel"):
        await ctx.channel.send(embed = discord.Embed(title=name,description="The match is canceled."))
        ok = 0
      else:
        await ctx.channel.send(embed = discord.Embed(title=name,description="Exception."))
      return
    if(ok != 0 and ok != 2):
      await ctx.channel.send(embed = discord.Embed(title=name,description="The match is running right now. Therefore, you can't prepare it."))
      return 
    if(ok == 2 and host_id != str(ctx.author.id)):
      await ctx.channel.send(embed = discord.Embed(title=name,description="You're not the host of the contest."))
      return
    ok = 1
    host = ctx.author.name
    host_id = str(ctx.author.id)
    db['contest_count'] += 1
    await ctx.channel.send(embed = discord.Embed(title=name,description="Please wait... \n(May took several minutes.)"))
    try:
        l=arg.split(",")
        if(len(l) <= 5 or len(l) > 33 or len(l) % 3 != 0): #max 10requests
           ok = 0 
           await ctx.channel.send(embed = discord.Embed(title=name,description="Format wrong or too long"))
           return
        r_time = int(l[0])
        type = -1
        if(l[1].strip() == "speedy"):type = 0
        if(l[1].strip() == "div"):type = 1
        if(l[1].strip() == "atcoder"):type = 2
        rated = -1
        if(l[2].strip() == "rated"):rated = 1
        if(l[2].strip() == "unrated"):rated = 0
        if(r_time < 3 or r_time > 120):
          ok = 0
          await ctx.channel.send(embed = discord.Embed(title=name,description="Time exceeds the limit"))
          return
        if(type == -1):
          ok = 0
          await ctx.channel.send(embed = discord.Embed(title=name,description="Invalid contest type."))
          return
        if(rated == -1):
          ok = 0
          await ctx.channel.send(embed = discord.Embed(title=name,description="Invalid rated format"))
          return
        clock = r_time
        r_time = clock 
        prob.clear()
        prob2.clear()
        user.clear()
        user_id.clear()
        user_name.clear()
        user_score.clear()
        score.clear()
        aced.clear()
        ac.clear()
        solve_count.clear()
        user_final_time.clear()
        for i in range(3,len(l),3):
          if(int(l[i+2])>4000 or int(l[i+2])<100):
            await ctx.send(embed = discord.Embed(title=name,description="Score limit exceed."))
            ok = 0
            return
          exit_code = await find_problem(int(l[i]),int(l[i+1]),int(l[i+2])) 
          if(exit_code!=0):
            print(exit_code)
            ok = 0
            await ctx.send(embed = discord.Embed(title=name,description="Something went wrong."))
            return
          if(len(prob)>20):
            print(len(prob))
            ok = 0
            await ctx.send(embed = discord.Embed(title=name,description="Too many problems."))
            return
         
    except:
      ok = 0
      await ctx.send(embed = discord.Embed(title=name,description="Something wrong"))
      return
    ok = 2
    d = ""
    for i in score:
      d += str(i)
      d += " "
    tmp=discord.Embed(title=name)
    tmp.add_field(name="CCP Match # "+str(db['contest_count']), value="Host by "+host, inline=False)
    tmp.add_field(name="Contest type", value=desc[type], inline=False)
    tmp.add_field(name="Duration", value=str(r_time)+" mins", inline=False)
    if(rated == 1):
      tmp.add_field(name="Rated", value="This match is rated.", inline=False)
    if(rated == 0):
      tmp.add_field(name="Unrated", value="This match is unrated.", inline=False)
    tmp.add_field(name="Score distribution :", value=d, inline=False)
    await ctx.send(embed = tmp)
##########################################################
@client.command()
async def past_contest(ctx,arg):   
    if(ok == 3):
      await ctx.channel.send(embed = discord.Embed(title=name,description="You can't do this command during the match."))
      return
    global db, my_ch, my_ch_1, my_ch_2, my_ch_3
    try:
      if((ok == 2 or ok == 1) and db['contest_count'] == int(arg)):
        await ctx.channel.send(embed = discord.Embed(title=name,description="Access denied."))
        return
      problem = db['ccpcontest'].get(arg)
      pastrank = db['ccprank'].get(arg)
      if(problem == None):
        await ctx.channel.send(embed = discord.Embed(title=name,description="Your query failed."))
        return
      tmp=discord.Embed(title=name)
      tmp.add_field(name="CCP Match # "+str(arg), value="Now you are watching the past contest.", inline=False)
      for i in range(len(problem[0])):
        ur="https://codeforces.com/problemset/problem/"+str(problem[0][i])+"/"+str(problem[1][i])
        tmp.add_field(name="Question # "+str(i+1)+" : "+str(problem[0][i])+" "+str(problem[1][i]), value="[Score: "+str(problem[2][i])+"]("+ur+")", inline=False)
      cha = client.get_channel(my_ch)
      msg = await cha.fetch_message(my_ch_2)
      await msg.edit(embed = tmp)
      if(pastrank == None or len(pastrank)==0): tmp=discord.Embed(title="None")
      else:
        tmp=discord.Embed(title="Final Standing")
        ma = len(pastrank)
        if(ma > 20): ma = 20
        for i in range(ma):
          tmp.add_field(name=str(i+1)+". "+pastrank[i][0], value="Score: "+str(pastrank[i][1]), inline=False)  
      msg = await cha.fetch_message(my_ch_3)
      await msg.edit(embed = tmp)
      await ctx.channel.send(embed = discord.Embed(title=name,description="Updated on channel ccp-match successfully."))
    except:
      await ctx.channel.send(embed = discord.Embed(title=name,description="Your query failed."))
#######################################################
@client.command()
async def my_account(ctx):
  tmp=discord.Embed(title="User profile")
  tmp.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  if(db['user_account'].get(str(ctx.author.id))==None):
    tmp.add_field(name="This user hasn't competed in a rated match yet.",value = "Join rated matches to gain rating", inline=False)
    await ctx.send(embed = tmp)
    return
  tot = db['ccprating'][str(ctx.author.id)].get('count')
  if(tot == None):
    tmp.add_field(name="This user hasn't competed in a rated match yet.",value = "Join rated matches to gain rating")
    await ctx.send(embed = tmp)
    return
  col = discord.Color.light_gray()
  now = int(db['ccprating'][str(ctx.author.id)]['rating'])
  if (now >= 1200):
    col = discord.Color.green()
  if (now >= 1400):
    col = discord.Color.teal()
  if (now >= 1600):
    col = discord.Color.blue()
  if (now >= 1900):
    col = discord.Color.purple()
  if (now >= 2100):
    col = discord.Color.gold()
  if (now >= 2400):
    col = discord.Color.dark_red()
  tmp=discord.Embed(title="User profile",color = col)
  tmp.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  tmp.set_footer(text="beta test v.1.5")
  tmp.add_field(name="Total Competed",value=str(tot), inline=False)
  xp = db['ccprating'][str(ctx.author.id)]['perf']
  xr = db['ccprating'][str(ctx.author.id)]['rating_change']
  dr = xr[len(xr)-1]-xr[len(xr)-2]
  sdr ="("
  if(dr > 0):
    sdr += "+"
  sdr += str(dr)
  sdr += ")"
  tmp.add_field(name="Last Match Performance",value=str(xp[len(xp)-1])+" "+sdr, inline=False)
  tmp.add_field(name="Current Rating",value=str(db['ccprating'][str(ctx.author.id)]['rating']), inline=False)
  mux = 0
  for i in db['ccprating'][str(ctx.author.id)]['rating_change']:
    if(int(i) > mux): mux = int(i)
  tmp.add_field(name="Max Rating",value=str(mux))
  await ctx.send(embed = tmp)
    
#########################################################
@client.event
async def update_status():
    global name, channel, clock, ok, score, aced, host, r_time, user, user_name, user_id, user_score, prob, prob2, db, chl, ac, type, solve_count, my_ch, my_ch_1, my_ch_2, my_ch_3, user_final_time, fastest, bot_talk
    cha = client.get_channel(chl)
    try:     
      if(type == 1):
        for i in range(len(user_id)):
          for j in range(len(prob)):
            if(ac[i][j] == True): #reset
              user_score[i]-=math.ceil(score[j]/solve_count[j])
      fastest=[]
      for i in range (len(prob)):
        fastest.append(["None",10000000000])
      exit_code = await get_new_status() 
      print(fastest)
      for i in range (len(prob)):        
         if(aced[i]=="0" and fastest[i][0]!="None"):
           aced[i]=fastest[i][0]
           for j in range(len(user_id)):
              if(fastest[i][0] == user_id[j]):
                if(type == 0):
                  user_score[j] += score[i]
                if(type == 1):
                  user_score[j] += math.ceil(score[i]/10)
      tmp=discord.Embed(title=name)
      if(exit_code == 0):
        tmp.add_field(name="CCP Match # "+str(db['contest_count']), value="Host by "+host, inline=False)
      else:
        tmp.add_field(name="CCP Match # "+str(db['contest_count']), value="Warning: Update failed.", inline=False)
      for i in range(len(prob)):
        ur="https://codeforces.com/problemset/problem/"+str(prob[i])+"/"+str(prob2[i])
        if(aced[i]=="0"):
          tmp.add_field(name="Question # "+str(i+1)+" : "+str(prob[i])+" "+str(prob2[i]), value="[Score: "+str(score[i])+"]("+ur+")", inline=False)
        else:
          if(type == 0): #first one get
            tmp.add_field(name="Question # "+str(i+1)+" : "+str(prob[i])+" "+str(prob2[i]), value="Score: "+str(score[i])+", solved by "+aced[i], inline=False)
          if(type == 1): #divide
            tmp.add_field(name="Question # "+str(i+1)+" : "+str(prob[i])+" "+str(prob2[i]), value="[Score: "+str(int(math.ceil(score[i]/(solve_count[i]+1))))+"(AC x "+str(solve_count[i])+")]("+ur+")", inline=False)
          if(type == 2): #atcoder
            tmp.add_field(name="Question # "+str(i+1)+" : "+str(prob[i])+" "+str(prob2[i]), value="[Score: "+str(score[i])+"(AC x "+str(solve_count[i])+")]("+ur+")", inline=False)
          
      #977522316177203240
      cha = client.get_channel(my_ch)
      msg = await cha.fetch_message(my_ch_2)
      print("test")
      await msg.edit(embed = tmp)
      msg = await cha.fetch_message(my_ch_3)
      if(type == 1):
        for i in range(len(user)):
          for j in range(len(prob)):
            if(ac[i][j] == True):
              user_score[i]+=math.ceil(score[j]/solve_count[j])
      if(len(user_name)==0):rank=discord.Embed(title="None")
      else:
        fin = []
        for i in range(len(user)):
          ac_str=""
          for j in range(len(prob)):
            if(ac[i][j]):
              ac_str+=":white_check_mark: "
            else:
              ac_str+=":black_large_square: "
          pi = [user_name[i],user_score[i],ac_str,-user_final_time[i]]
          fin.append(pi)   
        fin.sort(key = lambda x:(x[1],x[3]), reverse=True)
        rank=discord.Embed(title="Standing")
        ma = len(user)
        if(ma > 20):ma = 20
        for i in range(ma):
          rank.add_field(name=str(i+1)+". "+fin[i][0], value="Score: "+str(fin[i][1])+"\n"+fin[i][2], inline=False)
      await msg.edit(embed = rank)
    except:
      if(type == 1): #undone
        for i in range(len(user)):
          for j in range(len(prob)):
            if(ac[i][j] == True):
              user_score[i]+=math.ceil(score[j]/solve_count[j])
##########################################################      
@client.event
async def get_new_status():
  global score, aced, r_time, user, user_name, user_id,user_score, prob, prob2, db, chl, ac, type, solve_count , user_final_time, fastest
  try:
    for u in range(len(user_name)):
      r = requests.get("https://codeforces.com/api/user.status?handle="+db['user_account'][user_id[u]][0]+"&from=1&count=12", timeout=5)
      data=json.loads(r.text)
      if(data['status']!="OK"):
        print("failed on updating")
        continue
      ma=len(data['result'])
      if(ma>10):
        ma=10
      for i in range(0,ma):
          for j in range (len(prob)):
              if(ac[u][j] == False  and 
              data['result'][i]['verdict'] == "OK" 
              and str(data['result'][i]['problem']['contestId'])==str(prob[j]) 
              and str(data['result'][i]['problem']['index'])==str(prob2[j]) ):
                ac[u][j]=True
                if(type == 0 and aced[j]!="0"):
                  continue
                if(user_final_time[u]<int(data['result'][i]['creationTimeSeconds'])):
                  user_final_time[u]=int(data['result'][i]['creationTimeSeconds'])
                  
                solve_count[j]+=1 
                if(type == 2):
                  user_score[u] += score[j]
                if(int(data['result'][i]['creationTimeSeconds']) < fastest[j][1]):
                  fastest[j] = [user_id[u],int(data['result'][i]['creationTimeSeconds'])]
    return 0
  except:
    print("update failed")
    return 1 #err
#########################################################           
@client.event
async def find_problem(diff,x,cost):
    global prob, prob2,  score, aced, solve_count
    try:
      probs = get_problem(diff)
      if(probs == None):
          return 102
      if(x>len(probs)):
          return 101  
      arr = []
      cnt = 0
      while(len(arr) != x):
        cnt += 1
        i = random.randint(0,len(probs)-1)       
        if(i not in arr):
          arr.append(i)
          s1 = probs[i][0]
          s2 = probs[i][1]
          prob.append(s1)
          prob2.append(s2)
          score.append(cost)
          aced.append("0")
        if(cnt >= 100):return 106
      return 0
    except:
      return 100
###########################################
@client.event
async def update_rating(fin):
  all_rating = []
  seed = []
  #fin i 2
  for i in range(len(fin)):
    if(db['ccprating'][str(fin[i][2])].get('perf')==None):
      db['ccprating'][str(fin[i][2])]['perf'] = []
      db['ccprating'][str(fin[i][2])]['rating'] = 0
      db['ccprating'][str(fin[i][2])]['rating_change'] = [0]
      db['ccprating'][str(fin[i][2])]['count'] = 1
      all_rating.append(500)
    else:
      db['ccprating'][str(fin[i][2])]['count'] += 1
      all_rating.append(db['ccprating'][str(fin[i][2])]['rating'])
  for i in range(len(fin)): 
    seed.append(1)
    for j in range(len(fin)):
        if(j == i):continue
        seed[i] += 1/(1+math.pow(10,(all_rating[i]-all_rating[j])/400))
  for i in range(len(fin)): 
    l = 0
    r = 10000
    cnt = 0
    m = math.sqrt((i+1)*seed[i])
    print(m)
    while(r > l and cnt < 64):
      cnt += 1
      n_seed = 1
      mid = (l+r)/2
      for j in range(len(fin)):
        if(j == i):continue
        n_seed += 1/(1+math.pow(10,(mid-all_rating[j])/400))
      if(n_seed > m):l = mid
      if(n_seed < m):r = mid
    new_per = int(math.ceil((l+r)/2))
    db['ccprating'][str(fin[i][2])]['perf'] .append(new_per)
    c_rating = db['ccprating'][str(fin[i][2])]['rating']
    delta = new_per - c_rating 
    if(delta < 0):
      c_rating += (int)(delta/(2-delta/300))
    else:
      c_rating += (int)(delta/2)
    delta = new_per - c_rating 
    if(db['ccprating'][str(fin[i][2])]['count'] == 1):
      c_rating += 600
    if(db['ccprating'][str(fin[i][2])]['count'] == 2):
      c_rating += 300
    if(db['ccprating'][str(fin[i][2])]['count'] == 3):
      c_rating += 150
    if(db['ccprating'][str(fin[i][2])]['count'] == 4):
      c_rating += 100
    if(db['ccprating'][str(fin[i][2])]['count'] == 5):
      c_rating += 50
    db['ccprating'][str(fin[i][2])]['rating'] = c_rating
    db['ccprating'][str(fin[i][2])]['rating_change'].append(c_rating)
####################################################
@client.command()
async def update_problem(ctx):
    global ok
    if(ok == 3):
      await ctx.channel.send(embed = discord.Embed(title=name,description="You can't do this command during contest."))
      return
    try:
      r=requests.get("https://codeforces.com/api/problemset.problems",timeout=10)
      data=json.loads(r.text)
      leng=len(data['result']['problems'])
      
      for i in range(leng):
        ok = True
        a = int(data['result']['problems'][i]['contestId'])
        b = data['result']['problems'][i]['index']  
        r = data['result']['problems'][i].get('rating')
        t = data['result']['problems'][i].get('tags')
        if(a <= db['problem_now']):break
        if(t == None or r == None):
          continue
        for j in t:
          if(j.strip() == "*special" or j.strip() == "*special problem" ):
            ok = False
        if(ok == True):
          db['problem'][str(r)].append([a,b,t])
          print(str(a)+b)
      db['problem_now'] = int(data['result']['problems'][0]['contestId'])
      await ctx.channel.send(embed = discord.Embed(title=name, description="Problems have been updated."))
      return
    except:
      await ctx.channel.send(embed = discord.Embed(title=name, description="Updated problems failed..."))
      return
####################################################
@client.command()
async def orz(ctx):
   await ctx.channel.send(embed = discord.Embed(title=ctx.author.name+" orz"))

@client.command()
async def sendhehe(ctx,*str):
   cha = client.get_channel(940128222182514709)
   out = ""
   print(len(str))
   print(str[0])
   for i in range(0,len(str)):
     out += str[i] + " "
   await cha.send(out)

@client.command()
async def senddata(ctx):
  cha = client.get_channel(bot_talk)
  await cha.send("```count: "+str(db['contest_count'])+"```")
  time.sleep(0.1)
  for i in db['ccprating']:
    await cha.send("```ccprating: "+str(i)+":"+str(db['ccprating'][str(i)])+"```")
    time.sleep(0.1)
  for i in db['user_account']:
    await cha.send("```user_account: "+str(i)+":"+str(db['user_account'][str(i)])+"```")
    time.sleep(0.1)
  
@client.event
async def on_ready():
    global st
    game = discord.Game(st)
    await client.change_presence(status=discord.Status.online, activity=game) 
  
keep_alive()
try:
  client.run(db['token'])
except:
  os.system("kill 1")

