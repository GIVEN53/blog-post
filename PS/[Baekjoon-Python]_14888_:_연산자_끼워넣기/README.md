[Baekjoon-Python] 14888 : 연산자 끼워넣기
=
<https://www.acmicpc.net/problem/14888>


접근
--


1. 연산자 개수가 남아있으면 개수를 1 감소시킨 후 dfs 탐색한다.
2. `N`만큼 탐색했으면 값을 저장하고 리턴한다.
3. 호출이 끝났으면 연산자 개수를 다시 증가시킨다.
4. 값을 오름차순 정렬하여 첫번 째와 마지막 인덱스 값을 출력한다.
5. 시간복잡도는 `O((N - 1)!) = 3,628,800`이므로 브루트 포스 가능


풀이
--



```python
from sys import stdin


def dfs(idx, num):
    global add, sub, mul, div

    if idx == N:
        result.append(num)
        return

    if add > 0:
        add -= 1
        dfs(idx+1, num + numbers[idx])
        add += 1

    if sub > 0:
        sub -= 1
        dfs(idx+1, num - numbers[idx])
        sub += 1

    if mul > 0:
        mul -= 1
        dfs(idx+1, num * numbers[idx])
        mul += 1

    if div > 0:
        div -= 1
        dfs(idx+1, int(num / numbers[idx]))
        div += 1


N = int(stdin.readline())
numbers = list(map(int, stdin.readline().split()))
add, sub, mul, div = map(int, stdin.readline().split())
result = []
dfs(1, numbers[0])

result.sort()
print(result[-1])
print(result[0])
```

