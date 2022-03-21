from linebot.models import *
from linebot import LineBotApi
from linebot.models import *
import pymongo
from operator import itemgetter
import time
import threading
import requests
from bs4 import BeautifulSoup
import random

Admin = ["Uddb208c296fcbafbff7c0488824d3471"]
bot = LineBotApi(
    'R2EQ91eZrOij+P9TsvsuA9g3BkgNkMlnXihtzAt9uGW0c8PPONHRlnquTZ15TxY0F9dn3RXrPlfNW9ROMFAkRYSHxIXYNy+CLMTQbKbMuynhnzTH4HRnOdyudl3uYCjCHhhPPUoHrIopw/r1pJpfYQdB04t89/1O/w1cDnyilFU=')
client = pymongo.MongoClient(
    "mongodb+srv://nathan:1620zxcv@cluster0.lmlkk.mongodb.net/levels?retryWrites=true&w=majority")
gb = client.levels['global']  # 個人等級
db = client.levels  # 不太懂
bk = client.chats['blocking']
tic = client.tic['tic']
circle = client.tic['circle']

R_bag = client.RPG['Bags']
R_axie = client.RPG['Axies']
R_deposit = client.RPG['Deposit']

def calc_rank(exp: int):
    level = 0
    needed_exp = 100
    while exp > needed_exp:
        exp -= needed_exp
        needed_exp += 50
        level += 1
    return level, exp, needed_exp


