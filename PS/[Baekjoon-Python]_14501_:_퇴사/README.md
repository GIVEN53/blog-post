[Baekjoon-Python] 14501 : 퇴사
=
<https://www.acmicpc.net/problem/14501>


접근
--


1. 날짜를 역순으로 순회하면서 해당 날짜 수익의 최댓값을 메모이제이션한다.
2. 현재 날짜의 수익은 현재와 T일 뒤의 수익의 합, 다음날의 수익 중 최댓값이다. 즉, 오늘 상담해서 T일 뒤에 상담할 것인지, 오늘 상담을 포기하고 내일 상담할 것인지 선택하는 것이다.


풀이
--



```python
from sys import stdin

n = int(stdin.readline())
consulting = [tuple(map(int, stdin.readline().split())) for _ in range(n)]

dp = [0] * (n + 1)
for d in range(n - 1, -1, -1): # (1)
    t, p = consulting[d]
    if d + t > n: # (2)
        dp[d] = dp[d + 1]
    else: # (3)
        dp[d] = max(dp[d + t] + p, dp[d + 1])

print(dp[0])
```


* (1) 날짜를 역순으로 순회한다.
* (2) 퇴사해서 d일에 잡힌 상담을 할 수 없으면 다음 날의 수익을 저장한다.
* (3) d일의 상담을 할 수 있으면 d + t일의 수익과 d일 수익의 합, 다음 날의 수익 중 최댓값을 저장한다.
