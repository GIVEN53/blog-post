[Baekjoon-Python] 1202 : 보석 도둑
=
<https://www.acmicpc.net/problem/1202>


접근
--


1. 보석과 가방을 무게순으로 정렬한다.
2. 가방에 담을 수 있는 무게까지 보석을 꺼낸다.
3. 꺼낸 보석 중 가격이 가장 높은 보석을 구한다.


풀이
--



```python
from sys import stdin
from heapq import heappop, heappush

n, k = map(int, stdin.readline().split())
jewel = sorted(
    [tuple(map(int, stdin.readline().split())) for _ in range(n)], key=lambda x: x[0]
)
c = sorted(int(stdin.readline()) for _ in range(k))

price = 0
prices = []
for bag in c:
    while jewel and bag >= jewel[0][0]:
        heappush(prices, -heappop(jewel)[1])

    if prices:
        price += -heappop(prices)

print(price)
```

