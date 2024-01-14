[Baekjoon-Python] 1043 : 거짓말
=
<https://www.acmicpc.net/problem/1043>


접근
--


1. 진실을 아는 사람과 파티에 오는 사람들에 교집합이 있으면 합집합을 구한다.
2. 진실을 아는 사람과 교집합이 없는 파티의 수를 구한다.


풀이
--



```python
from sys import stdin

N, M = map(int, stdin.readline().split())
truth = set(stdin.readline().split()[1:])
party = []
for _ in range(M):
    party.append(set(stdin.readline().split()[1:]))

for _ in range(M):
    for p in party:
        if truth & p:
            truth = truth.union(p)

cnt = 0
for p in party:
    if not p & truth:
        cnt += 1

print(cnt)
```

