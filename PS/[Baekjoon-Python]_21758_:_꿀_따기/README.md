[Baekjoon-Python] 21758 : 꿀 따기
=
<https://www.acmicpc.net/problem/21758>


접근
--


1. 꿀의 누적합을 구한다.
2. 벌 또는 벌통은 양 끝에 위치해야 한다.
3. `벌, 벌, 벌통`, `벌, 벌통, 벌`, `벌통, 벌, 벌` 세 가지 경우의 수를 확인하고 최대의 꿀의 양을 구한다.


풀이
--



```python
from sys import stdin


def fly():
    honey_amount = 0
    for i in range(1, n - 1):
        # (1)
        bee_1 = accum_honey[n - 1] - honey[i] - honey[0] # (2)
        bee_2 = accum_honey[n - 1] - accum_honey[i] # (3)
        honey_amount = max(honey_amount, bee_1 + bee_2)

        # (4)
        bee_1 = accum_honey[i] - honey[0] # (5)
        bee_2 = accum_honey[n - 2] - accum_honey[i - 1] # (6)
        honey_amount = max(honey_amount, bee_1 + bee_2)

        # (7)
        bee_1 = accum_honey[i - 1] # (8)
        bee_2 = accum_honey[n - 2] - honey[i] # (9)
        honey_amount = max(honey_amount, bee_1 + bee_2)
    return honey_amount


n = int(stdin.readline())
honey = list(map(int, stdin.readline().split()))
accum_honey = honey[:] 
for i in range(1, n): # (10)
    accum_honey[i] += accum_honey[i - 1]

print(fly())
```


* (1) `벌1 = 0`, `벌2 = i`, `벌통 = n - 1`이다. **벌2**만 움직이면서 최댓값을 확인한다.
* (2) 벌1이 꿀을 딴 양은 `꿀 총합 - 벌1 위치의 꿀 양 - 벌2 위치의 꿀 양`이다.
* (3) 벌2가 꿀을 딴 양은 `꿀 총합 - 벌2 위치까지의 꿀 누적합`이다.
* (4) `벌1 = 0`, `벌통 = i`, `벌2 = n - 1`이다. **벌통**만 움직이면서 최댓값을 확인한다.
* (5) 벌1이 꿀을 딴 양은 `벌통까지의 꿀 누적합 - 벌1 위치의 꿀 양`이다.
* (6) 벌2가 꿀을 딴 양은 `벌2 위치 전까지의 꿀 누적합 - 벌통 전까지의 꿀 누적합`이다.
* (7) `벌통 = 0`, `벌1 = i`, `벌2 = n - 1`이다. **벌1**만 움직이면서 최댓값을 확인한다.
* (8) 벌1이 꿀을 딴 양은 `벌1 위치 전까지의 꿀 누적합`이다.
* (9) 벌2가 꿀을 딴 양은 `벌2 위치 전까지의 꿀 누적합 - 벌1 위치의 꿀 양`이다.
* (10) 꿀의 누적합을 구한다.
