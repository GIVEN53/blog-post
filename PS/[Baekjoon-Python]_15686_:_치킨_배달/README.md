[Baekjoon-Python] 15686 : 치킨 배달
=
<https://www.acmicpc.net/problem/15686>


접근
--


1. 집과 치킨집의 인덱스를 구한다.
2. 치킨집에서 m개를 조합하여 치킨 거리를 구한다.


풀이
--



```python
from sys import stdin
from itertools import combinations

n, m = map(int, stdin.readline().split())
house = []
chicken = []
for i in range(n):
    city = list(map(int, stdin.readline().split()))
    for j in range(n):
        if city[j] == 1:
            house.append((i, j))
        elif city[j] == 2:
            chicken.append((i, j))

res = 1e9
for chicken_pick in combinations(chicken, m):
    total_chicken_dist = 0
    for hr, hc in house:
        chicken_dist = 1e9
        for cr, cc in chicken_pick:
            chicken_dist = min(chicken_dist, abs(hr - cr) + abs(hc - cc))
        total_chicken_dist += chicken_dist
    res = min(res, total_chicken_dist)

print(res)
```

