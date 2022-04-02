import discord
from discord import errors, File, Message, Embed, TextChannel
from discord.ext.tasks import loop
from discord.ext import commands
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from PIL import Image, ImageDraw, ImageFont
import io
from twitch import get_notifications
import random
import requests 
from datetime import datetime, date
from users import db 

client = commands.Bot(command_prefix='!')
client.remove_command("help")

with open("config.json") as config_file:
  config=json.load(config_file)

with open("strimers.json") as strimers_file:
  strimers=json.load(strimers_file)

@client.event
async def on_ready():
  print('Chismestrum sta en linea')
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sus caritas preciosas"))

@client.command()
async def rank(ctx):
  content = ctx.message.content
  split=content.split()
  words=len(split)
  if words == 1:
    uid = ctx.author.id
    uuid=str(uid)
    plataforma=db[uuid][2]
    usuario=db[uuid][3]
  else:
    plataforma=split[1]
    usuario=split[2]

  chrome_options = Options()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.headless = True
  #chrome_options.add_argument('window-size=1400,600')
  #chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
  #chrome_options.add_experimental_option('useAutomationExtension', False)  
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
  driver.get("https://api.tracker.gg/api/v2/rocket-league/standard/profile/"+plataforma+"/"+usuario+"/")



  try:
    html = driver.page_source
    print(html)
  except:
    print('Nomás no jala esta wea')

  data = json.loads(pre)
  try:
    ini = data['data']['segments']
    s = len(ini)
    index = list(range(1, s))
    l=[]
    rewardlvl=ini[0]['stats']['seasonRewardLevel']['metadata']['rankName']
    #listas competitive
    for i in index:
      playlist = ini[i]['metadata']['name']
      tier = ini[i]['stats']['tier']['metadata']['name']
      division = ini[i]['stats']['division']['metadata']['name']
      divsplit=division.split()
      divnum=divsplit[1]
      matchesplayed = ini[i]['stats']['matchesPlayed']['displayValue']
      mmr=ini[i]['stats']['rating']['displayValue']
      mpint = int(matchesplayed)
      winstreak=ini[i]['stats']['winStreak']['displayValue']
      if (playlist == 'Ranked Duel 1v1') or (playlist == 'Ranked Doubles 2v2') or (playlist == 'Ranked Standard 3v3') or (playlist== 'Tournament Matches'):

        if playlist == 'Tournament Matches':
                #print(playlist + " - " + tier + " - " + division + " - " + matchesplayed)
          l.append([playlist,tier,division,(division[0:3]+". "+divnum) ,matchesplayed,mmr,winstreak])
        else:
          if mpint < 10:
            #print(playlist + " - Unranked - " + matchesplayed + "/10")
            l.append([playlist,"Unranked","","",matchesplayed,mmr,winstreak])
          else:
            # print(playlist + " - " + tier + " - " + division + " - " + matchesplayed)
            l.append([playlist,tier,division,(division[0:3]+". "+divnum),matchesplayed,mmr,winstreak])
      else:
        pass
    
  except:
    print('Usuario no encontrado')


  rimgs={
    'Supersonic Legend' : 'img/s15rank22.png',
    'Grand Champion III' : 'img/s15rank21.png',
    'Grand Champion II' : 'img/s15rank20.png',
    'Grand Champion I' : 'img/s15rank19.png',
    'Champion III' : 'img/s4-18.png',
    'Champion II' : 'img/s4-17.png',
    'Champion I' : 'img/s4-16.png',
    'Diamond III' : 'img/s4-15.png',
    'Diamond II' : 'img/s4-14.png',
    'Diamond I' : 'img/s4-13.png',
    'Platinum III' : 'img/s4-12.png',
    'Platinum II' : 'img/s4-11.png',
    'Platinum I' : 'img/s4-10.png',
    'Gold III' : 'img/s4-9.png',
    'Gold II' : 'img/s4-8.png',
    'Gold I' : 'img/s4-7.png',
    'Silver III' : 'img/s4-6.png',
    'Silver II' : 'img/s4-5.png',
    'Silver I' : 'img/s4-4.png',
    'Bronze III' : 'img/s4-3.png',
    'Bronze II' : 'img/s4-2.png',
    'Bronze I' : 'img/s4-1.png',
    'Unranked' : 'img/s4-0.png'}
  rwimgs={
    'None':'img/s4-0.png',
    'Bronze': 'img/swbronze.png',
    'Silver': 'img/swsilver.png',
    'Gold': 'img/swgold.png',
    'Platinum': 'img/swplatinum.png',
    'Diamond': 'img/swdiamond.png',
    'Champion': 'img/swchampion.png',
    'Grand Champion': 'img/swgrand_champion.png',
    'Supersonic Legend': 'img/swsslegend.png'}

  f=len(l)        
  x=4-(f)
  if x>0:
    a=range(0, x)
    for i in a:
      l.append(["a","b","c","d"])
  else:
    pass
    
  r=["Ranked Duel 1v1","Ranked Doubles 2v2","Ranked Standard 3v3","Tournament Matches"]
