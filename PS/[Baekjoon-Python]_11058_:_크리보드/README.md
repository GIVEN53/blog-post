[Baekjoon-Python] 11058 : 크리보드
=
<https://www.acmicpc.net/problem/11058>


접근
--


1. N이 1 ~ 6일 경우 N만큼 A를 출력하는 것이 최댓값이다.
2. 7부터는 붙여넣기를 한 번부터 세 번까지 시행한 것 중 최댓값을 선택한다.


풀이
--



```python
from sys import stdin

N = int(stdin.readline())
dp = [i for i in range(N + 1)]

for i in range(7, N + 1):
    dp[i] = max(dp[i - 3] * 2, dp[i - 4] * 3, dp[i - 5] * 4) # (1)

print(dp[N])
```


* (1)  
`dp[i - 3] * 2` : Ctrl-A, Ctrl-C, Ctrl-V  
`dp[i - 4] * 3` : Ctrl-A, Ctrl-C, Ctrl-V, Ctrl-V  
`dp[i - 5] * 4` : Ctrl-A, Ctrl-C, Ctrl-V, Ctrl-V, Ctrl-V
