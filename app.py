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
from crawl_qpesums import QPECrawler
from special_crawler import SpecialCrawler

# ======self written==========


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'XNUj1qPi/SwRUhXP0HqAlLcP1J3efxOF6SK5eTBhDwxP4oHWYAVSWKOfuE1KZUxO51bRlcy442SS+DwvF9wpA86ug+suW+MLCgeW/VWoKe7Ts9N3T4YjFUfvY+M2pliKPH5HYNhNq/N8yHBIJYYfZAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bf5dd4e6a1bfe57aa6a8973ec0c72a56')

# @app.route("/push/<string:push_text_str>")
# def push_message(push_text_str):
#     print(push_text_str)
#     for uid in UIDS:
#         line_bot_api.push_message(uid, TextSendMessage(text=push_text_str))
#     return push_text_str


# locationNames = ['大豹溪', 'asd', 'aaaaaaaaaaaa']


# # ! deposited
# @app.route("/web", methods=['GET'])
# def web():
#     location = int(request.args['place'])
#     print(location)
#     locationName = locationNames[location]
#
#     # prepare data and send into the view
#     ss = requests.Session()
#
#     return render_template('index.html', locationName=locationName)  # , id=userid)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 6hr weather condition
fster = Forcaster()
# 處理訊息
allInstruction = """所有指令：
「接收」-> 進到隨時處於接收警戒訊息的狀態，若有洪汛以及警特報將會通知！
「取消」-> 停止接收狀態，若有洪汛將 不會 通知
「看預報」-> 可以查看QPESUMS(氣象局新一代劇烈天氣監測系統)未來1小時各地點降雨量
以及各地點未來6小時以下氣象資訊：
1. 天氣狀況文字描述( 晴時多雲 )
2. 降雨機率
3. 氣溫
4. 對環境的感受
「看回波」-> 看過去最近三小時，各地區的最大6筆雷達迴波值"""

qpe_crawler = QPECrawler()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if msg == '接收':
        UIDS.add(event.source.sender_id)
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="訂閱成功！\n" + allInstruction),
            get_what_do_you_want_msg(),
        ])
        return 'OK'
    elif msg == '取消':
        UIDS.remove(event.source.sender_id)
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="取消成功！"),
            get_what_do_you_want_msg(),
        ])
        return 'OK'
    elif msg == '看預報':
        reply_see_report_msg(event)
        # for position in fster.table.keys():
        #     fster.get(position)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=fster.get_weather_msg()))
    elif msg.split()[0] == "我想查看":
        weather_msg = fster.get_one_location_weather_report(msg.split()[1])
        qpe_msg = qpe_crawler.get_location_rain_msg_text(msg.split()[1])
        emoji = []
        indexes = []
        for i, char in enumerate(qpe_msg):
            if char == "$":
                indexes.append(i)
        for i in indexes:
            emoji.append({
                "index": i,
                "productId": "5ac21a18040ab15980c9b43e",
                "emojiId": "025"
            })

        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text=weather_msg),
            TextSendMessage(text=qpe_msg, emojis=emoji if emoji else None),
            get_what_do_you_want_msg()
        ])
    elif msg == "看回波":# TODO: six highest records
        reply_see_radar_msg(event)
    elif msg.split()[0] == "查看回波":
        radar_message = rcal.get_max_six_signle_msg(msg.split()[1])
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=radar_message))
    else:
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text='''所有指令：
「接收」-> 進到隨時處於接收警戒訊息的狀態，若有洪汛以及警特報將會通知
「取消」-> 取消接收狀態，若有洪汛將 不會 通知
「看預報」-> 可以查看QPESUMS(氣象局新一代劇烈天氣監測系統)未來1小時各地點降雨量
以及各地點未來6小時以下氣象資訊：
        1. 天氣狀況文字描述( 晴時多雲 )
        2. 降雨機率
        3. 氣溫
        4. 對環境的感受
「看回波」-> 看過去最近三小時，各地區的最大6筆雷達迴波值'''),
            get_what_do_you_want_msg(),
        ])


