[Baekjoon-Python] 2109 : 순회강연
=
<https://www.acmicpc.net/problem/2109>


접근
--


1. d를 기준으로 오름차순 정렬한다.
2. 우선순위 큐에 p를 삽입하고 큐 사이즈가 d보다 크면 가장 작은 p를 삭제한다.


풀이
--



```python
from sys import stdin
from heapq import heappop, heappush

n = int(stdin.readline())
univ = sorted(
	[tuple(map(int, stdin.readline().split())) for _ in range(n)], key=lambda x: x[1]
)

ans = []
for pay, day in univ:
    heappush(ans, pay)
    if day < len(ans):
        heappop(ans)

print(sum(ans))
```

