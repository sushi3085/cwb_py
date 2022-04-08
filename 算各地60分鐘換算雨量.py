import os
import numpy
import json

from 曼寧等公式 import *


class RainCalculator:
    def __init__(self):
        self.radar_data = None
        self.location_rain = [0] * 40
        self.location_rain_3hr = [0]*40
        self.slope = numpy.concatenate((
            numpy.array(
                [5, 5, 5, 6, 8, 6, 7, 5, 2, 5, 7, 8, 8, 7, 5, 5, 5, 5, 8, 6]  # 最後一筆當作是6，沒資料
            ) / 100,
            numpy.array(
                [6, 6, 5, 8, 7, 8, 8, 8, 7, 6, 8, 7, 9, 6, 6, 5, 6, 5, 6, 7, 6]
            ) / 100
        ), axis=0
        )

        # m
        self.width = [
                         11, 25.11, 25, 28.6, 18.3, 16.22, 12.89, 12.5, 7.7, 7.4, 21, 8.86, 23, 15, 17, 15, 13, 37.4, 17.5, 37,
                     ] + \
                     [
                         17, 102, 68, 12, 26, 50, 27, 21, 24, 13, 17, 14.5, 16.5
                     ]

        # m
        self.depth = [
                         1.55, 1.55, 1.55, 1.3, 1.6, 1.3, 1.5, 1.5, 1.5, 1.7, 1.35, 1.3, 1.5, 1.55, 1.5, 1.2, 1.3, 1.7, 1, 1.4,
                     ] + \
                     [
                         1.5, 1.5, 1.3, 1.3, 1.1, 1.13, 1.31, 1.6, 1.6, 2.4, 2, 2
                     ]

        # km
        self.distance = [
                            3.2, 8.1, 8.5, 7.6, 6.3, 11.5, 10.2, 2.5, 3, 1.92, 1.14, 4.3, 9.3, 2.78, 2.5, 4.6, 5.2, 2.4, 0.47, 10,
                        ] + \
                        [
                            1.9, 1.1, 6.2, 7, 0.47, 1.35, 1.59, 2.34, 2.35, 0.52, 1.5, 2.22, 2.47
                        ]

        self.area_ha = [100] * 39

    def __dBZ_to_R(self, dBZ):
        # // Z = 300(R) ^ 1.4
        # let A = 32.5;
        a = 32.5
        # let B = 1.65;
        b = 1.65
        # // Z = 10 ^ (dBZ / 10)
        if dBZ == 0:
            return 0
        Z = 10 ** dBZ
        # let Z = Math.pow(10, dBZ / 10.0)
        return (a**(-1/b)) * (10**(dBZ/(10**b)))
        # return (Z / a) ** (1 / b)

    def update(self, min):
        if min == 60:
            self.location_rain = [0] * 40
            dname = '60min_data'
        else:
            self.location_rain_3hr = [0]*40
            dname = '3hr_data'
        for dirname, _, filenames in os.walk(dname):
            for filename in filenames:
                with open(os.path.join(dirname, filename)) as f:
                    self.radar_data = numpy.array(json.loads(f.readline()))
                    # all location code
                    # region
                    self.__update_rain_大豹溪()
                    self.__update_rain_泰崗野溪溫泉()
                    self.__update_rain_秀巒野溪溫泉()
                    self.__update_rain_琉璃灣露營區()
                    self.__update_rain_邦腹溪營地()#4
                    self.__update_rain_武界露營()
                    self.__update_rain_二山子野溪溫泉()
                    self.__update_rain_桶後溪營地()
                    self.__update_rain_八煙野溪溫泉()
                    self.__update_rain_天狗溪溫泉()#9
                    self.__update_rain_馬陵溫泉()
                    self.__update_rain_精英野溪溫泉()
                    self.__update_rain_栗松溫泉()
                    self.__update_rain_流霞谷親水烤肉園區()
                    self.__update_rain_八度野溪溫泉區()#14
                    self.__update_rain_梅淮露營區()
                    self.__update_rain_五六露營農場()
                    self.__update_rain_祕密基地露營區()
                    self.__update_rain_瑞岩溫泉野溪邊露營()
                    self.__update_rain_金崙溫泉野溪露營區()#19
                    # endregion
                    #
                    self.__update_rain_嘎拉賀溫泉()#20
                    self.__update_rain_四稜溫泉()
                    self.__update_rain_神駒谷溫泉()
                    self.__update_rain_太魯灣溪溫泉()
                    self.__update_rain_瑞岩溫泉()#24
                    self.__update_rain_紅香溫泉()
                    self.__update_rain_萬大南溪溫泉()
                    self.__update_rain_樂樂谷溫泉()
                    self.__update_rain_玉穗溫泉()
                    self.__update_rain_荖荖溫泉()#29
                    self.__update_rain_五區_拉卡_溫泉()
                    self.__update_rain_文山溫泉_有測站()
                    self.__update_rain_彩霞溫泉()
                    self.__update_rain_碧山溫泉()  # no WDD
                    self.__update_rain_轆轆溫泉()  # no WDD #34
                    self.__update_rain_暇末溫泉()  # no WDD
                    self.__update_rain_都飛魯溫泉()  # no WDD
                    self.__update_rain_比魯溫泉()  # no WDD
                    self.__update_rain_普沙羽揚溫泉()  # no WDD
                    #

    def check(self):
        # TODO : implement check and add into alert file
        # print(len(self.area_ha),len(self.width),len(self.depth), len(self.slope))
        with open('alert', 'w') as f:
            for i in range(len(self.depth)):
                q = Q_CIA(self.location_rain[i], 100) # 100 ha
                v = manning_velocity(self.width[i], self.depth[i], self.slope[i])
                h = H(q, v, self.width[i])
                print(f"station {i}, rainfall {self.location_rain[i]}mm -> river level rise ", h, "meters")
                if h >= 50*0.8:# 50cm
                    f.write(f"{i} {round(self.distance[i]*1000/v/60,2)}\n")
        return

    def print_location_rain(self):
        for i in range(0, len(self.location_rain), 2):
            print(f"{i}: {self.location_rain[i]}", f"{i + 1}: {self.location_rain[i + 1]}")
        pass

    # region
    # 15*1.25*1.25 km*km
    def __update_rain_大豹溪(self):
        # 516~518
        # 544~548
        dbZ = 0
        area = 0
        for x in range(516, 518 + 1):
            for y in range(544, 548 + 1):
                # self.location_rain[0] += self.__dBZ_to_R(max(0, self.radar_data[y, x]))
                dbZ += max(0, self.radar_data[y, x])
                area += 1
        average_dbZ = dbZ / area
        self.location_rain[0] += self.__dBZ_to_R(average_dbZ)
        return

    # 4*5
    def __update_rain_泰崗野溪溫泉(self):
        # 506~509
        # 521~525
        dbz = 0
        area = 0
        for x in range(506, 509 + 1):
            for y in range(521, 525 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[1] += self.__dBZ_to_R(average_dbz)
        # self.location_rain[2] += self.__dBZ_to_R(average_dbz)
        return

    # 20
    def __update_rain_秀巒野溪溫泉(self):
        # updated at self.location_rain[1]
        self.location_rain[2] = self.location_rain[1]
        return

    # 6*4
    def __update_rain_琉璃灣露營區(self):
        # 458~463
        # 394~397
        dbz = 0
        area = 0
        for x in range(458, 463 + 1):
            for y in range(394, 397 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[3] += self.__dBZ_to_R(average_dbz)

    # 3*4
    def __update_rain_邦腹溪營地(self):
        # 右上(458, 404)
        # 右下(458, 401)
        # 左上(456, 404)
        # 左下(456, 401)
        dbz = 0
        area = 0
        for x in range(456, 458 + 1):
            for y in range(401, 404 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[4] += self.__dBZ_to_R(average_dbz)
        return

    # [5]
    # 6*3
    def __update_rain_武界露營(self):
        # 右上(493, 478)
        # 右下(493, 476)
        # 左上(488, 478)
        # 左下(488, 476)
        dbz = 0
        area = 0
        for x in range(488, 493 + 1):
            for y in range(476, 478 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[5] += self.__dBZ_to_R(average_dbz)
        return

    # 5*3
    def __update_rain_二山子野溪溫泉(self):
        # 右上(506, 475)
        # 右下(506, 473)
        # 左上(502, 475)
        # 左下(502, 473)
        dbz = 0
        area = 0
        for x in range(502, 506 + 1):
            for y in range(473, 475 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[6] += self.__dBZ_to_R(average_dbz)
        return

    # 9*4
    def __update_rain_桶後溪營地(self):
        # 右上(525, 548)
        # 右下(525, 545)
        # 左上(533, 548)
        # 左下(533, 545)
        dbz = 0
        area = 0
        for x in range(525, 533 + 1):
            for y in range(545, 548 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[7] += self.__dBZ_to_R(average_dbz)
        return

    # 4*3
    def __update_rain_八煙野溪溫泉(self):
        # 右上(536, 576)
        # 右下(536, 574)
        # 左上(533, 576)
        # 左下(533, 574)
        dbz = 0
        area = 0
        for x in range(533, 536 + 1):
            for y in range(574, 576 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[8] += self.__dBZ_to_R(average_dbz)
        return

    # 4*5
    def __update_rain_天狗溪溫泉(self):
        # 右上(525, 524)
        # 右下(525, 520)
        # 左上(522, 524)
        # 左下(522, 520)
        dbz = 0
        area = 0
        for x in range(522, 525 + 1):
            for y in range(520, 524 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[9] += self.__dBZ_to_R(average_dbz)
        return

    # [10]
    # 2*2
    def __update_rain_馬陵溫泉(self):
        # 右上(486, 498)
        # 右下(486, 497)
        # 左上(485, 498)
        # 左下(485, 497)
        dbz = 0
        area = 0
        for x in range(485, 486 + 1):
            for y in range(497, 498 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[10] += self.__dBZ_to_R(average_dbz)
        return

    # 3*4
    def __update_rain_精英野溪溫泉(self):
        # 右上(502, 484)
        # 右下(502, 481)
        # 左上(500, 484)
        # 左下(500, 481)
        dbz = 0
        area = 0
        for x in range(500, 502 + 1):
            for y in range(481, 484 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        avg_dbz = dbz / area
        self.location_rain[11] = self.__dBZ_to_R(avg_dbz)

    # 5*2
    def __update_rain_栗松溫泉(self):
        # 右上(485, 416)
        # 右下(485, 415)
        # 左上(481, 416)
        # 左下(481, 415)
        dbz = 0
        area = 0
        for x in range(481, 485 + 1):
            for y in range(415, 416 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
            avg_dbz = dbz / area
            self.location_rain[12] = self.__dBZ_to_R(avg_dbz)

    # 3*3
    def __update_rain_流霞谷親水烤肉園區(self):
        # 右上(513, 546)
        # 右下(513, 544)
        # 左上(511, 546)
        # 左下(511, 544)
        dbz = 0
        area = 0
        for x in range(511, 513 + 1):
            for y in range(544, 546 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[13] += self.__dBZ_to_R(average_dbz)
        return

    # 2 * 2
    def __update_rain_八度野溪溫泉區(self):
        # 右上(506, 542)
        # 右下(506, 541)
        # 左上(505, 542)
        # 左下(505, 541)
        dbz = 0
        area = 0
        for x in range(505, 506 + 1):
            for y in range(541, 542 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[14] += self.__dBZ_to_R(average_dbz)
        return

    # [15]
    # 5*4
    def __update_rain_梅淮露營區(self):
        # 右上(499, 533)
        # 右下(499, 530)
        # 左上(495, 533)
        # 左下(495, 530)
        dbz = 0
        area = 0
        for x in range(495, 499 + 1):
            for y in range(530, 533 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[15] += self.__dBZ_to_R(average_dbz)
        return

    # 3*4
    def __update_rain_五六露營農場(self):
        # 右上(492, 485)
        # 右下(492, 482)
        # 左上(490, 485)
        # 左下(490, 482)
        dbz = 0
        area = 0
        for x in range(490, 492 + 1):
            for y in range(482, 485 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[16] += self.__dBZ_to_R(average_dbz)
        return

    # 3*3
    def __update_rain_祕密基地露營區(self):
        # 右上(524, 535)
        # 右下(524, 533)
        # 左上(522, 535)
        # 左下(522, 533)
        dbz = 0
        area = 0
        for x in range(522, 524 + 1):
            for y in range(533, 535 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[17] += self.__dBZ_to_R(average_dbz)
        return

    # 4*5
    def __update_rain_瑞岩溫泉野溪邊露營(self):
        # 右上(498, 498)
        # 右下(498, 494)
        # 左上(495, 498)
        # 左下(495, 494)
        dbz = 0
        area = 0
        for x in range(495, 498 + 1):
            for y in range(494, 498 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[18] += self.__dBZ_to_R(average_dbz)
        return

    # 9*4
    def __update_rain_金崙溫泉野溪露營區(self):
        # 右上(468, 364)
        # 右下(468, 361)
        # 左上(460, 364)
        # 左下(460, 361)
        dbz = 0
        area = 0
        for x in range(460, 468 + 1):
            for y in range(361, 364 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[19] += self.__dBZ_to_R(average_dbz)
        return

    # TL
    # BL
    # TR
    # BR
    # [20]
    # 6*3
    def __update_rain_嘎拉賀溫泉(self):
        # 512, 530
        # 508, 528
        # 513, 530
        # 513, 530
        dbz = 0
        area = 0
        for x in range(508, 513 + 1):
            for y in range(528, 530 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[20] += self.__dBZ_to_R(average_dbz)
        return

    # 4*7
    def __update_rain_四稜溫泉(self):
        dbz = 0
        area = 0
        for x in range(514, 517 + 1):
            for y in range(527, 533 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[21] += self.__dBZ_to_R(average_dbz)
        return

    # 10*12
    def __update_rain_神駒谷溫泉(self):
        dbz = 0
        area = 0
        for x in range(479, 488 + 1):
            for y in range(492, 503 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[22] += self.__dBZ_to_R(average_dbz)
        return

    # 10*2
    def __update_rain_太魯灣溪溫泉(self):
        dbz = 0
        area = 0
        for x in range(494, 503 + 1):
            for y in range(483, 484 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[23] += self.__dBZ_to_R(average_dbz)
        return

    # 2*2
    def __update_rain_瑞岩溫泉(self):
        dbz = 0
        area = 0
        for x in range(492, 493 + 1):
            for y in range(489, 490 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[24] += self.__dBZ_to_R(average_dbz)
        return

    # [25]
    # 7*7
    def __update_rain_紅香溫泉(self):
        dbz = 0
        area = 0
        for x in range(491, 497 + 1):
            for y in range(492, 498 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[25] += self.__dBZ_to_R(average_dbz)
        return

    # 12*4
    def __update_rain_萬大南溪溫泉(self):
        dbz = 0
        area = 0
        for x in range(490, 501 + 1):
            for y in range(475, 478 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[26] += self.__dBZ_to_R(average_dbz)
        return

    # 6*5
    def __update_rain_樂樂谷溫泉(self):
        dbz = 0
        area = 0
        for x in range(475, 480 + 1):
            for y in range(439, 443 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[27] += self.__dBZ_to_R(average_dbz)
        return

    # 5*3
    def __update_rain_玉穗溫泉(self):
        dbz = 0
        area = 0
        for x in range(464, 468 + 1):
            for y in range(413, 415 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[28] += self.__dBZ_to_R(average_dbz)
        return

    # 4*4
    def __update_rain_荖荖溫泉(self):
        dbz = 0
        area = 0
        for x in range(454, 457 + 1):
            for y in range(410, 413 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[29] += self.__dBZ_to_R(average_dbz)
        return

    # [30]
    # 5*6
    def __update_rain_五區_拉卡_溫泉(self):
        dbz = 0
        area = 0
        for x in range(535, 539 + 1):
            for y in range(518, 523 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[30] += self.__dBZ_to_R(average_dbz)
        return

    # 2*2
    def __update_rain_文山溫泉_有測站(self):
        dbz = 0
        area = 0
        for x in range(519, 520 + 1):
            for y in range(493, 494 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[31] += self.__dBZ_to_R(average_dbz)
        return

    # 2*2
    def __update_rain_彩霞溫泉(self):
        dbz = 0
        area = 0
        for x in range(485, 486 + 1):
            for y in range(411, 412 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[32] += self.__dBZ_to_R(average_dbz)
        return

    # 5*3
    def __update_rain_碧山溫泉(self):
        dbz = 0
        area = 0
        for x in range(473, 477 + 1):
            for y in range(415, 417 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[33] += self.__dBZ_to_R(average_dbz)
        return

    # 6*9
    def __update_rain_轆轆溫泉(self):
        dbz = 0
        area = 0
        for x in range(471, 476 + 1):
            for y in range(403, 411 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[34] += self.__dBZ_to_R(average_dbz)
        return

    # [35]
    # 6*9
    def __update_rain_暇末溫泉(self):
        dbz = 0
        area = 0
        for x in range(471, 476 + 1):
            for y in range(403, 411 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[35] += self.__dBZ_to_R(average_dbz)
        return

    # 9*4
    def __update_rain_都飛魯溫泉(self):
        dbz = 0
        area = 0
        for x in range(460, 468 + 1):
            for y in range(361, 364 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[36] += self.__dBZ_to_R(average_dbz)
        return

    # 3*4
    def __update_rain_比魯溫泉(self):
        dbz = 0
        area = 0
        for x in range(466, 468 + 1):
            for y in range(368, 371 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[37] += self.__dBZ_to_R(average_dbz)
        return

    # 3*2
    def __update_rain_普沙羽揚溫泉(self):
        dbz = 0
        area = 0
        for x in range(461, 463 + 1):
            for y in range(348, 349 + 1):
                dbz += max(0, self.radar_data[y, x])
                area += 1
        average_dbz = dbz / area
        self.location_rain[38] += self.__dBZ_to_R(average_dbz)
        return
    # endregion


if __name__ == '__main__':
    rain_calculator = RainCalculator()
    rain_calculator.update(60)
    # print(len(rain_calculator.area_ha))
    # print(len(rain_calculator.width), len(rain_calculator.depth), len(rain_calculator.slope))
    rain_calculator.location_rain[17] = 140
    rain_calculator.check()
    # rain_calculator.print_location_rain()
