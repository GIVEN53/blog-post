[Baekjoon-Python] 1717 : 집합의 표현
=
<https://www.acmicpc.net/problem/1717>


접근
--


1. 유니온\-파인드를 사용하여 두 집합을 합친다.


풀이
--



```python
from sys import stdin, setrecursionlimit


def find(x):
    if x != parent[x]:
        parent[x] = find(parent[x])
    return parent[x]


def union(a, b):
    a = find(a)
    b = find(b)

    if a < b:
        parent[b] = a
    else:
        parent[a] = b


setrecursionlimit(10**6)
n, m = map(int, stdin.readline().split())
parent = [i for i in range(n + 1)]

for _ in range(m):
    operator, a, b = map(int, stdin.readline().split())
    if operator == 0: # (1)
        union(a, b)
    elif operator == 1: # (2)
        print("YES") if find(a) == find(b) else print("NO")
```


* (1\) 합집합 연산한다.
* (2\) 포함 관계를 확인한다.
