dig_0 = 0.0
sum_0 = 0.0
dig_1 = 0.0
sum_1 = 0.0

lst = [74, 68, 68, 70, 67, 67, 79, 88, 88, 59]
rows = [74 + 1 + 0 + 2 + 0 + 1 + 1 + 4 + 0 + 8,
        2 + 68 + 2 + 4 + 5 + 2 + 3 + 1 + 4 + 3,
        1 + 68 + 2 + 1,
        12 + 2 + 4 + 70 + 12,
        9 + 67 + 4,
        9 + 67 + 9,
        5 + 4 + 79 + 4,
        12 + 88 + 1,
        8 + 88,
        18 + 11 + 59
        ]
weight = [0.02961946857694457, 0.06988263984148758, 0.03378550017781842, 0.03391251333638165, 0.44012599705329475,
          0.08598790834730478, 0.034623787024335724, 0.1963877457704618, 0.053015292384291014, 0.022659147487679724]
for i, value in enumerate(lst):
    dig_0 += value
    print(value)
    sum_0 += rows[i]

    dig_1 += weight[i] * value
    print(weight[i] * value)
    sum_1 += rows[i] * weight[i]

print(dig_0 / sum_0, dig_0, sum_0)
print(dig_1 / sum_1, dig_1, sum_1)