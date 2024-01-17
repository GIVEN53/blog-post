[Baekjoon-Python] 13904 : 과제
=
<https://www.acmicpc.net/problem/13904>


접근
--


1. 1일에 마감일이 6일 남은 과제를 하지 않기 위해 마감일을 내림차순으로 정렬해서 마감일이 큰 것부터 점수를 구한다.
2. 현재 날짜에 마감할 수 있는 과제까지 꺼낸다.
3. 꺼낸 과제 중 점수가 가장 큰 과제를 구한다.


풀이
--



```python
from sys import stdin
from heapq import heappop, heappush

n = int(stdin.readline())
task = []
for _ in range(n):
    d, w = map(int, stdin.readline().split())
    heappush(task, (-d, w))

possible_task, score = [], 0
for day in range(-task[0][0], 0, -1):
    while task and -task[0][0] >= day:
        heappush(possible_task, -heappop(task)[1])

    if possible_task:
        score += -heappop(possible_task)

print(score)
```

