n = int(input())
list_p = input().split(" ")
for i in range(n):
    list_p[i] = int(list_p[i])

list_p.sort(reverse=True)
_sum = sum(list_p)
twin_A = 0
count = 0
for i in range(n):
    twin_A += list_p[i]
    count += 1
    if 2 * twin_A > _sum:
        break
print(count)