[Baekjoon-Python] 17779 : 게리맨더링 2
=
<https://www.acmicpc.net/problem/17779>


접근
--


1. x, y 좌표에 따라 경계의 길이 d1, d2를 1씩 증가시키며 경계선을 그린다.
2. 1 ~ 4번 선거구별 인구 수를 구한다.
3. 5번 선거구의 인구 수는 총 인구 수에서 1 ~ 4번 선거구별 인구 수의 합을 뺀다.


풀이
--



```python
from sys import stdin


def get_wards(r, c, d1, d2) -> list:
    wards = [0] * 5
    boundary = draw_boundary(r, c, d1, d2)

    wards[0] = sum_ward(boundary, 0, r + d1, 0, c + 1, 1, 1) # (1)
    wards[1] = sum_ward(boundary, 0, r + d2 + 1, n - 1, c, 1, -1) # (2) 
    wards[2] = sum_ward(boundary, n - 1, r + d1 - 1, 0, c - d1 + d2, -1, 1) # (3)
    wards[3] = sum_ward(boundary, n - 1, r + d2, n - 1, c - d1 + d2 - 1, -1, -1) # (4)
    return wards


def draw_boundary(r, c, d1, d2) -> list:
    boundary = [[0] * n for _ in range(n)]

    for i in range(d1 + 1):
        boundary[r + i][c - i] = 1 # (5)
        boundary[r + i + d2][c - i + d2] = 1 # (6)
    for i in range(d2 + 1):
        visboundaryited[r + i][c + i] = 1 # (7)
        boundary[r + i + d1][c + i - d1] = 1 # (8)

    return boundary


def sum_ward(boundary, r_start, r_end, c_start, c_end, k, j) -> int:
    total = 0
    for r in range(r_start, r_end, k):
        for c in range(c_start, c_end, j):
            if boundary[r][c]:
                break # (9)
            total += city[r][c]
    return total


n = int(stdin.readline())
city = []
total_population = 0
for _ in range(n):
    c = list(map(int, stdin.readline().split()))
    total_population += sum(c) # (10)
    city.append(c)

res = 1e9
for r in range(n - 2):
    for c in range(1, n - 1):
        for d1 in range(1, n):
            if c - d1 < 0:
                continue
            for d2 in range(1, n):
                if r + d1 + d2 > n - 1 or c + d2 > n - 1:
                    continue
                wards = get_wards(r, c, d1, d2)
                wards[4] = total_population - sum(wards) # (11)
                res = min(res, max(wards) - min(wards))

print(res)
```


* (1) 1번 선거구: `(0, 0) ~ (r + d1 - 1, c)`, r 증가, c 증가
* (2) 2번 선거구: `(0, n - 1) ~ (r + d2, c + 1)`, r 증가, c 감소
* (3) 3번 선거구: `(n - 1, 0) ~ (r + d1, c - d1 + d2 - 1)`, r 감소, c 증가
* (4) 4번 선거구: `(n - 1, n - 1) ~ (r + d2 + 1, c - d1 + d2)`, r 감소, c 감소
* (5) 1번 경계선을 그린다.
* (6) 4번 경계선을 그린다.
* (7) 2번 경계선을 그린다.
* (8) 3번 경계선을 그린다.
* (9) 경계선을 만나면 탈출한다. continue일 경우 5번 선거구를 침범한다.
* (10) 총 인구 수를 구한다.
* (11) 5번 선거구는 총 인구 수에서 1, 2, 3, 4번 선거구별 인구 수의 합을 뺀다.
