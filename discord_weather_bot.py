import discord
import asyncio
import requests
import json
from time import sleep

f = open("config.json", encoding='utf-8')
config = json.load(f)
f.close()

f = open("weathercode.json", encoding='utf-8')
weathercode = json.load(f)
f.close()

token = config["discord"]["token"]
yahoo_appid = config["yahoo"]["appid"]
weather_key = config["openweathermap"]["key"]

client = discord.Client()

def get_Weather(lot,lat): 
    appid = weather_key
    output = "json"
    url = "http://api.openweathermap.org/data/2.5/weather?"
    url += "APPID=" + appid
    url += "&lat=" + lat
    url += "&lon=" + lot
    url += "&units=" + "metric" 
    r = requests.get(url)
    res = r.json()
    return res

def get_Coordinates(location_name):
    appid = yahoo_appid
    output = "json"
    query = location_name
    url = "https://map.yahooapis.jp/geocode/V1/geoCoder?"
    url += "appid=" + appid
    url += "&output=" + output
    url += "&query=" + query
    r = requests.get(url)
    res = r.json()
    return res["Feature"][0]["Geometry"]["Coordinates"]

def get_Weather_info(location_name):
    reslist = get_Coordinates(location_name).split(",")
    weather = get_Weather(reslist[0],reslist[1])
    em = discord.Embed(colour=0x3498db)
    em.add_field(name="天気", value=weathercode[str(weather["weather"][0]["id"])], inline=True)
    em.add_field(name="気温", value=str(int(weather["main"]["temp"]))+'°C', inline=True)
    em.add_field(name="湿度", value=str(weather["main"]["humidity"])+'％', inline=True)
    em.add_field(name="風速", value=str(weather["wind"]["speed"])+'m', inline=True)
    em.set_author(
        name=location_name+'の気象情報', 
        icon_url='https://upload.wikimedia.org/wikipedia/commons/1/15/OpenWeatherMap_logo.png'
        )
    em.set_thumbnail(url='http://openweathermap.org/img/w/' + weather["weather"][0]["icon"].replace('n', 'd') +'.png')
    return em

@client.event
async def on_ready():
    print('Login as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    messagelist = message.content.split()
    if len(messagelist) >= 2:
        if messagelist[0] == "天気":
            location_name = messagelist[1]
            em = get_Weather_info(location_name)
            return await message.channel.send(message.channel,embed=em)

        if messagelist[1] == "天気":
            location_name = messagelist[0]
            em = get_Weather_info(location_name)
            return await message.channel.send(message.channel,embed=em)


if __name__ == "__main__":
    client.run(token)