# -------- CABECERA ------- 

  listname=(["DUEL","DOUBLES","STANDARD","TOURNAMENT"])

  j=0
  k=range(0,4)
  m=[]
  for g in k:
    i1=r[g]
    i2=l[j][0]
    if i1 == i2:
      m.append([listname[g],rimgs[l[j][1]],l[j][5],l[j][6],l[j][4],l[j][3]])
      j=j+1
    else:
      m.append([listname[g],rimgs['Unranked'],"0","0","0",""])
      j=j

  image = Image.new(mode = "RGB", size = (800, 450),color = (44, 37, 89))
  section = Image.new(mode="RGB", size = (384, 156),color = (71, 39, 140))
  image.paste(section,(10,115))
  image.paste(section,(10,284))
  image.paste(section,(406,115))
  image.paste(section,(406,284))
  font = ImageFont.truetype("fonts/Poppins-Bold.ttf", 20)
  fontd = ImageFont.truetype("fonts/Poppins-Regular.ttf", 20)    
  fontde = ImageFont.truetype("fonts/Poppins-Regular.ttf", 23)
  I1 = ImageDraw.Draw(image)
    

# -------- CABECERA ------- 

  I1.text((35, 23), "PLAYER NAME", font=font, fill=(240, 133, 242))
  rwtrl = Image.open(rwimgs[rewardlvl])
  rwrl=rwtrl.resize((60,60))
  image.paste(rwrl, (717,30), mask=rwrl)
  nombredeusuario=data['data']['platformInfo']['platformUserHandle']
  I1.text((35, 60), nombredeusuario, font=fontd, fill=(240, 133, 242))
  I1.text((513, 23), "REWARD LEVEL", font=font, fill=(240, 133, 242))
  rewardlevel=rewardlvl
  I1.text(((513), 59), rewardlevel, font=fontd, fill=(240, 133, 242))

# -------- STANDARD ------- 

  I1.text((35, 130), m[2][0], font=font, fill=(22, 242, 180))
  stdrank = Image.open(m[2][1])
  sttr=stdrank.resize((94,94))
  image.paste(sttr, (281,137), mask=sttr)
  I1.text((35, 165), m[2][2]+" MMR", font=fontde, fill=(22, 242, 180))
  I1.text((35, 189), "Streak · "+m[2][3], font=fontd, fill=(22, 242, 180))
  I1.text((301, 231),m[2][5], font=fontd, fill=(22,242, 180))
  I1.text((35, 231), "Games Played · " + m[2][4], font=fontd, fill=(22, 242, 180))

# -------- DUEL ------- 

  I1.text((35, 299), m[0][0], font=font, fill=(22, 242, 180))
  dldrank = Image.open(m[0][1])
  dltr=dldrank.resize((94,94))
  image.paste(dltr, (281,304), mask=dltr)
  I1.text((35, 334), m[0][2]+" MMR", font=fontde, fill=(22, 242, 180))
  I1.text((35, 358), "Streak · "+m[0][3], font=fontd, fill=(22, 242, 180))
  I1.text((301, 400), m[0][5], font=fontd, fill=(22, 242, 180))
  I1.text((35, 400), "Games Played · " + m[0][4], font=fontd, fill=(22, 242, 180))

