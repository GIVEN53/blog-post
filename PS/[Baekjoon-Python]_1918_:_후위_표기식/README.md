[Baekjoon-Python] 1918 : 후위 표기식
=
<https://www.acmicpc.net/problem/1918>


접근
--


1. 여는 괄호와 연산자는 스택에 삽입한다.
2. 여는 괄호는 닫는 괄호를 만났을 때 스택에서 삭제한다.
3. 연산자는 다음 연산자보다 우선순위가 높을 때 스택에서 삭제한다.


풀이
--



```python
from sys import stdin

infix = stdin.readline().rstrip()
priority = {"*": 2, "/": 2, "+": 1, "-": 1}
stack = []
res = []
for token in infix:
    if 65 <= ord(token) <= 90: # (1)
        res.append(token)
    else:
        if token == ")":
            while stack[-1] != "(": # (2)
                res.append(stack.pop())
            stack.pop() # (3)
        elif token == "(":
            stack.append(token) # (4)
        else:
            if stack and stack[-1] != "(" and priority[stack[-1]] >= priority[token]: # (5)
                while stack and stack[-1] != "(" and priority[stack[-1]] >= priority[token]:
                    res.append(stack.pop())
            stack.append(token)

while stack:
    res.append(stack.pop()) # (6)

print("".join(res))
```


* (1) 알파벳이면 res에 삽입한다.
* (2) 닫는 괄호이면 여는 괄호를 만날 때까지 stack에서 꺼내서 res에 삽입한다.
* (3) 여는 괄호를 만나서 while문을 탈출했기 때문에 여는 괄호도 stack에서 꺼낸다.
* (4) 여는 괄호이면 stack에 삽입한다.
* (5) 연산자이면 연산자의 우선순위를 비교해서 현재 연산자의 우선순위가 클 때까지 stack에서 꺼내서 res에 삽입한다.
* (6) stack에 남아있는 연산자를 역순으로 res에 삽입한다.
