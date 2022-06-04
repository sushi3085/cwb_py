# from crypt import methods
from flask import Flask, request, abort, jsonify, render_template

# ======這裡是呼叫的檔案內容=====
# from message import *
# from new import *
# from Function import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import os
import time
import threading
import requests
import datetime

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
# ======python的函數庫==========

# ======self written==========
from typing import List

from 最近60分雷達回波抓XML import CrawlSixty
from 算各地60分鐘換算雨量 import RainCalculator
from 抓預報 import Forcaster
# ======self written==========



app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'XNUj1qPi/SwRUhXP0HqAlLcP1J3efxOF6SK5eTBhDwxP4oHWYAVSWKOfuE1KZUxO51bRlcy442SS+DwvF9wpA86ug+suW+MLCgeW/VWoKe7Ts9N3T4YjFUfvY+M2pliKPH5HYNhNq/N8yHBIJYYfZAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bf5dd4e6a1bfe57aa6a8973ec0c72a56')


# locationNames = ['大豹溪','asd','aaaaaaaaaaaa']
# # ! deposited
# @app.route("/web", methods=['GET'])
# def web():
#     location = int(request.args['place'])
#     print(location)
#     locationName = locationNames[location]

#     # prepare data and send into the view
#     ss = requests.Session()

#     return render_template('index.html',  locationName=locationName)#, id=userid)






# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



fster = Forcaster()
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    msg = event.message.text
    if msg == '接收':
        UIDS.add(event.source.sender_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="訂閱成功，若要取消請回覆「取消」"))
        return 'OK'
    elif msg == '取消':
        UIDS.remove(event.source.sender_id)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="取消成功，若要回復訂閱請回覆「訂閱」"))
        return 'OK'
    elif msg== '看預報':
        for position in fster.table.keys():
            fster.get(position)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=fster.get_weather_msg()))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='''所有指令：
「接收」-> 進到隨時處於接收警戒訊息的狀態，若有洪汛將會通知
「取消」-> 取消接收狀態，若有洪汛將 不會 通知
「看預報」-> 可以查看各地點未來6小時以下氣象資訊：
        1. 天氣狀況文字描述( 晴時多雲 )
        2. 降雨機率
        3. 氣溫
        4. 對環境的感受'''))


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    # UIDS.add(uid)
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=get_welcome_msg())
    line_bot_api.reply_message(event.reply_token, message)


UIDS = set()


def crawl_data():
    while True:
        crl60 = CrawlSixty()
        crl60.main()
        crl60.crawl_3hr()
        print("================ DONE crawling file====================")

        rcal = RainCalculator()
        rcal.update(60)
        print("under is 60min check")
        rcal.check(1)

        rcal.update(180)
        print("under is 3hr check")
        print("====== DONE CHECKING WATER LEVEL ======")

        time.sleep(8 * 60)


def wake():
    while True:
        s = requests.Session()
        s.get('https://avoid-coming-water.herokuapp.com/')
        print('== == WAKING UP == ==')
        time.sleep(20*60)


def get_welcome_msg():
    return'''嗨~ 這裡是「水來了，快逃！」
您可以藉由傳送指令來獲取對應的資訊。
目前支援的地點如下：
大豹溪蟾蜍山谷 泰岡野溪溫泉 秀巒野溪溫泉
琉璃灣露營區 邦腹溪營地 武界露營
二山子野溪溫泉 桶後溪營地
八煙野溪溫泉 天狗溪溫泉 馬陵溫泉
精英野溪溫泉 栗松溫泉 梅淮露營區
流霞谷親水烤肉園區 五六露營農場
八度野溪溫泉區 祕密基地露營區
瑞岩溫泉野溪邊露營 四稜溫泉
金崙溫泉野溪露營區 嘎拉賀溫泉
神駒谷溫泉 太魯灣溪溫泉 瑞岩溫泉
紅香溫泉 萬大南溪溫泉 樂樂谷溫泉
玉穗溫泉 荖荖溫泉 五區_拉卡_溫泉
文山溫泉
===== ===== =====
所有指令：
「接收」-> 進到隨時處於接收警戒訊息的狀態，若有洪汛將會通知
「取消」-> 取消接收狀態，若有洪汛將 不會 通知
「看預報」-> 可以查看各地點未來6小時以下氣象資訊：
        1. 天氣狀況文字描述( 晴時多雲 )
        2. 降雨機率
        3. 氣溫
        4. 對環境的感受

現在就試試下指令吧！
'''


