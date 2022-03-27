import json
import numpy
import seaborn as sb


def get_correspond_data(y, x, radarData: list, rainData: list) -> tuple:
    """
    *** this will return rainData corresponding to radarData ***
    remember to reverse x and y
    rainData original point => 117.975, 19.975 in the form of (x, y)
    radarData original point => 115.0, 18.0 in same form
    """
    real_x_coordinate = x * 0.0125 + 115.0
    real_y_coordinate = y * 0.0125 + 18.0

    rain_x_coordinate = int((real_x_coordinate - 117.975) // 0.075)
    rain_y_coordinate = int((real_y_coordinate - 19.975) // 0.075)
    if rain_y_coordinate <= 0 or rain_x_coordinate <= 0:
        return None

    return radarData[y][x], rainData[rain_y_coordinate][rain_x_coordinate]


def dBZ_to_Z(dBZ):
    # // Z = 300(R) ^ 1.4
    # let A = 32.5;
    a = 55.5
    # let B = 1.65;
    b = 1.2
    # // Z = 10 ^ (dBZ / 10)
    Z = 10 ** (dBZ / 10)
    # let Z = Math.pow(10, dBZ / 10.0)
    return (Z / a) ** (1 / b)
    # return 6 * Math.pow(Z / A, 1 / B);


if __name__ == '__main__':
    with open("data/2022-03-26T23_10_00+08_00_RAIN.txt") as f:
        rainData = json.loads(f.readline())
    with open("data/2022-03-26T23_10_00+08_00.txt") as f:
        radarData = json.loads(f.readline())
    radarData = numpy.reshape(radarData, (881, 921))
    rainData = numpy.reshape(rainData, (95, 75))

    for i in range(radarData.shape[0]):
        for j in range(radarData.shape[1]):
            radarData[i][j] = max(radarData[i][j], 0)
    # resolution of radarData is 0.0125
    # resolution of rainData is 0.075, which is (1/6)x of radarData's resolution

    result = []
    dataPair = get_correspond_data(500, 500, radarData, rainData)
    print(dBZ_to_Z(dataPair[0]), dataPair[1])
    # result.append(get_correspond_data(j, i, radarData, rainData)[1])
    # result = numpy.reshape(result, (881, 921))

    # print(radarData.shape)
    # photo = sb.heatmap(
    #     data=radarData,
    # )
    # photo.invert_yaxis()
    # photo.get_figure().savefig("out0_max.png")
