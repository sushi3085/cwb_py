import requests
import time

ss = requests.Session()
url = "https://cwb-js-test.herokuapp.com/"

while True:
	time.sleep(0.1*60)# 28 min
	response = ss.get(url)
	lt = time.localtime()
	print(f"{lt.tm_mon}/{lt.tm_mday} {lt.tm_hour}:{lt.tm_min}")