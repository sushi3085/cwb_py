import requests
import json
import numpy
from typing import Dict

from 算各地60分鐘換算雨量 import RainCalculator
from 曼寧等公式 import manning_velocity


class QPECrawler:
    COUNTY_COORs_TABLE = {
        '復興區': [{'流霞谷親水烤肉園區': (121.375, 24.8), '八度野溪露營區': (121.3375, 24.7875), '嘎拉賀溫泉': (121.4111, 24.6313), '四稜溫泉': (121.4346, 24.6379)}],
        '尖石鄉': [{'泰崗野溪溫泉': (121.3, 24.625), '梅淮露營區': (121.2125, 24.6875), '秀巒溫泉': (121.2875, 24.625), }],
        '大同鄉': [{'祕密基地露營區': (121.5625, 24.6625)}],
        '和平區': [{'神駒谷溫泉': (121.0119, 24.2043), '馬稜溫泉': (121.05, 24.225), }],
        '信義鄉': [{'樂樂谷溫泉': (120.9534, 23.5460), }, ],
        '仁愛鄉': [{'武界露營': (121.05, 23.8875), }, {'五六露營農場': (121.1125, 24.0125), }, {'太魯灣溪溫泉': (121.1704, 24.0206), }, {'精英野溪溫泉': (121.2, 24.025), },
                {'瑞岩溫泉': (121.1703, 24.1353), }, {'紅香溫泉': (121.18, 24.1625), }, {'萬大南溪溫泉': (121.1981, 23.9391), }, ],
        '海端鄉': [{'栗松溫泉': (121.0375, 23.2), }, ],
        '桃源區': [{'玉穗溫泉': (120.7948, 23.1818), }, {'荖荖溫泉': (120.7135, 23.1346), }, {'十坑溫泉': (120.7890, 23.1201), }, ],
        '六龜區': [{'邦腹溪營地': (120.6625, 23.0), }, {'七坑溫泉': (120.7528, 23.1018), }, ],
        '茂林區': [{'琉璃灣露營區': (120.675, 22.9), }, ],
        '金山區': [{'八煙野溪溫泉': (121.5875, 25.2125), }, ],
        '三峽區': [{'大豹溪蟾蜍山谷': (121.4375, 24.85), }, ],
        '烏來區': [{'桶後溪營地': (121.65, 24.8375), }, ],
    }
    QPESUMS_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0046-001?Authorization={}&downloadType=WEB&format=JSON"
    PAST_QPESUMS_URL = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-B0045-001?Authorization={}&downloadType=WEB&format=JSON"

    def __init__(self):
        QPECrawler.QPESUMS_URL = QPECrawler.QPESUMS_URL.format(self.__get_auth_token())
        QPECrawler.PAST_QPESUMS_URL = QPECrawler.PAST_QPESUMS_URL.format(self.__get_auth_token())
        self.data = None
        self.past_data = None
        self.rainCalculator = RainCalculator()

    def __get_auth_token(self):
        with open('auth_token.txt', 'r', encoding='UTF-8') as f:
            return f.readline()

    def get_image(self):
        ss = requests.Session()

        r = ss.get(QPECrawler.QPESUMS_URL)
        json_data = json.loads(r.text)
        data = json_data['cwbopendata']['dataset']['contents']['content'].split(',')
        self.data = numpy.array(list(map(self.__to_int, data))).reshape(95, 75)

        r = ss.get(QPECrawler.PAST_QPESUMS_URL)
        json_data = json.loads(r.text)
        data = json_data['cwbopendata']['dataset']['contents']['content'].split(',')
        self.past_data = numpy.array(list(map(self.__to_int, data))).reshape(95, 75)
        # return self.data

    def __get_position_rain(self, long1, lat1) -> int:  # , long2, lat2):
        # 117.975, 19.975
        x1 = int((long1 - 117.975) // 0.075)
        y1 = int((lat1 - 19.975) // 0.075)
        return self.data[y1, x1]

    def get_location_rain_msg_text(self, county_name):
        maps_arr = self.COUNTY_COORs_TABLE[county_name]
        result = "以下為" + county_name + "未來1小時降雨量預報：\n"
        for maps in maps_arr:
            for location_name in maps:
                print(location_name)
                result += location_name + "：\n"
                vals = maps[location_name]
                I = self.__get_position_rain(vals[0], vals[1])

                result += "降雨量為" + str(int(round(I, 0))) + " mm\n"

                if self.rainCalculator.check_rain_for_QPE(location_name, I):
                    result += "$ " + location_name + " 未來1小時有可能爆發\n"
        return result

    def __get_past_1hr_rain_all_location(self) -> Dict[str, int]:
        result = {}
        for location_list in self.COUNTY_COORs_TABLE.values():
            for location in location_list:
                for name, coor in location.items():
                    rain = self.__get_position_rain(coor[0], coor[1])
                    result[name] = rain

        return result

    def run_qpe_check(self):
        location_to_rain = self.__get_past_1hr_rain_all_location()
        # result = "以下為山洪暴發的溪流：\n"

        records = {}
        with open('alert', 'r') as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                records[int(line.split()[0])] = int(line.split()[1])

        for locations in self.COUNTY_COORs_TABLE.values():# for all location, or msg_county_name to select certain county
            for location_name, _ in locations.items():
                I = location_to_rain[location_name]
                ID = self.__get_id(location_name)
                try:
                    velocity = manning_velocity(self.rainCalculator.width[ID], self.rainCalculator.depth[ID], self.rainCalculator.slope[ID])
                except:
                    continue
                if (I*100)/velocity/self.rainCalculator.width[ID] >= 50:
                    if ID not in records:
                        with open('alert', 'w') as f:
                            f.write(f"{ID} {records[ID]}")

    def __get_id(self, location_name):
        return self.rainCalculator.maps[location_name]

    def __to_int(self, string):
        splits = string.split('E')
        return max(0.0, float(splits[0]) ** int(splits[1]))

    # def


if __name__ == '__main__':
    qpe = QPECrawler()
    image = qpe.get_image()
