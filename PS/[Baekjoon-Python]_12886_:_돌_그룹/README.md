[Baekjoon-Python] 12886 : 돌 그룹
=
<https://www.acmicpc.net/problem/12886>


접근
--


1. 전체 돌의 개수는 고정이므로 숫자 2개(a, b)만 사용한다.
2. c = 전체 돌의 개수 - (a + b)로 구한다.
3. 3개의 돌 그룹 중 2개를 선택해서 연산을 실행하고 큐에 추가한다.
4. 중복된 a, b가 나올 수 있기 때문에 중복을 제거한다.


풀이
--



```python
from sys import stdin
from collections import deque


def find_group(a, b):
    q = deque([(a, b)])
    visited[a][b] = True
    while q:
        a, b = q.popleft()
        c = tot - a - b
        if a == b == c:
            return 1

        for x, y in (a, b), (a, c), (b, c):
            if x == y:
                continue

            x, y = 2 * x, y - x
            x, y, _ = sorted((x, y, tot - x - y)) # (1)
            if not visited[x][y]:
                q.append((x, y))
                visited[x][y] = True
    return 0


a, b, c = map(int, stdin.readline().split())
a, b, c = sorted((a, b, c))
tot = a + b + c
visited = [[False] * (tot + 1) for _ in range(tot + 1)]

if tot % 3 != 0: # (2)
    print(0)
else:
    print(find_group(a, b))
```


* (1) 정렬해서 큐에 추가하기 때문에 큐에서 꺼낸 후 a, b, c는 항상 `a <= b <= c`를 만족한다.
* (2) 전체 돌의 개수가 3의 배수가 아니면 돌 그룹을 같은 개수로 만들 수 없기 때문에 0을 출력한다.
