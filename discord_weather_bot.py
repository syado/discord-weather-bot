import discord
import asyncio
import requests
import json
from time import sleep

weathercode = {
    "200": "小雨と雷雨",
    "201": "雨と雷雨",
    "202": "大雨と雷雨",
    "210": "光雷雨",
    "211": "雷雨",
    "212": "重い雷雨",
    "221": "ぼろぼろの雷雨",
    "230": "小雨と雷雨",
    "231": "霧雨と雷雨",
    "232": "重い霧雨と雷雨",
    "300": "中くらいの霧雨",
    "301": "霧雨",
    "302": "重い強度霧雨",
    "310": "中くらいの霧雨の雨",
    "311": "霧雨の雨",
    "312": "重い強度霧雨の雨",
    "313": "にわか雨と霧雨",
    "314": "重いにわか雨と霧雨",
    "321": "にわか霧雨",
    "500": "小雨",
    "501": "適度な雨",
    "502": "重い強度の雨",
    "503": "非常に激しい雨",
    "504": "極端な雨",
    "511": "雨氷",
    "520": "中くらいのにわか雨",
    "521": "にわか雨",
    "522": "重い強度にわか雨",
    "531": "不規則なにわか雨",
    "600": "小雪",
    "601": "雪",
    "602": "大雪",
    "611": "みぞれ",
    "612": "にわかみぞれ",
    "615": "光雨と雪",
    "616": "雨や雪",
    "620": "光のにわか雪",
    "621": "にわか雪",
    "622": "重いにわか雪",
    "701": "ミスト",
    "711": "煙",
    "721": "ヘイズ",
    "731": "砂、ほこり旋回する",
    "741": "霧",
    "751": "砂",
    "761": "ほこり",
    "762": "火山灰",
    "771": "スコール",
    "781": "竜巻",
    "800": "晴天",
    "801": "薄い雲",
    "802": "雲",
    "803": "曇りがち",
    "804": "厚い雲",
    "900": "竜巻",
    "901": "熱帯低気圧",
    "902": "ハリケーン",
    "903": "寒い",
    "904": "暑い",
    "905": "強い風",
    "906": "雹",
    "951": "落ち着いた",
    "952": "弱い風",
    "953": "そよ風",
    "954": "風",
    "955": "爽やかな風",
    "956": "強風",
    "957": "暴風に近い強風",
    "958": "暴風",
    "959": "深刻な暴風",
    "960": "嵐",
    "961": "暴風雨",
    "962": "ハリケーン"
  }

client = discord.Client()

def get_Weather(lot,lat):
    appid = "xxxAPIKeyxxx"#openweathermap APIKey
    url = "http://api.openweathermap.org/data/2.5/weather?"
    url += "APPID=" + appid
    url += "&lat=" + lat
    url += "&lon=" + lot
    url += "&units=" + "metric" 
    r = requests.get(url)
    res = r.json()
    return res

def get_Coordinates(location_name):
    appid = "xxxAppidxxx"#Yahoo! Open Local Platform APIKey
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
    print('Logged in as')
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
            return await client.send_message(message.channel,embed=em)

        if messagelist[1] == "天気":
            location_name = messagelist[0]
            em = get_Weather_info(location_name)
            return await client.send_message(message.channel,embed=em)


if __name__ == "__main__":
    client.run("xxxTokenxxx")#Discord Token

