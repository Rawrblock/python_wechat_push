#coding:utf-8
from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import requests
import os
import random

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") #今天的日期

start_date = "2020-12-28"
she_city = "佛山"
he_city = "重庆"
# birthday = os.getenv('BIRTHDAY')

app_id = "wx5b1dcd2abfd26909"
app_secret = "c058f0d0cada3480d3c4f3742703d10f"

user_ids = "o_h_L6Ww1qMK31ndUXLSIxpYp_g4 o_h_L6flejNGUxsn8TZwtlA7yS4A".split(" ")
template_id = "Hys8ZvGFi61cOfr8RpMy0ZBAKMW_wkCB0P8xAf3sgQw"

defaultCity = "佛山"

if app_id is None or app_secret is None:
  print('请设置 APP_ID 和 APP_SECRET')
  exit(422)

if not user_ids:
  print('请设置 USER_ID，若存在多个 ID 用回车分开')
  exit(422)

if template_id is None:
  print('请设置 TEMPLATE_ID')
  exit(422)

# weather 直接返回对象，在使用的地方用字段进行调用。
def get_she_weather():
  if she_city is None:
    print('请设置城市')
    return None
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + she_city
  res = requests.get(url).json()
  if res is None:
    return None
  she_weather = res['data']['list'][0]
  return she_weather
# weather 直接返回对象，在使用的地方用字段进行调用。
def get_he_weather():
  if he_city is None:
    print('请设置城市')
    return None
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + he_city
  res = requests.get(url).json()
  if res is None:
    return None
  he_weather = res['data']['list'][0]
  return he_weather

# 纪念日正数
def get_memorial_days_count():
  if start_date is None:
    print('没有设置 START_DATE')
    return 0
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 生日倒计时
# def get_birthday_left():
#   if birthday is None:
#     print('没有设置 BIRTHDAY')
#     return 0
#   next = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d")
#   if next < nowtime:
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def format_temperature(temperature):
  return math.floor(temperature)

# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

try:
  client = WeChatClient(app_id, app_secret)
except WeChatClientException as e:
  print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
  exit(502)

wm = WeChatMessage(client)
she_weather = get_she_weather()
he_weather = get_he_weather()
if she_weather is None:
  print('获取她天气失败')
  exit(422)
if he_weather is None:
  print('获取他天气失败')
  exit(422)
data = {
  "she_city": {
    "value": defaultCity,
    "color": get_random_color()
  },
  # 她的今日天气
  "she_weather": {
    "value": she_weather['weather'],
    "color": get_random_color()
  },
  # 她的今日温度
  "she_temperature": {
    "value": math.floor(she_weather['temp']),
    "color": get_random_color()
  },
  # 她的最高温度
  "she_highest": {
    "value": math.floor(she_weather['high']),
    "color": get_random_color()
  },
  # 她的最低温度
  "she_lowest": {
    "value": math.floor(she_weather['low']),
    "color": get_random_color()
  },
  "he_city": {
    "value": he_city,
    "color": get_random_color()
  },
  # 他的今日天气
  "he_weather": {
    "value": he_weather['weather'],
    "color": get_random_color()
  },
   # 他的今日温度
  "he_temperature": {
    "value": math.floor(he_weather['temp']),
    "color": get_random_color()
  },
  # 他的最高温度
  "he_highest": {
    "value": math.floor(he_weather['high']),
    "color": get_random_color()
  },
  # 他的最低温度
  "he_lowest": {
    "value": math.floor(he_weather['low']),
    "color": get_random_color()
  },
  "date": {
    "value": today.strftime('%Y年%m月%d日'),
    "color": get_random_color()
  },
  "love_days": {
    "value": get_memorial_days_count(),
    "color": get_random_color()
  },
  # "birthday_left": {
  #   "value": get_birthday_left(),
  #   "color": get_random_color()
  # },
  "words": {
    "value": get_words(),
    "color": get_random_color()
  },
}

if __name__ == '__main__':
  count = 0
  try:
    for user_id in user_ids:
      res = wm.send_template(user_id, template_id, data)
      count+=1
  except WeChatClientException as e:
    print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
    exit(502)

  print("发送了" + str(count) + "条消息")
