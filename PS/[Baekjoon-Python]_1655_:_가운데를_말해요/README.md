[Baekjoon-Python] 1655 : 가운데를 말해요
=
<https://www.acmicpc.net/problem/1655>


접근
--


1. 최대 힙과 최소 힙 두 개를 사용한다.
2. 최대 힙 길이와 최소 힙 길이가 같으면 최대 힙에 삽입하고, 길이가 다르면 최소 힙에 삽입한다.
3. 최대 힙의 최댓값을 최소 힙의 최솟값보다 작게 만든다.
4. 최대 힙의 0번 인덱스 값이 중간 값이다.


풀이
--



```python
from sys import stdin
from heapq import heappush, heappop


max_heap = []
min_heap = []
for _ in range(int(stdin.readline())):
    x = int(stdin.readline())

    if len(max_heap) == len(min_heap): # (1)
        heappush(max_heap, x * -1)
    else: # (2)
        heappush(min_heap, x)

    if len(max_heap) > 0 and len(min_heap) > 0 and max_heap[0] * -1 > min_heap[0]: # (3)
        mx = heappop(max_heap) * -1
        mn = heappop(min_heap)

        heappush(max_heap, mn * -1)
        heappush(min_heap, mx)

    print(max_heap[0] * -1) # (4)
```


* (1) 두 힙의 길이가 같으면 정수를 최대 힙에 삽입한다.
* (2) 길이가 다르면 정수를 최소 힙에 삽입한다.
* (3) 최대 힙의 최댓값이 최소 힙의 최솟값보다 크면 두 값의 힙 위치를 교체한다.
* (4) 최대 힙의 0번 인덱스 값이 중간 값이 된다.
