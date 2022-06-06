import requests
import json

class SpecialCrawler:
    URL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/W-C0033-001?Authorization={}\
&phenomena=%E5%A4%A7%E9%9B%A8,%E8%B1%AA%E9%9B%A8,%E5%A4%A7%E8%B1%AA%E9%9B%A8,%E8%B6%85%E5%A4%A7%E8%B1%AA%E9%9B%A8"

    def __init__(self):
        with open('auth_token.txt', 'r') as f:
            SpecialCrawler.URL = SpecialCrawler.URL.format(f.readline())
        self.countiesData = json.loads(requests.get(SpecialCrawler.URL).text)['records']['location']

    def get_spetial_warning_msg(self):
        self.countiesData = json.loads(requests.get(SpecialCrawler.URL).text)['records']['location']
        result = ""
        has_data = False
        for records in self.countiesData:
            if len(records['hazardConditions']['hazards']) == 0:
                continue

            hazards = records['hazardConditions']['hazards']

            has_data = True
            result += records['locationName']+" 警特報：\n"
            for element_map in hazards:
                result += element_map['info']['phenomena']+"\n"
                result += "將從：\n" + element_map['validTime']['startTime']+"\n"
                result += "持續至：\n" + element_map['validTime']['endTime']+"\n"
            result += "\n"
        return result
