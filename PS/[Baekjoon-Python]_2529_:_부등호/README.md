[Baekjoon-Python] 2529 : 부등호
=
<https://www.acmicpc.net/problem/2529>


접근
--


1. 0 ~ 9까지 순회하면서 dfs 탐색한다.
2. 해당 숫자가 부등호를 만족하면 방문 처리한다.
3. 만족하는 숫자를 모두 뽑으면(K + 1개) 최댓값과 최솟값을 갱신하고 탐색을 종료한다.


풀이
--



```python
from sys import stdin


def dfs(r, num):
    global min_result, max_result

    if r == K + 1:
        if int(min_result) > int(num):
            min_result = num
        if int(max_result) < int(num):
            max_result = num
        return

    for i in range(10):
        if visited[i]:
            continue

        if r == 0 or check_sign(signs[r - 1], int(num[-1]), i):
            visited[i] = True
            dfs(r + 1, num + str(i))
            visited[i] = False


def check_sign(sign, num1, num2):
    if sign == ">":
        return num1 > num2
    else:
        return num1 < num2


K = int(stdin.readline())
signs = stdin.readline().split()

visited = [False] * 10
min_result = "9876543210"
max_result = "0"
dfs(0, "")

print(max_result)
print(min_result)
```

