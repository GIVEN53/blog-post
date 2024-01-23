[Baekjoon-Python] 20056 : 마법사 상어와 파이어볼
=
<https://www.acmicpc.net/problem/20056>


접근
--


1. 행, 열의 양 끝이 연결되어 있기 때문에 이동한 `(r, c)`는 N으로 나눈 나머지로 구한다.
2. 이동 후 파이어볼이 2개 이상 있는 칸은 모든 파이어볼의 질량과 속력을 합한다.
3. 합쳐진 파이어볼을 4개로 나누고 질량이 0이면 소멸한다.


풀이
--



```python
from sys import stdin


def move() -> dict: # (1)
    moved_grid = {}
    for (r, c), fire_balls in grid.items():
        for m, s, d in fire_balls:
            nr = (r + direction[d][0] * s) % N
            nc = (c + direction[d][1] * s) % N

            if (nr, nc) in moved_grid:
                moved_grid[(nr, nc)].append((m, s, d))
            else:
                moved_grid[(nr, nc)] = [(m, s, d)]
    return moved_grid


def add_fire_ball() -> list: # (2)
    added_result = []
    for (r, c), fire_balls in grid.items():
        if len(fire_balls) < 2:
            continue
        mass = speed = 0
        odd = even = len(fire_balls)
        for m, s, d in fire_balls:
            mass += m
            speed += s
            if d % 2 == 0: # (3)
                even -= 1
            else:
                odd -= 1
        mass //= 5
        speed //= len(fire_balls)
        if even == 0 or odd == 0:
            added_result.append(((r, c), mass, speed, [0, 2, 4, 6]))
        else:
            added_result.append(((r, c), mass, speed, [1, 3, 5, 7]))

    return added_result


def devide_fire_ball(added_result: list): # (4)
    for (r, c), per_mass, per_speed, direction in added_result:
        grid[(r, c)] = []
        if per_mass == 0:  # (5)
            continue
        for d in direction:
            grid[(r, c)].append((per_mass, per_speed, d))


def get_total_mass(): # (6)
    total_mass = 0
    for _, fire_balls in grid.items():
        for m, _, _ in fire_balls:
            total_mass += m

    return total_mass


N, M, K = map(int, stdin.readline().split())
grid = {}
for _ in range(M):
    r, c, m, s, d = map(int, stdin.readline().split())
    grid[(r - 1, c - 1)] = [(m, s, d)]

direction = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
while K:
    K -= 1
    grid = move()
    added_result = add_fire_ball()
    devide_fire_ball(added_result)

print(get_total_mass())
```


* (1) 파이어볼을 이동한다.
* (2) 파이어볼을 합친다.
* (3) 파이어볼 방향이 홀수인지 짝수인지 확인한다.
* (4) 파이어볼을 4개로 나눈다.
* (5) 파이어볼 한 개당 질량이 0이면 소멸한다.
* (6) 남아있는 파이어볼 질량의 합을 구한다.
