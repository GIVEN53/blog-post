[Baekjoon-Python] 2437 : 저울
=
<https://www.acmicpc.net/problem/2437>


접근
--


1. 저울추의 누적합을 구하면서 다음 저울추가 누적합보다 크면 더 이상 무게를 측정할 수 없다.


풀이
--



```python
from sys import stdin

n = int(stdin.readline())
scale = sorted(map(int, stdin.readline().split()))

weight = 1
for i in range(n):
    if weight < scale[i]:
        break
    weight += scale[i]

print(weight)
```

