import numpy as np

# A = np.array([
#     [1, 2, 3],
#     [4, 5, 6]
# ])
#
# C = np.array([
#     [1, 2],
#     [3, 4],
#     [5, 6]
# ])
#
# print(A @ C) # matrix product

# X = np.array([
#     [1, 2, 3],
#     [4, 5, 6]
# ])
# print(X.sum(axis=0)) # along vertical
# print(X.sum(axis=1)) # along horizontal

# broadcasting
X = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

# b = np.array([10, 20, 30])

# print(X + b)
# # [[11 22 33]
# #  [14 25 36]]
#
# print(X * 2)
# # [[ 2  4  6]
# #  [ 8 10 12]]

# vectorisation
# x = np.array([1, 2, 3, 4, 5])
#
# print(x ** 2)
# print(np.sqrt(x))
# print(np.exp(x))
# [ 1  4  9 16 25]
# [1.         1.41421356 1.73205081 2.         2.23606798]
# [  2.71828183   7.3890561   20.08553692  54.59815003 148.4131591 ]

# x = np.arange(24) # gives 0at0, 1at1...
#
# print(x)
# print(x.shape)
#
# A = x.reshape(4, 6)
# B = x.reshape(6, 4)
# C = x.reshape(2, -1) # -1 means u figure that value on own