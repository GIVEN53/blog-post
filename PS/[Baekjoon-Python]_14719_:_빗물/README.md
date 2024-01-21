[Baekjoon-Python] 14719 : 빗물
=
<https://www.acmicpc.net/problem/14719>


접근
--


1. 블록을 순회하면서 현재 블록 기준 왼쪽에서 가장 높은 높이, 오른쪽에서 가장 높은 높이를 구한다.
2. 두 높이 중 최솟값까지 물이 고일 수 있다.


풀이
--



```python
from sys import stdin

h, w = map(int, stdin.readline().split())
blocks = list(map(int, stdin.readline().split()))

res = 0
for i in range(1, w - 1): # (1)
    left = max(blocks[:i]) # (2)
    right = max(blocks[i + 1 :]) # (3)
    min_height = min(left, right) # (4)
    if min_height > blocks[i]: # (5)
        res += min_height - blocks[i]

print(res)
```


* (1) 양쪽 끝 블록은 빗물이 고일 수 없기 때문에 제외하고 순회한다.
* (2) 현재 블록을 기준으로 왼쪽에서 가장 높은 높이이다.
* (3) 현재 블록을 기준으로 오른쪽에서 가장 높은 높이이다.
* (4) 현재 블록은 두 높이 중 최솟값까지 물이 고일 수 있다.
* (5) 현재 블록이 최솟값보다 작아야 물이 고일 수 있다.
