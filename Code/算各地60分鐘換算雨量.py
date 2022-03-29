import os
import numpy
import json


class RainCalculator:
    def __init__(self):
        self.radar_data = None
        self.location_rain = [0] * 40

    def __dBZ_to_R(self, dBZ):
        # // Z = 300(R) ^ 1.4
        # let A = 32.5;
        a = 32.5
        # let B = 1.65;
        b = 1.65
        # // Z = 10 ^ (dBZ / 10)
        Z = 10 ** (dBZ / 10)
        # let Z = Math.pow(10, dBZ / 10.0)
        return (Z / a) ** (1 / b)

    def update(self):
        self.location_rain = [0] * 40
        for dirname, _, filenames in os.walk('60min_data'):
            for filename in filenames:
                with open(os.path.join(dirname, filename)) as f:
                    self.radar_data = numpy.array(json.loads(f.readline()))
                    # all location code
                    self.__update_rain_大豹溪()
                    self.__update_rain_泰崗野溪溫泉()
                    self.__update_rain_秀巒野溪溫泉()
                    self.__update_rain_琉璃灣露營區()
                    self.__update_rain_邦腹溪營地()
                    self.__update_rain_武界露營()
                    self.__update_rain_二山子野溪溫泉()
                    self.__update_rain_桶後溪營地()
                    self.__update_rain_八煙野溪溫泉()
                    self.__update_rain_天狗溪溫泉()

    def check(self):
        # TODO : implement check and add into alert file
        print(NotImplemented)
        return

    def print_location_rain(self):
        for i, e in enumerate(self.location_rain):
            print(i, ":", e)
        pass

    def __update_rain_大豹溪(self):
        # 516~518
        # 544~548
        dbZ = 0
        # area = 0
        for x in range(516, 518 + 1):
            for y in range(544, 548 + 1):
                self.location_rain[0] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbZ += max(0, self.radar_data[y, x])
                # area += 1
        # average_dbZ = dbZ  # / area
        # self.location_rain[0] += self.__dBZ_to_R(average_dbZ)
        # print(dbZ)
        # print(self.__dBZ_to_R(average_dbZ))
        # print(f"cumulated: {self.location_rain[0]}")
        return

    def __update_rain_泰崗野溪溫泉(self):
        # 506~509
        # 521~525
        # dbz = 0
        for x in range(506, 509 + 1):
            for y in range(521, 525 + 1):
                self.location_rain[1] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbz += max(0, self.radar_data[y, x])
        # average_dbz = dbz
        # self.location_rain[1] += self.__dBZ_to_R(average_dbz)
        # self.location_rain[2] += self.__dBZ_to_R(average_dbz)
        return

    def __update_rain_秀巒野溪溫泉(self):
        # updated at self.location_rain[1]
        self.location_rain[2] = self.location_rain[1]
        return

    def __update_rain_琉璃灣露營區(self):
        # 458~463
        # 394~397
        dbz = 0
        for x in range(458, 463 + 1):
            for y in range(394, 397 + 1):
                self.location_rain[3] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbz += max(0, self.radar_data[y, x])
        average_dbz = dbz
        # self.location_rain[3] += self.__dBZ_to_R(average_dbz)

    def __update_rain_邦腹溪營地(self):
        # 右上(458, 404)
        # 右下(458, 401)
        # 左上(456, 404)
        # 左下(456, 401)
        dbz = 0
        for x in range(456, 458 + 1):
            for y in range(401, 404 + 1):
                self.location_rain[4] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbz += max(0, self.radar_data[y, x])
        average_dbz = dbz
        self.location_rain[4] += self.__dBZ_to_R(average_dbz)
        return

    def __update_rain_武界露營(self):
        # 右上(493, 478)
        # 右下(493, 476)
        # 左上(488, 478)
        # 左下(488, 476)
        dbz = 0
        for x in range(488, 493 + 1):
            for y in range(476, 478 + 1):
                self.location_rain[5] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbz += max(0, self.radar_data[y, x])
        average_dbz = dbz
        self.location_rain[5] += self.__dBZ_to_R(average_dbz)
        return

    def __update_rain_二山子野溪溫泉(self):
        # 右上(506, 475)
        # 右下(506, 473)
        # 左上(502, 475)
        # 左下(502, 473)
        dbz = 0
        for x in range(502, 506 + 1):
            for y in range(473, 475 + 1):
                self.location_rain[6] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbz += max(0, self.radar_data[y, x])
        average_dbz = dbz
        self.location_rain[6] += self.__dBZ_to_R(average_dbz)
        return

    def __update_rain_桶後溪營地(self):
        # 右上(525, 548)
        # 右下(525, 545)
        # 左上(533, 548)
        # 左下(533, 545)
        dbz = 0
        for x in range(525, 533 + 1):
            for y in range(545, 548 + 1):
                self.location_rain[7] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # dbz += max(0, self.radar_data[y, x])
        # average_dbz = dbz
        # self.location_rain[7] += self.__dBZ_to_R(average_dbz)
        return

    def __update_rain_八煙野溪溫泉(self):
        # 右上(536, 576)
        # 右下(536, 574)
        # 左上(533, 576)
        # 左下(533, 574)
        dbz = 0
        for x in range(533, 536 + 1):
            for y in range(574, 576 + 1):
                self.location_rain[8] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                # print(dbz)
        # average_dbz = dbz
        # self.location_rain[8] += self.__dBZ_to_R(average_dbz)
        return

    def __update_rain_天狗溪溫泉(self):
        # 右上(525, 524)
        # 右下(525, 520)
        # 左上(522, 524)
        # 左下(522, 520)
        dbz = 0
        for x in range(522, 525 + 1):
            for y in range(520, 524 + 1):
                dbz += max(0, self.radar_data[y, x])
        average_dbz = dbz
        self.location_rain[9] += self.__dBZ_to_R(average_dbz)
        return


if __name__ == '__main__':
    rain_calculator = RainCalculator()
    rain_calculator.update()
    rain_calculator.check()
    rain_calculator.print_location_rain()
