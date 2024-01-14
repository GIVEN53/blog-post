[Baekjoon-Python] 2805 : 나무 자르기
=
<https://www.acmicpc.net/problem/2805>


접근
--


1. 나무 높이는 최대 10억이므로 이분 탐색으로 높이를 구해야 한다.
2. `low`를 1, `high`를 N개의 나무 중 최대 길이로 설정한다.
3. `low`와 `high`의 중간 값인 `mid`로 나무를 잘라서 M보다 크거나 같은지 확인한다.
4. M미터를 만들 수 있으면 low = mid + 1, 만들 수 없으면 high = mid - 1로 설정한다.
5. low가 high보다 작거나 같을 때까지 반복한다.
6. N개의 나무 중 최대 높이를 L이라고 할 때, 시간복잡도는 `O(NlogL)`


풀이
--



```python
from sys import stdin
from collections import Counter

_, M = map(int, stdin.readline().split())
trees = Counter(map(int, stdin.readline().split())) # (1)

low = 1
high = max(trees)
while low <= high:
    mid = (low + high) // 2
    cutting_height = sum((i - mid) * cnt for i, cnt in trees.items() if i > mid)

    if cutting_height >= M:
        low = mid + 1
    else:
        high = mid - 1

print(high)
```


* (1) 중복된 나무 개수를 구하기 위해 Counter 클래스를 사용한다. key는 나무 높이, value는 데이터의 개수가 저장된다.
