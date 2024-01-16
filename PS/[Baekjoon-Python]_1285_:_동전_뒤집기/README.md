[Baekjoon-Python] 1285 : 동전 뒤집기
=
<https://www.acmicpc.net/problem/1285>


접근
--


1. 비트마스크를 적용하기 위해 H = 0, T = 1 이진수로 치환한다.
2. 행 방향으로 뒤집을 수 있는 모든 경우의 수를 구한다.
3. 열 방향으로 탐색하면서 T 개수가 많으면 뒤집는다.


풀이
--



```python
from sys import stdin


N = int(stdin.readline())
coins = []
reverse_coins = []
for _ in range(N):
    i = N - 1
    bit = 0
    for state in stdin.readline().rstrip():
        if state == "T": # (1)
            bit += 1 << i
        i -= 1
    coins.append(bit)
    reverse_coins.append(~bit) # (2)

ans = N**2
for bit in range(1 << N): # (3)
    tmp_coins = []
    for i in range(N): # (4)
        if 1 << i & bit:
            tmp_coins.append(coins[i])
        else:
            tmp_coins.append(reverse_coins[i])

    total_t_cnt = 0
    for i in range(N):
        t_cnt = 0
        for coin in tmp_coins: # (5)
            if 1 << i & coin:
                t_cnt += 1
        total_t_cnt += min(t_cnt, N - t_cnt) # (6)
    ans = min(ans, total_t_cnt)

print(ans)
```


* (1) `T`면 1로 치환한다. `THT`라면 `1 << i` 연산으로 101이 된다.
* (2) 비트를 반전시켜 뒤집은 동전을 저장한다.
* (3) 행 또는 열로 뒤집을 수 있는 경우의 수는 2N이다.
* (4) 비트 연산으로 0이면 행을 뒤집는다. (모든 경우의 수를 구하기 위함)

| bit (N = 3) | 1 << i | 1 << i & bit |
| --- | --- | --- |
| 0: 000 | 001 | 0 |
| 010 | 0 |
| 100 | 0 |
| 1: 001 | 001 | 1 |
| 010 | 0 |
| 100 | 0 |
| 2: 010 | 001 | 0 |
| 010 | 1 |
| 100 | 0 |
| 3: 011 | 001 | 1 |
| 010 | 1 |
| 100 | 0 |
| 4: 100 | 001 | 0 |
| 010 | 0 |
| 100 | 1 |
| 5: 101 | 001 | 1 |
| 010 | 0 |
| 100 | 1 |
| 6: 110 | 001 | 0 |
| 010 | 1 |
| 100 | 1 |
| 7: 111 | 001 | 1 |
| 010 | 1 |
| 100 | 1 |
* (5) 위에서 행을 기준으로 뒤집었기 때문에 열을 기준으로 `T` 개수를 확인한다.
* (6) `N - t_cnt`는 열을 뒤집은 후 `T`의 개수가 된다.
