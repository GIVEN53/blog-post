[Baekjoon-Python] 1509 : 팰린드롬 분할
=
<https://www.acmicpc.net/problem/1509>


접근
--


1. 팰린드롬은 거꾸로 읽어도 제대로 읽은 것과 같은 문장을 의미한다.
2. 현재 문자열의 시작 문자와 끝 문자가 같고 내부 문자열이 팰린드롬이면 현재 문자열은 팰린드롬이다.


풀이
--



```python
from sys import stdin

letter = stdin.readline().rstrip()
n = len(letter)
palindrome = [[0] * n for _ in range(n)]
dp = [2500] * (n + 1)
dp[-1] = 0
for e in range(n):
    for s in range(e + 1):
        if letter[s] == letter[e] and (e - s < 2 or palindrome[s + 1][e - 1]): # (1)
            palindrome[s][e] = 1
            dp[e] = min(dp[e], dp[s - 1] + 1)

print(dp[n - 1])
```


* (1) 시작 문자와 끝 문자가 같고, 현재 길이가 1이거나 내부 문자열이 팰린드롬일 경우 팰린드롬 처리하고 dp 값을 갱신한다.
