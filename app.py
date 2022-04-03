from email.message import EmailMessage
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import time
import requests
import json
from bs4 import BeautifulSoup
import random
import threading
from commands import Commands
import pymongo
import smtplib
import datetime
from datetime import datetime, timedelta, timezone
import linebot
from google_translate_py import Translator

app = Flask(__name__)

bot = LineBotApi(
    'R2EQ91eZrOij+P9TsvsuA9g3BkgNkMlnXihtzAt9uGW0c8PPONHRlnquTZ15TxY0F9dn3RXrPlfNW9ROMFAkRYSHxIXYNy+CLMTQbKbMuynhnzTH4HRnOdyudl3uYCjCHhhPPUoHrIopw/r1pJpfYQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3bd317940dcdc209b09bbefc94fd63c0')

global cached_messages
cached_messages = {}

count = {}
emails = []

global results
results = []

global unsendall
global unsendlist
unsendall = {}
unsendlist = []

trans = []
trans1 = []
trans2 = []
trans3 = []
unknown = []
transName = []
using = []
ip = []

client = pymongo.MongoClient(
    "mongodb+srv://nathan:1620zxcv@cluster0.lmlkk.mongodb.net/levels?retryWrites=true&w=majority")
gb = client.levels['global']
db = client.levels
cb = client.chats['chat']
eb = client.chats['enable']
tic = client.tic['tic']
bk = client.chats['blocking']
bullshit = client.bullshit['bullshit']
unsend1 = []
now1 = []
admin = []

global sent
sent = {}
waiting = []
waiting2 = []
waitName = []
circlewait = []
heroks = []



def c(url, page):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find_all(class_="img-fluid lazy")
    for e in result:
        results.append(result)
        print(f"{page} | {e}")


for i in range(1, 51):
    url = f"https://memes.tw/wtf?sort=top-week&contest=795&page={i}"
    t = threading.Thread(target=c, args=(url, i,))
    t.start()

gmail = "linetellmemore@gmail.com"
secret = "selina0906Z"


def send(mail: str = gmail, password: str = secret):
    target5 = emails[0]
    subject5 = emails[1]
    body5 = emails[2]
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(mail, password)
        msg = EmailMessage()
        msg['Subject'] = subject5
        msg['From'] = mail
        msg['To'] = target5
        msg.add_alternative(f"""\
            <!DOCTYPE html>
            <html>
                <body>
                    <h1 style="color:red;">{subject5}</h1>
                    <h2  style="color:black;">{body5}</h2>
            </html>
        """, subtype="html")
        smtp.send_message(msg)
        print("發送成功")
        emails.clear()


# 天氣
token = "CWB-716BDC0D-31B2-4A9B-8DC7-32C3DA8763AD"
url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName='
waitWeather = []


def cooldown():
    while True:
        time.sleep(1)
        try:
            for i in count:
                if count[i] <= 0:
                    count.pop(i)
                    continue
                count[i] -= 1
        except:
            continue


def calc_rank(exp: int):
    level = 0
    needed_exp = 100
    while exp > needed_exp:
        exp -= needed_exp
        needed_exp += 50
        level += 1
    return level, exp, needed_exp


@app.route("/", methods=['GET'])
def index():
    return 'hi'


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print("簽名:" + signature)
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
        return
    return 'OK'


@handler.add(linebot.models.events.UnsendEvent)
def snipe(event):
    unsendall.setdefault(event.unsend.message_id, {'user': event.source.user_id, 'group': event.source.group_id, 'msg': cached_messages[event.unsend.message_id]})
    unsendlist.append(event.unsend.message_id)
    unsend1.clear()
    now1.clear()
    tz = timezone(timedelta(hours=+8))
    isotime = datetime.now(tz).isoformat()
    now = datetime.fromisoformat(isotime)
    head, sep, tail = str(now).partition('.')
    now1.append(str(head))
    unsend1.append(event.unsend.message_id)
    unsend1.append(event.source.user_id)
    unsend1.append(event.source.group_id)


@handler.add(MemberJoinedEvent)
def handle_member_join(event):
    group_id = event.source.group_id
    user_id = event.joined.members[0].user_id
    team = bot.get_group_summary(group_id)
    profile = bot.get_group_member_profile(group_id, user_id)
    chatToken = event.reply_token
    bot.reply_message(chatToken, FlexSendMessage('加入群組', {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": profile.display_name,
                    "size": "4xl",
                    "weight": "bold",
                    "color": "#fffef4",
                    "align": "center",
                    "flex": 0
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "歡迎您加入",
                            "color": "#fffef4",
                            "flex": 0,
                            "weight": "bold",
                            "size": "xxl",
                            "offsetStart": "none",
                            "offsetEnd": "none",
                            "offsetBottom": "none"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": []
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": team.group_name,
                            "flex": 0,
                            "color": "#fffef6",
                            "weight": "bold",
                            "size": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "margin": "xxl"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "打 !幫助 可以獲取說明書",
                                    "color": "#fffef6",
                                    "size": "xl",
                                    "weight": "bold",
                                    "align": "center",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "(｡◕∀◕｡)",
                                    "flex": 0,
                                    "size": "3xl",
                                    "color": "#fffef6",
                                    "weight": "bold",
                                    "align": "center"
                                }
                            ]
                        }
                    ]
                }
            ],
            "backgroundColor": "#011105",
            "background": {
                "type": "linearGradient",
                "startColor": "#000000",
                "endColor": "#666561",
                "angle": "176deg"
            }
        }
    }))
    print(user_id)
    return


@handler.add(JoinEvent)
def handle_join(event):
    chatToken = event.reply_token
    user_id = event.source.user_id
    group_id = event.source.group_id
    print("獲取加入群組訊息")
    if eb.find_one({'group_id': event.source.group_id}) is None:
        data = {
            "group_id": event.source.group_id,
            "enable": "True"
        }
        eb.insert(data)
        bot.reply_message(chatToken, TextSendMessage(text="謝謝把卡米喵加入本群組請打\n"
                                                          "請先將本喵加為好友\n"
                                                          "!幫助 獲取使用功能說明書\n"
                                                          "!戰鬥系統:說明RPG玩法\n"
                                                          "此機器人有類似卡米狗的聊天功能\n"
                                                          "更多使用明請打!幫助\n"
                                                          "(｡◕∀◕｡)"))
        print(group_id)
    else:
        bot.reply_message(chatToken, TextSendMessage(text="謝謝把卡米喵加入本群組請打\n"
                                                          "請先將本喵加為好友\n"
                                                          "!幫助 獲取使用功能說明書\n"
                                                          "!戰鬥系統:說明RPG玩法\n"
                                                          "此機器人有類似卡米狗的聊天功能\n"
                                                          "更多使用明請打!幫助\n"
                                                          "(｡◕∀◕｡)"))
        print(group_id)


rpswait = []
bullshit0 = []
bullshit1 = []


