import json
import requests
import numpy as np
import os

RADAR_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0059-001?Authorization=CWB-41DC9AED-4979-4F29-8CB7-E6BF577E5036&downloadType=WEB&format=JSON"
RAIN_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-B0045-001?Authorization=CWB-41DC9AED-4979-4F29-8CB7-E6BF577E5036&downloadType=WEB&format=JSON"

def toNum(x:str):
	tem = x.split("E")
	return float(tem[0]) * pow(10, int(tem[1]))

def wrapStamp(stamp:str):
	result = ""
	for ch in stamp:
		if ch == ":":
			result += "_"
			continue
		result += ch
	return result

def getRadarData() -> list:
	ss = requests.Session()
	response = ss.get(RADAR_URL)
	content = json.loads(response.text)

	data = content['cwbopendata']['dataset']['contents']['content']
	stamp = content['cwbopendata']['sent']

	data = data.split(",")
	data = list(map(toNum, data))

	# data = np.reshape(data, (881, 921))
	
	return data, wrapStamp(stamp)

def main():
	radarData , timeStamp = getRadarData()
	
	with open(f'data/{timeStamp}.txt','w') as f:
		f.write(json.dumps(radarData))

if __name__ == "__main__":
	main()
	