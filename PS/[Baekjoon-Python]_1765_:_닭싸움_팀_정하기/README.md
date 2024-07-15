[Baekjoon-Python] 1765 : 닭싸움 팀 정하기
=
<https://www.acmicpc.net/problem/1765>


접근
--


1. 유니온\-파인드를 사용하여 인간관계를 합친다.


풀이
--



```python
from sys import stdin


def find(x):
    if x != friend[x]:
        friend[x] = find(friend[x])
    return friend[x]


def union(a, b):
    a, b = find(a), find(b)
    if a == b:
        return

    friend[b] = a


n, m = int(stdin.readline()), int(stdin.readline())
friend = [i for i in range(n + 1)]
enemy = [[] for _ in range(n + 1)]
for _ in range(m):
    letter, p, q = stdin.readline().split()
    p, q = int(p), int(q)
    if letter == "F":
        union(p, q) # (1)
    else:
        enemy[p].append(q)
        enemy[q].append(p)

for e in enemy: # (2)
    if len(e) > 1:
        a = e[0]
        for i in range(1, len(e)):
            union(a, e[i])

for i in range(1, n + 1):
    find(i) # (3)
print(len(set(friend)) - 1)
```


* (1\) p와 q는 서로 친구이므로 친구의 친구도 자신의 친구로 합친다.
* (2\) 임의의 학생 x의 원수는 리스트 e에 있다. 리스트 e에 있는 학생끼리는 서로 원수의 원수이므로 친구이다.
* (3\) 경로를 압축한다.
