[Baekjoon-Python] 1092 : 배
=
<https://www.acmicpc.net/problem/1092>


접근
--


1. 크레인과 박스를 내림차순 정렬한다.
2. 첫 번째 크레인이 첫 번째 박스를 옮길 수 없으면 -1을 출력한다.
3. 두 번째 크레인부터 순회하면서 박스를 옮길 수 있는지 확인한다.
4. 박스를 옮길 수 있는 크레인 중에서 가장 적게 옮긴 크레인이 박스를 옮긴다.
5. 박스를 옮길 수 있는 크레인이 없거나 가장 적게 옮긴 크레인이 첫 번째 크레인이면 첫 번째 크레인이 박스를 옮긴다.


풀이
--



```python
from sys import stdin
from collections import deque

n = int(stdin.readline())
crane = sorted(list(map(int, stdin.readline().split())), reverse=True) # (1)
_ = int(stdin.readline())
box = deque(sorted(map(int, stdin.readline().split()), reverse=True)) # (2)

if box[0] > crane[0]:
    print(-1)
    exit()

batch_crane = [0] * n # (3)
while box:
    b = box.popleft()
    worker, min_batch = 0, batch_crane[0]
    for i in range(1, n): # (4)
        if crane[i] >= b: # (5)
            if batch_crane[i] < min_batch:
                worker = i
                min_batch = batch_crane[i]
        else:
            break
    batch_crane[worker] += 1

print(max(batch_crane))
```


* (1) 크레인의 무게 제한을 내림차순 정렬한다.
* (2) 박스의 무게를 내림차순 정렬한다.
* (3) 각 크레인마다 박스를 옮긴 개수이다. 모든 크레인은 동시에 움직이기 때문에 박스를 옮긴 개수가 최대한 균일해야 한다.
* (4) 두 번째 크레인부터 순회한다. 크레인을 내림차순 정렬했기 때문에 두 번째 크레인에서 else문을 만나면 첫 번째 크레인이 박스를 옮긴다.
* (5) i번째 크레인이 박스를 옮길 수 있을 때 옮긴 개수가 가장 적으면 박스를 옮길 대상이 된다.
