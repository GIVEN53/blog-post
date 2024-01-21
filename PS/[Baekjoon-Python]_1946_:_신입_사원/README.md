[Baekjoon-Python] 1946 : 신입 사원
=
<https://www.acmicpc.net/problem/1946>


접근
--


1. 서류 성적 순위를 인덱스로 사용한다.
2. 인덱스를 순회하면서 면접 성적 순위를 비교한다.


풀이
--



```python
from sys import stdin

for _ in range(int(stdin.readline())):
    n = int(stdin.readline()) 
    interview_rank = [0] * n
    for _ in range(n):
        a, b = map(int, stdin.readline().split())
        interview_rank[a - 1] = b - 1 # (1)

    min_interview_rank = interview_rank[0] # (2)
    cnt = 1 # (3)
    for rank in interview_rank[1:]: # (4)
        if min_interview_rank > rank:
            min_interview_rank = rank
            cnt += 1

    print(cnt)
```


* (1) 인덱스는 서류 성적 순위이다. 각각의 인덱스에 면접 성적 순위를 저장한다.
* (2) 서류 성적 1위의 면접 성적 순위를 최솟값으로 초기화한다.
* (3) 서류 성적 1위는 무조건 선발된다.
* (4) 서류 성적 순위 순으로 순회하면서 면접 성적 순위를 비교한다. 면접 성적 순위의 최솟값을 갱신하는 신입 사원은 앞의 신입 사원보다 서류 성적은 떨어지지만 면접 성적은 우수하므로 선발된다.
