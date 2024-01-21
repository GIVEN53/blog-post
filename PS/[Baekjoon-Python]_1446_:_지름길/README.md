[Baekjoon-Python] 1446 : 지름길
=
<https://www.acmicpc.net/problem/1446>


접근
--


1. 도로 길이를 순회하면서 현재 운전거리의 최솟값을 메모이제이션한다.
2. 지름길을 지나지 않는 것이 거리가 더 짧을 수 있다.
3. 현재 위치가 지름길 도착 위치와 같다면 지름길을 지나서 온 거리와 현재 값 중 작은 것을 선택한다.


풀이
--



```python
from sys import stdin

n, d = map(int, stdin.readline().split())
short_road = [tuple(map(int, stdin.readline().split())) for _ in range(n)]

dp = [1e9] * (d + 1)
dp[0] = 0
for i in range(1, d + 1):
    dp[i] = dp[i - 1] + 1
    for start, end, length in short_road:
        if i == end: # (1)
            dp[i] = min(dp[i], dp[start] + length)

print(dp[d])
```


* (1) 지름길이 있으면 dp 값과 지름길의 시작 위치에서 지름길 길이만큼 온 것 중 최솟값을 저장한다.
