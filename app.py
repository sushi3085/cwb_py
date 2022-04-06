# from crypt import methods
from flask import Flask, request, abort, jsonify, current_app

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# ======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
# ======這裡是呼叫的檔案內容=====

# ======python的函數庫==========
import tempfile, os
import datetime
import time
import threading
import requests
# ======python的函數庫==========

# ======self written==========
from Code.dataCrawler import dumpRadarData, getRadarData
import numpy as np
from Code.算各地60分鐘換算雨量 import RainCalculator
from Code.最近60分雷達回波抓XML import CrawlSixty

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
    current_app.logger.info(push_text_str)
    for uid in UIDS:
        line_bot_api.push_message(uid, TextSendMessage(text=push_text_str))


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
    profile = None
    try:
        profile = line_bot_api.get_profile('<user_id>')
    except Exception as e:
        pass
    if profile == None: return
    UIDS.add(profile)
    msg = event.message.text
    line_bot_api.push_message(profile, TextSendMessage(text=str(UIDS)))

    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    UIDS.add(uid)
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)


UIDS = set()


def process():
    while True:
        time.sleep(8 * 60)
        crl60 = CrawlSixty()
        crl60.main()

        rcal = RainCalculator()
        rcal.update()
        rcal.check()
        print("================Loop Done====================")


# import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    threading.Thread(target=process).start()