@handler.add(PostbackEvent)
def post_back(event):

    chatToken = event.reply_token
    user_id = event.source.user_id
    postback = event.postback.data
    profile = bot.get_group_member_profile(event.source.group_id, user_id)
    print(postback)
    if tic.find_one({"攻擊者": user_id}) is not None:
        if tic.find_one({"攻擊者": user_id})["攻擊者出"] != "未知":
            bot.reply_message(chatToken, TextSendMessage(f"{profile.display_name}請不要點兩次或以上!"))
        if postback == "1" and tic.find_one({"攻擊者": user_id})["攻擊者出"] == "未知" and tic.find_one({"攻擊者": user_id})[
            "被攻擊者出"] == "未知":
            tic.update_one({"攻擊者": user_id}, {"$set": {"攻擊者出": "✌🏼"}})
        if postback == "2" and tic.find_one({"攻擊者": user_id})["攻擊者出"] == "未知" and tic.find_one({"攻擊者": user_id})[
            "被攻擊者出"] == "未知":
            tic.update_one({"攻擊者": user_id}, {"$set": {"攻擊者出": "✊🏻"}})
        if postback == "3" and tic.find_one({"攻擊者": user_id})["攻擊者出"] == "未知" and tic.find_one({"攻擊者": user_id})[
            "被攻擊者出"] == "未知":
            tic.update_one({"攻擊者": user_id}, {"$set": {"攻擊者出": "✋🏻"}})
        if postback == "1" and tic.find_one({"攻擊者": user_id})["攻擊者出"] == "未知" and tic.find_one({"攻擊者": user_id})[
            "被攻擊者出"] != "未知":
            tic.update_one({"攻擊者": user_id}, {"$set": {"攻擊者出": "✌🏼"}})
            atkuser = tic.find_one({"攻擊者": user_id})["攻擊者"]
            gotatkuser = tic.find_one({"攻擊者": user_id})["被攻擊者"]
            atk = tic.find_one({"攻擊者": user_id})["攻擊者出"]
            gotatk = tic.find_one({"攻擊者": user_id})["被攻擊者出"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if atk == "✌🏼" and gotatk == "✌🏼":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✌🏼\n"
                                                             f"{gotatkname.display_name}出:✌🏼\n"
                                                             f"\n"
                                                             f"這局平手"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if atk == "✌🏼" and gotatk == "✊🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✌🏼\n"
                                                             f"{gotatkname.display_name}出:✊🏻\n"
                                                             f"\n"
                                                             f"這局由{gotatkname.display_name}獲勝"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if atk == "✌🏼" and gotatk == "✋🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✌🏼\n"
                                                             f"{gotatkname.display_name}出:✋🏻\n"
                                                             f"\n"
                                                             f"這局由{atkname.display_name}獲勝"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
        if postback == "2" and tic.find_one({"攻擊者": user_id})["攻擊者出"] == "未知" and tic.find_one({"攻擊者": user_id})[
            "被攻擊者出"] != "未知":
            tic.update_one({"攻擊者": user_id}, {"$set": {"攻擊者出": "✊🏻"}})
            atkuser = tic.find_one({"攻擊者": user_id})["攻擊者"]
            gotatkuser = tic.find_one({"攻擊者": user_id})["被攻擊者"]
            atk = tic.find_one({"攻擊者": user_id})["攻擊者出"]
            gotatk = tic.find_one({"攻擊者": user_id})["被攻擊者出"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if atk == "✊🏻" and gotatk == "✌🏼":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✊🏻\n"
                                                             f"{gotatkname.display_name}出:✌🏼\n"
                                                             f"\n"
                                                             f"這局由{atkname.display_name}獲勝"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if atk == "✊🏻" and gotatk == "✊🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✊🏻\n"
                                                             f"{gotatkname.display_name}出:✊🏻\n"
                                                             f"\n"
                                                             f"這局平手"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if atk == "✊🏻" and gotatk == "✋🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✊🏻\n"
                                                             f"{gotatkname.display_name}出:✋🏻\n"
                                                             f"\n"
                                                             f"這局由{gotatkname.display_name}獲勝"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
        if postback == "3" and tic.find_one({"攻擊者": user_id})["攻擊者出"] == "未知" and tic.find_one({"攻擊者": user_id})[
            "被攻擊者出"] != "未知":
            tic.update_one({"攻擊者": user_id}, {"$set": {"攻擊者出": "✋🏻"}})
            atkuser = tic.find_one({"攻擊者": user_id})["攻擊者"]
            gotatkuser = tic.find_one({"攻擊者": user_id})["被攻擊者"]
            atk = tic.find_one({"攻擊者": user_id})["攻擊者出"]
            gotatk = tic.find_one({"攻擊者": user_id})["被攻擊者出"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if atk == "✋🏻" and gotatk == "✌🏼":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✋🏻\n"
                                                             f"{gotatkname.display_name}出:✌🏼\n"
                                                             f"\n"
                                                             f"這局由{gotatkname.display_name}獲勝"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if atk == "✋🏻" and gotatk == "✊🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✋🏻\n"
                                                             f"{gotatkname.display_name}出:✊🏻\n"
                                                             f"\n"
                                                             f"這局由{atkname.display_name}獲勝"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if atk == "✋🏻" and gotatk == "✋🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✋🏻\n"
                                                             f"{gotatkname.display_name}出:✋🏻\n"
                                                             f"\n"
                                                             f"這局平手"))
                tic.delete_one({"攻擊者": user_id})
                rpswait.remove(gotatkuser)
    if tic.find_one({"被攻擊者": user_id}) is not None:
        if tic.find_one({"被攻擊者": user_id})["被攻擊者出"] != "未知":
            bot.reply_message(chatToken, TextSendMessage(f"{profile.display_name}請不要點兩次或以上!"))
        if postback == "1" and tic.find_one({"被攻擊者": user_id})["被攻擊者出"] == "未知" and tic.find_one({"被攻擊者": user_id})[
            "攻擊者出"] == "未知":
            tic.update_one({"被攻擊者": user_id}, {"$set": {"被攻擊者出": "✌🏼"}})
        if postback == "2" and tic.find_one({"被攻擊者": user_id})["被攻擊者出"] == "未知" and tic.find_one({"被攻擊者": user_id})[
            "攻擊者出"] == "未知":
            tic.update_one({"被攻擊者": user_id}, {"$set": {"被攻擊者出": "✊🏻"}})
        if postback == "3" and tic.find_one({"被攻擊者": user_id})["被攻擊者出"] == "未知" and tic.find_one({"被攻擊者": user_id})[
            "攻擊者出"] == "未知":
            tic.update_one({"被攻擊者": user_id}, {"$set": {"被攻擊者出": "✋🏻"}})
        if postback == "1" and tic.find_one({"被攻擊者": user_id})["被攻擊者出"] == "未知" and tic.find_one({"被攻擊者": user_id})[
            "攻擊者出"] != "未知":
            tic.update_one({"被攻擊者": user_id}, {"$set": {"被攻擊者出": "✌🏼"}})
            atkuser = tic.find_one({"被攻擊者": user_id})["攻擊者"]
            gotatkuser = tic.find_one({"被攻擊者": user_id})["被攻擊者"]
            atk = tic.find_one({"被攻擊者": user_id})["攻擊者出"]
            gotatk = tic.find_one({"被攻擊者": user_id})["被攻擊者出"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if gotatk == "✌🏼" and atk == "✌🏼":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✌🏼\n"
                                                             f"{gotatkname.display_name}出:✌🏼\n"
                                                             f"\n"
                                                             f"這局平手"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "✌🏼" and atk == "✊🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✊🏻\n"
                                                             f"{gotatkname.display_name}出:✌🏼\n"
                                                             f"\n"
                                                             f"這局由{atkname.display_name}獲勝"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "✌🏼" and atk == "✋🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✋🏻\n"
                                                             f"{gotatkname.display_name}出:✌🏼\n"
                                                             f"\n"
                                                             f"這局由{gotatkname.display_name}獲勝"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
        if postback == "2" and tic.find_one({"被攻擊者": user_id})["被攻擊者出"] == "未知" and tic.find_one({"被攻擊者": user_id})[
            "攻擊者出"] != "未知":
            tic.update_one({"被攻擊者": user_id}, {"$set": {"被攻擊者出": "✊🏻"}})
            atkuser = tic.find_one({"被攻擊者": user_id})["攻擊者"]
            gotatkuser = tic.find_one({"被攻擊者": user_id})["被攻擊者"]
            atk = tic.find_one({"被攻擊者": user_id})["攻擊者出"]
            gotatk = tic.find_one({"被攻擊者": user_id})["被攻擊者出"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if gotatk == "✊🏻" and atk == "✌🏼":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✌🏼\n"
                                                             f"{gotatkname.display_name}出:✊🏻\n"
                                                             f"\n"
                                                             f"這局由{gotatkname.display_name}獲勝"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "✊🏻" and atk == "✊🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✊🏻\n"
                                                             f"{gotatkname.display_name}出:✊🏻\n"
                                                             f"\n"
                                                             f"這局平手"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "✊🏻" and atk == "✋🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✋🏻\n"
                                                             f"{gotatkname.display_name}出:✊🏻\n"
                                                             f"\n"
                                                             f"這局由{atkname.display_name}獲勝"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
        if postback == "3" and tic.find_one({"被攻擊者": user_id})["被攻擊者出"] == "未知" and tic.find_one({"被攻擊者": user_id})[
            "攻擊者出"] != "未知":
            tic.update_one({"被攻擊者": user_id}, {"$set": {"被攻擊者出": "✋🏻"}})
            atkuser = tic.find_one({"被攻擊者": user_id})["攻擊者"]
            gotatkuser = tic.find_one({"被攻擊者": user_id})["被攻擊者"]
            atk = tic.find_one({"被攻擊者": user_id})["攻擊者出"]
            gotatk = tic.find_one({"被攻擊者": user_id})["被攻擊者出"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if gotatk == "✋🏻" and atk == "✌🏼":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✌🏼\n"
                                                             f"{gotatkname.display_name}出:✋🏻\n"
                                                             f"\n"
                                                             f"這局由{atkname.display_name}獲勝"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "✋🏻" and atk == "✊🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✊🏻\n"
                                                             f"{gotatkname.display_name}出:✋🏻\n"
                                                             f"\n"
                                                             f"這局由{gotatkname.display_name}獲勝"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "✋🏻" and atk == "✋🏻":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}出:✋🏻\n"
                                                             f"{gotatkname.display_name}出:✋🏻\n"
                                                             f"\n"
                                                             f"這局平手"))
                tic.delete_one({"被攻擊者": user_id})
                rpswait.remove(gotatkuser)

allMessage = []
cct = 0


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event, cct=0):
    print(event.message.text)
    cached_messages[event.message.id] = event.message.text
    msg = event.message.text
    chatToken = event.reply_token
    user_id = event.source.user_id
    lender = msg.split(";")
    try: #群組裡
        team = bot.get_group_summary(event.source.group_id)
        teamtake = bot.get_group_member_profile(event.source.group_id, user_id)
        allMessage.append(f"🧑‍💻:【{teamtake.display_name}】\n"
                          f"👪:【{team.group_name}】\n"
                          f"💬:【{msg}】\n"
                          f"\n")
    except:  #個人
        alone = bot.get_profile(user_id)
        allMessage.append(f"🧑‍💻:【{alone.display_name}】\n"
                          f"👪:【與卡米喵的私聊】\n"
                          f"💬:【{msg}】\n"
                          f"\n")

    if len(unsendlist) >= 20:
        unsendlist.clear()
        unsendall.clear()
    elif msg == "!清空訊息":
        allMessage.clear()
        bot.reply_message(chatToken, TextSendMessage("已清空allMessage"))
    elif bk.find_one({"user": user_id}) is not None:
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        if user_id == "Uf5eefecbe1bedaf8f228eb1552e3832f":
            bot.reply_message(chatToken, TextSendMessage("閉嘴臭海鮮你沒有發言權"))
        else:
            f = open("fuck.txt", encoding='utf-8')
            lines = f.readlines()
            test = []
            for line in lines:
                test.append(line.replace('\n', '').replace("''", ''))
                f.close()
            i = 0
            while True:
                if i < 52:
                    test.remove('')
                    i += 1
                else:
                    break
            last = []
            for g in test:
                last.append(str(g))
        bot.reply_message(chatToken, TextSendMessage(take.display_name + " " + random.choice(last)))
    elif "學" in msg and len(lender) == 3:
        d = cb.find_one({'detect': str(lender[1])})
        if d is None:
            test = bot.get_profile(user_id)
            data = {
                'name': test.display_name,
                'detect': str(lender[1]),
                'reply': str(lender[2])
            }
            cb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("神奇的知識+1"))
        else:
            test = bot.get_profile(user_id)
            data = {
                'name': test.display_name,
                'detect': str(lender[1]),
                'reply': str(lender[2])
            }
            cb.delete_one({"detect": str(lender[1])})
            cb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("神奇的知識+1"))
    elif user_id in admin:
        gb.delete_one({"name": msg})
        bot.reply_message(chatToken, TextSendMessage("刪除成功"))
        admin.remove(user_id)
    elif user_id in ip:
        try:
            r = requests.get(f'https://ipapi.co/{msg}/json/', timeout=1)
            j = json.loads(r.text)
            bot.reply_message(chatToken, TextSendMessage(f"IP:{j['ip']}\n"
                                                         f"類型:{j['version']}\n"
                                                         f"城市:{j['city']}\n"
                                                         f"地區:{j['region']}\n"
                                                         f"區碼:{j['region_code']}\n"
                                                         f"國家:{j['country']}\n"
                                                         f"國名:{j['country_name']}\n"
                                                         f"國家代碼:{j['country_code']}\n"
                                                         f"準國家代碼:{j['country_code_iso3']}\n"
                                                         f"國家域名:{j['country_tld']}\n"
                                                         f"分布代碼:{j['continent_code']}\n"
                                                         f"歐盟:{j['in_eu']}\n"
                                                         f"郵政:{j['postal']}\n"
                                                         f"緯度:{j['latitude']}\n"
                                                         f"經度:{j['longitude']}\n"
                                                         f"時區:{j['timezone']}\n"
                                                         f"時區+:{j['utc_offset']}\n"
                                                         f"電話編號:{j['country_calling_code']}\n"
                                                         f"貨幣:{j['currency']}\n"
                                                         f"語言:{j['languages']}\n"
                                                         f"國家面積:{j['country_area']}\n(千公頃)\n"
                                                         f"國家人口:{j['country_population']}\n"
                                                         f"自治系統號:{j['asn']}\n"
                                                         f"電信公司:{j['org']}"))
            ip.remove(user_id)
        except:
            bot.reply_message(chatToken, TextSendMessage("請輸入正確IP"))
    elif user_id in bullshit1:
        tint = int(msg)
        try:
            if tint < 100 or tint > 1000:
                bot.reply_message(chatToken, TextSendMessage("請輸入100-1000的數字謝謝"))
            else:
                payload = {
                    "Topic": bullshit.find_one({"user": user_id})["主題"],
                    "MinLen": tint
                }
                res = requests.post("https://api.howtobullshit.me/bullshit", json=payload)
                text = res.text
                output = text.replace('&nbsp;', '').replace('<br><br>', '')
                bot.reply_message(chatToken, TextSendMessage(output))
                bullshit1.remove(user_id)
                bullshit.delete_one({"user": user_id})
        except ValueError:
            bot.reply_message(chatToken, TextSendMessage("請輸入100-1000的數字謝謝"))
    elif user_id in bullshit0:
        bot.reply_message(chatToken, TextSendMessage(f"您輸入得主題為{msg}\n"
                                                     f"請輸入你的字數上限\n"
                                                     f"100-1000"))
        bullshit0.remove(user_id)
        bullshit1.append(user_id)
        data = {
            "user": user_id,
            "主題": msg
        }
        bullshit.insert(data)
    elif user_id in waitWeather:
        weathermsg = msg.replace('台', '臺')
        if msg == "北市":
            bot.reply_message(chatToken, TextSendMessage("請輸入正確名稱"))
            return
        elif weathermsg in "宜蘭縣," \
                           " 花蓮縣," \
                           " 臺東縣," \
                           " 澎湖縣," \
                           " 金門縣," \
                           " 連江縣," \
                           " 臺北市," \
                           " 新北市," \
                           " 桃園市," \
                           " 臺中市," \
                           " 臺南市," \
                           " 高雄市," \
                           " 基隆市," \
                           " 新竹縣," \
                           " 新竹市," \
                           " 苗栗縣," \
                           " 彰化縣," \
                           " 南投縣," \
                           " 雲林縣," \
                           " 嘉義縣," \
                           " 嘉義市," \
                           " 屏東縣":
            weather = requests.get(url + weathermsg)
            data = weather.json()
            a = data["records"]["location"][0]
            # 城市名
            City = a["locationName"]
            # 開始結束時間
            start1 = a["weatherElement"][0]["time"][0]["startTime"]
            start2 = a["weatherElement"][0]["time"][1]["startTime"]
            start3 = a["weatherElement"][0]["time"][2]["startTime"]
            over1 = a["weatherElement"][0]["time"][0]["endTime"]
            over2 = a["weatherElement"][0]["time"][1]["endTime"]
            over3 = a["weatherElement"][0]["time"][2]["endTime"]
            # Wx天氣狀況
            weatherdes1 = a["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
            weatherdes2 = a["weatherElement"][0]["time"][1]["parameter"]["parameterName"]
            weatherdes3 = a["weatherElement"][0]["time"][2]["parameter"]["parameterName"]
            # PoP降雨機率 # 百分比%
            maybe1 = a["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
            maybe2 = a["weatherElement"][1]["time"][1]["parameter"]["parameterName"]
            maybe3 = a["weatherElement"][1]["time"][2]["parameter"]["parameterName"]
            # MinT最低溫 #度C
            cold1 = a["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
            cold2 = a["weatherElement"][2]["time"][1]["parameter"]["parameterName"]
            cold3 = a["weatherElement"][2]["time"][2]["parameter"]["parameterName"]
            # MaxT最高溫 #度C
            hot1 = a["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
            hot2 = a["weatherElement"][4]["time"][1]["parameter"]["parameterName"]
            hot3 = a["weatherElement"][4]["time"][2]["parameter"]["parameterName"]
            # CI舒適度
            comfor1 = a["weatherElement"][3]["time"][0]["parameter"]["parameterName"]
            comfor2 = a["weatherElement"][3]["time"][1]["parameter"]["parameterName"]
            comfor3 = a["weatherElement"][3]["time"][2]["parameter"]["parameterName"]
            bot.reply_message(chatToken, FlexSendMessage('天氣概況', {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2dv_VbsKL91IfGZ8Il-fSKs-ZXloswiS0uA&usqp=CAU",
                            "aspectRatio": "1:1",
                            "margin": "xs",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": City,
                            "weight": "bold",
                            "size": "4xl",
                            "margin": "md",
                            "color": "#FFFFFF",
                            "align": "start"
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"開始:{start1}",
                                            "color": "#9f9a99",
                                            "size": "md",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"狀態:{weatherdes1}",
                                            "size": "lg",
                                            "color": "#e7e5e5",
                                            "flex": 0,
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"降雨機率:{maybe1}%",
                                            "size": "lg",
                                            "color": "#e7e5e5",
                                            "flex": 0,
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"最低溫:{cold1}°C",
                                            "size": "lg",
                                            "color": "#e7e5e5",
                                            "flex": 0,
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"最高溫:{hot1}°C",
                                            "size": "lg",
                                            "flex": 0,
                                            "color": "#e7e5e5",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"舒適度:{comfor1}",
                                            "size": "lg",
                                            "flex": 0,
                                            "color": "#e7e5e5",
                                            "weight": "bold"
                                        }
                                    ],
                                    "margin": "none"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"結束:{over1}",
                                            "color": "#9f9a99",
                                            "weight": "bold",
                                            "size": "md"
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "xxl"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"開始:{start2}",
                                            "color": "#9f9a99",
                                            "weight": "bold",
                                            "size": "md",
                                            "flex": 0
                                        }
                                    ],
                                    "margin": "xl"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"狀態:{weatherdes2}",
                                            "color": "#e7e5e5",
                                            "flex": 0,
                                            "size": "lg",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"降雨機率:{maybe2}%",
                                            "color": "#e7e5e5",
                                            "size": "lg",
                                            "weight": "bold",
                                            "flex": 0
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"最低溫:{cold2}°C",
                                            "color": "#e7e5e5",
                                            "flex": 0,
                                            "size": "lg",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"最高溫:{hot2}°C",
                                            "color": "#e7e5e5",
                                            "flex": 0,
                                            "size": "lg",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"舒適度:{comfor2}",
                                            "flex": 0,
                                            "size": "lg",
                                            "weight": "bold",
                                            "color": "#e7e5e5"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"結束:{over2}",
                                            "color": "#9f9a99",
                                            "weight": "bold",
                                            "size": "md",
                                            "flex": 0
                                        }
                                    ]
                                },
                                {
                                    "type": "separator",
                                    "margin": "xxl"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"開始:{start3}",
                                    "flex": 0,
                                    "size": "md",
                                    "color": "#9f9a99",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "xl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"狀態:{weatherdes3}",
                                    "color": "#e7e5e5",
                                    "flex": 0,
                                    "size": "lg",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"降雨機率:{maybe3}%",
                                    "flex": 0,
                                    "size": "lg",
                                    "color": "#e7e5e5",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"最低溫:{cold3}°C",
                                    "flex": 0,
                                    "size": "lg",
                                    "color": "#e7e5e5",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"最高溫:{hot3}°C",
                                    "flex": 0,
                                    "size": "lg",
                                    "color": "#e7e5e5",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"舒適度:{comfor3}",
                                    "flex": 0,
                                    "size": "lg",
                                    "color": "#e7e5e5",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"結束:{over3}",
                                    "flex": 0,
                                    "size": "md",
                                    "color": "#9f9a99",
                                    "weight": "bold"
                                },
                                {
                                    "type": "separator",
                                    "margin": "xxl"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                                },
                                {
                                    "type": "text",
                                    "text": "天氣",
                                    "flex": 0,
                                    "size": "lg",
                                    "color": "#ffd400",
                                    "weight": "bold"
                                }
                            ]
                        }
                    ],
                    "background": {
                        "type": "linearGradient",
                        "angle": "50deg",
                        "startColor": "#290a02",
                        "endColor": "#000000"
                    }
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }))
            waitWeather.clear()
        else:
            bot.reply_message(chatToken, TextSendMessage("請輸入正確名稱"))
            return
    elif user_id in trans1:
        unknown.append(msg)
        bot.reply_message(chatToken, TextSendMessage("請輸入你想翻譯成哪國語言:\n"
                                                     "英文\n"
                                                     "日文\n"
                                                     "韓文\n"
                                                     "習近平語言\n"
                                                     "繁體中文\n"
                                                     "法文\n"
                                                     "菲律賓文\n"
                                                     "希伯來文\n"
                                                     "南非荷蘭語\n"
                                                     "阿爾哈啦語\n"
                                                     "阿拉伯語\n"
                                                     "孟加拉語\n"
                                                     "捷克語\n"
                                                     "丹麥語\n"
                                                     "荷蘭語\n"
                                                     "世界語\n"
                                                     "希臘文\n"
                                                     "夏威夷語\n"
                                                     "印地語\n"
                                                     "義大利\n"
                                                     "戰鬥民族語言\n"
                                                     "西班牙語\n"
                                                     "泰語\n"
                                                     "越語\n"
                                                     "目前只支持這幾種"))
        trans1.remove(user_id)
        trans2.append(user_id)
    elif user_id in trans2:
        if "英文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為英文\n確認後請輸入\n!確認"))
            trans.append("en")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "日文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為日文\n確認後請輸入\n!確認"))
            trans.append("ja")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "韓文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為韓文\n確認後請輸入\n!確認"))
            trans.append("ko")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "習近平語言" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為武漢肺炎研發區的語言\n確認後請輸入\n!確認"))
            trans.append("zh-cn")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "繁體中文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為繁體中文\n確認後請輸入\n!確認"))
            trans.append("zh-tw")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "法文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為法文\n確認後請輸入\n!確認"))
            trans.append("fr")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "菲律賓文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為菲律賓文\n確認後請輸入\n!確認"))
            trans.append("fil")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "希伯來文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為希伯來文\n確認後請輸入\n!確認"))
            trans.append("he")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "南非荷蘭語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為南非荷蘭語\n確認後請輸入\n!確認"))
            trans.append("af")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "阿爾哈啦語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為阿爾哈啦語\n確認後請輸入\n!確認"))
            trans.append("am")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "阿拉伯語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為阿拉伯語\n確認後請輸入\n!確認"))
            trans.append("ar")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "孟加拉語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為孟加拉語\n確認後請輸入\n!確認"))
            trans.append("bn")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "捷克語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為捷克語\n確認後請輸入\n!確認"))
            trans.append("cs")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "丹麥語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為丹麥語\n確認後請輸入\n!確認"))
            trans.append("da")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "荷蘭語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為荷蘭語\n確認後請輸入\n!確認"))
            trans.append("nl")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "世界語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為世界語\n確認後請輸入\n!確認"))
            trans.append("eo")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "希臘文" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為希臘文\n確認後請輸入\n!確認"))
            trans.append("el")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "夏威夷語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為夏威夷語\n確認後請輸入\n!確認"))
            trans.append("haw")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "印地語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為印地語\n確認後請輸入\n!確認"))
            trans.append("hi")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "義大利" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為義大利\n確認後請輸入\n!確認"))
            trans.append("it")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "戰鬥民族語言" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為戰鬥民族語言\n確認後請輸入\n!確認"))
            trans.append("ru")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "西班牙語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為西班牙語\n確認後請輸入\n!確認"))
            trans.append("es")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "泰語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為泰語\n確認後請輸入\n!確認"))
            trans.append("th")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "越語" in msg:
            bot.reply_message(chatToken, TextSendMessage("將轉換為越語\n確認後請輸入\n!確認"))
            trans.append("vi")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "!停止" in msg:
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            transName.clear()
            bot.reply_message(chatToken, TextSendMessage("翻譯程序已結束"))
            return
        else:
            bot.reply_message(chatToken, TextSendMessage("似乎還沒有這語言哦~\n請再輸入一次\n如要退出請打\n!停止"))
            return
    elif user_id in trans3:
        before = unknown[0]
        middle = trans[0]
        after = Translator().translate(before, "", middle)
        if "!確認" in msg:
            bot.reply_message(chatToken, FlexSendMessage('翻譯資訊', {
                "type": "carousel",
                "contents": [
                    {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"翻譯前:{before}",
                                    "color": "#2c3e50",
                                    "weight": "bold"
                                }
                            ],
                            "backgroundColor": "#1abc9c"
                        }
                    },
                    {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"翻譯後:{after}",
                                    "color": "#2c3e50",
                                    "weight": "bold"
                                }
                            ],
                            "backgroundColor": "#3498db"
                        }
                    },
                    {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "!複製:獲取翻譯後文字",
                                    "color": "#2c3e50",
                                    "weight": "bold"
                                }
                            ],
                            "backgroundColor": "#feca57"
                        }
                    }
                ]
            }))
            countdown = 15
            while countdown:
                if user_id in using:
                    countdown = 0
                    using.clear()
                else:
                    print(countdown),
                    countdown -= 1
                    time.sleep(1)
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            transName.clear()
        elif "!複製" in msg:
            bot.reply_message(chatToken, TextSendMessage(after))
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            using.append(user_id)
        elif "!停止" in msg:
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            bot.reply_message(chatToken, TextSendMessage("翻譯程序已結束"))
    elif user_id in waiting2:
        if "!發送" in msg:
            send()
            bot.reply_message(chatToken, TextSendMessage("發送郵件成功"))
            waiting2.remove(user_id)
            waitName.clear()
        elif "!停止" in msg:
            bot.reply_message(chatToken, TextSendMessage("郵件傳送已停止"))
            waiting2.remove(user_id)
            emails.clear()
            waitName.clear()
            return
    elif user_id in waiting:
        if "!收件人:" in msg:
            target = msg.replace("!收件人:", "")
            emails.append(target)
            bot.reply_message(chatToken,
                              TextSendMessage(f"收件人:{target}\n請輸入郵件標題(主旨)\nEx:\n!主旨:信用卡到期通知\n(記得打!主旨:  )\n請用半形的標點符號!!"))
            return
        elif "!主旨:" in msg:
            subject = msg.replace("!主旨:", "")
            emails.append(subject)
            target2 = emails[0]
            subject2 = emails[1]
            bot.reply_message(chatToken, TextSendMessage(
                f"收件人:{target2}\n主旨:{subject2}\n請輸入!內容\nEx:\n!內容:ianchen您好你的信用卡...\n(記得打!內容:  )\n請用半形的標點符號!!"))
            return
        elif "!內容:" in msg:
            body = msg.replace("!內容:", "")
            emails.append(body)
            target3 = emails[0]
            subject3 = emails[1]
            body3 = emails[2]
            bot.reply_message(chatToken, TextSendMessage(
                f"收件人:{target3}\n主旨:{subject3}\n內容:{body3}\n++確認無誤後請打++\n!郵件確認\n(有誤時打\n!停止\n全部重來)"))
            return
        elif "!郵件確認" in msg:
            bot.reply_message(chatToken, TextSendMessage(f"<=郵件確認=>\n打!檢查郵件\n可以確認郵件內容"))
        elif "!檢查郵件" in msg:
            target4 = emails[0]
            subject4 = emails[1]
            body4 = emails[2]
            bot.reply_message(chatToken, TextSendMessage(
                f"收件人:{target4}\n主旨:{subject4}\n內容:{body4}\n++檢查郵件++\n確認完畢後請打\n!發送\n有錯打!停止全部重來"))
            waiting2.append(user_id)
            waiting.remove(user_id)
        else:
            if "!停止" in msg:
                bot.reply_message(chatToken, TextSendMessage("郵件傳送已停止"))
                waiting.remove(user_id)
                emails.clear()
                waitName.clear()
                return
            else:
                bot.reply_message(chatToken, TextSendMessage("格式錯誤 請在輸入一次哦~\n要中止郵件功能請打\n!停止"))
    elif user_id in sent:
        if msg == "!迷因":
            lease = sent[f"{user_id}"]
            bot.reply_message(chatToken, TextSendMessage(f"迷因系統冷卻中，還有\n"
                                                         f"{lease}/10秒"))
    elif msg == "!所有訊息":
        try:
            allCmessage = ""
            for i in allMessage:
                allCmessage += i
            bot.reply_message(chatToken, TextSendMessage(allCmessage))
        except:
            allMessage.clear()
            bot.reply_message(chatToken, TextSendMessage("字數超過5000字已清空列表"))
    elif msg == "!幫助":
        bot.reply_message(chatToken, TextSendMessage("⚠=🤍=🤖=指令區=🤖=🤍=\n"
                                                     "🔰功能指令🔰\n"
                                                     "1.!請離開:讓機器人離開群組\n"
                                                     "2.!個人資料:自己的個人資料\n"
                                                     "3.!群組資料:目前群組資料\n"
                                                     "4.!:一個驚嘆號查看收回的訊息\n"
                                                     "5.!全:查看收回訊息前20\n"
                                                     "6.!戰鬥系統:說明RPG玩法\n"
                                                     "(戰鬥系統為新功能)\n"
                                                     "❤小遊戲❤\n"
                                                     "1.!猜拳 @(標記你要的人)\n"
                                                     "2.!比大小 @(標記你要的人)\n"
                                                     "🎁娛樂指令🎁\n"
                                                     "1.!迷因:隨機台灣迷因\n"
                                                     "2.!等級:查詢目前個人等級\n"
                                                     "3.!等級 @(標記你要的人):\n"
                                                     "查詢他的個人等級\n"
                                                     "4.!聊天 開:開啟聊天模式\n"
                                                     "5.!聊天 關:關閉聊天模式\n"
                                                     "6.學;輸入;輸出:聊天功能學習\n"
                                                     "7.!聊天說明:說明聊天功能\n"
                                                     "8.!排行榜:查看前20總等級排行榜\n"
                                                     "🚩實用小功能指令🚩\n"
                                                     "1.!天氣:及時查看未來天氣\n"
                                                     "2.!唬爛:用了就知道多強大\n"
                                                     "(唬爛為您的心得小幫手)\n"
                                                     "3.!小冷:隨機冷知識\n"
                                                     "4.!肉搜:查詢該ip相關資訊\n"
                                                     "❗注意❗\n"
                                                     "1.!所有指令請使用半形符號!\n"
                                                     "2.等級系統使用說明:\n"
                                                     "在聊天室每次發送訊息會增加\n"
                                                     "5-10經驗值(有防刷功能)\n"
                                                     "3.翻譯系統:如果15秒內沒打\n"
                                                     "!複製or!停止\n"
                                                     "系統將會自動退出翻譯程序\n"
                                                     " 🛑此為群組機器人🛑\n"
                                                     "🛑私聊版本還未開放🛑"))
    elif msg == "!個人資料":
        bot.reply_message(chatToken, TextSendMessage(f"您的user_ID為:{user_id}"))
    elif msg == "!群組資料":
        team = bot.get_group_summary(event.source.group_id)
        group_count = bot.get_group_members_count(event.source.group_id)
        bgok = str(group_count + 1)
        print("群組id:" + team.group_id)
        print("群組名字:" + team.group_name)
        print("群組照片:" + team.picture_url)
        print("群組總人數:" + str(group_count + 1))
        time.sleep(1)
        bot.reply_message(chatToken, FlexSendMessage('群組資料', {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": team.picture_url,
                "margin": "none",
                "size": "full",
                "offsetTop": "none",
                "offsetBottom": "none",
                "offsetEnd": "none",
                "aspectRatio": "1:1",
                "position": "relative",
                "flex": 20
            },
            "body": {
                "type": "box",
                "layout": "baseline",
                "contents": [
                    {
                        "type": "text",
                        "text": f"༺๑{team.group_name}๑༻",
                        "size": "3xl",
                        "color": "#c74385",
                        "weight": "bold",
                        "contents": [],
                        "align": "center"
                    }
                ],
                "backgroundColor": "#42515a"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Group_ID",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#bfbcbd",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": team.group_id,
                        "size": "sm",
                        "weight": "bold",
                        "style": "italic",
                        "color": "#fdfdfb",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "群組人數",
                                "size": "xl",
                                "weight": "bold",
                                "color": "#bfbcbd",
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": bgok,
                                "size": "lg",
                                "weight": "bold",
                                "color": "#fdfdfb",
                                "align": "center"
                            }
                        ],
                        "margin": "40px",
                        "spacing": "10px"
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                                "type": "icon",
                                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                "margin": "none",
                                "aspectRatio": "19:18"
                            },
                            {
                                "type": "text",
                                "text": "群組",
                                "color": "#ffd400",
                                "size": "lg",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": "#42515a",
                        "borderWidth": "none"
                    }
                ],
                "backgroundColor": "#42515a",
                "spacing": "10px"
            },
            "styles": {
                "header": {
                    "separator": True,
                    "backgroundColor": "#ff9900",
                    "separatorColor": "#ff9900"
                }
            }
        }))
    elif msg == "!請離開":
        bot.reply_message(chatToken, TextSendMessage("為什麼要叫我離開QAQ"))
        bot.leave_group(event.source.group_id)
    elif msg == "!全" or msg == "！全":
        message = "收回訊息前20:\n"
        ctt = 1
        for i in unsendlist:
            profile = bot.get_group_member_profile(unsendall[i]['group'], unsendall[i]['user'])
            message += f"{str(ctt)}.{profile.display_name}:" \
                       f"{unsendall[i]['msg']}\n"
            ctt += 1
        bot.reply_message(event.reply_token, TextSendMessage(message))
    elif msg == "!clear":
        if user_id == "Uddb208c296fcbafbff7c0488824d3471":
            unsendall.clear()
            unsendlist.clear()
            bot.reply_message(event.reply_token, TextSendMessage("清除成功"))
        else:
            bot.reply_message(event.reply_token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    elif msg == "!" or msg == "！":
        profile = bot.get_group_member_profile(unsend1[2], unsend1[1])
        team = bot.get_group_summary(unsend1[2])
        tz = timezone(timedelta(hours=+8))
        isotime = datetime.now(tz).isoformat()
        now = datetime.fromisoformat(isotime)
        head, sep, tail = str(now).partition('.')
        bot.reply_message(event.reply_token, TextSendMessage("使用者:\n" +
                                                             f"[{profile.display_name}]" +
                                                             "\n在:\n" +
                                                             f"[{team.group_name}]" +
                                                             "\n最近一次收回的訊息:\n" +
                                                             f"[{cached_messages[unsend1[0]]}]" +
                                                             "\n收回時台灣時間:\n" +
                                                             f"[{now1[0]}]" +
                                                             "\n現在台灣時間:\n" +
                                                             f"[{head}]"))
    elif msg == "!迷因":
        img = random.choice(results)
        image_message = ImageSendMessage(
            original_content_url=img[0]['data-src'],
            preview_image_url=img[0]['data-src']
        )
        bot.reply_message(chatToken, image_message)
        sent[f"{user_id}"] = 10
        while sent[f"{user_id}"] > 0:
            sent[f"{user_id}"] -= 1
            time.sleep(1)
        del sent[f"{user_id}"]
    elif msg == "!唬爛":
        bot.reply_message(chatToken, TextSendMessage("請輸入你要唬爛的主題:"))
        bullshit0.append(user_id)
    elif event.message.text == "!郵件":
        if len(waiting) == True:
            waitName2 = waitName[0]
            bot.reply_message(chatToken, TextSendMessage(f"郵件系統 {waitName2} \n在使用中請稍後"))
            return
        else:
            profile = bot.get_group_member_profile(event.source.group_id, user_id)
            bot.reply_message(chatToken,
                              TextSendMessage("請輸入目標郵件Ex:\n!收件人:ianchen@gmail.com\n(記得打!收件人:  )\n請用半形的標點符號!!"))
            waiting.append(user_id)
            waitName.append(profile.display_name)
    elif msg == "!翻譯":
        profile = bot.get_group_member_profile(event.source.group_id, user_id)
        if len(trans1) == True:
            transUser = transName[0]
            bot.reply_message(chatToken, TextSendMessage(f"翻譯系統 {transUser} \n在使用中請稍後"))
            return
        elif len(trans2) == True:
            transUser = transName[0]
            bot.reply_message(chatToken, TextSendMessage(f"翻譯系統 {transUser} \n在使用中請稍後"))
            return
        elif len(trans3) == True:
            transUser = transName[0]
            bot.reply_message(chatToken, TextSendMessage(f"翻譯系統 {transUser} \n在使用中請稍後"))
            return
        else:
            bot.reply_message(chatToken, TextSendMessage("請輸入你想翻譯的文字Ex:\nわたしは、あなたを愛しています"))
            trans1.append(user_id)
            transName.append(profile.display_name)
    elif msg == "!天氣":
        print(user_id)
        bot.reply_message(chatToken, TextSendMessage("請輸入您要查詢的地區Ex:\n"
                                                     "宜蘭縣\n"
                                                     "花蓮縣\n"
                                                     "臺東縣\n"
                                                     "澎湖縣\n"
                                                     "金門縣\n"
                                                     "連江縣\n"
                                                     "臺北市\n"
                                                     "新北市\n"
                                                     "桃園市\n"
                                                     "臺中市\n"
                                                     "臺南市\n"
                                                     "高雄市\n"
                                                     "基隆市\n"
                                                     "新竹縣\n"
                                                     "新竹市\n"
                                                     "苗栗縣\n"
                                                     "彰化縣\n"
                                                     "南投縣\n"
                                                     "雲林縣\n"
                                                     "嘉義縣\n"
                                                     "嘉義市\n"
                                                     "屏東縣"))
        waitWeather.append(user_id)
    elif msg == "!聊天 開":
        if eb.find_one({'group_id': event.source.group_id}) is None:
            data = {
                "group_id": event.source.group_id,
                "enable": "True"
            }
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("聊天功能已開啟\n如果沒反應請再打一次"))
        else:
            data = {
                "group_id": event.source.group_id,
                "enable": "True"
            }
            eb.delete_one({"group_id": event.source.group_id})
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("聊天功能已開啟\n如果沒反應請再打一次"))
    elif msg == "!聊天說明":
        bot.reply_message(chatToken, TextSendMessage("==聊天功能使用說明==\n"
                                                     "!聊天 開:開啟聊天\n"
                                                     "!聊天 關:關閉聊天\n"
                                                     "學;輸入;輸出\n"
                                                     "Ex:學;早安;早呀\n"
                                                     "學習功能在\n"
                                                     "機器人私聊\n"
                                                     "群組\n"
                                                     "都能用\n"
                                                     "格式都是\n"
                                                     "學;輸入;輸出"))
    elif msg == "!聊天 關":
        if eb.find_one({'group_id': event.source.group_id}) is None:
            data = {
                "group_id": event.source.group_id,
                "enable": "False"
            }
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("聊天功能已關閉"))
        else:
            data = {
                "group_id": event.source.group_id,
                "enable": "False"
            }
            eb.delete_one({"group_id": event.source.group_id})
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("聊天功能已關閉"))
    elif tic.find_one({"被攻擊者": user_id}) is not None:
        if msg == "!我願意" and user_id == tic.find_one({"被攻擊者": user_id})["被攻擊者"]:
            if user_id not in rpswait:
                tic.update_one({"被攻擊者": user_id}, {"$set": {"接受": "接受"}})
                bot.reply_message(chatToken, FlexSendMessage('WebHook', {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "請選擇",
                                "weight": "bold",
                                "align": "center",
                                "margin": "xxl",
                                "size": "4xl",
                                "color": "#535f65",
                                "style": "normal",
                                "decoration": "none"
                            }
                        ],
                        "backgroundColor": "#d0effe",
                        "flex": 5
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "剪刀",
                                    "data": "1"
                                },
                                "color": "#e2f5fe",
                                "style": "secondary",
                                "flex": 9
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "石頭",
                                    "data": "2"
                                },
                                "color": "#e2f5fe",
                                "style": "secondary",
                                "margin": "lg"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "布",
                                    "data": "3"
                                },
                                "color": "#e2f5fe",
                                "style": "secondary",
                                "flex": 9,
                                "margin": "lg"
                            }
                        ],
                        "backgroundColor": "#d0effe"
                    }
                }))
                rpswait.append(user_id)
        elif msg == "!我不願意" and user_id == tic.find_one({"被攻擊者": user_id})["被攻擊者"]:
            tic.delete_one({"被攻擊者": user_id})
            bot.reply_message(chatToken, TextSendMessage("抱歉 此挑戰被拒絕"))
    elif msg == "!肉搜":
        bot.reply_message(chatToken, TextSendMessage("請輸入你要查詢的ip:\n"
                                                     "Ex:123.195.16.26"))
        ip.append(user_id)
    elif msg == "!del":
        if user_id == "Uddb208c296fcbafbff7c0488824d3471":
            bot.reply_message(chatToken, TextSendMessage("請輸入要刪除的名稱:"))
            admin.append(user_id)
        else:
            bot.reply_message(chatToken, TextSendMessage("抱歉 您沒有權限使用這條指令"))
    elif "油價" in msg:
        r = requests.get('https://gasoline.weiyuan.com.tw', timeout=1)
        soup = BeautifulSoup(r.text, 'html.parser')
        # 下週油價預測
        try:
            NTweek = soup.find('h2', class_='h4 pull-left page-title mt-0').getText()
            size = "xxl"
            ntcolor = "#F2AA4CFF"
        except:
            NTweek = soup.find('h2', class_='h4 pull-left page-title mt-0 text-danger').getText()
            size = "xl"
            ntcolor = "#b20000"
        try:
            NTgas = soup.find_all('span', class_='text-success', style='font-size: 40px;')[0].getText()
            NTfuel = soup.find_all('span', class_='text-success', style='font-size: 40px;')[1].getText()
        except:
            NTgas = soup.find_all('span', class_='text-danger', style='font-size: 40px;')[0].getText()
            NTfuel = soup.find_all('span', class_='text-danger', style='font-size: 40px;')[1].getText()
        if '降' in NTgas:
            gascolor = '#00FF00'
        if '降' in NTfuel:
            fuelcolor = '#00FF00'
        if '漲' in NTgas:
            gascolor = '#FF0000'
        if '漲' in NTfuel:
            fuelcolor = '#FF0000'
        # 今日油價
        TSweek = soup.find_all('h1', class_='h4 pull-left page-title')[1].getText()
        # 油品
        T98 = soup.find_all('tr')[9].find_all('th')[1].getText()
        T95 = soup.find_all('tr')[9].find_all('th')[2].getText()
        T92 = soup.find_all('tr')[9].find_all('th')[3].getText()
        Tfuel = soup.find_all('tr')[9].find_all('th')[4].getText()
        # 中油
        M98p = soup.find_all('tr')[10].find_all('td')[0].getText()
        M95p = soup.find_all('tr')[10].find_all('td')[1].getText()
        M92p = soup.find_all('tr')[10].find_all('td')[2].getText()
        Mfuelp = soup.find_all('tr')[10].find_all('td')[3].getText()
        # 石化
        S98p = soup.find_all('tr')[11].find_all('td')[0].getText()
        S95p = soup.find_all('tr')[11].find_all('td')[1].getText()
        S92p = soup.find_all('tr')[11].find_all('td')[2].getText()
        Sfuelp = soup.find_all('tr')[11].find_all('td')[3].getText()
        print(NTweek.split('(')[1])
        bot.reply_message(chatToken, FlexSendMessage('近期油價', {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": "https://i.imgur.com/7qV1hwp.png",
                        "position": "absolute",
                        "offsetTop": "xxl",
                        "offsetStart": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "近期油價",
                                "align": "center",
                                "offsetTop": "xxl",
                                "weight": "bold",
                                "size": "3xl",
                                "offsetStart": "sm",
                                "color": "#89ABE3FF"
                            }
                        ],
                        "offsetStart": "xxl",
                        "width": "300px",
                        "height": "130px",
                        "offsetEnd": "none",
                        "offsetTop": "md"
                    }
                ],
                "width": "300px",
                "height": "120px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"● {NTweek.split('(')[0].replace(' ', '')}",
                        "weight": "bold",
                        "size": size,
                        "color": ntcolor
                    },
                    {
                        "type": "text",
                        "text": f"◉ ({NTweek.split('(')[1]}",
                        "style": "normal",
                        "align": "start",
                        "weight": "bold",
                        "color": "#F2AA4CFF",
                        "margin": "md",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": f"➤ 汽油:{NTgas}",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "xxl",
                        "color": f"{gascolor}"
                    },
                    {
                        "type": "text",
                        "text": f"➤ 柴油:{NTfuel}",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "sm",
                        "color": f"{fuelcolor}"
                    },
                    {
                        "type": "text",
                        "text": f"● {TSweek.split('(')[0].replace(' ', '')}",
                        "weight": "bold",
                        "size": "xxl",
                        "color": "#F2AA4CFF",
                        "margin": "xxl"
                    },
                    {
                        "type": "text",
                        "text": f"◉ ({TSweek.split('(')[1]}",
                        "style": "normal",
                        "align": "start",
                        "weight": "bold",
                        "color": "#F2AA4CFF",
                        "margin": "md",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": "➤98無鉛",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md",
                        "color": "#ADEFD1FF",
                        "contents": [
                            {
                                "type": "span",
                                "text": "♦ 台灣中油",
                                "color": "#89ABE3FF",
                                "size": "3xl"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"➤ {T98}: {M98p} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"➤ {T95}: {M95p} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"➤ {T92}: {M92p} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"➤ {Tfuel}: {Mfuelp} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": "➤98無鉛",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md",
                        "color": "#ADEFD1FF",
                        "contents": [
                            {
                                "type": "span",
                                "text": "♦ 台塑石化",
                                "color": "#89ABE3FF",
                                "size": "3xl"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"➤ {T98}: {S98p} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"➤ {T95}: {S95p} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"➤ {T92}: {S92p} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"➤ {Tfuel}: {Sfuelp} 元",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    }
                ],
                "offsetTop": "md",
                "width": "900px"
            },
            "styles": {
                "header": {
                    "backgroundColor": "#101820FF"
                },
                "body": {
                    "backgroundColor": "#101820FF"
                }
            }
        }))
    elif event.message.text.startswith("!"):
        try:
            cmds = Commands(bot, chatToken)

            a = event.message.text.split(" ")
            cmd = a[0].replace("!", "")
            args = a.pop(0)
            eval(f"cmds.{cmd}(event, args)")
        except Exception as e:
            bot.reply_message(chatToken, TextSendMessage(str(e)))
    else:
        grout = eb.find_one({'group_id': event.source.group_id})
        user_data = gb.find_one({"user": event.source.user_id})
        if cb.find_one({'detect': msg}) is not None:
            if user_data is None:
                if grout['enable'] == "False":
                    take = bot.get_group_member_profile(event.source.group_id, user_id)
                    gb.insert({"name": take.display_name, "user": event.source.user_id, "exp": 0})
                elif grout['enable'] == "True":
                    take = bot.get_group_member_profile(event.source.group_id, user_id)
                    gb.insert({"name": take.display_name, "user": event.source.user_id, "exp": 0})
                    bot.reply_message(chatToken, TextSendMessage(cb.find_one({'detect': msg})['reply']))
            else:
                if grout['enable'] == "False":
                    try:
                        if count[user_id] > 0:
                            return
                    except KeyError:
                        pass
                    count[user_id] = 5
                    randomexp = random.randint(5, 10)
                    add_exp = user_data['exp'] + randomexp
                    gb.update_one({"user": event.source.user_id}, {"$set": {"exp": add_exp}})
                    print(randomexp)
                    level, exp, need = calc_rank(user_data['exp'])
                    level_, exp_, need_ = calc_rank(add_exp)
                    user = bot.get_profile(user_id)
                    if level_ > level:
                        bot.reply_message(chatToken,
                                          TextSendMessage(text=f"恭喜 {user.display_name} 從 {level}級 升級到 {level_}級 !"))
                elif grout['enable'] == "True":
                    try:
                        if count[user_id] > 0:
                            return
                    except KeyError:
                        pass
                    count[user_id] = 5
                    randomexp = random.randint(5, 10)
                    add_exp = user_data['exp'] + randomexp
                    gb.update_one({"user": event.source.user_id}, {"$set": {"exp": add_exp}})
                    print(randomexp)
                    level, exp, need = calc_rank(user_data['exp'])
                    level_, exp_, need_ = calc_rank(add_exp)
                    user = bot.get_profile(user_id)
                    bot.reply_message(chatToken, TextSendMessage(cb.find_one({'detect': msg})['reply']))
                    if level_ > level:
                        bot.reply_message(chatToken,
                                          TextSendMessage(text=f"恭喜 {user.display_name} 從 {level}級 升級到 {level_}級 !"))
        elif cb.find_one({'detect': msg}) is None:
            try:
                if user_data is None:
                    take = bot.get_group_member_profile(event.source.group_id, user_id)
                    gb.insert({"name": take.display_name, "user": event.source.user_id, "exp": 0})
                else:
                    try:
                        if count[user_id] > 0:
                            return
                    except KeyError:
                        pass
                    count[user_id] = 5
                    randomexp = random.randint(5, 10)
                    add_exp = user_data['exp'] + randomexp
                    gb.update_one({"user": event.source.user_id}, {"$set": {"exp": add_exp}})
                    print(randomexp)
                    level, exp, need = calc_rank(user_data['exp'])
                    level_, exp_, need_ = calc_rank(add_exp)
                    user = bot.get_profile(user_id)
                    if level_ > level:
                        bot.reply_message(chatToken,
                                          TextSendMessage(text=f"恭喜 {user.display_name} 從 {level}級 升級到 {level_}級 !"))
            except:
                if user_data is None:
                    take = bot.get_group_member_profile(event.source.group_id, user_id)
                    gb.insert({"name": take.display_name, "user": event.source.user_id, "exp": 0})
                else:
                    try:
                        if count[user_id] > 0:
                            return
                    except KeyError:
                        pass
                    count[user_id] = 5
                    randomexp = random.randint(5, 10)
                    add_exp = user_data['exp'] + randomexp
                    gb.update_one({"user": event.source.user_id}, {"$set": {"exp": add_exp}})
                    print(randomexp)
                    level, exp, need = calc_rank(user_data['exp'])
                    level_, exp_, need_ = calc_rank(add_exp)
                    user = bot.get_profile(user_id)
                    if level_ > level:
                        bot.reply_message(chatToken,
                                          TextSendMessage(text=f"恭喜 {user.display_name} 從 {level}級 升級到 {level_}級 !"))


if __name__ == "__main__":
    t = threading.Thread(target=cooldown)
    t.start()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
