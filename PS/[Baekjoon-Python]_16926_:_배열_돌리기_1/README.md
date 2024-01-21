[Baekjoon-Python] 16926 : 배열 돌리기 1
=
<https://www.acmicpc.net/problem/16926>


접근
--


1. 함께 회전하는 배열을 계층이라고 할 때, 각 계층을 순회한다.
2. 계층의 총 개수는 `min(n, m) / 2`이다.
3. i번째 계층의 시작 좌표 `(x, y)`는 `(i , i)`이다.
4. `(i , i)`부터 반시계 방향으로 i번째 계층의 값을 큐에 삽입한다.
5. 큐를 r만큼 회전한 후 큐에서 값을 삭제하면서 `(i , i)`부터 반시계 방향으로 값을 저장한다.


풀이
--



```python
from sys import stdin
from collections import deque

n, m, r = map(int, stdin.readline().split())
arr = [stdin.readline().split() for _ in range(n)]

q = deque()
for i in range(min(n, m) // 2): # (1)
    total = (n - 1 - 2 * i + m - 1 - 2 * i) * 2
    rotate_cnt = r % total # (2)

    q.extend([row[i] for row in arr[i : n - i - 1]]) # (3)
    q.extend(arr[n - i - 1][i : m - i - 1])
    q.extend([row[m - i - 1] for row in arr[i + 1 : n - i][::-1]])
    q.extend(arr[i][i + 1 : m - i][::-1])
    q.rotate(rotate_cnt)

    for k in range(i, n - i - 1): # (4)
        arr[k][i] = q.popleft()
    for k in range(i, m - i - 1):
        arr[n - i - 1][k] = q.popleft()
    for k in range(n - i - 1, i, -1):
        arr[k][m - i - 1] = q.popleft()
    for k in range(m - i - 1, i, -1):
        arr[i][k] = q.popleft()

for row in arr:
    print(*row)
```


* (1) 계층을 순회한다.
* (2) total은 i번째 계층의 총 요소 개수이다. total = 4일 때 1번 회전한 것과 5번 회전한 것은 같으므로 나머지 연산하여 중복 회전을 제거한다.
* (3) 색칠한 부분은 하나의 계층을 의미한다. 계층을 4개의 구간으로 잘라 큐에 삽입한다.  
![](https://blog.kakaocdn.net/dn/tHGY1/btsDJBVmFfF/gCi77kKKlrQxC3YqGWDQAk/img.png)
* (4) 반시계 방향으로 다시 배열에 저장한다.
