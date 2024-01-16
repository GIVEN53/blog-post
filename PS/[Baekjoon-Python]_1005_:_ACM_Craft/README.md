[Baekjoon-Python] 1005 : ACM Craft
=
<https://www.acmicpc.net/problem/1005>


접근
--


1. 위상 정렬 알고리즘을 사용한다.
2. 이전 순서의 건설 시간을 메모이제이션해서 현재 건물의 건설 시간을 계산한다.
3. 현재 건물은 이전 순서의 건설 시간의 최댓값이 지난 후 건설이 시작된다.


풀이
--



```python
from sys import stdin
from collections import deque


def topological_sort(target):
    q = deque()
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            q.append(i) # (1)

    dp = [0] * (N + 1)
    while q:
        now = q.popleft()
        dp[now] += time[now - 1] # (2)

        if now == target:
            return dp[now]

        for next in graph[now]: # (3)
            in_degree[next] -= 1
            dp[next] = max(dp[now], dp[next]) # (4)
            if in_degree[next] == 0:
                q.append(next)


T = int(stdin.readline())
for _ in range(T):
    N, K = map(int, stdin.readline().split())
    time = [*map(int, stdin.readline().split())]
    graph = [[] for _ in range(N + 1)]

    in_degree = [0] * (N + 1)
    for _ in range(K):
        a, b = map(int, stdin.readline().split())
        graph[a].append(b)
        in_degree[b] += 1 # (5)

    W = int(stdin.readline())
    print(topological_sort(W))
```


* (1) 진입 차수가 0인 노드를 큐에 삽입한다.
* (2) 자신의 건설 시간을 더한다.
* (3) 다음 노드를 순회하면서 진입 차수를 1씩 감소시키고, 진입 차수가 0이면 큐에 삽입한다.
* (4) 현재 차수 건설 시간의 최댓값을 저장한다.
* (5) a -> b 간선이 존재할 때 b의 진입 차수가 증가한다.


### 예시


![](https://blog.kakaocdn.net/dn/cZAQjD/btsDxLXkj4x/JPSbAjY5ZDoIK1aeT0HQak/img.png)


* 정점(v)과 건설 시간(t), 간선 정보가 위와 같이 주어졌을 때 진입 차수가 0인 정점 1부터 큐에 삽입한다.


![](https://blog.kakaocdn.net/dn/cNMzrr/btsDqjVVJwr/ej90K9soGNRS7L9KFjyHWK/img.png)


* now = 1 : dp에 자신의 건설 시간(10)을 더한다.
* next = 2, 3 : dp에 1의 건설 시간을 저장하고, 진입 차수가 0이 되어 큐에 삽입한다.


![](https://blog.kakaocdn.net/dn/bhqoEP/btsDuyYMCE3/5KpzIwKikgEiO381X9h7BK/img.png)


* now = 2 : dp에 자신의 건설 시간(20)을 더한다.
* next = 4, 5 : dp에 2의 건설 시간을 저장하고, 4는 진입 차수가 0이 되어 큐에 삽입한다.


![](https://blog.kakaocdn.net/dn/bemiug/btsDs2yZsYk/pu3mFnMRlciihdDd7Kar6K/img.png)


* now = 3 : dp에 자신의 건설 시간(1)을 더한다.
* next = 5, 6 : 5는 2의 건설 시간이 더 크므로 3의 건설 시간을 저장하지 않고 6은 dp에 3의 건설 시간을 저장한다. 5, 6 모두 진입 차수가 0이 되어 큐에 삽입한다.


![](https://blog.kakaocdn.net/dn/LduDD/btsDxxEYSKP/wK88raJUyIl1Dw6f1AFFZk/img.png)


* now = 4 : dp에 자신의 건설 시간(5)을 더한다.


![](https://blog.kakaocdn.net/dn/R4K9w/btsDxhoQ0x0/xSA13O2y84RAIPdTyixOu0/img.png)


* now = 5 : dp에 자신의 건설 시간(8)을 더한다.
* next = 7 : dp에 5의 건설 시간을 저장한다.


![](https://blog.kakaocdn.net/dn/cDcMep/btsDxlxSlnn/xhI1nWFmy5jKcnGhOjjVQK/img.png)


* now = 6 : dp에 자신의 건설 시간(7)을 더한다.
* next = 7 : 5의 건설 시간이 더 크므로 6의 건설 시간을 저장하지 않고, 진입 차수가 0이 되어 큐에 삽입한다.


![](https://blog.kakaocdn.net/dn/84hOK/btsDxhI9LA5/5uG2sOus2AvzzJHfvG84m0/img.png)


* now = 7 : dp에 자신의 건설 시간(1)을 더한다.
* next = 8 : dp에 7의 건설 시간을 저장하고, 진입 차수가 0이 되어 큐에 삽입한다.


![](https://blog.kakaocdn.net/dn/vmtad/btsDrCtOSxD/BBdbpGABUMTFYMgqFkKt01/img.png)


* now = 8 : dp에 자신의 건설 시간(43)을 더한다.
