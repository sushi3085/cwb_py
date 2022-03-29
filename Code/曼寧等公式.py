def manning_velocity(width, depth, S, n_manning_coefficient=0.07) -> float:
    # return speed of water
    # R => 水力半徑 = 截面積/濕周 = ab/(2a+b)
    R = width * depth / (2 * depth + width)
    # S => slope, in 'not angle' format
    return (R ** (2 / 3)) * (S ** 0.5) / n_manning_coefficient


def Q_cMS(velocity, area):
    # Q = VA
    return velocity * area


if __name__ == '__main__':
    print(Q_cMS(manning_velocity(10, 5, 0.05), 50))
    pass
