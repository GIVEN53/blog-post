[Baekjoon-Python] 2493 : 탑
=
<https://github.com/co-niverse/algorithm-study/pull/111>


접근
--


1. 스택 맨 위의 탑보다 현재 탑의 높이가 더 높으면 높이가 작거나 같을 때까지 스택을 삭제한다.
2. 스택 맨 위의 탑보다 현재 탑의 높이가 작거나 같으면 스택 맨 위의 탑의 인덱스를 저장한다.
3. 스택에 현재 탑을 삽입한다.


풀이
--



```python
from sys import stdin

n = int(stdin.readline())

res = [0] * n
stack = []
for i, height in enumerate(map(int, stdin.readline().split())):
    if stack and stack[-1][0] < height: # (1)
        while stack and stack[-1][0] < height:
            stack.pop()
    if stack: # (2)
        res[i] = stack[-1][1]
    stack.append((height, i + 1)) # (3)

print(*res)
```


* (1) 현재 탑의 높이가 stack 맨 위의 탑보다 높으면 높이가 작거나 같을 때까지 stack을 삭제한다.
* (2) stack이 비어있지 않으면 레이저 신호가 stack 맨위의 탑에서 수신한다. stack이 빈 경우는 신호가 어떤 탑에서도 수신하지 못하며 res를 0으로 초기화했기 때문에 따로 처리하지 않는다.
* (3) stack에 높이와 인덱스를 삽입한다.