# -------- DOUBLES ------- 

  I1.text((431, 130), m[1][0], font=font, fill=(22, 242, 180))
  doudrank = Image.open(m[1][1])
  doutr=doudrank.resize((94,94))
  image.paste(doutr, (676,137), mask=doutr)
  I1.text((431, 165), m[1][2]+" MMR", font=fontde, fill=(22, 242, 180))
  I1.text((431, 189), "Streak · "+m[1][3], font=fontd, fill=(22, 242, 180))
  I1.text((697, 231), m[1][5], font=fontd, fill=(22, 242, 180))
  I1.text((431, 231), "Games Played · " + m[0][4], font=fontd, fill=(22, 242, 180))

# -------- TOURNAMENT ------- 

  I1.text((431, 299), m[3][0], font=font, fill=(22, 242, 180))
  tourrank = Image.open(m[3][1])
  tourtr=tourrank.resize((94,94))
  image.paste(tourtr, (676,304), mask=tourtr)
  I1.text((431, 334), m[3][2]+" MMR", font=fontde, fill=(22, 242, 180))
  I1.text((431, 358), "Streak · "+m[3][3], font=fontd, fill=(22, 242, 180))
  I1.text((697, 400), m[3][5], font=fontd, fill=(22, 242, 180))
  I1.text((431, 400), "Games Played · " + m[3][4], font=fontd, fill=(22, 242, 180))


  with io.BytesIO() as image_binary:
    image.save(image_binary, 'PNG')
    image_binary.seek(0)
    await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))  
    driver.close()

# FIN  DE RANKS ROCKET LEAGUE 

@loop(seconds=60)
async def check_twitch_online_streamers():
  chnl = client.get_channel(892472599228084315)
  notifi=[]
  if not chnl:
    return
  

  with open("config.json") as config_file:
    config=json.load(config_file)


  notifications = get_notifications()
  with open("strimers.json") as strimers_file:
    strimers=json.load(strimers_file)

  for notification in notifications:
    embed=discord.Embed(url="https://www.twitch.tv/{}".format(notification["user_login"]),title=notification["title"],description="{} sta enbibo en Tuich".format(notification["user_login"]), color=discord.Colour.from_rgb(204, 152, 197))
    imgstrim=notification["thumbnail_url"]
    img_strim=imgstrim.replace("{width}","400")
    imagenstrim=img_strim.replace("{height}","225")
    embed.set_image(url=imagenstrim)
    embed.add_field(name="Playing",value=notification["game_name"], inline=True)
    embed.set_thumbnail(url=notification["foto_juego"])
    embed.set_footer(icon_url="https://www.iconheaven.com/download/63/png/twitch_logo_png512.png", text="El Tuich")
    embed.set_author(icon_url=notification["foto_perfil"],name=notification["user_login"])
    
    if notification["user_login"] in strimers:
      cuantos=len(strimers[notification["user_login"]])
      if cuantos == 0:
        pass
      else:
        rango=range(0,cuantos)
        for i in rango:
          b=strimers[notification["user_login"]][i]
          ba=str(b)
          a="<@!"+ba+">"
          notifi.append(a)
        final=" ".join(notifi)
        await chnl.send(final+" - {} inicio strim :  https://www.twitch.tv/{}".format(notification["user_login"],notification["user_login"]),embed=embed)
      
    else:   
      await chnl.send("@everyone - {} inicio strim :  https://www.twitch.tv/{}".format(notification["user_login"],notification["user_login"]),embed=embed)
      
if __name__ == "__main__":
  check_twitch_online_streamers.start()
  

@client.command()
async def kiss(ctx,member: discord.Member):
  apikey = "LIVDSRZULELA"  # test value
  lmt = 250

  # our test search
  search_term = "anime kiss gif"
  pos = '0'
  pos2 = '50'
  pos3 = '100'

  # get the top 8 GIFs for the search term
  r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos))
  r2 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos2))
  r3 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos3))

  if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    busqueda = json.loads(r.text)
    busqueda2 = json.loads(r2.text)
    busqueda3 = json.loads(r3.text)
    ds = [busqueda, busqueda2, busqueda3]
    d = {}
    for k in busqueda.keys():
      d[k] = tuple(d[k] for d in ds)
    indice=random.randint(0, 2)
    numero=random.randint(0, 49)
    gif=d['results'][indice][numero]['media'][0]['gif']['url']

  else:
    busqueda = None
  
  embed=discord.Embed(description=ctx.author.mention + " le ha dado besito a "+ member.mention, color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)

