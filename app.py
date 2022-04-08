# from crypt import methods
from flask import Flask, request, abort, jsonify

# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import os
import time
import threading
import requests
import datetime
# ======python的函數庫==========

# ======self written==========
from 最近60分雷達回波抓XML import CrawlSixty
from 算各地60分鐘換算雨量 import RainCalculator

# ======self written==========


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(
    'XNUj1qPi/SwRUhXP0HqAlLcP1J3efxOF6SK5eTBhDwxP4oHWYAVSWKOfuE1KZUxO51bRlcy442SS+DwvF9wpA86ug+suW+MLCgeW/VWoKe7Ts9N3T4YjFUfvY+M2pliKPH5HYNhNq/N8yHBIJYYfZAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bf5dd4e6a1bfe57aa6a8973ec0c72a56')


@app.route("/push/<string:push_text_str>")
def push_message(push_text_str):
    print(push_text_str)
    for uid in UIDS:
        line_bot_api.push_message(uid, TextSendMessage(text=push_text_str))
    return push_text_str


@app.route("/debug")
def debug():
    return "E)$"
    startpath = os.getcwd()
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
    for dirname, _, filenames in os.walk(os.path.join(os.getcwd(), "60min_data\\")):
        with open(os.path.join(dirname, filenames[0]), 'r') as f:
            data = f.readline()
            print(data[:500])
    return jsonify(data)


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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # profile = None
    # try:
    #     profile = line_bot_api.get_profile('<user_id>')
    # except Exception as e:
    #     pass
    # if profile == None: return
    # UIDS.add(profile)
    msg = event.message.text
    if msg == '接收':
        UIDS.add(event.source.sender_id)
        return 'OK'
    elif msg == '取消':
        UIDS.remove(event.source.sender_id)
        return 'OK'
    else:
        with open(os.path.join(os.getcwd(), '60min_data', 'testfile'), 'r') as f:
            msg += f.readline()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg+"\n"+"我就學..."))

    # UIDS[event.source.sender_id] = event.message
    # if msg == 'sc':
    #     uid = event.source.sender_id
    #     if uid in UIDS:
    #         line_bot_api.reply_message(event.reply_token, UIDS[uid])
    #         return
    # line_bot_api.push_message(profile, TextSendMessage(text=str(UIDS)))

    # if '最新合作廠商' in msg:
    #     message = imagemap_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '最新活動訊息' in msg:
    #     message = buttons_message()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '註冊會員' in msg:
    #     message = Confirm_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '旋轉木馬' in msg:
    #     message = Carousel_Template()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '圖片畫廊' in msg:
    #     message = test()
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif '功能列表' in msg:
    #     message = function_list()
    #     line_bot_api.reply_message(event.reply_token, message)
    # else:
    #     message = TextSendMessage(text=msg)
    #     line_bot_api.reply_message(event.reply_token, message)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    # UIDS.add(uid)
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


UIDS = set()


def process():
    s = requests.Session()
    river_name = {
        "0": "大豹溪","1": "泰岡野溪溫泉","2": "秀巒野溪溫泉","3": "琉璃灣露營區","4": "邦腹溪營地",
        "5": "武界露營","6": "二山子野溪溫泉","7": "桶後溪營地","8": "八煙野溪溫泉","9": "天狗溪溫泉",
        "10": "馬陵溫泉","11": "精英野溪溫泉","12": "栗松溫泉","13": "流霞谷親水烤肉園區","14": "八度野溪溫泉區",
        "15": "梅淮露營區","16": "五六露營農場","17": "祕密基地露營區","18": "瑞岩溫泉野溪邊露營","19": "金崙溫泉野溪露營區",
        "20": "嘎拉賀溫泉","21": "四稜溫泉","22": "神駒谷溫泉","23": "太魯灣溪溫泉","24": "瑞岩溫泉",
        "25": "紅香溫泉","26": "萬大南溪溫泉","27": "樂樂谷溫泉","28": "玉穗溫泉","29": "荖荖溫泉",
        "30": "五區_拉卡_溫泉","31": "文山溫泉",
    }
    while True:
        crl60 = CrawlSixty()
        crl60.main()
        crl60.crawl_3hr()
        print("================ DONE crawling file====================")

        rcal = RainCalculator()
        rcal.update(60)
        rcal.update(180)
        rcal.check()
        print(datetime.datetime.now())

        result = ""
        with open('alert', 'r') as f:
            for line in f.readlines():
                result += river_name[line]+"警戒囉！\n"
        s.get('https://03d0-61-221-225-123.ngrok.io/push/'+result)

        time.sleep(8 * 60)


# import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    print('starting')
    threading.Thread(target=process).start()
    print("finished")
    app.run(host='0.0.0.0', port=port)