class Commands:
    def __init__(self, bot, token):
        self.bot = bot
        self.token = token
    def add(self, event, args):
        if event.source.user_id in Admin:
            try:
                user = event.source.user_id
                mentionuser = event.message.mention.mentionees[0].user_id
                group_id = event.source.group_id
                take = bot.get_group_member_profile(group_id, user)
                mentiontake = bot.get_group_member_profile(group_id, mentionuser)
                deposit = R_deposit.find_one({"user": mentionuser})
                R_deposit.update_one({"user": mentionuser}, {"$set": {"deposit": round(deposit['deposit'] + 7, 2)}})
                self.bot.reply_message(self.token, TextSendMessage("成功新增該使用者7元"))
            except AttributeError:
                self.bot.reply_message(self.token, TextSendMessage("請@正確目標對象"))
                return
        else:
            self.bot.reply_message(self.token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    def Admin(self, event, args):
        if event.source.user_id in Admin:
            try:
                user = event.source.user_id
                mentionuser = event.message.mention.mentionees[0].user_id
                group_id = event.source.group_id
                take = bot.get_group_member_profile(group_id, user)
                mentiontake = bot.get_group_member_profile(group_id, mentionuser)
                Admin.append(mentionuser)
                self.bot.reply_message(self.token, TextSendMessage("成功新增該使用者"))
            except AttributeError:
                self.bot.reply_message(self.token, TextSendMessage("請@正確目標對象"))
                return
        else:
            self.bot.reply_message(self.token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    def deAdmin(self, event, args):
        if event.source.user_id in Admin:
            try:
                user = event.source.user_id
                mentionuser = event.message.mention.mentionees[0].user_id
                group_id = event.source.group_id
                take = bot.get_group_member_profile(group_id, user)
                mentiontake = bot.get_group_member_profile(group_id, mentionuser)
                Admin.remove(mentionuser)
                self.bot.reply_message(self.token, TextSendMessage("成功移除該使用者"))
            except AttributeError:
                self.bot.reply_message(self.token, TextSendMessage("請@正確目標對象"))
                return
        else:
            self.bot.reply_message(self.token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    def allAdmin(self, event, args):
        if event.source.user_id in Admin:
             user = event.source.user_id
             mentionuser = event.message.mention.mentionees[0].user_id
             group_id = event.source.group_id
             take = bot.get_group_member_profile(group_id, user)
             mentiontake = bot.get_group_member_profile(group_id, mentionuser)
             self.bot.reply_message(self.token, TextSendMessage(f"以下為擁有權限之user_ID的列表" + Admin))
        else:
            self.bot.reply_message(self.token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    def block(self, event, args):
        if event.source.user_id in Admin:
            try:
                user = event.source.user_id
                mentionuser = event.message.mention.mentionees[0].user_id
                group_id = event.source.group_id
                take = bot.get_group_member_profile(group_id, user)
                mentiontake = bot.get_group_member_profile(group_id, mentionuser)
                data = {
                    "name": mentiontake.display_name,
                    "user": mentionuser
                }
                bk.insert(data)
                self.bot.reply_message(self.token, TextSendMessage("成功新增該使用者"))
            except AttributeError:
                self.bot.reply_message(self.token, TextSendMessage("請@正確目標對象"))
                return
        else:
            self.bot.reply_message(self.token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    def deblock(self, event, args):
        if event.source.user_id in Admin:
            try:
                user = event.source.user_id
                mentionuser = event.message.mention.mentionees[0].user_id
                group_id = event.source.group_id
                take = bot.get_group_member_profile(group_id, user)
                mentiontake = bot.get_group_member_profile(group_id, mentionuser)
                bk.delete_one({"user": mentionuser})
                self.bot.reply_message(self.token, TextSendMessage("成功移除該使用者"))
            except AttributeError:
                self.bot.reply_message(self.token, TextSendMessage("請@正確目標對象"))
                return
        else:
            self.bot.reply_message(self.token, TextSendMessage("抱歉 你沒有權限執行這條指令"))
    def 等級(self, event, args):
        try:
            user = event.message.mention.mentionees[0].user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            name = take.display_name
        except AttributeError:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            name = take.display_name
        if db[event.source.group_id] is not None:
            user_id = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user_id)
            name = take.display_name
            group_level = "⚠尚未設定"
        user_data = gb.find_one({"user": user})
        if user_data is None:
            print("user_data is none")
            data = {
                "name": name,
                "user": user,
                "exp": 0
            }
            gb.insert(data)
            level, exp, need = calc_rank(0)
            global_level = f"等級: {level} | 經驗值: {exp}/{need}"
            message = f"===等級查詢===\n公有等級:\n  {global_level}\n私人等級:\n  {group_level}"
            message += "\n\n等級系統Beta版"

            self.bot.reply_message(self.token, TextSendMessage(message))
        else:
            level, exp, need = calc_rank(user_data['exp'])
            global_level = f"等級: {level} | 經驗值: {exp}/{need}"
            message = f"===等級查詢===\n公有等級:\n  {global_level}\n私人等級:\n  {group_level}"
            message += "\n\n等級系統Beta版"
            self.bot.reply_message(self.token, TextSendMessage(message))

    def 排行榜(self, event, args):
        raw_data = gb.find()
        data = sorted(raw_data, key=itemgetter("exp"), reverse=True)
        print(data)
        message = "======排行榜======\n"
        p = 0
        for d in data:
            if p < 20:
                p += 1
                level, exp, need = calc_rank(d['exp'])
                message += f"{p}: {d['name']} - {level}級 | {exp}/{need}\n"
        self.bot.reply_message(self.token, TextSendMessage(message + "\n💫全用戶等級前20總排行💫"))
    # 比大小
    def 比大小(self, event, args):
        try:
            user = event.source.user_id
            mentionuser = event.message.mention.mentionees[0].user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            mentiontake = bot.get_group_member_profile(group_id, mentionuser)
            deposit = R_deposit.find_one({"user": user})
            mentiondeposit = R_deposit.find_one({"user": mentionuser})
            a = random.randint(0, 100)
            b = random.randint(0, 100)
            money = round(random.uniform(0, 3), 2)
            if a > b:
                R_deposit.update_one({"user": user}, {"$set": {"deposit": round(deposit["deposit"] + money, 2)}})
                R_deposit.update_one({"user": mentionuser}, {"$set": {"deposit": round(mentiondeposit["deposit"] - money, 2)}})
                self.bot.reply_message(self.token, TextSendMessage("\比大小結果/\n"
                                                                   f"{take.display_name}:{a}點\n"
                                                                   f"{mentiontake.display_name}:{b}點\n"
                                                                   f"看來是{take.display_name}贏了!\n"
                                                                   f"{take.display_name}+{money}$\n"
                                                                   f"{mentiontake.display_name}-{money}$"))
            if a < b:
                R_deposit.update_one({"user": mentionuser}, {"$set": {"deposit": round(mentiondeposit["deposit"] + money, 2)}})
                R_deposit.update_one({"user": user}, {"$set": {"deposit": round(deposit["deposit"] - money, 2)}})
                self.bot.reply_message(self.token, TextSendMessage("\比大小結果/\n"
                                                                   f"{take.display_name}:{a}點\n"
                                                                   f"{mentiontake.display_name}:{b}點\n"
                                                                   f"看來是{mentiontake.display_name}贏了!\n"
                                                                   f"{mentiontake.display_name}+{money}$\n"
                                                                   f"{take.display_name}-{money}$"))
        except AttributeError:
            self.bot.reply_message(self.token, TextSendMessage("請@你要挑戰的人哦~"))
            return
    def 猜拳(self, event, args):
        try:
            user = event.source.user_id
            mentionuser = event.message.mention.mentionees[0].user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            mentiontake = bot.get_group_member_profile(group_id, mentionuser)
            if tic.find_one({"攻擊者": user}) is not None:
                self.bot.reply_message(self.token, TextSendMessage("你現在在對戰中或\n"
                                                                   "請求挑戰狀態中哦~"))
            if tic.find_one({"被攻擊者": mentionuser}) is not None:
                self.bot.reply_message(self.token, TextSendMessage("該使用者在挑戰或\n"
                                                                   "被請求挑戰狀態中哦~"))
            elif tic.find_one({"被攻擊者": mentionuser}) is None:
                self.bot.reply_message(self.token, FlexSendMessage('猜拳挑戰', {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{take.display_name}  向",
                                "weight": "bold",
                                "align": "center",
                                "margin": "xxl",
                                "size": "xl",
                                "color": "#535f65",
                                "style": "italic",
                                "decoration": "none"
                            },
                            {
                                "type": "text",
                                "text": mentiontake.display_name,
                                "margin": "md",
                                "size": "xl",
                                "color": "#535f65",
                                "weight": "bold",
                                "style": "italic",
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "發起了猜拳挑戰",
                                "margin": "lg",
                                "size": "3xl",
                                "color": "#535f65",
                                "weight": "bold",
                                "style": "normal",
                                "align": "center"
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
                                    "type": "message",
                                    "label": "接受這挑戰!",
                                    "text": "!我願意"
                                },
                                "color": "#e2f5fe",
                                "style": "secondary",
                                "flex": 9
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "人家怕怕先不要~",
                                    "text": "!我不願意"
                                },
                                "color": "#e2f5fe",
                                "style": "secondary",
                                "margin": "xl"
                            }
                        ],
                        "backgroundColor": "#d0effe"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "若不回覆，挑戰將在60秒後解除!",
                                "color": "#bc153b",
                                "weight": "bold",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": "#d0effe"
                    }
                }))
                data = {
                    "攻擊者": user,
                    "被攻擊者": mentionuser,
                    "接受": "未知",
                    "攻擊者出": "未知",
                    "被攻擊者出": "未知"
                }
                tic.insert(data)
                time.sleep(60)
                if tic.find_one({"攻擊者": user})["接受"] == "未知":
                    try:
                        tic.delete_one({"攻擊者": user})
                    except KeyError:
                        pass
                elif tic.find_one({"攻擊者": user})["接受"] == "接受":
                    print("success")
                else:
                    tic.delete_one({"攻擊者": user})
        except AttributeError:
            self.bot.reply_message(self.token, TextSendMessage("請@你要挑戰的人哦~"))
            return
    def pttT(self, event, args):
        r = requests.get("https://www.pttweb.cc/hot/all/today")
        soup = BeautifulSoup(r.text, 'html.parser')
        tittle2 = soup.find_all("span", class_="e7-show-if-device-is-not-xs")  # 標題
        links = soup.find_all("a", {"data-v-efd3e102": True})
        reply2 = soup.find_all(class_="e7-recommendCount text-no-wrap e7-grey-text")
        tittle = []
        href = []
        reply = []
        i = 0
        for tittle1 in tittle2:
            tittle0 = tittle1.getText()
            tittle.append(tittle0)
        noRepeat = []
        for link in links:
            if link.getText() == "":
                pass
            if len(link["href"]) > 18 and link["href"] not in noRepeat:
                noRepeat.append(link["href"])
                href.append("https://www.pttweb.cc" + link["href"])
        for reply1 in reply2:
            reply0 = str(list(reply1)[1]).replace(" ", "").replace("\n", "")
            reply.append(reply0)
        message = "🔥文章PTT-今日熱門🔥\n"
        while True:
            if i <= 30:
                message += "⚜標題:\n" \
                           f"{tittle[i]}\n" \
                           f"✔連結:\n" \
                           f"{href[i]}\n" \
                           f"💬留言數:\n" \
                           f"▶{reply[i]}◀\n"
                i += 1
            else:
                self.bot.reply_message(self.token, TextSendMessage(message))
                break
    def pttN(self, event, args):
        r = requests.get("https://www.pttweb.cc/hot/all")
        soup = BeautifulSoup(r.text, 'html.parser')
        tittle2 = soup.find_all("span", class_="e7-show-if-device-is-not-xs")  # 標題
        links = soup.find_all("a", {"data-v-efd3e102": True})
        reply2 = soup.find_all(class_="e7-recommendCount text-no-wrap e7-grey-text")
        tittle = []
        href = []
        reply = []
        i = 0
        for tittle1 in tittle2:
            tittle0 = tittle1.getText()
            tittle.append(tittle0)
        noRepeat = []
        for link in links:
            if link.getText() == "":
                pass
            if len(link["href"]) > 18 and link["href"] not in noRepeat:
                noRepeat.append(link["href"])
                href.append("https://www.pttweb.cc" + link["href"])
        for reply1 in reply2:
            reply0 = str(list(reply1)[1]).replace(" ", "").replace("\n", "")
            reply.append(reply0)
        message = "📍文章PTT-最新熱門📍\n"
        while True:
            if i <= 30:
                message += "⚜標題:\n" \
                           f"{tittle[i]}\n" \
                           f"✔連結:\n" \
                           f"{href[i]}\n" \
                           f"💬留言數:\n" \
                           f"▶{reply[i]}◀\n"
                i += 1
            else:
                self.bot.reply_message(self.token, TextSendMessage(message))
                break
    def pttL(self, event, args):
        r = requests.get("https://www.pttweb.cc/hot/all/yesterday")
        soup = BeautifulSoup(r.text, 'html.parser')
        tittle2 = soup.find_all("span", class_="e7-show-if-device-is-not-xs")  # 標題
        links = soup.find_all("a", {"data-v-efd3e102": True})
        reply2 = soup.find_all(class_="e7-recommendCount text-no-wrap e7-grey-text")
        tittle = []
        href = []
        reply = []
        i = 0
        for tittle1 in tittle2:
            tittle0 = tittle1.getText()
            tittle.append(tittle0)
        noRepeat = []
        for link in links:
            if link.getText() == "":
                pass
            if len(link["href"]) > 18 and link["href"] not in noRepeat:
                noRepeat.append(link["href"])
                href.append("https://www.pttweb.cc" + link["href"])
        for reply1 in reply2:
            reply0 = str(list(reply1)[1]).replace(" ", "").replace("\n", "")
            reply.append(reply0)
        message = "💫文章PTT-昨日熱門💫\n"
        while True:
            if i <= 30:
                message += "⚜標題:\n" \
                           f"{tittle[i]}\n" \
                           f"✔連結:\n" \
                           f"{href[i]}\n" \
                           f"💬留言數:\n" \
                           f"▶{reply[i]}◀\n"
                i += 1
            else:
                self.bot.reply_message(self.token, TextSendMessage(message))
                break
    def pttW(self, event, args):
        r = requests.get("https://www.pttweb.cc/hot/all/this-week")
        soup = BeautifulSoup(r.text, 'html.parser')
        tittle2 = soup.find_all("span", class_="e7-show-if-device-is-not-xs")  # 標題
        links = soup.find_all("a", {"data-v-efd3e102": True})
        reply2 = soup.find_all(class_="e7-recommendCount text-no-wrap e7-grey-text")
        tittle = []
        href = []
        reply = []
        i = 0
        for tittle1 in tittle2:
            tittle0 = tittle1.getText()
            tittle.append(tittle0)
        noRepeat = []
        for link in links:
            if link.getText() == "":
                pass
            if len(link["href"]) > 18 and link["href"] not in noRepeat:
                noRepeat.append(link["href"])
                href.append("https://www.pttweb.cc" + link["href"])
        for reply1 in reply2:
            reply0 = str(list(reply1)[1]).replace(" ", "").replace("\n", "")
            reply.append(reply0)
        message = "🎇文章PTT-本週熱門🎇\n"
        while True:
            if i <= 30:
                message += "⚜標題:\n" \
                           f"{tittle[i]}\n" \
                           f"✔連結:\n" \
                           f"{href[i]}\n" \
                           f"💬留言數:\n" \
                           f"▶{reply[i]}◀\n"
                i += 1
            else:
                self.bot.reply_message(self.token, TextSendMessage(message))
                break
    def pttM(self, event, args):
        r = requests.get("https://www.pttweb.cc/hot/all/this-month")
        soup = BeautifulSoup(r.text, 'html.parser')
        tittle2 = soup.find_all("span", class_="e7-show-if-device-is-not-xs")  # 標題
        links = soup.find_all("a", {"data-v-efd3e102": True})
        reply2 = soup.find_all(class_="e7-recommendCount text-no-wrap e7-grey-text")
        tittle = []
        href = []
        reply = []
        i = 0
        for tittle1 in tittle2:
            tittle0 = tittle1.getText()
            tittle.append(tittle0)
        noRepeat = []
        for link in links:
            if link.getText() == "":
                pass
            if len(link["href"]) > 18 and link["href"] not in noRepeat:
                noRepeat.append(link["href"])
                href.append("https://www.pttweb.cc" + link["href"])
        for reply1 in reply2:
            reply0 = str(list(reply1)[1]).replace(" ", "").replace("\n", "")
            reply.append(reply0)
        message = "🖤文章PTT-本月熱門❤\n"
        while True:
            if i <= 30:
                message += "⚜標題:\n" \
                           f"{tittle[i]}\n" \
                           f"✔連結:\n" \
                           f"{href[i]}\n" \
                           f"💬留言數:\n" \
                           f"▶{reply[i]}◀\n"
                i += 1
            else:
                self.bot.reply_message(self.token, TextSendMessage(message))
                break
    def 小冷(self, event, args):
        f = open("cold.txt", encoding='utf-8')
        lines = f.readlines()
        test = []
        for line in lines:
            test.append(line.replace('\n', '').replace("''", ''))
            f.close()
        i = 0
        while True:
            if i < 249:
                test.remove('')
                i += 1
            else:
                break
        last = []
        for g in test:
            last.append(str(g).split('.')[1])
        self.bot.reply_message(self.token, TextSendMessage(random.choice(last)))
    # RPG 系統
    def 戰鬥系統(self, event, args):
        self.bot.reply_message(self.token, TextSendMessage("此為Line Bot\n"
                                                           "獨一無二的戰鬥系統\n"
                                                           "1.!存款:查看存款\n"
                                                           "2.!背包:查看背包\n"
                                                           "3.!扭蛋:新增戰寵\n"
                                                           "4.!出售:出售戰寵\n"
                                                           "5.!出戰:設定出戰的戰寵\n"
                                                           "6.!決鬥 @標記你要的人\n"
                                                           "<==========>\n"
                                                           "(扭蛋一次7$)\n"
                                                           "(決鬥會輸錢&贏錢)\n"
                                                           "Tip:\n"
                                                           "(!比大小:可以賺錢)\n"
                                                           "❗注意\n"
                                                           "出現NoneType錯誤\n"
                                                           "是因為你還沒新增使用者\n"
                                                           "請先將\n"
                                                           "!存款\n"
                                                           "!背包\n"
                                                           "指令打過一遍❗\n"
                                                           "還是有錯就是沒有加\n"
                                                           "卡米喵好友 跟 追蹤❗"))
    def 扭蛋(self, event, args):
        axies = []
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        deposit = R_deposit.find_one({"user": user})
        bag = R_bag.find_one({"user": user})
        a = R_axie.find()
        for i in a:
            axies.append(i['name'])
        if "NONE" in bag['axies']:
            if deposit['deposit'] < 7:
                talk = ["窮光蛋你可以先把錢湊齊嗎?", "抱歉餘額不足", "錢不夠啦 還扭蛋 扭你媽", "錢不夠 哈哈 笑你", "抱歉你真的太窮 不能扭", "可以先檢查自己剩多少錢嗎?"]
                self.bot.reply_message(self.token, TextSendMessage(random.choice(talk)))
            else:
                axies.remove("NONE")
                R_deposit.update_one({"user": user}, {"$set": {"deposit": round(deposit['deposit'] - 7, 2)}})
                got = random.choice(axies)
                axies = bag['axies']
                axies.remove("NONE")
                axies.insert(0, got)
                R_bag.update_one({"user": user}, {"$set": {"axies": axies}})
                self.bot.reply_message(self.token, TextSendMessage(f"恭喜你獲得一隻 {got}\n"
                                                                   f"餘額:{round(deposit['deposit'] - 7, 2)}\n"
                                                                   f"!背包:查看背包"))
        else:
            self.bot.reply_message(self.token, TextSendMessage("包包滿了啦!\n請先賣掉包包裡的AXIES"))
    def 存款(self, event, args):
        color = ["#ffffff", "#ffd700", "#e6e6fa", "#f0f8ff", "#ff7373", "#0ff1ce", "#7fffd4", "#ff80ed"]
        g = random.choice(color)
        try:
            mentionuser = event.message.mention.mentionees[0].user_id
            group_id = event.source.group_id
            mentiontake = bot.get_group_member_profile(group_id, mentionuser)
            deposit = R_deposit.find_one({"user": mentionuser})
            if deposit is None:
                data = {
                    "user": mentionuser,
                    "name": mentiontake.display_name,
                    "deposit": 0
                }
                R_deposit.insert(data)
                self.bot.reply_message(self.token, TextSendMessage("以新增該使用者"))
            else:
                self.bot.reply_message(self.token, FlexSendMessage('標記之個人存款', {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": f"{mentiontake.display_name}的帳戶",
        "weight": "bold",
        "flex": 90,
        "align": "center",
        "size": "xxl"
      }
    ],
    "backgroundColor": f"{g}"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": f"存款:{deposit['deposit']}",
        "weight": "bold",
        "margin": "none",
        "size": "xxl",
        "flex": 90
      }
    ],
    "backgroundColor": f"{g}"
  }
}))
        except AttributeError:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            deposit = R_deposit.find_one({"user": user})
            if deposit is None:
                data = {
                    "user": user,
                    "name": take.display_name,
                    "deposit": 0
                }
                R_deposit.insert(data)
                self.bot.reply_message(self.token, TextSendMessage("以新增使用者"))
            else:
                self.bot.reply_message(self.token, FlexSendMessage('個人存款', {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": f"{take.display_name}的帳戶",
        "weight": "bold",
        "flex": 90,
        "align": "center",
        "size": "xxl"
      }
    ],
    "backgroundColor": f"{g}"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": f"存款:{deposit['deposit']}",
        "weight": "bold",
        "margin": "none",
        "size": "xxl",
        "flex": 90
      }
    ],
    "backgroundColor": f"{g}"
  }
}))
    def 背包(self, event, args):
        try:
            mentionuser = event.message.mention.mentionees[0].user_id
            group_id = event.source.group_id
            mentiontake = bot.get_group_member_profile(group_id, mentionuser)
            bag = R_bag.find_one({"user": mentionuser})
            deposit = R_deposit.find_one({"user": mentionuser})
            if bag is None:
                data = {
                    "name": mentiontake.display_name,
                    "user": mentionuser,
                    "RPG": 0,
                    "axies": ["NONE", "NONE", "NONE", "NONE", "NONE"]
                }
                R_bag.insert(data)
                self.bot.reply_message(self.token, TextSendMessage("以新增該使用者背包"))
            else:
                self.bot.reply_message(self.token, FlexSendMessage('背包', {
                    "type": "carousel",
                    "contents": [
                        {
                            "type": "bubble",
                            "header": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"{mentiontake.display_name}的個人背包",
                                        "weight": "bold",
                                        "margin": "none",
                                        "size": "xl",
                                        "style": "normal",
                                        "align": "center"
                                    }
                                ]
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"● 存款:{deposit['deposit']}$",
                                        "weight": "bold",
                                        "size": "xxl",
                                        "margin": "none",
                                        "color": "#3f3f3f"
                                    },
                                    {
                                        "type": "text",
                                        "text": "● 背包容量:5",
                                        "weight": "bold",
                                        "size": "xxl",
                                        "margin": "none",
                                        "color": "#3f3f3f"
                                    }
                                ]
                            },
                            "styles": {
                                "header": {
                                    "backgroundColor": "#f0f0f0"
                                },
                                "body": {
                                    "backgroundColor": "#f0f0f0"
                                }
                            }
                        },
                        {
                            "type": "bubble",
                            "header": {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f" ▶ {R_axie.find_one({'name': bag['axies'][0]})['name']} ◀",
                                        "weight": "bold",
                                        "style": "normal",
                                        "decoration": "none",
                                        "position": "absolute",
                                        "align": "start",
                                        "margin": "xxl",
                                        "size": "lg",
                                        "offsetStart": "xxl",
                                        "offsetTop": "xxl",
                                        "flex": 90,
                                        "color": "#000000"
                                    }
                                ],
                                "position": "relative"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": f"{R_axie.find_one({'name': bag['axies'][0]})['link']}",
                                        "position": "relative",
                                        "margin": "none",
                                        "align": "center",
                                        "size": "full",
                                        "offsetTop": "none",
                                        "offsetBottom": "none",
                                        "offsetStart": "none",
                                        "offsetEnd": "none",
                                        "aspectMode": "cover",
                                        "aspectRatio": "9:4"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"● HP:{R_axie.find_one({'name': bag['axies'][0]})['HP']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][0]})['ATK']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][0]})['PRICE']}$",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": "🎒 1/5",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "header": {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f" ▶ {R_axie.find_one({'name': bag['axies'][1]})['name']} ◀",
                                        "weight": "bold",
                                        "style": "normal",
                                        "decoration": "none",
                                        "position": "absolute",
                                        "align": "start",
                                        "margin": "xxl",
                                        "size": "lg",
                                        "offsetStart": "xxl",
                                        "offsetTop": "xxl",
                                        "flex": 90,
                                        "color": "#000000"
                                    }
                                ],
                                "position": "relative"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "position": "relative",
                                        "margin": "none",
                                        "align": "center",
                                        "size": "full",
                                        "offsetTop": "none",
                                        "offsetBottom": "none",
                                        "offsetStart": "none",
                                        "offsetEnd": "none",
                                        "aspectMode": "cover",
                                        "aspectRatio": "9:4",
                                        "url": f"{R_axie.find_one({'name': bag['axies'][1]})['link']}"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"● HP:{R_axie.find_one({'name': bag['axies'][1]})['HP']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][1]})['ATK']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][1]})['PRICE']}$",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": "🎒 2/5",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "header": {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f" ▶ {R_axie.find_one({'name': bag['axies'][2]})['name']} ◀",
                                        "weight": "bold",
                                        "style": "normal",
                                        "decoration": "none",
                                        "position": "absolute",
                                        "align": "start",
                                        "margin": "xxl",
                                        "size": "lg",
                                        "offsetStart": "xxl",
                                        "offsetTop": "xxl",
                                        "flex": 90,
                                        "color": "#000000"
                                    }
                                ],
                                "position": "relative"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "position": "relative",
                                        "margin": "none",
                                        "align": "center",
                                        "size": "full",
                                        "offsetTop": "none",
                                        "offsetBottom": "none",
                                        "offsetStart": "none",
                                        "offsetEnd": "none",
                                        "aspectMode": "cover",
                                        "aspectRatio": "9:4",
                                        "url": f"{R_axie.find_one({'name': bag['axies'][2]})['link']}"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"● HP:{R_axie.find_one({'name': bag['axies'][2]})['HP']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][2]})['ATK']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][2]})['PRICE']}$",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": "🎒 3/5",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "header": {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f" ▶ {R_axie.find_one({'name': bag['axies'][3]})['name']} ◀",
                                        "weight": "bold",
                                        "style": "normal",
                                        "decoration": "none",
                                        "position": "absolute",
                                        "align": "start",
                                        "margin": "xxl",
                                        "size": "lg",
                                        "offsetStart": "xxl",
                                        "offsetTop": "xxl",
                                        "flex": 90,
                                        "color": "#000000"
                                    }
                                ],
                                "position": "relative"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "position": "relative",
                                        "margin": "none",
                                        "align": "center",
                                        "size": "full",
                                        "offsetTop": "none",
                                        "offsetBottom": "none",
                                        "offsetStart": "none",
                                        "offsetEnd": "none",
                                        "aspectMode": "cover",
                                        "aspectRatio": "9:4",
                                        "url": f"{R_axie.find_one({'name': bag['axies'][3]})['link']}"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"● HP:{R_axie.find_one({'name': bag['axies'][3]})['HP']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][3]})['ATK']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][3]})['PRICE']}$",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": "🎒 4/5",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "header": {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f" ▶ {R_axie.find_one({'name': bag['axies'][4]})['name']} ◀",
                                        "weight": "bold",
                                        "style": "normal",
                                        "decoration": "none",
                                        "position": "absolute",
                                        "align": "start",
                                        "margin": "xxl",
                                        "size": "lg",
                                        "offsetStart": "xxl",
                                        "offsetTop": "xxl",
                                        "flex": 90,
                                        "color": "#000000"
                                    }
                                ],
                                "position": "relative"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "position": "relative",
                                        "margin": "none",
                                        "align": "center",
                                        "size": "full",
                                        "offsetTop": "none",
                                        "offsetBottom": "none",
                                        "offsetStart": "none",
                                        "offsetEnd": "none",
                                        "aspectMode": "cover",
                                        "aspectRatio": "9:4",
                                        "url": f"{R_axie.find_one({'name': bag['axies'][4]})['link']}"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"● HP:{R_axie.find_one({'name': bag['axies'][4]})['HP']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][4]})['ATK']}",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][4]})['PRICE']}$",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    },
                                    {
                                        "type": "text",
                                        "text": "🎒 5/5",
                                        "weight": "bold",
                                        "margin": "xs",
                                        "size": "xxl",
                                        "color": "#696969",
                                        "align": "start",
                                        "offsetStart": "xs"
                                    }
                                ]
                            }
                        }
                    ]
                }))
        except AttributeError:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            if bag is None:
                data = {
                    "name": take.display_name,
                    "user": user,
                    "RPG": 0,
                    "axies": ["NONE", "NONE", "NONE", "NONE", "NONE"]
                }
                R_bag.insert(data)
                self.bot.reply_message(self.token, TextSendMessage("以新增使用者背包"))
            else:
                self.bot.reply_message(self.token, FlexSendMessage('背包', {
          "type": "carousel",
          "contents": [
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{take.display_name}的個人背包",
                    "weight": "bold",
                    "margin": "none",
                    "size": "xl",
                    "style": "normal",
                    "align": "center"
                  }
                ]
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"● 存款:{deposit['deposit']}$",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "none",
                    "color": "#3f3f3f"
                  },
                  {
                    "type": "text",
                    "text": "● 背包容量:5",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "none",
                    "color": "#3f3f3f"
                  }
                ]
              },
              "styles": {
                "header": {
                  "backgroundColor": "#f0f0f0"
                },
                "body": {
                  "backgroundColor": "#f0f0f0"
                }
              }
            },
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": f" ▶ {R_axie.find_one({'name': bag['axies'][0]})['name']} ◀",
                    "weight": "bold",
                    "style": "normal",
                    "decoration": "none",
                    "position": "absolute",
                    "align": "start",
                    "margin": "xxl",
                    "size": "lg",
                    "offsetStart": "xxl",
                    "offsetTop": "xxl",
                    "flex": 90,
                    "color": "#000000"
                  }
                ],
                "position": "relative"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "url": f"{R_axie.find_one({'name': bag['axies'][0]})['link']}",
                    "position": "relative",
                    "margin": "none",
                    "align": "center",
                    "size": "full",
                    "offsetTop": "none",
                    "offsetBottom": "none",
                    "offsetStart": "none",
                    "offsetEnd": "none",
                    "aspectMode": "cover",
                    "aspectRatio": "9:4"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"● HP:{R_axie.find_one({'name': bag['axies'][0]})['HP']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][0]})['ATK']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][0]})['PRICE']}$",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": "🎒 1/5",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  }
                ]
              }
            },
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": f" ▶ {R_axie.find_one({'name': bag['axies'][1]})['name']} ◀",
                    "weight": "bold",
                    "style": "normal",
                    "decoration": "none",
                    "position": "absolute",
                    "align": "start",
                    "margin": "xxl",
                    "size": "lg",
                    "offsetStart": "xxl",
                    "offsetTop": "xxl",
                    "flex": 90,
                    "color": "#000000"
                  }
                ],
                "position": "relative"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "position": "relative",
                    "margin": "none",
                    "align": "center",
                    "size": "full",
                    "offsetTop": "none",
                    "offsetBottom": "none",
                    "offsetStart": "none",
                    "offsetEnd": "none",
                    "aspectMode": "cover",
                    "aspectRatio": "9:4",
                    "url": f"{R_axie.find_one({'name': bag['axies'][1]})['link']}"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"● HP:{R_axie.find_one({'name': bag['axies'][1]})['HP']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][1]})['ATK']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][1]})['PRICE']}$",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": "🎒 2/5",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  }
                ]
              }
            },
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": f" ▶ {R_axie.find_one({'name': bag['axies'][2]})['name']} ◀",
                    "weight": "bold",
                    "style": "normal",
                    "decoration": "none",
                    "position": "absolute",
                    "align": "start",
                    "margin": "xxl",
                    "size": "lg",
                    "offsetStart": "xxl",
                    "offsetTop": "xxl",
                    "flex": 90,
                    "color": "#000000"
                  }
                ],
                "position": "relative"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "position": "relative",
                    "margin": "none",
                    "align": "center",
                    "size": "full",
                    "offsetTop": "none",
                    "offsetBottom": "none",
                    "offsetStart": "none",
                    "offsetEnd": "none",
                    "aspectMode": "cover",
                    "aspectRatio": "9:4",
                    "url": f"{R_axie.find_one({'name': bag['axies'][2]})['link']}"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"● HP:{R_axie.find_one({'name': bag['axies'][2]})['HP']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][2]})['ATK']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][2]})['PRICE']}$",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": "🎒 3/5",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  }
                ]
              }
            },
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": f" ▶ {R_axie.find_one({'name': bag['axies'][3]})['name']} ◀",
                    "weight": "bold",
                    "style": "normal",
                    "decoration": "none",
                    "position": "absolute",
                    "align": "start",
                    "margin": "xxl",
                    "size": "lg",
                    "offsetStart": "xxl",
                    "offsetTop": "xxl",
                    "flex": 90,
                    "color": "#000000"
                  }
                ],
                "position": "relative"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "position": "relative",
                    "margin": "none",
                    "align": "center",
                    "size": "full",
                    "offsetTop": "none",
                    "offsetBottom": "none",
                    "offsetStart": "none",
                    "offsetEnd": "none",
                    "aspectMode": "cover",
                    "aspectRatio": "9:4",
                    "url": f"{R_axie.find_one({'name': bag['axies'][3]})['link']}"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"● HP:{R_axie.find_one({'name': bag['axies'][3]})['HP']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][3]})['ATK']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][3]})['PRICE']}$",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": "🎒 4/5",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  }
                ]
              }
            },
            {
              "type": "bubble",
              "header": {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": f" ▶ {R_axie.find_one({'name': bag['axies'][4]})['name']} ◀",
                    "weight": "bold",
                    "style": "normal",
                    "decoration": "none",
                    "position": "absolute",
                    "align": "start",
                    "margin": "xxl",
                    "size": "lg",
                    "offsetStart": "xxl",
                    "offsetTop": "xxl",
                    "flex": 90,
                    "color": "#000000"
                  }
                ],
                "position": "relative"
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "position": "relative",
                    "margin": "none",
                    "align": "center",
                    "size": "full",
                    "offsetTop": "none",
                    "offsetBottom": "none",
                    "offsetStart": "none",
                    "offsetEnd": "none",
                    "aspectMode": "cover",
                    "aspectRatio": "9:4",
                    "url": f"{R_axie.find_one({'name': bag['axies'][4]})['link']}"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"● HP:{R_axie.find_one({'name': bag['axies'][4]})['HP']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][4]})['ATK']}",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": f"● PRICE:{R_axie.find_one({'name': bag['axies'][4]})['PRICE']}$",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  },
                  {
                    "type": "text",
                    "text": "🎒 5/5",
                    "weight": "bold",
                    "margin": "xs",
                    "size": "xxl",
                    "color": "#696969",
                    "align": "start",
                    "offsetStart": "xs"
                  }
                ]
              }
            }
          ]
        }))
    def 出售(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        self.bot.reply_message(self.token, FlexSendMessage('出售', {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "選擇要出售哪一隻",
        "weight": "bold",
        "flex": 90,
        "align": "center",
        "size": "xxl"
      }
    ],
    "backgroundColor": "#ffffff"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"▶ {bag['axies'][0]} ◀",
          "text": "!delONE"
        },
        "style": "secondary",
        "height": "md"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"▶ {bag['axies'][1]} ◀",
          "text": "!delTWO"
        },
        "style": "secondary",
        "margin": "xxl"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"▶ {bag['axies'][2]} ◀",
          "text": "!delTHR"
        },
        "style": "secondary",
        "margin": "xxl"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"▶ {bag['axies'][3]} ◀",
          "text": "!delFOU"
        },
        "margin": "xxl",
        "style": "secondary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"▶ {bag['axies'][4]} ◀",
          "text": "!delFIV"
        },
        "style": "secondary",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
            "offsetStart": "xxl"
          },
          {
            "type": "text",
            "text": "NONE 不能出售",
            "weight": "bold",
            "margin": "none",
            "color": "#f7347a",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "icon",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
            "offsetEnd": "xxl"
          }
        ],
        "margin": "xxl"
      }
    ],
    "backgroundColor": "#ffffff"
  }
}))
    def delONE(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        delete = []
        a = bag['axies']
        if a[0] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("跟你說NONE不能出售\n"
                                                               "是在哭哦?"))
        else:
            delete.append(a[0])
            del(a[0])
            a.insert(0, "NONE")
            R_bag.update_one({"user": user}, {"$set": {"axies": a}})
            R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit['deposit'] + R_axie.find_one({"name": delete[0]})['PRICE']}})
            self.bot.reply_message(self.token, TextSendMessage(f"已出售{delete[0]}\n"
                                                               f"價格:{R_axie.find_one({'name': delete[0]})['PRICE']}\n"
                                                               f"存款:{deposit['deposit'] + R_axie.find_one({'name': delete[0]})['PRICE']}"))
    def delTWO(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        delete = []
        a = bag['axies']
        if a[1] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("跟你說NONE不能出售\n"
                                                               "是在哭哦?"))
        else:
            delete.append(a[1])
            del(a[1])
            a.insert(1, "NONE")
            R_bag.update_one({"user": user}, {"$set": {"axies": a}})
            R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit['deposit'] + R_axie.find_one({"name": delete[0]})['PRICE']}})
            self.bot.reply_message(self.token, TextSendMessage(f"已出售{delete[0]}\n"
                                                               f"價格:{R_axie.find_one({'name': delete[0]})['PRICE']}\n"
                                                               f"存款:{deposit['deposit'] + R_axie.find_one({'name': delete[0]})['PRICE']}"))
    def delTHR(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        delete = []
        a = bag['axies']
        if a[2] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("跟你說NONE不能出售\n"
                                                               "是在哭哦?"))
        else:
            delete.append(a[2])
            del(a[2])
            a.insert(2, "NONE")
            R_bag.update_one({"user": user}, {"$set": {"axies": a}})
            R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit['deposit'] + R_axie.find_one({"name": delete[0]})['PRICE']}})
            self.bot.reply_message(self.token, TextSendMessage(f"已出售{delete[0]}\n"
                                                               f"價格:{R_axie.find_one({'name': delete[0]})['PRICE']}\n"
                                                               f"存款:{deposit['deposit'] + R_axie.find_one({'name': delete[0]})['PRICE']}"))
    def delFOU(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        delete = []
        a = bag['axies']
        if a[3] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("跟你說NONE不能出售\n"
                                                               "是在哭哦?"))
        else:
            delete.append(a[3])
            del(a[3])
            a.insert(3, "NONE")
            R_bag.update_one({"user": user}, {"$set": {"axies": a}})
            R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit['deposit'] + R_axie.find_one({"name": delete[0]})['PRICE']}})
            self.bot.reply_message(self.token, TextSendMessage(f"已出售{delete[0]}\n"
                                                               f"價格:{R_axie.find_one({'name': delete[0]})['PRICE']}\n"
                                                               f"存款:{deposit['deposit'] + R_axie.find_one({'name': delete[0]})['PRICE']}"))
    def delFIV(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        delete = []
        a = bag['axies']
        if a[4] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("跟你說NONE不能出售\n"
                                                               "是在哭哦?"))
        else:
            delete.append(a[4])
            del(a[4])
            a.insert(4, "NONE")
            R_bag.update_one({"user": user}, {"$set": {"axies": a}})
            R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit['deposit'] + R_axie.find_one({"name": delete[0]})['PRICE']}})
            self.bot.reply_message(self.token, TextSendMessage(f"已出售{delete[0]}\n"
                                                               f"價格:{R_axie.find_one({'name': delete[0]})['PRICE']}\n"
                                                               f"存款:{deposit['deposit'] + R_axie.find_one({'name': delete[0]})['PRICE']}"))
    def 出戰(self, event, args):
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            self.bot.reply_message(self.token, FlexSendMessage('出戰設置', {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "選擇預設出戰寵物",
                            "weight": "bold",
                            "flex": 90,
                            "align": "center",
                            "size": "xxl"
                        }
                    ],
                    "backgroundColor": "#ffffff"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"▶ {bag['axies'][0]} ◀",
                                "text": "!atk1"
                            },
                            "style": "secondary",
                            "height": "md"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"▶ {bag['axies'][1]} ◀",
                                "text": "!atk2"
                            },
                            "style": "secondary",
                            "margin": "xxl"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"▶ {bag['axies'][2]} ◀",
                                "text": "!atk3"
                            },
                            "style": "secondary",
                            "margin": "xxl"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"▶ {bag['axies'][3]} ◀",
                                "text": "!atk4"
                            },
                            "margin": "xxl",
                            "style": "secondary"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"▶ {bag['axies'][4]} ◀",
                                "text": "!atk5"
                            },
                            "style": "secondary",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "offsetStart": "xxl"
                                },
                                {
                                    "type": "text",
                                    "text": "NONE 不能出戰",
                                    "weight": "bold",
                                    "margin": "none",
                                    "color": "#f7347a",
                                    "size": "xl",
                                    "align": "center"
                                },
                                {
                                    "type": "icon",
                                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png",
                                    "offsetEnd": "xxl"
                                }
                            ],
                            "margin": "xxl"
                        }
                    ],
                    "backgroundColor": "#ffffff"
                }
            }))
    def atk1(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        if bag['axies'][0] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("你是眼睛脫窗嗎?\n"
                                                               "不是說NONE不能出戰"))
        else:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            R_bag.update_one({"user": user}, {"$set": {"RPG": 0}})
            self.bot.reply_message(self.token, TextSendMessage("已將預設出戰改為\n"
                                                               "背包第1格"))
    def atk2(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        if bag['axies'][1] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("你是眼睛脫窗嗎?\n"
                                                               "不是說NONE不能出戰"))
        else:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            R_bag.update_one({"user": user}, {"$set": {"RPG": 1}})
            self.bot.reply_message(self.token, TextSendMessage("已將預設出戰改為\n"
                                                               "背包第2格"))
    def atk3(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        if bag['axies'][2] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("你是眼睛脫窗嗎?\n"
                                                               "不是說NONE不能出戰"))
        else:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            R_bag.update_one({"user": user}, {"$set": {"RPG": 2}})
            self.bot.reply_message(self.token, TextSendMessage("已將預設出戰改為\n"
                                                               "背包第3格"))
    def atk4(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        if bag['axies'][3] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("你是眼睛脫窗嗎?\n"
                                                               "不是說NONE不能出戰"))
        else:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            R_bag.update_one({"user": user}, {"$set": {"RPG": 3}})
            self.bot.reply_message(self.token, TextSendMessage("已將預設出戰改為\n"
                                                               "背包第4格"))
    def atk5(self, event, args):
        user = event.source.user_id
        group_id = event.source.group_id
        take = bot.get_group_member_profile(group_id, user)
        bag = R_bag.find_one({"user": user})
        deposit = R_deposit.find_one({"user": user})
        if bag['axies'][4] == "NONE":
            self.bot.reply_message(self.token, TextSendMessage("你是眼睛脫窗嗎?\n"
                                                               "不是說NONE不能出戰"))
        else:
            user = event.source.user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            R_bag.update_one({"user": user}, {"$set": {"RPG": 4}})
            self.bot.reply_message(self.token, TextSendMessage("已將預設出戰改為\n"
                                                               "背包第5格"))
    def 決鬥(self, event, args):
        try:
            user = event.source.user_id
            mentionuser = event.message.mention.mentionees[0].user_id
            group_id = event.source.group_id
            take = bot.get_group_member_profile(group_id, user)
            bag = R_bag.find_one({"user": user})
            deposit = R_deposit.find_one({"user": user})
            mentiontake = bot.get_group_member_profile(group_id, mentionuser)
            mentionbag = R_bag.find_one({"user": mentionuser})
            mentiondeposit = R_deposit.find_one({"user": mentionuser})
            if bag['axies'][bag['RPG']] == "NONE":
                self.bot.reply_message(self.token, TextSendMessage("你預設出戰寵物空的\n"
                                                                   "還想跟別人決鬥?"))
            elif mentionbag['axies'][mentionbag['RPG']] == "NONE":
                self.bot.reply_message(self.token, TextSendMessage("很抱歉 他的預設出戰寵物\n"
                                                                   "是空的"))
            else:
                winner = []
                a = random.uniform(0, 5)
                money = round(a, 2)
                aHP = R_axie.find_one({'name': bag['axies'][bag['RPG']]})['HP']
                aATK = R_axie.find_one({'name': bag['axies'][bag['RPG']]})['ATK']
                bHP = R_axie.find_one({'name': mentionbag['axies'][mentionbag['RPG']]})['HP']
                bATK = R_axie.find_one({'name': mentionbag['axies'][mentionbag['RPG']]})['ATK']
                if bHP - aATK < aHP - bATK: # user 贏
                    winner.append(take.display_name)
                    R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit["deposit"] + money}})
                    R_deposit.update_one({"user": mentionuser}, {"$set": {"deposit": mentiondeposit["deposit"] - money}})
                elif bHP - aATK > aHP - bATK: # mentionuser 贏
                    winner.append(mentiontake.display_name)
                    R_deposit.update_one({"user": user}, {"$set": {"deposit": deposit['deposit'] - money}})
                    R_deposit.update_one({"user": mentionuser}, {"$set": {"deposit": mentiondeposit['deposit'] + money}})
                else:
                    talk = ["平手欸好扯", "本局平手", "居然平手呀~"]
                    self.bot.reply_message(self.token, TextSendMessage(random.choice(talk)))
                    return
                print(winner[0])
                self.bot.reply_message(self.token, FlexSendMessage('決鬥資訊', {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": f" ▶ {R_axie.find_one({'name': bag['axies'][bag['RPG']]})['name']} ◀",
            "weight": "bold",
            "style": "normal",
            "decoration": "none",
            "position": "absolute",
            "align": "start",
            "margin": "xxl",
            "size": "lg",
            "offsetStart": "xxl",
            "offsetTop": "xxl",
            "flex": 90,
            "color": "#000000"
          }
        ],
        "position": "relative"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{R_axie.find_one({'name': bag['axies'][bag['RPG']]})['link']}",
            "position": "relative",
            "margin": "none",
            "align": "center",
            "size": "full",
            "offsetTop": "none",
            "offsetBottom": "none",
            "offsetStart": "none",
            "offsetEnd": "none",
            "aspectMode": "cover",
            "aspectRatio": "9:4"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"● HP:{R_axie.find_one({'name': bag['axies'][bag['RPG']]})['HP']}",
            "weight": "bold",
            "margin": "xs",
            "size": "xxl",
            "color": "#f7347a",
            "align": "start",
            "offsetStart": "xs"
          },
          {
            "type": "text",
            "text": f"● ATK:{R_axie.find_one({'name': bag['axies'][bag['RPG']]})['ATK']}",
            "weight": "bold",
            "margin": "xs",
            "size": "xxl",
            "color": "#ff7373",
            "align": "start",
            "offsetStart": "xs"
          },
          {
            "type": "text",
            "text": f"攻擊方:{take.display_name}",
            "weight": "bold",
            "margin": "xs",
            "size": "xxl",
            "color": "#696969",
            "align": "start",
            "offsetStart": "xs"
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#fdcf58"
        },
        "body": {
          "backgroundColor": "#fdcf58"
        },
        "footer": {
          "backgroundColor": "#fdcf58"
        }
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "filler"
          },
          {
            "type": "text",
            "text": "V.S",
            "margin": "xxl",
            "size": "5xl",
            "offsetTop": "none",
            "offsetBottom": "none",
            "offsetStart": "none",
            "offsetEnd": "none",
            "align": "center",
            "contents": [],
            "weight": "bold",
            "color": "#800909"
          },
          {
            "type": "filler"
          }
        ],
        "background": {
          "type": "linearGradient",
          "angle": "90deg",
          "startColor": "#f27d0c",
          "endColor": "#fdcf58"
        }
      }
    },
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": f" ▶ {R_axie.find_one({'name': mentionbag['axies'][mentionbag['RPG']]})['name']} ◀",
            "weight": "bold",
            "style": "normal",
            "decoration": "none",
            "position": "absolute",
            "align": "start",
            "margin": "xxl",
            "size": "lg",
            "offsetStart": "xxl",
            "offsetTop": "xxl",
            "flex": 90,
            "color": "#000000"
          }
        ],
        "position": "relative"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "position": "relative",
            "margin": "none",
            "align": "center",
            "size": "full",
            "offsetTop": "none",
            "offsetBottom": "none",
            "offsetStart": "none",
            "offsetEnd": "none",
            "aspectMode": "cover",
            "aspectRatio": "9:4",
            "url": f"{R_axie.find_one({'name': mentionbag['axies'][mentionbag['RPG']]})['link']}"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"● HP:{R_axie.find_one({'name': mentionbag['axies'][mentionbag['RPG']]})['HP']}",
            "weight": "bold",
            "margin": "xs",
            "size": "xxl",
            "color": "#f7347a",
            "align": "start",
            "offsetStart": "xs"
          },
          {
            "type": "text",
            "text": f"● ATK:{R_axie.find_one({'name': mentionbag['axies'][mentionbag['RPG']]})['ATK']}",
            "weight": "bold",
            "margin": "xs",
            "size": "xxl",
            "color": "#ff7373",
            "align": "start",
            "offsetStart": "xs"
          },
          {
            "type": "text",
            "text": f"防守方:{mentiontake.display_name}",
            "weight": "bold",
            "margin": "xs",
            "size": "xxl",
            "color": "#696969",
            "align": "start",
            "offsetStart": "xs"
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#fdcf58"
        },
        "body": {
          "backgroundColor": "#fdcf58"
        },
        "footer": {
          "backgroundColor": "#fdcf58"
        }
      }
    },
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"贏家:{winner[0]}🎉",
            "size": "xxl",
            "margin": "xs",
            "weight": "bold",
            "align": "center",
            "color": "#f6546a"
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"👍贏家加{money}$",
            "weight": "bold",
            "color": "#ff7f50",
            "margin": "xxl",
            "size": "xxl"
          },
          {
            "type": "filler"
          },
          {
            "type": "text",
            "text": f"👎輸家扣{money}$",
            "weight": "bold",
            "color": "#ff6666",
            "margin": "xxl",
            "size": "xxl"
          },
          {
            "type": "filler"
          }
        ]
      },
      "styles": {
        "header": {
          "backgroundColor": "#eeeeee"
        },
        "body": {
          "backgroundColor": "#eeeeee"
        }
      }
    }
  ]
}))
        except AttributeError:
            self.bot.reply_message(self.token, TextSendMessage("請@你要決鬥的對手"))
