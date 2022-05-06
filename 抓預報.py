import requests
import json


class Forcaster:

    def __init__(self):
        self.table = {
            '桃園': '07',
            '新竹': '11',
            '宜蘭': '03',
            '台中': '75',
            '南投': '23',
            '台東': '39',
            '高雄': '67',
            '新北': '71',
        }
        self.requestUrl = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-0"
        self.auth = "?Authorization=CWB-41DC9AED-4979-4F29-8CB7-E6BF577E5036"
        self.s = requests.Session()
        self.targets = {
            '三峽區', '尖石鄉', '茂林區', '六龜區', '烏來區', '金山區', '海端鄉', '復興區', '復興區', '尖石鄉', '仁愛鄉', '大同鄉', 'CHANGE',
            # ? 呂季霖
            # region
            # ? 1.	大豹溪蟾蜍山谷       三峽區 新北市
            # ? 2.	泰崗野溪溫泉         尖石鄉 新竹縣
            # ? 3.	琉璃灣露營區         茂林區 高雄市
            # ? 4.	邦腹溪營地           六龜區 高雄市
            # ? 5.	武界露營             仁愛鄉 南投縣
            # ? 6.	桶後溪營地           烏來區 新北市
            # ? 7.	八煙野溪溫泉         金山區 新北市
            # ? 8.	栗松溫泉             海端鄉 台東縣
            # ? 9.	流霞谷親水烤肉園區   復興區 桃園市
            # ? 10.	八度野溪露營區       復興區 桃園市
            # ? 11.	梅淮露營區           尖石鄉 新竹縣
            # ? 12.	五六露營農場         仁愛鄉 南投縣
            # ? 13.	祕密基地露營區       大同鄉 宜蘭縣
            # endregion
            '復興區', '復興區', '尖石鄉', '和平區', '和平區', '仁愛鄉', '仁愛鄉', '仁愛鄉', '仁愛鄉', '仁愛鄉', '信義鄉', '桃源區', '六龜區', '桃源區', '桃源區', '大同鄉'
            # ? 莊佩蓁
            # region
            # ? 1.	嘎拉賀溫泉       復興區 桃園市
            # ? 2.	四稜溫泉         復興區 桃園市
            # ? 3.	秀巒溫泉         尖石鄉 新竹縣
            # ? 4.	神駒谷溫泉       和平區 台中市
            # ? 5.	馬稜溫泉         和平區 台中市
            # ? 6.	太魯灣溪溫泉     仁愛鄉 南投縣
            # ? 7.	精英野溪溫泉     仁愛鄉 南投縣
            # ? 8.	瑞岩溫泉         仁愛鄉 南投縣
            # ? 9.	紅香溫泉         仁愛鄉 南投縣
            # ? 10.	萬大南溪溫泉    仁愛鄉 南投縣
            # ? 11.	樂樂谷溫泉      信義鄉 南投縣
            # ? 12.	玉穗溫泉        桃源區 高雄市
            # ? 13.	七坑溫泉        六龜區 高雄市
            # ? 14.	荖荖溫泉        桃源區 高雄市
            # ? 15.	十坑溫泉        桃源區 高雄市
            # ! 16.	 HG76+F5        大同鄉 宜蘭縣
            # endregion
        }
        self.results = []
        self.location_to_camps = {
            '復興區': ['流霞谷親水烤肉園區', '八度野溪露營區', '嘎拉賀溫泉', '四稜溫泉'],
            '尖石鄉': ['泰崗野溪溫泉', '梅淮露營區', '秀巒溫泉'],
            '大同鄉': ['祕密基地露營區'],
            '和平區': ['神駒谷溫泉', '馬稜溫泉'],
            '信義鄉': ['樂樂谷溫泉'],
            '仁愛鄉': ['武界露營', '五六露營農場', '太魯灣溪溫泉', '精英野溪溫泉', '瑞岩溫泉', '紅香溫泉', '萬大南溪溫泉'],
            '海端鄉': ['栗松溫泉'],
            '桃源區': ['玉穗溫泉', '荖荖溫泉', '十坑溫泉'],
            '六龜區': ['邦腹溪營地', '七坑溫泉'],
            '茂林區': ['琉璃灣露營區'],
            '金山區': ['八煙野溪溫泉'],
            '三峽區': ['大豹溪蟾蜍山谷'],
            '烏來區': ['桶後溪營地'],
        }

    def get(self, county_name):
        if self.table.get(county_name) is None:
            return None

        data = json.loads(self.s.get(self.requestUrl + self.table[county_name] + self.auth).text)
        # print(data['records']['locations'][0]['location'][0]['weatherElement'])
        for dic in data['records']['locations'][0]['location']:
            if dic['locationName'] in self.targets:
                self.results.append({
                    dic['locationName']: dic['weatherElement'][10]['time'][0]['elementValue'][0]['value'],
                    "PoP6h": dic['weatherElement'][0]['time'][0]['elementValue'][0]['value'] + "%",
                })

    def print_targets_information(self):
        result = ""
        for data in self.results:
            print('[')
            result += '['
            for k, v in data.items():
                print(f'    {k} : {v}')
                result += f'    {k} : {v}'
            print(']')
            result += ']'
        return result

    def get_weather_msg(self):
        result = ""
        for location, camps in self.location_to_camps.items():
            result += location + ":\n"
            for i, camp in enumerate(camps):
                result += f"{i + 1}. {camp}\n"
            for it in self.results:
                if it.get(location) != None:
                    string = it[location].split("。")
                    result += f"  {string[0]}\n  {string[1]}\n  {string[2]}\n  {string[3]}\n\n"
                    break
        return result


if __name__ == "__main__":
    forcaster = Forcaster()
    for position in forcaster.table.keys():
        forcaster.get(position)
    print(forcaster.get_weather_msg())
