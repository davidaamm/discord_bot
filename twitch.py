import requests
import os 
import json
from datetime import datetime 

with open("config.json") as config_file:
  config=json.load(config_file)

def get_app_acess_token():
  params={
    "client_id":os.environ['CLIENT_ID'],
    "client_secret":os.environ['CLIENT_SECRET'],
    "grant_type":"client_credentials"
  }

  r=requests.post("https://id.twitch.tv/oauth2/token",params=params)
  access_token=r.json()['access_token']
  print(access_token)
    
  return access_token

def get_users(login_names):
  params={
    "login":login_names
  }

  headers={
    "Authorization": "Bearer {}".format(os.environ['ACCESS_TOKEN']),
    "Client-Id": os.environ['CLIENT_ID']
  }

  r=requests.get("https://api.twitch.tv/helix/users",params=params, headers=headers)

  return {entry["login"]:entry["id"] for entry in r.json()["data"]}

def get_streams(users):
  params = {
    "user_id":users.values()
  }

  headers={
    "Authorization": "Bearer {}".format(os.environ['ACCESS_TOKEN']),
    "Client-Id": os.environ['CLIENT_ID']
  }

  r=requests.get("https://api.twitch.tv/helix/streams",params=params, headers=headers)
  return {entry["user_login"]: entry for entry in r.json()["data"]}


online_users={}

def get_notifications():
  with open("config.json") as config_file:
    config=json.load(config_file)

  users=get_users(config["watchlist"])
  streams=get_streams(users)
  for stream in streams:
    params = {
      "user_id":users.values()
    }

    headers={
      "Authorization": "Bearer {}".format(os.environ['ACCESS_TOKEN']),
      "Client-Id": os.environ['CLIENT_ID']
    }

    rfoto=requests.get(("https://api.twitch.tv/helix/users?login="+streams[stream]['user_login']),params=params, headers=headers)
    foto=rfoto.json()['data'][0]['profile_image_url']
    streams[stream]['foto_perfil']=foto

    params = {
      "id":streams[stream]['game_id']
    }

    headers={
      "Authorization": "Bearer {}".format(os.environ['ACCESS_TOKEN']),
      "Client-Id": os.environ['CLIENT_ID']
    }

    rgame=requests.get("https://api.twitch.tv/helix/games",params=params, headers=headers)
    gamefoto=rgame.json()['data'][0]['box_art_url']
    g_foto=gamefoto.replace("{width}","60")
    game_foto=g_foto.replace("{height}","85")
    streams[stream]['foto_juego']=game_foto

  notifications=[]

  for user_name in config["watchlist"]:
    if user_name not in online_users:
      online_users[user_name] = datetime.utcnow()
      
    if user_name not in streams:
      online_users[user_name]= None
    else:
      started_at = datetime.strptime(streams[user_name]["started_at"], "%Y-%m-%dT%H:%M:%SZ")
      if online_users[user_name]is None or started_at > online_users[user_name]:
        notifications.append(streams[user_name])
        online_users[user_name]=started_at

  return notifications