def reply_see_report_msg(event):
    camp_msg = ""
    camps = fster.get_location_camps_dict()
    for k in camps:
        camp_msg += k + "的露營溫泉區有:\n"
        for camp in camps[k]:
            camp_msg += camp + "\n"
        camp_msg += "\n"
    camp_msg += "請問您想查看哪地區的\n1.未來六小時降雨機率、氣溫等資訊\n2.未來一小時降雨預測值"
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text=camp_msg),
            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='北部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='復興區',
                            text='我想查看 復興區'
                        ),
                        MessageTemplateAction(
                            label='尖石鄉',
                            text='我想查看 尖石鄉'
                        ),
                        MessageTemplateAction(
                            label='大同鄉',
                            text='我想查看 大同鄉'
                        ),
                    ]
                )
            ),

            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='北部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='金山區',
                            text='我想查看 金山區'
                        ),
                        MessageTemplateAction(
                            label='三峽區',
                            text='我想查看 三峽區'
                        ),
                        MessageTemplateAction(
                            label='烏來區',
                            text='我想查看 烏來區'
                        ),
                    ]
                )
            ),
            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='中部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='信義鄉',
                            text='我想查看 信義鄉'
                        ),
                        MessageTemplateAction(
                            label='仁愛鄉',
                            text='我想查看 仁愛鄉'
                        ),
                        MessageTemplateAction(
                            label='桃源區',
                            text='我想查看 桃源區'
                        ),
                        MessageTemplateAction(
                            label='和平區',
                            text='我想查看 和平區'
                        ),
                    ]
                )
            ),
            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='南部、東部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='六龜區',
                            text='我想查看 六龜區'
                        ),
                        MessageTemplateAction(
                            label='茂林區',
                            text='我想查看 茂林區'
                        ),
                        MessageTemplateAction(
                            label='海端鄉',
                            text='我想查看 海端鄉'
                        ),
                    ]
                )
            ),
        ]
    )


def reply_see_radar_msg(event):
    camp_msg = ""
    camps = fster.get_location_camps_dict()
    for k in camps:
        camp_msg += k + "的露營溫泉區有:\n"
        for camp in camps[k]:
            camp_msg += camp + "\n"
        camp_msg += "\n"
    camp_msg += "請問您想查看哪地區的\n>> 過去最近3小時的降雨雷達回波\n前6名最大值\n"
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text=camp_msg),
            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='北部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='復興區',
                            text='查看回波 復興區'
                        ),
                        MessageTemplateAction(
                            label='尖石鄉',
                            text='查看回波 尖石鄉'
                        ),
                        MessageTemplateAction(
                            label='大同鄉',
                            text='查看回波 大同鄉'
                        ),
                    ]
                )
            ),

            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='北部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='金山區',
                            text='查看回波 金山區'
                        ),
                        MessageTemplateAction(
                            label='三峽區',
                            text='查看回波 三峽區'
                        ),
                        MessageTemplateAction(
                            label='烏來區',
                            text='查看回波 烏來區'
                        ),
                    ]
                )
            ),
            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='中部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='信義鄉',
                            text='查看回波 信義鄉'
                        ),
                        MessageTemplateAction(
                            label='仁愛鄉',
                            text='查看回波 仁愛鄉'
                        ),
                        MessageTemplateAction(
                            label='桃源區',
                            text='查看回波 桃源區'
                        ),
                        MessageTemplateAction(
                            label='和平區',
                            text='查看回波 和平區'
                        ),
                    ]
                )
            ),
            TemplateSendMessage(
                alt_text='請選擇鄉鎮市區',
                template=ButtonsTemplate(
                    title='南部、東部',
                    text='請選擇鄉鎮市區',
                    actions=[
                        MessageTemplateAction(
                            label='六龜區',
                            text='查看回波 六龜區'
                        ),
                        MessageTemplateAction(
                            label='茂林區',
                            text='查看回波 茂林區'
                        ),
                        MessageTemplateAction(
                            label='海端鄉',
                            text='查看回波 海端鄉'
                        ),
                    ]
                )
            ),
        ]
    )


def get_what_do_you_want_msg():
    return TemplateSendMessage(
        alt_text='請問您想做什麼？',
        template=ButtonsTemplate(
            title='請問您想做什麼？',
            text='請選擇指令',
            actions=[
                MessageTemplateAction(
                    label='開始接收警戒資訊',
                    text='接收'
                ),
                MessageTemplateAction(
                    label='停止接收警戒資訊',
                    text='取消'
                ),
                MessageTemplateAction(
                    label='我想看氣象雨量預報',
                    text='看預報'
                ),
                MessageTemplateAction(
                    label='看近3小時雷達迴波極值',
                    text='看回波'
                ),
            ]
        )
    )


