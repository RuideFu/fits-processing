from numpy import floor, sqrt
from scipy import special

# this is the robust rejection criterion we use to determine whether or not we reject a pixel from a set
# important, this needs to use a sorted set of absolute deviations (SORTING FROM LEAST TO GREATEST IS NECESSARY)


def rejectionGenerator(absdev, f):
    N = len(absdev)

    # now we have the final set to be tested (absdev) we find the rejection facto
    # print(absdev)
    if N >= 6:
        correction = 1 + (2.2212 * (N ** (-1.137)))
    if N == 5:
        correction = 1.31
    if N == 4:
        correction = 1.53
    if N == 3:
        correction = 1.59
    if N == 2:
        correction = 1.76

    i = floor(0.683 * N)
    i_minus = 0.683 * (N - 1)
    sigma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) * correction
    rejection_factor = f * sigma * sqrt(2) * special.erfinv(1 - (0.5 / N))
    return rejection_factor, sigma
