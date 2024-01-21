[Baekjoon-Python] 15685 : 드래곤 커브
=
<https://www.acmicpc.net/problem/15685>


접근
--


1. `0:우, 1:상, 2:좌, 3:하`로 방향 인덱스를 정한다.
2. `k`세대 드래곤 커브의 방향은 `k - 1`세대 드래곤 커브의 방향을 역순으로 순회하면서 1씩 증가한다.


풀이
--



```python
from sys import stdin

dragon = [[False] * 101 for _ in range(101)]
direction = [(0, 1), (-1, 0), (0, -1), (1, 0)]
for _ in range(int(stdin.readline())):
    x, y, d, g = map(int, stdin.readline().split())

    dragon[y][x] = True # (1)
    y += direction[d][0]
    x += direction[d][1]
    dragon[y][x] = True # (2)

    dir = [d]
    for _ in range(g): # (3)
        for i in range(len(dir) - 1, -1, -1): # (4)
            next_d = (dir[i] + 1) % 4
            y += direction[next_d][0]
            x += direction[next_d][1]
            dir.append(next_d)
            dragon[y][x] = True

square_cnt = 0
for i in range(100):
    for j in range(100):
        if (dragon[i][j] and dragon[i][j + 1] and dragon[i + 1][j] and dragon[i + 1][j + 1]):
            square_cnt += 1

print(square_cnt)
```


* (1) 드래곤 커브의 시작점을 방문 처리한다.
* (2) 0세대 드래곤 커브의 끝점을 방문 처리한다.
* (3) 세대만큼 반복한다.
* (4) 이전 세대의 방향을 역순으로 순회하면서 다음 방향으로 이동하고, 방향을 리스트에 추가한다.  
 `d = 0`일 때



| 세대 | 방향 |
| --- | --- |
| 0 | [0] |
| 1 | [0, 1] |
| 2 | [0, 1, 2, 1] |
| 3 | [0, 1, 2, 1, 2, 3, 2, 1] |
| 4 | [0, 1, 2, 1, 2, 3, 2, 1, 2, 3, 0, 3, 2, 3, 2, 1] |

 3세대에서 4세대가 될 때 추가되는 선분은 3세대의 방향 `0, 1, 2, 1, 2, 3, 2, 1`을 역순으로  
 `1, 2, 3, 2, 1, 2, 1, 0` 순회하면서 다음 방향으로 `2, 3, 0, 3, 2, 3, 2, 1` 이동한 것이다.  
 따라서 4세대의 전체 방향은 `0, 1, 2, 1, 2, 3, 2, 1, 2, 3, 0, 3, 2, 3, 2, 1`이 된다.
