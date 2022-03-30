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
                    self.__update_rain_馬陵溫泉()
                    self.__update_rain_精英野溪溫泉()
                    self.__update_rain_栗松溫泉()
                    self.__update_rain_流霞谷親水烤肉園區()
                    self.__update_rain_八度野溪溫泉區()
                    self.__update_rain_梅淮露營區()
                    self.__update_rain_五六露營農場()
                    self.__update_rain_祕密基地露營區()
                    self.__update_rain_瑞岩溫泉野溪邊露營()
                    self.__update_rain_金崙溫泉野溪露營區()

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

    # [5]
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
        # dbz = 0
        for x in range(522, 525 + 1):
            for y in range(520, 524 + 1):
                self.location_rain[9] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
        # average_dbz = dbz
        # self.location_rain[9] += self.__dBZ_to_R(average_dbz)
        return

    # [10]
    def __update_rain_馬陵溫泉(self):
        # 右上(486, 498)
        # 右下(486, 497)
        # 左上(485, 498)
        # 左下(485, 497)
        for x in range(485, 486 + 1):
            for y in range(497, 498 + 1):
                self.location_rain[10] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_精英野溪溫泉(self):
        # 右上(502, 484)
        # 右下(502, 481)
        # 左上(500, 484)
        # 左下(500, 481)
        for x in range(500, 502 + 1):
            for y in range(481, 484 + 1):
                self.location_rain[11] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_栗松溫泉(self):
        # 右上(485, 416)
        # 右下(485, 415)
        # 左上(481, 416)
        # 左下(481, 415)
        for x in range(481, 485 + 1):
            for y in range(415, 416 + 1):
                self.location_rain[12] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_流霞谷親水烤肉園區(self):
        # 右上(513, 546)
        # 右下(513, 544)
        # 左上(511, 546)
        # 左下(511, 544)
        for x in range(511, 513 + 1):
            for y in range(544, 546 + 1):
                self.location_rain[13] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_八度野溪溫泉區(self):
        # 右上(506, 542)
        # 右下(506, 541)
        # 左上(505, 542)
        # 左下(505, 541)
        for x in range(505, 506 + 1):
            for y in range(541, 542 + 1):
                self.location_rain[14] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    # [15]
    def __update_rain_梅淮露營區(self):
        # 右上(499, 533)
        # 右下(499, 530)
        # 左上(495, 533)
        # 左下(495, 530)
        for x in range(495, 499 + 1):
            for y in range(530, 533 + 1):
                self.location_rain[15] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_五六露營農場(self):
        # 右上(492, 485)
        # 右下(492, 482)
        # 左上(490, 485)
        # 左下(490, 482)
        for x in range(490, 492 + 1):
            for y in range(482, 485 + 1):
                self.location_rain[16] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_祕密基地露營區(self):
        # 右上(524, 535)
        # 右下(524, 533)
        # 左上(522, 535)
        # 左下(522, 533)
        for x in range(522, 524 + 1):
            for y in range(533, 535 + 1):
                self.location_rain[17] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_瑞岩溫泉野溪邊露營(self):
        # 右上(498, 498)
        # 右下(498, 494)
        # 左上(495, 498)
        # 左下(495, 494)
        for x in range(495, 498 + 1):
            for y in range(494, 498 + 1):
                self.location_rain[18] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))

    def __update_rain_金崙溫泉野溪露營區(self):
        # 右上(468, 364)
        # 右下(468, 361)
        # 左上(460, 364)
        # 左下(460, 361)
        for x in range(460, 468 + 1):
            for y in range(361, 364 + 1):
                self.location_rain[19] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))


if __name__ == '__main__':
    rain_calculator = RainCalculator()
    rain_calculator.update()
    rain_calculator.check()
    rain_calculator.print_location_rain()
    print(
        rain_calculator.location_rain[11]
    )
