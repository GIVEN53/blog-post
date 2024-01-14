[Baekjoon-Python] 1654 : 랜선 자르기
=
<https://www.acmicpc.net/problem/1654>


접근
--


1. 랜선의 길이는 최대 231 - 1 (int형 최댓값 = 21억)이기 때문에 선형 탐색은 시간 초과가 발생한다.  
log2 (231 - 1) = 약 31이므로 이분 탐색으로 랜선의 길이를 구할 수 있다.
2. `low`를 1, `high`를 가지고 있는 K개의 랜선 중 최대 길이로 설정한다.
3. `low`와 `high`의 중간 값인 `mid`로 랜선을 잘라서 개수가 N보다 크거나 같은지 확인한다. (N개보다 많이 만드는 것도 N개를 만드는 것에 포함)
4. N개를 만들 수 있으면 `low = mid + 1`, 만들 수 없으면 `high = mid - 1`로 설정한다.
5. `low`가 `high`보다 작거나 같을 때까지 반복한다.
6. K개의 랜선 중 최대 길이를 L이라고 할 때, 시간복잡도는 `O(KlogL)`


풀이
--



```python
from sys import stdin

K, N = map(int, stdin.readline().split())
lan_cables = [int(stdin.readline()) for _ in range(K)]

low = 1
high = max(lan_cables)
while low <= high:
    mid = (low + high) // 2
    cnt = sum(length // mid for length in lan_cables) # (1)

    if cnt >= N:
        low = mid + 1
    else:
        high = mid - 1

print(high)
```


* (1) `mid`길이로 자른 총 개수를 구한다.
