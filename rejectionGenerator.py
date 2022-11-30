from numpy import floor, sqrt, pi, tan, median, cos, arccos
from scipy import special


# this is the robust rejection criterion we use to determine whether or not we reject a pixel from a set
# important, this needs to use a sorted set of absolute deviations (SORTING FROM LEAST TO GREATEST IS NECESSARY)


def rejectionGeneratorFinal(absdev, nu):
    N = len(absdev)
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
    # if N == 1:
    #     correction = 0
    if nu == 0:
        i = floor(0.683 * N)
        i_minus = 0.683 * (N - 1)
        gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) # * correction
        rejectionFactor = gamma * sqrt(2) * special.erfinv(1 - (0.5 / N))

    if nu == 1:
        i = floor(0.5 * N)
        i_minus = 0.5 * (N - 1)
        gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) # * correction
        rejectionFactor = gamma * tan(pi * (0.5 - (0.25 / N)))

    if nu == 2:
        i = floor(0.577 * N)
        i_minus = 0.577 * (N - 1)
        gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) # * correction
        alpha = (1 - 0.25 / N) / N
        rejectionFactor = gamma * 2 * (0.5 - (0.25 / N)) * sqrt(2 / alpha)

    if nu == 4:
        i = floor(0.626 * N)
        i_minus = 0.626 * (N - 1)
        gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) # * correction
        alpha = (1 - 0.25 / N) / N
        q = cos(1 / 3 * arccos(sqrt(alpha))) / sqrt(alpha)
        rejectionFactor = gamma * 2 * sqrt(q - 1)

    return rejectionFactor, gamma

# ##### For reference later if we need it
# # nu = inf
# def rejectionGenerator(absdev, f):
#     N = len(absdev)
#
#     # now we have the final set to be tested (absdev) we find the rejection facto
#     # print(absdev)
#     if N >= 6:
#         correction = 1 + (2.2212 * (N ** (-1.137)))
#     if N == 5:
#         correction = 1.31
#     if N == 4:
#         correction = 1.53
#     if N == 3:
#         correction = 1.59
#     if N == 2:
#         correction = 1.76
#
#     i = floor(0.683 * N)
#     i_minus = 0.683 * (N - 1)
#     sigma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus))) * correction
#     rejection_factor = f * sigma * sqrt(2) * special.erfinv(1 - (0.5 / N))
#     return rejection_factor, sigma
#
#
# # nu = 1
# def lorentzianRejectionGenerator(absdev):
#     # x0 is the median of the set
#     # gamma is the 50%tile deviation
#     x0 = median(absdev)
#     N = len(absdev)
#     i = floor(0.5 * N)
#     i_minus = 0.5 * (N - 1)
#     gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus)))
#     rejectionFactor = x0 + gamma * tan(pi * (0.5 - (0.25 / N)))
#
#     return rejectionFactor, gamma
#
#
# # This is the first intermediate case in the student's T distribution, closer to the lorentzian side: nu = 2
# def studentsTOne(absdev):
#     # x0 is the median of the set
#     # gamma is the 50%tile deviation
#     x0 = median(absdev)
#     N = len(absdev)
#     i = floor(0.577 * N)
#     i_minus = 0.577 * (N - 1)
#     gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus)))
#     alpha = (1 - 0.25 / N) / N
#     rejectionFactor = x0 + gamma * 2 * (pi * (0.5 - (0.25 / N))) * sqrt(2 / alpha)
#
#     return rejectionFactor, gamma
#
#
# # This is the second intermediate case in the student's T distribution, closer to the gaussian side:  nu = 4
# def studentsTTwo(absdev):
#     # x0 is the median of the set
#     # gamma is the 50%tile deviation
#     x0 = median(absdev)
#     N = len(absdev)
#     i = floor(0.626 * N)
#     i_minus = 0.626 * (N - 1)
#     gamma = (absdev[int(i) - 1] + (absdev[int(i)] - absdev[int(i) - 1]) * (i_minus - floor(i_minus)))
#     alpha = (1 - 0.25 / N) / N
#     q = cos(1 / 3 * arccos(sqrt(alpha))) / sqrt(alpha)
#     rejectionFactor = x0 + gamma * 2 * sqrt(q - 1)
#
#     return rejectionFactor, gamma