calc_thread: List[threading.Thread] = []


def maintain():
    while True:
        if not calc_thread[0].is_alive():
            with open('fail_running.txt', 'a') as f:
                now = time.localtime()
                f.write(f"process is dead at {now.tm_wday}, {now.tm_hour}hr, {now.tm_min}min, {now.tm_sec}sec\n")
            calc_thread[0] = threading.Thread(target=crawl_data, name="process_rebuild")
            calc_thread[0].start()
            # raise RuntimeError('Not running with the Werkzeug Server')
        time.sleep(1*60)


def pushWarning():
    # time.sleep(5*60)
    river_name = {
        "0": "大豹溪", "1": "泰岡野溪溫泉", "2": "秀巒野溪溫泉", "3": "琉璃灣露營區", "4": "邦腹溪營地",
        "5": "武界露營", "6": "二山子野溪溫泉", "7": "桶後溪營地", "8": "八煙野溪溫泉", "9": "天狗溪溫泉",
        "10": "馬陵溫泉", "11": "精英野溪溫泉", "12": "栗松溫泉", "13": "流霞谷親水烤肉園區", "14": "八度野溪溫泉區",
        "15": "梅淮露營區", "16": "五六露營農場", "17": "祕密基地露營區", "18": "瑞岩溫泉野溪邊露營", "19": "金崙溫泉野溪露營區",
        "20": "嘎拉賀溫泉", "21": "四稜溫泉", "22": "神駒谷溫泉", "23": "太魯灣溪溫泉", "24": "瑞岩溫泉",
        "25": "紅香溫泉", "26": "萬大南溪溫泉", "27": "樂樂谷溫泉", "28": "玉穗溫泉", "29": "荖荖溫泉",
        "30": "五區_拉卡_溫泉", "31": "文山溫泉",
    }
    while True:
        cache = {}
        with open('alert', 'r') as f:
            for line in f.readlines():
                sp = line.split()
                cache[sp[0]] = int(sp[1]) - 1

        with open('alert', 'w') as f:
            for k, v in cache.items():
                if v < -60:
                    continue
                f.write(f"{k} {v}\n")

        result = ""
        with open('alert', 'r') as f:
            for line in f.readlines():
                splits = line.replace('\n', '').split(' ')
                result += river_name[splits[0]] + "警戒囉！\n"
                if cache[splits[0]] <= 0:
                    result += f"山洪已經到了！\n"
                else:
                    base_num = cache[splits[0]]
                    result += f"最多還有{base_num//5*5}~{(base_num//5+1)*5}分鐘洪水會到，盡速撤離喔\n"

        for uid in UIDS:
            line_bot_api.push_message(uid, TextSendMessage(text=result))
        print(f"push\n{result}")
        print("====== DONE PUSHING MESSAGE ======")
        time.sleep(1*60)

# import os
if __name__ == "__main__":
    # print(os.path.isfile(os.path.join(os.getcwd(), 'testfile')))
    # print(os.path.isdir(os.path.join(os.getcwd(), '60min_data')))
    port = int(os.environ.get('PORT', 5000))
    thread = threading.Thread(target=crawl_data, name="process")
    calc_thread.append(thread)
    thread.start()
    thread2 = threading.Thread(target=wake, name="wake")
    thread2.start()

    maintainThread = threading.Thread(target=maintain, name="maintain process")
    maintainThread.start()

    pushWarningThread = threading.Thread(target=pushWarning, name='pushWarningThread')
    pushWarningThread.start()

    app.run(host='0.0.0.0', port=port)
