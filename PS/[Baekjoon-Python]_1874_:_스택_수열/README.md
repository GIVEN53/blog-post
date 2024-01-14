[Baekjoon-Python] 1874 : 스택 수열
=
<https://www.acmicpc.net/problem/1874>


접근
--


1. 수열을 순회하면서 해당 값까지 스택에 push한다.
2. 스택을 pop하여 같은지 확인한다.


풀이
--



```python
from sys import stdin


def get_operator(nums):
    stack = []
    operator = []
    i = 1

    for num in nums:
        while i <= num:
            stack.append(i)
            operator.append("+")
            i += 1

        top = stack.pop()
        if top != num:
            return "NO"
        operator.append("-")

    return "\n".join(operator)


n = int(stdin.readline())
nums = [int(stdin.readline()) for _ in range(n)]

print(get_operator(nums))
```

