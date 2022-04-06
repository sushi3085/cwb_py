import numpy
import requests
import xmltodict as xml
import json
import os
from .dataCrawler import toNum

url = "https://opendata.cwb.gov.tw/historyapi/v1/getMetadata/O-A0059-001?Authorization=CWB-41DC9AED-4979-4F29-8CB7-E6BF577E5036&limit=10&offset=1431"


class CrawlSixty:
    @staticmethod
    def wrapper(date: str) -> str:
        result = ""
        for ch in date:
            if ch == ":":
                result += "-"
                continue
            result += ch
        return result

    @staticmethod
    def convolution(data):
        # 400---600
        # 300|||600
        for y in range(400, 600):
            for x in range(300, 600):
                # (x, y) is center point
                break
            break
            # TODO: figure out ratio or method to convolution

        return data

    def main(self):
        s = requests.Session()
        response = s.get(url)
        obj = json.loads(response.text)
        data_list = obj['dataset']['resources']['resource']['data']['time']
        time_url_map = {}
        # build time-url map
        data_list = data_list[-6:]
        for i in data_list:
            time_url_map[self.wrapper(i['dataTime'])] = i['url']

        # delete expired file
        for dirname, _, filenames in os.walk('60min_data'):
            for filename in filenames:
                if filename not in time_url_map.keys():
                    os.remove(os.path.join(dirname, filename))

        # write data in to file
        for k, v in time_url_map.items():
            for dirname, _, filenames in os.walk('60min_data'):
                if k not in filenames:
                    response = s.get(v)
                    datas = xml.parse(response.text)
                    data = datas['cwbopendata']['dataset']['contents']['content'].split(',')
                    data = list(map(toNum, data))
                    data = numpy.reshape(data, (881, 921))
                    # data = convolution(data)
                    with open("60min_data/" + k, 'w') as f:
                        f.write('[')
                        for i, raw in enumerate(data):
                            f.write(json.dumps(list(raw)))
                            if i != 880:
                                f.write(',')
                        f.write(']')


if __name__ == '__main__':
    crawler = CrawlSixty()
    crawler.main()
    # file will store at 60min_data folder
