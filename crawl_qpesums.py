import requests
import json
import numpy

class QPECrawler:

    QPESUMS_URL = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0046-001?Authorization={}&downloadType=WEB&format=JSON'

    def __init__(self):
        QPECrawler.QPUSUMS_URL = QPECrawler.QPESUMS_URL.format(self.get_auth_token())
        self.data = None

    def get_auth_token(self):
        with open('auth_token.txt', 'r', encoding='UTF-8') as f:
            return f.readline()

    def get_image(self):
        ss = requests.Session()
        r = ss.get(self.QPUSUMS_URL)
        json_data = json.loads(r.text)

        data = json_data['cwbopendata']['dataset']['contents']['content'].split(',')
        self.data = numpy.array(list(map(self.to_int, data))).reshape(95, 75)
        return self.data

    def get_range_rain(self, long1, lat1, long2, lat2):
        # 117.975, 19.975
        x1 = (long1-117.975)//0.075
        y1 = (lat1-19.975)//0.075
        x2 = (long2-117.975)//0.075
        y2 = (lat2-19.975)//0.075
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                result += self.data[y,x]
        return result

    def to_int(self, string):
        splits = string.split('E')
        return max(0, float(splits[0])**int(splits[1]))

    def 

if __name__ == '__main__':
    qpe = QPECrawler()
    image = qpe.get_image()