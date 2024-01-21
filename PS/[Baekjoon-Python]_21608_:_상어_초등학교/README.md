[Baekjoon-Python] 21608 : 상어 초등학교
=
<https://www.acmicpc.net/problem/21608>


접근
--


1. 입력받은 학생 번호 순서로 자리를 지정한다.
2. 교실을 순회하면서 상하좌우를 확인한다.
3. 상하좌우에 좋아하는 학생이 가장 많은 자리를 찾는다.
4. 좋아하는 학생이 가장 많은 자리가 여러 개이면 상하좌우에 빈 칸이 많은 자리를 찾는다.
5. 행, 열을 오름차순으로 순회하기 때문에 빈 칸이 많은 자리가 여러 개여도 가장 먼저 찾은 자리가 행, 열 번호가 가장 작다.


풀이
--



```python
from sys import stdin


def sit(my_favorite):
    now_r = now_c = -1
    max_my_favorite_cnt = max_blank_cnt = 0
    for r in range(n):
        for c in range(n):
            if classroom[r][c] != 0:
                continue

            my_favorite_cnt, blank_cnt = 0, 0
            for i in range(4):
                nr, nc = r + direction[i], c + direction[3 - i]
                if is_out_of_range(nr, nc):
                    continue

                if classroom[nr][nc] in my_favorite:
                    my_favorite_cnt += 1
                elif classroom[nr][nc] == 0:
                    blank_cnt += 1

            if my_favorite_cnt > max_my_favorite_cnt: # (1)
                max_my_favorite_cnt = my_favorite_cnt
                max_blank_cnt = blank_cnt
                now_r, now_c = r, c
            elif my_favorite_cnt == max_my_favorite_cnt and blank_cnt > max_blank_cnt: # (2)
                max_blank_cnt = blank_cnt
                now_r, now_c = r, c
            elif now_r == now_c == -1: # (3)
                now_r, now_c = r, c

    return now_r, now_c


def is_out_of_range(r, c):
    return 0 > r or r >= n or 0 > c or c >= n


n = int(stdin.readline())
students = []
my_favorites = [None] * (n**2 + 1)
for _ in range(n**2):
    s, *favorite_students = map(int, stdin.readline().split())
    students.append(s) # (4)
    my_favorites[s] = favorite_students

classroom = [[0] * n for _ in range(n)]
direction = [1, 0, -1, 0]
for s in students: # (5)
    r, c = sit(my_favorites[s])
    classroom[r][c] = s

satisfaction = 0
for r in range(n):
    for c in range(n):
        s = classroom[r][c]
        favorite_cnt = 0
        for i in range(4):
            nr, nc = r + direction[i], c + direction[3 - i]
            if is_out_of_range(nr, nc):
                continue
            if classroom[nr][nc] in my_favorites[s]:
                favorite_cnt += 1

        if favorite_cnt > 0:
            satisfaction += 10 ** (favorite_cnt - 1)

print(satisfaction)
```


* (1) 좋아하는 학생이 가장 많은 자리일 경우 좋아하는 학생 수, 빈 칸 개수의 최댓값을 갱신하고 현재 r, c를 저장한다.
* (2) 좋아하는 학생 수의 최댓값과 같고 빈 칸 개수가 더 많은 자리 경우 빈 칸 개수의 최댓값을 갱신하고 현재 r, c를 저장한다.
* (3) 아무도 앉지 않은 자리일 경우 현재 r, c를 저장한다. 자리를 찾지 못한 학생이 앉게 된다.
* (4) 입력받은 순서대로 자리를 찾기 위해 학생 번호를 순서대로 리스트에 추가한다.
* (5) 학생을 순회하면서 자리를 찾는다.
