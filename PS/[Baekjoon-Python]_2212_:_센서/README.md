[Baekjoon-Python] 2212 : 센서
=
<https://www.acmicpc.net/problem/2212>


접근
--


1. 센서를 오름차순 정렬한다.
2. 센서 사이의 거리를 구한다.
3. 거리를 내림차순 정렬해서 앞에서 k - 1개를 뺀 나머지의 합을 구한다.


풀이
--



```python
from sys import stdin

n, k = int(stdin.readline()), int(stdin.readline())
sensor = sorted(map(int, stdin.readline().split()))
distance = sorted([sensor[i + 1] - sensor[i] for i in range(n - 1)], reverse=True)

print(sum(distance[k - 1 :])) # (1)
```


* (1) k가 2이상일 때부터 센서 사이의 거리를 줄일 수 있기 때문에 k - 1을 한다.
