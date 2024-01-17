[Baekjoon-Python] 12904 : A와 B
=
<https://www.acmicpc.net/problem/12904>


접근
--


1. 반대로 문자열 t를 연산하여 s가 되는지 확인한다.
2. 두 연산 모두 문자열 마지막에 A 또는 B를 추가하기 때문에 t의 마지막 인덱스를 삭제한다.
3. 삭제한 문자가 B면 t를 뒤집는다.


풀이
--



```python
from sys import stdin

s, t = list(stdin.readline().rstrip()), list(stdin.readline().rstrip())
while len(s) < len(t):
    last = t.pop()
    if last == "B":
        t = t[::-1]

print(1 if s == t else 0)
```