@client.command()
async def hug(ctx,member: discord.Member):
  apikey = "LIVDSRZULELA"  # test value
  lmt = 250

  # our test search
  search_term = "anime hug gif"
  pos = '0'
  pos2 = '50'
  pos3 = '100'

  # get the top 8 GIFs for the search term
  r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos))
  r2 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos2))
  r3 = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, apikey, lmt, pos3))

  if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    busqueda = json.loads(r.text)
    busqueda2 = json.loads(r2.text)
    busqueda3 = json.loads(r3.text)
    ds = [busqueda, busqueda2, busqueda3]
    d = {}
    for k in busqueda.keys():
      d[k] = tuple(d[k] for d in ds)
    indice=random.randint(0, 2)
    numero=random.randint(0, 49)
    gif=d['results'][indice][numero]['media'][0]['gif']['url']

  else:
    busqueda = None
  
  embed=discord.Embed(description=ctx.author.mention + " le ha dado abracito a "+ member.mention, color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)

@client.command()
async def cat(ctx):
  r = requests.get("https://api.thecatapi.com/v1/images/search")

  if r.status_code == 200:
    busqueda = json.loads(r.content)
    gif=busqueda[0]['url']
  else:
    busqueda = None

  embed=discord.Embed(color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)
  
@client.command()
async def dog(ctx):
  r = requests.get("https://api.thedogapi.com/v1/images/search")

  if r.status_code == 200:
    busqueda = json.loads(r.content)
    gif=busqueda[0]['url']
  else:
    busqueda = None

  embed=discord.Embed(color=discord.Colour.from_rgb(204, 152, 197))
  embed.set_image(url=gif)
  await ctx.send(embed=embed)

@client.command()
async def sub(ctx):
  add = ctx.message.content
  split=add.split()
  words=len(split)
  if words == 2:
    
   texto=split[1]
   if texto == 'add':
    uid = ctx.author.id
    uuid=str(uid)
    if uuid == "727384087714857050":
      await ctx.send("Naambre " + ctx.author.mention + " tu no te puedes regalar subs")
    else:
      now = datetime.now()
      timestamp =datetime.timestamp(now)
      db[uuid][1]=timestamp
      await ctx.send(ctx.author.mention + " agregaste una sub regalada por <@!727384087714857050> ")
  elif words == 1:
    uid = ctx.author.id
    uuid=str(uid)
    if uuid == "727384087714857050":
      await ctx.send("Naambre " + ctx.author.mention + " tu no te puedes regalar subs")
    else:
      fechag=db[uuid][1]
      if fechag == "":
        await ctx.send(ctx.author.mention + " <@!727384087714857050> no te ha regalado ninguna sub")
      else:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        fechaok = float(fechag)
        min = fechaok           #removing milli seconds
        max = timestamp
        min = datetime.fromtimestamp(min)
        max = datetime.fromtimestamp(max)
        diferencia=str((max-min).days)
        await ctx.send(ctx.author.mention + " han pasado " +diferencia+" días sin que <@!727384087714857050> te regale una sub")

