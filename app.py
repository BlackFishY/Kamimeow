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
        print("????????????")
        emails.clear()


# ??????
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


# ?????????????????? /callback ??? Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print("??????:" + signature)
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
    bot.reply_message(chatToken, FlexSendMessage('????????????', {
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
                            "text": "???????????????",
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
                                    "text": "??? !?????? ?????????????????????",
                                    "color": "#fffef6",
                                    "size": "xl",
                                    "weight": "bold",
                                    "align": "center",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "(???????????????)",
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
    print("????????????????????????")
    if eb.find_one({'group_id': event.source.group_id}) is None:
        data = {
            "group_id": event.source.group_id,
            "enable": "True"
        }
        eb.insert(data)
        bot.reply_message(chatToken, TextSendMessage(text="???????????????????????????????????????\n"
                                                          "???????????????????????????\n"
                                                          "!?????? ???????????????????????????\n"
                                                          "!????????????:??????RPG??????\n"
                                                          "?????????????????????????????????????????????\n"
                                                          "?????????????????????!??????\n"
                                                          "(???????????????)"))
        print(group_id)
    else:
        bot.reply_message(chatToken, TextSendMessage(text="???????????????????????????????????????\n"
                                                          "???????????????????????????\n"
                                                          "!?????? ???????????????????????????\n"
                                                          "!????????????:??????RPG??????\n"
                                                          "?????????????????????????????????????????????\n"
                                                          "?????????????????????!??????\n"
                                                          "(???????????????)"))
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
    if tic.find_one({"?????????": user_id}) is not None:
        if tic.find_one({"?????????": user_id})["????????????"] != "??????":
            bot.reply_message(chatToken, TextSendMessage(f"{profile.display_name}???????????????????????????!"))
        if postback == "1" and tic.find_one({"?????????": user_id})["????????????"] == "??????" and tic.find_one({"?????????": user_id})[
            "???????????????"] == "??????":
            tic.update_one({"?????????": user_id}, {"$set": {"????????????": "???????"}})
        if postback == "2" and tic.find_one({"?????????": user_id})["????????????"] == "??????" and tic.find_one({"?????????": user_id})[
            "???????????????"] == "??????":
            tic.update_one({"?????????": user_id}, {"$set": {"????????????": "???????"}})
        if postback == "3" and tic.find_one({"?????????": user_id})["????????????"] == "??????" and tic.find_one({"?????????": user_id})[
            "???????????????"] == "??????":
            tic.update_one({"?????????": user_id}, {"$set": {"????????????": "???????"}})
        if postback == "1" and tic.find_one({"?????????": user_id})["????????????"] == "??????" and tic.find_one({"?????????": user_id})[
            "???????????????"] != "??????":
            tic.update_one({"?????????": user_id}, {"$set": {"????????????": "???????"}})
            atkuser = tic.find_one({"?????????": user_id})["?????????"]
            gotatkuser = tic.find_one({"?????????": user_id})["????????????"]
            atk = tic.find_one({"?????????": user_id})["????????????"]
            gotatk = tic.find_one({"?????????": user_id})["???????????????"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"????????????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{gotatkname.display_name}??????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{atkname.display_name}??????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
        if postback == "2" and tic.find_one({"?????????": user_id})["????????????"] == "??????" and tic.find_one({"?????????": user_id})[
            "???????????????"] != "??????":
            tic.update_one({"?????????": user_id}, {"$set": {"????????????": "???????"}})
            atkuser = tic.find_one({"?????????": user_id})["?????????"]
            gotatkuser = tic.find_one({"?????????": user_id})["????????????"]
            atk = tic.find_one({"?????????": user_id})["????????????"]
            gotatk = tic.find_one({"?????????": user_id})["???????????????"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{atkname.display_name}??????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"????????????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{gotatkname.display_name}??????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
        if postback == "3" and tic.find_one({"?????????": user_id})["????????????"] == "??????" and tic.find_one({"?????????": user_id})[
            "???????????????"] != "??????":
            tic.update_one({"?????????": user_id}, {"$set": {"????????????": "???????"}})
            atkuser = tic.find_one({"?????????": user_id})["?????????"]
            gotatkuser = tic.find_one({"?????????": user_id})["????????????"]
            atk = tic.find_one({"?????????": user_id})["????????????"]
            gotatk = tic.find_one({"?????????": user_id})["???????????????"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{gotatkname.display_name}??????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{atkname.display_name}??????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
            if atk == "???????" and gotatk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"????????????"))
                tic.delete_one({"?????????": user_id})
                rpswait.remove(gotatkuser)
    if tic.find_one({"????????????": user_id}) is not None:
        if tic.find_one({"????????????": user_id})["???????????????"] != "??????":
            bot.reply_message(chatToken, TextSendMessage(f"{profile.display_name}???????????????????????????!"))
        if postback == "1" and tic.find_one({"????????????": user_id})["???????????????"] == "??????" and tic.find_one({"????????????": user_id})[
            "????????????"] == "??????":
            tic.update_one({"????????????": user_id}, {"$set": {"???????????????": "???????"}})
        if postback == "2" and tic.find_one({"????????????": user_id})["???????????????"] == "??????" and tic.find_one({"????????????": user_id})[
            "????????????"] == "??????":
            tic.update_one({"????????????": user_id}, {"$set": {"???????????????": "???????"}})
        if postback == "3" and tic.find_one({"????????????": user_id})["???????????????"] == "??????" and tic.find_one({"????????????": user_id})[
            "????????????"] == "??????":
            tic.update_one({"????????????": user_id}, {"$set": {"???????????????": "???????"}})
        if postback == "1" and tic.find_one({"????????????": user_id})["???????????????"] == "??????" and tic.find_one({"????????????": user_id})[
            "????????????"] != "??????":
            tic.update_one({"????????????": user_id}, {"$set": {"???????????????": "???????"}})
            atkuser = tic.find_one({"????????????": user_id})["?????????"]
            gotatkuser = tic.find_one({"????????????": user_id})["????????????"]
            atk = tic.find_one({"????????????": user_id})["????????????"]
            gotatk = tic.find_one({"????????????": user_id})["???????????????"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"????????????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{atkname.display_name}??????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{gotatkname.display_name}??????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
        if postback == "2" and tic.find_one({"????????????": user_id})["???????????????"] == "??????" and tic.find_one({"????????????": user_id})[
            "????????????"] != "??????":
            tic.update_one({"????????????": user_id}, {"$set": {"???????????????": "???????"}})
            atkuser = tic.find_one({"????????????": user_id})["?????????"]
            gotatkuser = tic.find_one({"????????????": user_id})["????????????"]
            atk = tic.find_one({"????????????": user_id})["????????????"]
            gotatk = tic.find_one({"????????????": user_id})["???????????????"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{gotatkname.display_name}??????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"????????????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{atkname.display_name}??????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
        if postback == "3" and tic.find_one({"????????????": user_id})["???????????????"] == "??????" and tic.find_one({"????????????": user_id})[
            "????????????"] != "??????":
            tic.update_one({"????????????": user_id}, {"$set": {"???????????????": "???????"}})
            atkuser = tic.find_one({"????????????": user_id})["?????????"]
            gotatkuser = tic.find_one({"????????????": user_id})["????????????"]
            atk = tic.find_one({"????????????": user_id})["????????????"]
            gotatk = tic.find_one({"????????????": user_id})["???????????????"]
            atkname = bot.get_group_member_profile(event.source.group_id, atkuser)
            gotatkname = bot.get_group_member_profile(event.source.group_id, gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{atkname.display_name}??????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"?????????{gotatkname.display_name}??????"))
                tic.delete_one({"????????????": user_id})
                rpswait.remove(gotatkuser)
            if gotatk == "???????" and atk == "???????":
                bot.reply_message(chatToken, TextSendMessage(f"{atkname.display_name}???:???????\n"
                                                             f"{gotatkname.display_name}???:???????\n"
                                                             f"\n"
                                                             f"????????????"))
                tic.delete_one({"????????????": user_id})
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
    try: #?????????
        team = bot.get_group_summary(event.source.group_id)
        teamtake = bot.get_group_member_profile(event.source.group_id, user_id)
        allMessage.append(f"???????????:???{teamtake.display_name}???\n"
                          f"????:???{team.group_name}???\n"
                          f"????:???{msg}???\n"
                          f"\n")
    except:  #??????
        alone = bot.get_profile(user_id)
        allMessage.append(f"???????????:???{alone.display_name}???\n"
                          f"????:???????????????????????????\n"
                          f"????:???{msg}???\n"
                          f"\n")

    if len(unsendlist) >= 20:
        unsendlist.clear()
        unsendall.clear()
    elif msg == "!????????????":
        allMessage.clear()
        bot.reply_message(chatToken, TextSendMessage("?????????allMessage"))
    elif bk.find_one({"user": user_id}) is not None:
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        if user_id == "Uf5eefecbe1bedaf8f228eb1552e3832f":
            bot.reply_message(chatToken, TextSendMessage("?????????????????????????????????"))
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
    elif "????????????" in msg:
        bot.reply_message(chatToken, TextSendMessage("???????????????????????????(????????????):\n"
                                                     "https://tw-covid-19.herokuapp.com"))
    elif "???" in msg and len(lender) == 3:
        d = cb.find_one({'detect': str(lender[1])})
        if d is None:
            test = bot.get_profile(user_id)
            data = {
                'name': test.display_name,
                'detect': str(lender[1]),
                'reply': str(lender[2])
            }
            cb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("???????????????+1"))
        else:
            test = bot.get_profile(user_id)
            data = {
                'name': test.display_name,
                'detect': str(lender[1]),
                'reply': str(lender[2])
            }
            cb.delete_one({"detect": str(lender[1])})
            cb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("???????????????+1"))
    elif user_id in admin:
        gb.delete_one({"name": msg})
        bot.reply_message(chatToken, TextSendMessage("????????????"))
        admin.remove(user_id)
    elif user_id in ip:
        try:
            r = requests.get(f'https://ipapi.co/{msg}/json/', timeout=1)
            j = json.loads(r.text)
            bot.reply_message(chatToken, TextSendMessage(f"IP:{j['ip']}\n"
                                                         f"??????:{j['version']}\n"
                                                         f"??????:{j['city']}\n"
                                                         f"??????:{j['region']}\n"
                                                         f"??????:{j['region_code']}\n"
                                                         f"??????:{j['country']}\n"
                                                         f"??????:{j['country_name']}\n"
                                                         f"????????????:{j['country_code']}\n"
                                                         f"???????????????:{j['country_code_iso3']}\n"
                                                         f"????????????:{j['country_tld']}\n"
                                                         f"????????????:{j['continent_code']}\n"
                                                         f"??????:{j['in_eu']}\n"
                                                         f"??????:{j['postal']}\n"
                                                         f"??????:{j['latitude']}\n"
                                                         f"??????:{j['longitude']}\n"
                                                         f"??????:{j['timezone']}\n"
                                                         f"??????+:{j['utc_offset']}\n"
                                                         f"????????????:{j['country_calling_code']}\n"
                                                         f"??????:{j['currency']}\n"
                                                         f"??????:{j['languages']}\n"
                                                         f"????????????:{j['country_area']}\n(?????????)\n"
                                                         f"????????????:{j['country_population']}\n"
                                                         f"???????????????:{j['asn']}\n"
                                                         f"????????????:{j['org']}"))
            ip.remove(user_id)
        except:
            bot.reply_message(chatToken, TextSendMessage("???????????????IP"))
    elif user_id in bullshit1:
        tint = int(msg)
        try:
            if tint < 100 or tint > 1000:
                bot.reply_message(chatToken, TextSendMessage("?????????100-1000???????????????"))
            else:
                payload = {
                    "Topic": bullshit.find_one({"user": user_id})["??????"],
                    "MinLen": tint
                }
                res = requests.post("https://api.howtobullshit.me/bullshit", json=payload)
                text = res.text
                output = text.replace('&nbsp;', '').replace('<br><br>', '')
                bot.reply_message(chatToken, TextSendMessage(output))
                bullshit1.remove(user_id)
                bullshit.delete_one({"user": user_id})
        except ValueError:
            bot.reply_message(chatToken, TextSendMessage("?????????100-1000???????????????"))
    elif user_id in bullshit0:
        bot.reply_message(chatToken, TextSendMessage(f"?????????????????????{msg}\n"
                                                     f"???????????????????????????\n"
                                                     f"100-1000"))
        bullshit0.remove(user_id)
        bullshit1.append(user_id)
        data = {
            "user": user_id,
            "??????": msg
        }
        bullshit.insert(data)
    elif user_id in waitWeather:
        weathermsg = msg.replace('???', '???')
        if msg == "??????":
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
            return
        elif weathermsg in "?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????," \
                           " ?????????":
            weather = requests.get(url + weathermsg)
            data = weather.json()
            a = data["records"]["location"][0]
            # ?????????
            City = a["locationName"]
            # ??????????????????
            start1 = a["weatherElement"][0]["time"][0]["startTime"]
            start2 = a["weatherElement"][0]["time"][1]["startTime"]
            start3 = a["weatherElement"][0]["time"][2]["startTime"]
            over1 = a["weatherElement"][0]["time"][0]["endTime"]
            over2 = a["weatherElement"][0]["time"][1]["endTime"]
            over3 = a["weatherElement"][0]["time"][2]["endTime"]
            # Wx????????????
            weatherdes1 = a["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
            weatherdes2 = a["weatherElement"][0]["time"][1]["parameter"]["parameterName"]
            weatherdes3 = a["weatherElement"][0]["time"][2]["parameter"]["parameterName"]
            # PoP???????????? # ?????????%
            maybe1 = a["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
            maybe2 = a["weatherElement"][1]["time"][1]["parameter"]["parameterName"]
            maybe3 = a["weatherElement"][1]["time"][2]["parameter"]["parameterName"]
            # MinT????????? #???C
            cold1 = a["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
            cold2 = a["weatherElement"][2]["time"][1]["parameter"]["parameterName"]
            cold3 = a["weatherElement"][2]["time"][2]["parameter"]["parameterName"]
            # MaxT????????? #???C
            hot1 = a["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
            hot2 = a["weatherElement"][4]["time"][1]["parameter"]["parameterName"]
            hot3 = a["weatherElement"][4]["time"][2]["parameter"]["parameterName"]
            # CI?????????
            comfor1 = a["weatherElement"][3]["time"][0]["parameter"]["parameterName"]
            comfor2 = a["weatherElement"][3]["time"][1]["parameter"]["parameterName"]
            comfor3 = a["weatherElement"][3]["time"][2]["parameter"]["parameterName"]
            bot.reply_message(chatToken, FlexSendMessage('????????????', {
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
                                            "text": f"??????:{start1}",
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
                                            "text": f"??????:{weatherdes1}",
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
                                            "text": f"????????????:{maybe1}%",
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
                                            "text": f"?????????:{cold1}??C",
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
                                            "text": f"?????????:{hot1}??C",
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
                                            "text": f"?????????:{comfor1}",
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
                                            "text": f"??????:{over1}",
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
                                            "text": f"??????:{start2}",
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
                                            "text": f"??????:{weatherdes2}",
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
                                            "text": f"????????????:{maybe2}%",
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
                                            "text": f"?????????:{cold2}??C",
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
                                            "text": f"?????????:{hot2}??C",
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
                                            "text": f"?????????:{comfor2}",
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
                                            "text": f"??????:{over2}",
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
                                    "text": f"??????:{start3}",
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
                                    "text": f"??????:{weatherdes3}",
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
                                    "text": f"????????????:{maybe3}%",
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
                                    "text": f"?????????:{cold3}??C",
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
                                    "text": f"?????????:{hot3}??C",
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
                                    "text": f"?????????:{comfor3}",
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
                                    "text": f"??????:{over3}",
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
                                    "text": "??????",
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
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
            return
    elif user_id in trans1:
        unknown.append(msg)
        bot.reply_message(chatToken, TextSendMessage("????????????????????????????????????:\n"
                                                     "??????\n"
                                                     "??????\n"
                                                     "??????\n"
                                                     "???????????????\n"
                                                     "????????????\n"
                                                     "??????\n"
                                                     "????????????\n"
                                                     "????????????\n"
                                                     "???????????????\n"
                                                     "???????????????\n"
                                                     "????????????\n"
                                                     "????????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "????????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "??????????????????\n"
                                                     "????????????\n"
                                                     "??????\n"
                                                     "??????\n"
                                                     "????????????????????????"))
        trans1.remove(user_id)
        trans2.append(user_id)
    elif user_id in trans2:
        if "??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????\n??????????????????\n!??????"))
            trans.append("en")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????\n??????????????????\n!??????"))
            trans.append("ja")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????\n??????????????????\n!??????"))
            trans.append("ko")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "???????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????????????????????????????\n??????????????????\n!??????"))
            trans.append("zh-cn")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("zh-tw")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????\n??????????????????\n!??????"))
            trans.append("fr")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("fil")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("he")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "???????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("???????????????????????????\n??????????????????\n!??????"))
            trans.append("af")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "???????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("???????????????????????????\n??????????????????\n!??????"))
            trans.append("am")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("ar")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("bn")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("cs")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("da")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("nl")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("eo")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("el")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("haw")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("hi")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "?????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????\n!??????"))
            trans.append("it")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "??????????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????????????????\n??????????????????\n!??????"))
            trans.append("ru")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage("????????????????????????\n??????????????????\n!??????"))
            trans.append("es")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????\n??????????????????\n!??????"))
            trans.append("th")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("??????????????????\n??????????????????\n!??????"))
            trans.append("vi")
            trans3.append(user_id)
            trans2.remove(user_id)
        elif "!??????" in msg:
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            transName.clear()
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
            return
        else:
            bot.reply_message(chatToken, TextSendMessage("???????????????????????????~\n??????????????????\n??????????????????\n!??????"))
            return
    elif user_id in trans3:
        before = unknown[0]
        middle = trans[0]
        after = Translator().translate(before, "", middle)
        if "!??????" in msg:
            bot.reply_message(chatToken, FlexSendMessage('????????????', {
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
                                    "text": f"?????????:{before}",
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
                                    "text": f"?????????:{after}",
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
                                    "text": "!??????:?????????????????????",
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
        elif "!??????" in msg:
            bot.reply_message(chatToken, TextSendMessage(after))
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            using.append(user_id)
        elif "!??????" in msg:
            unknown.clear()
            trans.clear()
            trans1.clear()
            trans2.clear()
            trans3.clear()
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
    elif user_id in waiting2:
        if "!??????" in msg:
            send()
            bot.reply_message(chatToken, TextSendMessage("??????????????????"))
            waiting2.remove(user_id)
            waitName.clear()
        elif "!??????" in msg:
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
            waiting2.remove(user_id)
            emails.clear()
            waitName.clear()
            return
    elif user_id in waiting:
        if "!?????????:" in msg:
            target = msg.replace("!?????????:", "")
            emails.append(target)
            bot.reply_message(chatToken,
                              TextSendMessage(f"?????????:{target}\n?????????????????????(??????)\nEx:\n!??????:?????????????????????\n(?????????!??????:  )\n???????????????????????????!!"))
            return
        elif "!??????:" in msg:
            subject = msg.replace("!??????:", "")
            emails.append(subject)
            target2 = emails[0]
            subject2 = emails[1]
            bot.reply_message(chatToken, TextSendMessage(
                f"?????????:{target2}\n??????:{subject2}\n?????????!??????\nEx:\n!??????:ianchen?????????????????????...\n(?????????!??????:  )\n???????????????????????????!!"))
            return
        elif "!??????:" in msg:
            body = msg.replace("!??????:", "")
            emails.append(body)
            target3 = emails[0]
            subject3 = emails[1]
            body3 = emails[2]
            bot.reply_message(chatToken, TextSendMessage(
                f"?????????:{target3}\n??????:{subject3}\n??????:{body3}\n++?????????????????????++\n!????????????\n(????????????\n!??????\n????????????)"))
            return
        elif "!????????????" in msg:
            bot.reply_message(chatToken, TextSendMessage(f"<=????????????=>\n???!????????????\n????????????????????????"))
        elif "!????????????" in msg:
            target4 = emails[0]
            subject4 = emails[1]
            body4 = emails[2]
            bot.reply_message(chatToken, TextSendMessage(
                f"?????????:{target4}\n??????:{subject4}\n??????:{body4}\n++????????????++\n?????????????????????\n!??????\n?????????!??????????????????"))
            waiting2.append(user_id)
            waiting.remove(user_id)
        else:
            if "!??????" in msg:
                bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
                waiting.remove(user_id)
                emails.clear()
                waitName.clear()
                return
            else:
                bot.reply_message(chatToken, TextSendMessage("???????????? ?????????????????????~\n???????????????????????????\n!??????"))
    elif user_id in sent:
        if msg == "!??????":
            lease = sent[f"{user_id}"]
            bot.reply_message(chatToken, TextSendMessage(f"??????????????????????????????\n"
                                                         f"{lease}/10???"))
    elif msg == "!????????????":
        try:
            allCmessage = ""
            for i in allMessage:
                allCmessage += i
            bot.reply_message(chatToken, TextSendMessage(allCmessage))
        except:
            allMessage.clear()
            bot.reply_message(chatToken, TextSendMessage("????????????5000??????????????????"))
    elif msg == "!??????":
        bot.reply_message(chatToken, TextSendMessage("???=????=????=?????????=????=????=\n"
                                                     "????????????????????\n"
                                                     "1.!?????????:????????????????????????\n"
                                                     "2.!????????????:?????????????????????\n"
                                                     "3.!????????????:??????????????????\n"
                                                     "4.!:????????????????????????????????????\n"
                                                     "5.!???:?????????????????????20\n"
                                                     "6.!????????????:??????RPG??????\n"
                                                     "(????????????????????????)\n"
                                                     "???????????????\n"
                                                     "1.!?????? @(??????????????????)\n"
                                                     "2.!????????? @(??????????????????)\n"
                                                     "????????????????????\n"
                                                     "1.!??????:??????????????????\n"
                                                     "2.!??????:????????????????????????\n"
                                                     "3.!?????? @(??????????????????):\n"
                                                     "????????????????????????\n"
                                                     "4.!?????? ???:??????????????????\n"
                                                     "5.!?????? ???:??????????????????\n"
                                                     "6.???;??????;??????:??????????????????\n"
                                                     "7.!????????????:??????????????????\n"
                                                     "8.!?????????:?????????20??????????????????\n"
                                                     "?????????????????????????????\n"
                                                     "1.!??????:??????????????????\n"
                                                     "2.!??????:????????????????????????\n"
                                                     "3.!??????:????????????????????????\n"
                                                     "(??????????????????????????????)\n"
                                                     "4.!??????:???????????????\n"
                                                     "5.!??????:?????????ip????????????\n"
                                                     "????????????\n"
                                                     "1.!?????????????????????????????????!\n"
                                                     "2.????????????????????????:\n"
                                                     "???????????????????????????????????????\n"
                                                     "5-10?????????(???????????????)\n"
                                                     "3.????????????:??????15????????????\n"
                                                     "!??????or!??????\n"
                                                     "????????????????????????????????????\n"
                                                     "??????????????????:\n"
                                                     "https://tw-covid-19.herokuapp.com \n"
                                                     " ?????????????????????????????\n"
                                                     "????????????????????????????????"))
    elif msg == "!????????????":
        bot.reply_message(chatToken, TextSendMessage(f"??????user_ID???:{user_id}"))
    elif msg == "!????????????":
        team = bot.get_group_summary(event.source.group_id)
        group_count = bot.get_group_members_count(event.source.group_id)
        bgok = str(group_count + 1)
        print("??????id:" + team.group_id)
        print("????????????:" + team.group_name)
        print("????????????:" + team.picture_url)
        print("???????????????:" + str(group_count + 1))
        time.sleep(1)
        bot.reply_message(chatToken, FlexSendMessage('????????????', {
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
                        "text": f"??????{team.group_name}??????",
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
                                "text": "????????????",
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
                                "text": "??????",
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
    elif msg == "!?????????":
        bot.reply_message(chatToken, TextSendMessage("????????????????????????QAQ"))
        bot.leave_group(event.source.group_id)
    elif msg == "!???" or msg == "??????":
        message = "???????????????20:\n"
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
            bot.reply_message(event.reply_token, TextSendMessage("????????????"))
        else:
            bot.reply_message(event.reply_token, TextSendMessage("?????? ?????????????????????????????????"))
    elif msg == "!" or msg == "???":
        profile = bot.get_group_member_profile(unsend1[2], unsend1[1])
        team = bot.get_group_summary(unsend1[2])
        tz = timezone(timedelta(hours=+8))
        isotime = datetime.now(tz).isoformat()
        now = datetime.fromisoformat(isotime)
        head, sep, tail = str(now).partition('.')
        bot.reply_message(event.reply_token, TextSendMessage("?????????:\n" +
                                                             f"[{profile.display_name}]" +
                                                             "\n???:\n" +
                                                             f"[{team.group_name}]" +
                                                             "\n???????????????????????????:\n" +
                                                             f"[{cached_messages[unsend1[0]]}]" +
                                                             "\n?????????????????????:\n" +
                                                             f"[{now1[0]}]" +
                                                             "\n??????????????????:\n" +
                                                             f"[{head}]"))
    elif msg == "!??????":
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
    elif msg == "!??????":
        bot.reply_message(chatToken, TextSendMessage("??????????????????????????????:"))
        bullshit0.append(user_id)
    elif event.message.text == "!??????":
        if len(waiting) == True:
            waitName2 = waitName[0]
            bot.reply_message(chatToken, TextSendMessage(f"???????????? {waitName2} \n?????????????????????"))
            return
        else:
            profile = bot.get_group_member_profile(event.source.group_id, user_id)
            bot.reply_message(chatToken,
                              TextSendMessage("?????????????????????Ex:\n!?????????:ianchen@gmail.com\n(?????????!?????????:  )\n???????????????????????????!!"))
            waiting.append(user_id)
            waitName.append(profile.display_name)
    elif msg == "!??????":
        profile = bot.get_group_member_profile(event.source.group_id, user_id)
        if len(trans1) == True:
            transUser = transName[0]
            bot.reply_message(chatToken, TextSendMessage(f"???????????? {transUser} \n?????????????????????"))
            return
        elif len(trans2) == True:
            transUser = transName[0]
            bot.reply_message(chatToken, TextSendMessage(f"???????????? {transUser} \n?????????????????????"))
            return
        elif len(trans3) == True:
            transUser = transName[0]
            bot.reply_message(chatToken, TextSendMessage(f"???????????? {transUser} \n?????????????????????"))
            return
        else:
            bot.reply_message(chatToken, TextSendMessage("??????????????????????????????Ex:\n?????????????????????????????????????????????"))
            trans1.append(user_id)
            transName.append(profile.display_name)
    elif msg == "!??????":
        print(user_id)
        bot.reply_message(chatToken, TextSendMessage("??????????????????????????????Ex:\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????\n"
                                                     "?????????"))
        waitWeather.append(user_id)
    elif msg == "!?????? ???":
        if eb.find_one({'group_id': event.source.group_id}) is None:
            data = {
                "group_id": event.source.group_id,
                "enable": "True"
            }
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????????????????"))
        else:
            data = {
                "group_id": event.source.group_id,
                "enable": "True"
            }
            eb.delete_one({"group_id": event.source.group_id})
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("?????????????????????\n??????????????????????????????"))
    elif msg == "!????????????":
        bot.reply_message(chatToken, TextSendMessage("==????????????????????????==\n"
                                                     "!?????? ???:????????????\n"
                                                     "!?????? ???:????????????\n"
                                                     "???;??????;??????\n"
                                                     "Ex:???;??????;??????\n"
                                                     "???????????????\n"
                                                     "???????????????\n"
                                                     "??????\n"
                                                     "?????????\n"
                                                     "????????????\n"
                                                     "???;??????;??????"))
    elif msg == "!?????? ???":
        if eb.find_one({'group_id': event.source.group_id}) is None:
            data = {
                "group_id": event.source.group_id,
                "enable": "False"
            }
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
        else:
            data = {
                "group_id": event.source.group_id,
                "enable": "False"
            }
            eb.delete_one({"group_id": event.source.group_id})
            time.sleep(1)
            eb.insert(data)
            bot.reply_message(chatToken, TextSendMessage("?????????????????????"))
    elif tic.find_one({"????????????": user_id}) is not None:
        if msg == "!?????????" and user_id == tic.find_one({"????????????": user_id})["????????????"]:
            if user_id not in rpswait:
                tic.update_one({"????????????": user_id}, {"$set": {"??????": "??????"}})
                bot.reply_message(chatToken, FlexSendMessage('WebHook', {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "?????????",
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
                                    "label": "??????",
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
                                    "label": "??????",
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
                                    "label": "???",
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
        elif msg == "!????????????" and user_id == tic.find_one({"????????????": user_id})["????????????"]:
            tic.delete_one({"????????????": user_id})
            bot.reply_message(chatToken, TextSendMessage("?????? ??????????????????"))
    elif msg == "!??????":
        bot.reply_message(chatToken, TextSendMessage("????????????????????????ip:\n"
                                                     "Ex:123.195.16.26"))
        ip.append(user_id)
    elif msg == "!del":
        if user_id == "Uddb208c296fcbafbff7c0488824d3471":
            bot.reply_message(chatToken, TextSendMessage("???????????????????????????:"))
            admin.append(user_id)
        else:
            bot.reply_message(chatToken, TextSendMessage("?????? ?????????????????????????????????"))
    elif "??????" in msg:
        r = requests.get('https://gasoline.weiyuan.com.tw', timeout=1)
        soup = BeautifulSoup(r.text, 'html.parser')
        # ??????????????????
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
        if '???' in NTgas:
            gascolor = '#00FF00'
        if '???' in NTfuel:
            fuelcolor = '#00FF00'
        if '???' in NTgas:
            gascolor = '#FF0000'
        if '???' in NTfuel:
            fuelcolor = '#FF0000'
        # ????????????
        TSweek = soup.find_all('h1', class_='h4 pull-left page-title')[1].getText()
        # ??????
        T98 = soup.find_all('tr')[9].find_all('th')[1].getText()
        T95 = soup.find_all('tr')[9].find_all('th')[2].getText()
        T92 = soup.find_all('tr')[9].find_all('th')[3].getText()
        Tfuel = soup.find_all('tr')[9].find_all('th')[4].getText()
        # ??????
        M98p = soup.find_all('tr')[10].find_all('td')[0].getText()
        M95p = soup.find_all('tr')[10].find_all('td')[1].getText()
        M92p = soup.find_all('tr')[10].find_all('td')[2].getText()
        Mfuelp = soup.find_all('tr')[10].find_all('td')[3].getText()
        # ??????
        S98p = soup.find_all('tr')[11].find_all('td')[0].getText()
        S95p = soup.find_all('tr')[11].find_all('td')[1].getText()
        S92p = soup.find_all('tr')[11].find_all('td')[2].getText()
        Sfuelp = soup.find_all('tr')[11].find_all('td')[3].getText()
        print(NTweek.split('(')[1])
        bot.reply_message(chatToken, FlexSendMessage('????????????', {
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
                                "text": "????????????",
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
                        "text": f"??? {NTweek.split('(')[0].replace(' ', '')}",
                        "weight": "bold",
                        "size": size,
                        "color": ntcolor
                    },
                    {
                        "type": "text",
                        "text": f"??? ({NTweek.split('(')[1]}",
                        "style": "normal",
                        "align": "start",
                        "weight": "bold",
                        "color": "#F2AA4CFF",
                        "margin": "md",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": f"??? ??????:{NTgas}",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "xxl",
                        "color": f"{gascolor}"
                    },
                    {
                        "type": "text",
                        "text": f"??? ??????:{NTfuel}",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "sm",
                        "color": f"{fuelcolor}"
                    },
                    {
                        "type": "text",
                        "text": f"??? {TSweek.split('(')[0].replace(' ', '')}",
                        "weight": "bold",
                        "size": "xxl",
                        "color": "#F2AA4CFF",
                        "margin": "xxl"
                    },
                    {
                        "type": "text",
                        "text": f"??? ({TSweek.split('(')[1]}",
                        "style": "normal",
                        "align": "start",
                        "weight": "bold",
                        "color": "#F2AA4CFF",
                        "margin": "md",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": "???98??????",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md",
                        "color": "#ADEFD1FF",
                        "contents": [
                            {
                                "type": "span",
                                "text": "??? ????????????",
                                "color": "#89ABE3FF",
                                "size": "3xl"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"??? {T98}: {M98p} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"??? {T95}: {M95p} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"??? {T92}: {M92p} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"??? {Tfuel}: {Mfuelp} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": "???98??????",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md",
                        "color": "#ADEFD1FF",
                        "contents": [
                            {
                                "type": "span",
                                "text": "??? ????????????",
                                "color": "#89ABE3FF",
                                "size": "3xl"
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"??? {T98}: {S98p} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"??? {T95}: {S95p} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"??? {T92}: {S92p} ???",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "color": "#ADEFD1FF"
                    },
                    {
                        "type": "text",
                        "text": f"??? {Tfuel}: {Sfuelp} ???",
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
                                          TextSendMessage(text=f"?????? {user.display_name} ??? {level}??? ????????? {level_}??? !"))
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
                                          TextSendMessage(text=f"?????? {user.display_name} ??? {level}??? ????????? {level_}??? !"))
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
                                          TextSendMessage(text=f"?????? {user.display_name} ??? {level}??? ????????? {level_}??? !"))
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
                                          TextSendMessage(text=f"?????? {user.display_name} ??? {level}??? ????????? {level_}??? !"))


if __name__ == "__main__":
    t = threading.Thread(target=cooldown)
    t.start()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
