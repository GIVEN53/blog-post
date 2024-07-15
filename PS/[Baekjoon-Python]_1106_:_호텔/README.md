[Baekjoon-Python] 1106 : 호텔
=
<https://www.acmicpc.net/problem/1106>


접근
--


1. 최소 비용을 메모이제이션한다.
2. dp의 인덱스를 고객 수로 설정한다.


풀이
--



```python
from sys import stdin

c, n = map(int, stdin.readline().split())
city = [list(map(int, stdin.readline().split())) for _ in range(n)]
dp = [1e9] * (c + 1) # (1)
dp[0] = 0

for i in range(1, c + 1):
    for cost, customer in city:
        if i <= customer: # (2)
            dp[i] = min(dp[i], cost)
        else: # (3)
            dp[i] = min(dp[i], dp[i - customer] + cost)

print(dp[-1])
```


* (1\) 인덱스는 고객 수, 값은 해당 고객 수를 얻을 수 있는 최소 비용이다.
* (2\) 해당 도시에 홍보할 때 i 고객 수 이상을 만들 수 있으면 현재 도시의 비용과 최솟값을 갱신한다.
* (3\) 만들 수 없으면 i \- customer의 비용 \+ 현재 도시의 비용과 최솟값을 갱신한다.
