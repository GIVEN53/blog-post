[Baekjoon-Python] 1107 : 리모컨
=
<https://www.acmicpc.net/problem/1107>


접근
--


1. 최대로 버튼을 누른 횟수는 + 또는 - 버튼만 사용한 횟수이다.
2. 숫자 버튼을 눌러 어떤 채널로 이동한 후 + 또는 - 버튼으로 이동하려는 채널에 도달할 수 있다.
3. 채널은 무한대이기 때문에 탈출 조건이 없으면 무한 루프에 빠진다.


풀이
--



```python
from sys import stdin


def check_button(limit, next):
    move_cnt = res
    channel = 100
    while channel != limit:
        for num in str(channel):
            if num in broken: # (1)
                break
        else:
            move_cnt = min(move_cnt, len(str(channel)) + abs(channel - n)) # (2)
        channel += next
    return move_cnt


n, m = int(stdin.readline()), int(stdin.readline())
broken = set(stdin.readline().split())

res = abs(n - 100) # (3)
if n == 100: # (4)
    print(0)
elif m == 0: # (5)
    print(min(res, len(str(n))))
elif m == 10: # (6)
    print(res)
else:
    if 100 < n:
        print(min(res, check_button(999894, 1))) # (7)
    else:
        print(min(res, check_button(-1, -1)))
```


* (1) 고장난 숫자가 포함되어 있을 경우 탈출하여 최솟값을 갱신하지 않는다.
* (2) 고장난 숫자가 포함되어 있지 않을 경우 버튼 횟수의 최솟값을 갱신한다.
* (3) + 또는 - 버튼으로만 누른 횟수를 기준으로 한다.
* (4) 현재 채널과 같을 경우 0이다.
* (5) 고장난 버튼이 없을 경우 + 또는 -버튼만 누르거나 숫자 버튼만 누른 경우 중에서 최솟값이다.
* (6) 0에서 9까지 모든 버튼이 고장났을 경우 + 또는 -버튼만 사용한 횟수이다.
* (7) 채널은 무한이기 때문에 탈출 조건을 두어야 한다. 이동하려는 채널은 최대 `500,000` 채널이고, 최대로 버튼을 누른 횟수는 `100` 채널에서 +버튼만 사용한 499,900이다.  
 반대로 채널 이동 후 -버튼으로 `500,000` 채널에 도달할 수 있다. 숫자 버튼을 누른 횟수 6번 포함 `999,894` 채널로 이동해서 499,894번 -버튼을 누르면 되지만, 최대 횟수인 499,900번보다 작아야 하기 때문에 `999,983` 채널까지 반복한다.