@client.command()
async def strimer(ctx):
  with open("config.json") as config_file:
    config=json.load(config_file)

  with open("strimers.json") as strimers_file:
    strimers=json.load(strimers_file)
    
  add=ctx.message.content
  split=add.split()
  func=split[1]
  try:
      strimer=split[2].lower()
  except IndexError:
      strimer=""    

  userid=ctx.author.id
  test = config['watchlist']
  if (strimer == 'hpavel82') or (strimer == 'sicaac') or (strimer == 'marf0n') or (strimer == 'tiranodiego') or (strimer == 'deividaam'):
    await ctx.send(ctx.author.mention + "el papucho que intentas agregar ya esta en la lista general")
  else:
    if func == 'add':
      if strimer in strimers:
        if userid in strimers[strimer]:
          await ctx.send(ctx.author.mention + " ya habias registrao a este usario en tus notificaciones")
        else:
          strimers[strimer].append(userid)
          nstrimer=strimers
          with open("strimers.json", "w") as strimers_file:
            json.dump(nstrimer, strimers_file)
          await ctx.send(ctx.author.mention + " searegistrao a "+strimer+ " en tus notificaciones")
      else:
        strimers[strimer]=[userid]
        nstrimer=strimers
        with open("strimers.json", "w") as strimers_file:
          json.dump(nstrimer, strimers_file)

        await ctx.send(ctx.author.mention + " searegistrao a  "+strimer+ " en tus notificaciones")
      
    elif func == 'del':
      if strimer in strimers:
        if userid in strimers[strimer]:
          strimers[strimer].remove(userid)
          with open("strimers.json", "w") as strimers_file:
            json.dump(strimers, strimers_file)

          await ctx.send(ctx.author.mention + " eliminaste a "+strimer+ " de tus notificaciones")

        else:
          await ctx.send(ctx.author.mention + strimer + " no esta registrao en tus notificaciones")
      else:
        await ctx.send(ctx.author.mention + " este strimer no esta registrao en la lista de notificaciones")
    elif func == 'list':
      embed=discord.Embed(title="Strimers registrados",description=ctx.author.mention + ' acá esta tu lista: ',color=discord.Colour.from_rgb(204, 152, 197))
      key_list = list(strimers.keys())
      val_list = list(strimers.values())
      list_strimers=[]
      for i in range(0,len(key_list)):
        valor = val_list[i]
        if userid in valor:
          strimer = key_list[i]
          list_strimers.append(strimer)
      cantstrimers=len(list_strimers)
      if cantstrimers == 0:
        await ctx.author.send('No tienes strimers registrados')
      else:
        lista_final = ' | '.join(list_strimers)
        embed.add_field(name = chr(173), value=lista_final, inline=False)
        await ctx.author.send(embed=embed)

  if strimer in test:
    pass
  else:
    if strimer == "":
      pass
    else:
      test.append(strimer)
      nuevo={'watchlist':test}
      with open("config.json", "w") as config_file:
        json.dump(nuevo, config_file)




@client.command()
async def help(ctx):
  embed=discord.Embed(title="Comandos de Chismestrum",description="aca sta la lista",color=discord.Colour.from_rgb(204, 152, 197))
  embed.add_field(name="Rocket League", value="Comandos de rokelij",inline=False)
  embed.add_field(name="!rank",value="Muestra tus rangos en listas competitvas de rokelij, si quieren ver el rango de otro usuario escriban: __**!rank plataforma usuario**__ , ejemplo de comando: __**!rank epic chismestrum**__", inline=False)
  
  embed.add_field(name="Twitch", value="Comandos de tuich",inline=False)
  embed.add_field(name="!strimer add usuario",value="Agrega al usuario de tuich a tus notificaciones, ejemplo de comando: __**!strimer add chismestrum**__", inline=True)
  embed.add_field(name="!strimer del usuario",value="Elimina al usuario de tuich de tus notificaciones, ejemplo de comando: __**!strimer del chismestrum**__", inline=True)
  embed.add_field(name="!strimer list",value="Para ver la lista de strimers que has puesto en tus notificaciones", inline=True)

  embed.add_field(name="Amorts", value="Comandos de besitos, abracitos, gatitos y perritos ",inline=False)
  embed.add_field(name="!kiss",value="Manda un gif random de besito a la persona que quieras, ejemplo de comando: __**!kiss @chismestrum**__", inline=True)
  embed.add_field(name="!hug",value="Manda un gif random de abracito a la persona que quieras, ejemplo de comando: __**!hug @chismestrum**__", inline=True)
  embed.add_field(name="!dog o !cat",value="Muestra una imagen random de perrito o de gatito", inline=True)

  embed.add_field(name="!sub", value="Comando para saber cuantos días han pasado desde que sicaac te ha regalado una sub, para agregar la fecha en la que sicaac te regale una sub utiliza el comando __**!sub add**__",inline=False)

  await ctx.author.send(embed=embed)

client.run(os.environ['TOKEN'])