@handler.add(FollowEvent)
def welcome(event):
    print("TEST")# TODO
    uid = event.source.sender_id
    profile = line_bot_api.get_profile(uid)
    name = profile.display_name
    message = TextSendMessage(text=get_welcome_msg(name))
    line_bot_api.reply_message(event.reply_token, [message, get_what_do_you_want_msg()])


@handler.add(LeaveEvent)
def leave(event):
    uid = event.source.sender_id
    UIDS.remove(uid)
    return "OK"


UIDS = set()

rcal = RainCalculator()


def crawl_data():
    #! if there is bug while running, consider add this:
    # rcal = RainCalculator()
    while True:
        crl60 = CrawlSixty()
        crl60.main()
        crl60.crawl_3hr()
        print("================ DONE crawling file====================")

        rcal.initialize()
        rcal.update(60)
        print("under is 60min check")
        rcal.check(1)

        rcal.update(180)
        print("====== DONE CHECKING WATER LEVEL ======")

        time.sleep(8 * 60)


def wake():
    while True:
        s = requests.Session()
        s.get('https://avoid-coming-water.herokuapp.com/')
        print('== == WAKING UP == ==')
        time.sleep(20 * 60)


def get_welcome_msg(name):
    return f'''歡迎！{name}！
這裡是「水來了，快逃！」
您可以藉由傳送指令來獲取對應的資訊。
目前支援的地點如下：
大豹溪蟾蜍山谷 泰岡野溪溫泉
秀巒野溪溫泉 琉璃灣露營區 邦腹溪營地
武界露營 二山子野溪溫泉 桶後溪營地
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
「接收」-> 進到隨時處於接收警戒訊息的狀態，若有洪汛以及警特報將會通知
「取消」-> 取消接收狀態，若有洪汛將 不會 通知
「看預報」-> 可以查看QPESUMS(氣象局新一代劇烈天氣監測系統)未來1小時各地點降雨量
以及各地點未來6小時以下氣象資訊：
        1. 天氣狀況文字描述( 晴時多雲 )
        2. 降雨機率
        3. 氣溫
        4. 對環境的感受
「看回波」-> 看過去最近三小時，各地區的最大6筆雷達迴波值

現在就試試下指令吧！
'''


calc_thread: List[threading.Thread] = []


def qpe_crawl_thread():
    while True:
        qpe_crawler.get_image()
        print("-- -- DONE QPE CRAWL-- --")
        time.sleep(8 * 60)


def maintain():
    while True:
        if not calc_thread[0].is_alive():
            with open('fail_running.txt', 'a') as f:
                now = time.localtime()
                f.write(f"process is dead at {now.tm_wday}, {now.tm_hour}hr, {now.tm_min}min, {now.tm_sec}sec\n")
            calc_thread[0] = threading.Thread(target=crawl_data, name="process_rebuild")
            calc_thread[0].start()
            # raise RuntimeError('Not running with the Werkzeug Server')
        time.sleep(1 * 60)


special_crawler = SpecialCrawler()

def pushWarning():
    time.sleep(1 * 60)
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
                    result += f"最多還有{base_num // 5 * 5}~{(base_num // 5 + 1) * 5}分鐘洪水會到，盡速撤離喔\n"

        # deal with spetial report
        special_massage = special_crawler.get_spetial_warning_msg()
        # print(special_massage)

        for uid in UIDS:
            push_arr = []
            if special_massage:
                push_arr.append(TextSendMessage(text="以下為警特報資訊：\n"+special_massage))
            if result:
                push_arr.append(TextSendMessage(text="以下為警戒資訊：\n"+result))
            if len(push_arr):
                line_bot_api.push_message(uid, push_arr)
        print(f"push\n{result}")
        print("====== DONE PUSHING MESSAGE ======")
        time.sleep(1 * 60)


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

    qpeThread = threading.Thread(target=qpe_crawl_thread, name='qpe_crawl_thread')
    qpeThread.start()

    app.run(host='0.0.0.0', port=port)
