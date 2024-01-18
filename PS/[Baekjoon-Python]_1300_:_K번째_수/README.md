[Baekjoon-Python] 1300 : K번째 수
=
<https://www.acmicpc.net/problem/1300>


접근
--


1. N이 최대 105이기 때문에 N x N 배열을 만들어서 풀면 1010이 소요되어 시간 초과로 해결할 수 없다.
2. `i <= k`에 대하여 `B[i] <= k`가 성립한다.
3. k번째 수를 이분 탐색해서 `mid` 값보다 작거나 같은 수의 개수를 찾고 k개인지 확인한다.


풀이
--



```python
from sys import stdin


def get_cnt(mid):
    cnt = 0
    for i in range(1, n + 1):
        cnt += min(mid // i, n) # (1)

    return cnt


def binary_search(start, end):
    while start <= end:
        mid = (start + end) // 2

        if get_cnt(mid) < k:
            start = mid + 1
        else:
            end = mid - 1 # (2)

    return start


n, k = int(stdin.readline()), int(stdin.readline())
print(binary_search(1, k)) # (3)
```


* (1) n = 3이면 A는 아래와 같다.



| - | - | - |
| --- | --- | --- |
| 1 | 2 | 3 |
| 2 | 4 | 6 |
| 3 | 6 | 9 |

i는 각 행을 의미하고 `mid // i`로 i행에서 mid보다 작은 개수를 구할 수 있다. 개수가 n보다 클 수 없기 때문에 n과 비교해서 작은 값을 더한다.
* (2) k보다 크거나 같을 때 end를 좁히기 때문에 조건을 만족하는 가장 큰 수를 찾을 수 있다.
* (3) k번째 수는 항상 k보다 작거나 같기 때문에 탐색 범위를 1 ~ k로 잡는다.
