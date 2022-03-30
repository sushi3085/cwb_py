def manning_velocity(width, depth, S, n_manning_coefficient=0.07) -> float:
    # return speed of water
    # R => 水力半徑 = 截面積/濕周 = ab/(2a+b)
    R = width * depth / (2 * depth + width)
    # S => slope, in 'not angle' format
    return (R ** (2 / 3)) * (S ** 0.5) / n_manning_coefficient


def Q_cMS(velocity, area):
    # Q = VA
    return velocity * area


def Q_CIA(C, I, A):
    return


def river_water_level(Q, V, width):
    return Q / V / width


if __name__ == '__main__':
    print(manning_velocity(10, 5, 0.05), 'm/s')
    pass
