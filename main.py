from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
#import emoji

today = datetime.now()

weekStr="星期一星期二星期三星期四星期五星期六星期日"
pos=(today.isoweekday()-1)*3
week_day = weekStr[pos:pos+3]

today1 = datetime.strftime(today,'%Y年%m月%d日')
start_date = os.environ['START_DATE']
city = os.environ['CITY']
wbirthday = os.environ['WBIRTHDAY']
mbirthday = os.environ['MBIRTHDAY']
marry_date = os.environ['MARRY_DATE']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

#def get_weather():
#  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#  res = requests.get(url).json()
#  weather = res['data']['list'][0]
#  return weather['weather'], weather['humidity'], weather['wind'], weather['airData'], weather['airQuality'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])

def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/" + city
  res = requests.get(url).json()
  citys = res['cityInfo']
  weather = res['data']['forecast']
  humidity = res['data']['shidu']
  air_quality = res['data']['quality']
  temperature = res['data']['wendu'] + "℃"
  return humidity, air_quality, temperature, weather, citys

def get_love_days_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_marry_day_count():
  delta = today - datetime.strptime(marry_date, "%Y-%m-%d")
  return delta.days

def get_wbirthday():
  next = datetime.strptime(str(date.today().year) + "-" + wbirthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_mbirthday():
  next = datetime.strptime(str(date.today().year) + "-" + mbirthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)


humidity, air_quality, temperature, weather_list, city_list = get_weather()
#print(weather_list)
wea = weather_list[0]['type']
highest = weather_list[0]['high']
lowest = weather_list[0]['low']
notice = weather_list[0]['notice']
wind = weather_list[0]['fx'] + " " + weather_list[0]['fl']
air_data = weather_list[0]['aqi']
parent = city_list['parent']
citys = city_list['city']

#wea, humidity, wind, air_data, air_quality, temperature, lowest, highest = get_weather()
#data = {"date":{"value":today1, "color":get_random_color()},
#        "week_day":{"value":week_day, "color":get_random_color()},
#        "parent":{"value":parent, "color": get_random_color()},
#        "city":{"value":citys, "color": get_random_color()},
#        "notice":{"value":notice, "color": get_random_color()},
#        "weather":{"value":wea, "color":get_random_color()},
#        "humidity":{"value":humidity, "color":get_random_color()},
#        "wind":{"value":wind, "color":get_random_color()},
#        "air_data":{"value":air_data, "color":get_random_color()},
#        "air_quality":{"value":air_quality, "color":get_random_color()},
#        "temperature":{"value":temperature, "color":get_random_color()},
#        "lowest":{"value":lowest, "color":get_random_color()},
#        "highest":{"value":highest, "color":get_random_color()},
#        "love_days":{"value":get_count(), "color":get_random_color()},
#        "birthday_left":{"value":get_birthday(), "color":get_random_color()},
#        "words":{"value":get_words(), "color":get_random_color()}}


data = {"date":{"value":today1},
        "week_day":{"value":week_day},
        "parent":{"value":parent},
        "city":{"value":citys},
        "notice":{"value":notice},
        "weather":{"value":wea},
        "humidity":{"value":humidity},
        "wind":{"value":wind},
        "air_data":{"value":air_data},
        "air_quality":{"value":air_quality},
        "temperature":{"value":temperature},
        "lowest":{"value":lowest},
        "highest":{"value":highest},
        "love_days":{"value":get_love_days_count()},
        "marry_days":{"value":get_marry_day_count()},
        "love_day":{"value":start_date},
        "marry_day":{"value":marry_date},
        "w_birthday_left":{"value":get_wbirthday()},
        "m_birthday_left":{"value":get_mbirthday()},
        "words":{"value":get_words()}}

#        "week_day_icon":{"value":emoji.emojize(':calendar:')},
#        "city_icon":{"value":emoji.emojize(':city_sunset:')},
#        "notice_icon":{"value":emoji.emojize(':clipboard:')},
#        "weather_icon":{"value":emoji.emojize(':sunny:')},
#        "wind_icon":{"value":emoji.emojize(':cyclone:')},
#        "temperature_icon":{"value":emoji.emojize(':hotsprings:')},
#        "lowest_icon":{"value":emoji.emojize(':snowflake:')},
#        "highest_icon":{"value":emoji.emojize(':fire:')},
#        "love_days_icon":{"value":emoji.emojize(':couplekiss:')},
#        "birthday_left_icon":{"value":emoji.emojize(':birthday:')}}

user_id_list = user_id.split(',')
for i in range(len(user_id_list)):
  res = wm.send_template(user_id_list[i], template_id, data)
  print(res)
