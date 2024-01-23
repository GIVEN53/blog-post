[Baekjoon-Python] 17143 : 낚시왕
=
<https://www.acmicpc.net/problem/17143>


접근
--


1. 격자의 열 크기(C)가 5라면 상어가 이동할 때 인덱스(c)는 `0, 1, 2, 3, 4, 3, 2, 1, ...`이 된다.
2. 상어가 움직일 때 인덱스에 사이클이 발생한다. 사이클 길이는 `2 * (C - 1)`이다.
3. 상어의 이동 후 인덱스를 중복없이 한 번에 찾도록 최적화해야 시간 초과가 발생하지 않는다.
4. 열, 오른쪽 방향 기준으로 상어의 이동 후 인덱스는 `(현재 인덱스 + 속력) % 열 사이클 길이`  
즉, `(c + s) % (2 * (C - 1))`이다.


풀이
--



```python
from sys import stdin


def catch(j):
    for i in range(R): # (1)
        if (i, j) in sharks:
            return sharks.pop((i, j))[2] # (2)
    return 0


def move():
    tmp_sharks = {}
    for (r, c), (s, d, z) in sharks.items():
        nr, nc, d = get_next_location(r, c, s, d) # (3)

        if (nr, nc) in tmp_sharks and tmp_sharks[(nr, nc)][2] > z: # (4)
            continue
        tmp_sharks[(nr, nc)] = (s, d, z) # (5)

    return tmp_sharks


def get_next_location(r, c, s, d):
    if d < 2:
        if d == 0: # (6)
            r = r_cycle - r + s
        else: # (7)
            r += s
        r %= r_cycle
        if r >= R: # (8)
            return r_cycle - r, c, 0
        return r, c, 1
    else:
        if d == 3: # (9)
            c = c_cycle - c + s
        else: # (10)
            c += s
        c %= c_cycle
        if c >= C: # (11)
            return r, c_cycle - c, 3
        return c, s, 2


R, C, M = map(int, stdin.readline().split())
sharks = {}
for _ in range(M):
    r, c, s, d, z = map(int, stdin.readline().split())
    sharks[(r - 1, c - 1)] = (s, d - 1, z)

catch_size = 0
r_cycle = 2 * (R - 1)
c_cycle = 2 * (C - 1)
for j in range(C):
    catch_size += catch(j)
    sharks = move()

print(catch_size)
```


* (1) 열은 낚시왕과 같은 열이고 행만 순회하면서 상어를 찾는다.
* (2) 땅과 제일 가까운 상어를 삭제하고 상어의 사이즈를 리턴한다.
* (3) 상어가 이동 후 위치를 가져온다.
* (4) 이동 후 위치에 다른 상어가 있고 현재 상어보다 사이즈가 크면 현재 상어가 잡아먹히기 때문에 건너뛴다.
* (5) 이동 후 위치에 다른 상어가 없거나 다른 상어가 있지만 현재 상어의 사이즈가 더 크면 현재 상어를 저장한다.
* (6) 위쪽 방향일 때 `r = (r_cycle - r + s) % r_cycle`
* (7) 아래쪽 방향일 때 `r = (r + s) % r_cycle`
* (8) 범위를 벗어났을 경우 `r = r_cycle - r`이고 방향은 위쪽이 된다.
* (9) 왼쪽 방향일 때 `c = (c_cycle - c + s) % c_cycle`
* (10) 오른쪽 방향일 때 `c = (c + s) % c_cycle`
* (11) 범위를 벗어났을 경우 `c = c_cycle - c`이고 방향은 왼쪽이 된다.


### 예시


격자의 열 크기(C) = 5, 상어의 인덱스(c) = 2, 속력(s) = 9이라고 가정한다.  
사이클의 길이는 `2 * (C - 1) = 8`이 된다.


![](https://blog.kakaocdn.net/dn/bv72Ai/btsDJkHn9f0/SqwG2tGQWKDFS7bv5go8pk/img.png)


#### 오른쪽 방향일 경우


1. `c + s = 11`이므로 상어는 11번 인덱스에 위치한다.


![](https://blog.kakaocdn.net/dn/N9EQu/btsDLIUNIGu/YZNd26mSGbtBwwdhDlDdK0/img.png)


2. 상어 인덱스를 찾기 위해 사이클 길이로 나눈 나머지를 구한다. `11 % 8 = 3`


![](https://blog.kakaocdn.net/dn/cKYEbj/btsDLr6BYLI/wdpevyJ6kwdQ9k3XIwz6J0/img.png)


#### 왼쪽 방향일 경우


1. 왼쪽 방향은 상어 인덱스가 `4, 3, 2, 1, 0, ...`으로 감소한다. 따라서 `사이클 길이 - c`로 인덱스를 조정한다.


![](https://blog.kakaocdn.net/dn/lq8Xd/btsDQ4pbPPl/gctt0Xk2YpD98q8Ha2jko0/img.png)


2. `c + s = 15`이므로 상어는 15번 인덱스에 위치한다.


![](https://blog.kakaocdn.net/dn/AEHHL/btsDQTH1T2Z/pz0uKOyNvhuHqzfblyRyAk/img.png)


3. 상어 인덱스를 찾기 위해 사이클 길이로 나눈 나머지를 구한다. `15 % 8 = 7`


![](https://blog.kakaocdn.net/dn/ctjHQi/btsDQUAdViJ/aMn9tdYy36DlBw6gWpE9B1/img.png)


4. 격자 범위 밖이기 때문에 `사이클 길이 - c`로 인덱스를 조정한다.


![](https://blog.kakaocdn.net/dn/bmDaoY/btsDQ6UQphx/d6bilCnY1amjNgLXQEBEkK/img.png)

