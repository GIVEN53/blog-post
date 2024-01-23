[Baekjoon-Python] 2294 : 동전 2
=
<https://www.acmicpc.net/problem/2294>


접근
--


1. 가치를 순회하면서 동전 개수의 최솟값을 메모이제이션한다.


풀이
--



```python
from sys import stdin

n, k = map(int, stdin.readline().split())
coins = set() # (1)
for _ in range(n):
    coin = int(stdin.readline())
    if coin <= k: # (2)
        coins.add(coin)

dp = [1e9] * (k + 1)
dp[0] = 0
for v in range(1, k + 1):
    for coin in coins:
        if v >= coin: # (3)
            dp[v] = min(dp[v], dp[v - coin] + 1)

print(dp[k] if dp[k] != 1e9 else -1)
```


* (1) 가치가 같은 동전이 여러 번 주어질 수 있기 때문에 set을 사용한다.
* (2) k보다 작거나 같은 동전만 삽입한다.
* (3) 현재 동전이 가치보다 작거나 같으면 최솟값을 갱신한다. 예를 들어 v = 10이고 현재 동전이 7원일 때 3원을 만드는 최소 동전 개수에 7원 한 개를 더하면 10을 만들 수 있다.
