[Baekjoon-Python] 17140 : 이차원 배열과 연산
=
<https://www.acmicpc.net/problem/17140>


접근
--


1. Counter 클래스를 사용하여 등장 횟수를 구한다.
2. C 연산은 열을 행으로 변환해서 정렬하고 다시 열로 변환한다.


풀이
--



```python
from sys import stdin
from collections import Counter


def sort(array):
    res, max_len = [], 0
    for arr in array:
        counter = Counter(arr) # (1)
        counter.pop(0, None) # (2)
        row = sorted(counter.items(), key=lambda x: (x[1], x[0])) # (3)
        row = list(sum(row, ())) # (4)

        if len(row) > 100: # (5)
            row = row[:100]

        max_len = max(max_len, len(row)) # (6)
        res.append(row)

    return fill_zero(max_len, res)


def fill_zero(max_len, res):
    for row in res:
        if len(row) < max_len: # (7)
            row.extend([0] * (max_len - len(row)))

    return res


r, c, k = map(int, stdin.readline().split())
array = [list(map(int, stdin.readline().split())) for _ in range(3)]

sec = 0
while sec < 101:
    row_cnt = len(array)
    col_cnt = len(array[0])
    if row_cnt >= r and col_cnt >= c and array[r - 1][c - 1] == k:
        break

    if row_cnt >= col_cnt: # (8)
        array = sort(array)
    else: # (9)
        res = sort(list(zip(*array)))
        array = list(zip(*res))

    sec += 1

if sec == 101:
    print(-1)
else:
    print(sec)
```


* (1) `{수 : 등장 횟수, ...}`의 dictionary를 생성한다.
* (2) 0인 수는 정렬할 때 제거한다. 0이 없을 때 KeyError 대신 None을 반환하도록 한다.
* (3) 등장 횟수, 수로 오름차순 정렬한 list를 생성한다.
* (4) `[(1, 2), (3, 4), ...]`의 형태이기 때문에 `[1, 2, 3, 4, ...]`으로 변환한다.
* (5) 길이가 100을 넘어가면 슬라이싱한다.
* (6) 행의 최대 길이를 갱신한다.
* (7) 최대 길이보다 작은 행은 차이만큼 0으로 채운다.
* (8) R 연산을 실행한다.
* (9) C 연산을 실행한다. 열을 행으로 변환해서 정렬한 후 다시 열로 변환한다.
