def Q_CIA(I, A):
    """
    we assert that C to be 1.

    !! IMPORTANT !! A is in 'ha' unit
    """
    return I * A


def manning_velocity(width, depth, S, n_manning_coefficient=0.07) -> float:
    # return speed of water
    # R => 水力半徑 = 截面積/濕周 = ab/(2a+b)
    R = width * depth / (2 * depth + width)
    # S => slope, in 'not angle' format
    return (R ** (2 / 3)) * (S ** 0.5) / n_manning_coefficient


def arrive_time(distance, velocity):
    return distance / velocity


def H(Q, velocity, width):
    return Q / velocity / width


# ======================== #
def km2_to_ha(km2):
    return 100 * km2


if __name__ == '__main__':
    print(manning_velocity(10, 5, 0.05), 'm/s')
    pass
