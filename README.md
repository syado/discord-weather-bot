# Discord-Weather-Bot
地名を基に、Yahoo!のGeocoderで経度と緯度を求め、OpenWeatherMapでその位置の気象情報を取得している。<br>
<br>
## 動作に必要な環境
- [python3](https://www.python.org/downloads/)<br>
- [discord.py](https://github.com/Rapptz/discord.py)<br>
- [requests](https://github.com/requests/requests)(Python Library)<br>

## APIkey等の設定
- [OpenWeatherMap](https://openweathermap.org/)でkeyを取得し、ソースコードに追加<br>
- [Yahoo!API](https://e.developer.yahoo.co.jp/register)でappidを取得し、ソースコードに追加<br>
- [Discord](https://discordapp.com/developers/applications/me)でtokenを取得し、ソースコードに追加<br>

## コマンド
```
地名　天気
```
```
天気　地名
```
