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

app_id = "wx4d641c93736d804b"
app_secret = "216f333cacc3762043b105b5625b3d88"

countdown_date="03-15"

user_ids = "oa3s-5k7gpwSKpZNkcJIgtS8FRPk oa3s-5iVxLhnjthewnYeMrRi80FY oa3s-5tne3PTV8qI9CXjGJ1NizFY oa3s-5r-rUhsS7IXKgST_Cgc7Euk".split(" ")

template_id = "V7NbI9095kyYXgvE5y6DOF3uVL79Ekckjg73KdGNj-4"

if app_id is None or app_secret is None:
  print('请设置 APP_ID 和 APP_SECRET')
  exit(422)

if not user_ids:
  print('请设置 USER_ID，若存在多个 ID 用回车分开')
  exit(422)

if template_id is None:
  print('请设置 TEMPLATE_ID')
  exit(422)

# 倒计时
def get_date_left():
  if countdown_date is None:
    print('没有设置 Date')
    return 0
  next = datetime.strptime(str(date.today().year) + "-" + countdown_date, "%Y-%m-%d")
  if next < nowtime:
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
# def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
#     return get_words()
#   return words.json()['data']['text']

# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

try:
  client = WeChatClient(app_id, app_secret)
except WeChatClientException as e:
  print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
  exit(502)

wm = WeChatMessage(client)
data = {
  "date_left": {
    "value": get_date_left(),
    "color": get_random_color()
  }
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
