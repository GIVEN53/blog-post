[Baekjoon-Python] 2110 : 공유기 설치
=
<https://www.acmicpc.net/problem/2110>


접근
--


* 공유기 사이의 거리를 이분 탐색한다.
* 1번 집에는 공유기를 무조건 설치한다.
* `mid` 거리만큼 집에 공유기를 설치했을 때 c개를 모두 설치할 수 있는지 확인한다.


풀이
--



```python
from sys import stdin


def binary_search(start, end):
    while start <= end:
        mid = (start + end) // 2
        cnt, bound = 1, house[0] + mid
        for h in house:
            if h >= bound: # (1)
                cnt += 1
                bound = h + mid

        if cnt >= c:
            start = mid + 1
        else:
            end = mid - 1
    return end


n, c = map(int, stdin.readline().split())
house = [int(stdin.readline()) for _ in range(n)]
house.sort()

start, end = 1, (house[-1] - house[0]) // (c - 1) # (2)
print(binary_search(start, end))
```


* (1) 공유기를 설치할 수 있는지 확인한다.
* (2) c에 따라 공유기를 설치할 수 있는 최대 거리가 달라지기 때문에 범위를 좁혀준다.
