list1 = []
nums = []
res = []
for i in range(1, 50):
    for j in range(1, 50):
        if (i, j) in nums:
            continue
        num1 = i ** 3 + j ** 3
        if num1 in list1 and num1 not in res:
            res.append(num1)
        else:
            list1.append(num1)
            nums.append((i, j))
            nums.append((j, i))

print(*sorted(res))