[Baekjoon-Python] 4948 : 베르트랑 공준
=
<https://www.acmicpc.net/problem/4948>


접근
--


1. boolean 리스트를 선언한다.
2. 소수가 아닌 값은 False 처리한다.
3. n + 1 ~ 2n 인덱스를 슬라이싱하여 True 개수를 구한다.


풀이 1
----



```python
from sys import stdin
from math import sqrt

arr = [True for i in range(123456 * 2 + 1)]
for i in range(2, int(sqrt(123456 * 2)) + 1) : # (1)
  if arr[i] :
    j = 2
    while i * j <= 123456 * 2 : # (2)
      arr[i * j] = False
      j += 1

while True :
  n = int(stdin.readline())
  if n == 0 :
    break

  primes = arr[n + 1 : 2 * n + 1]
  print(primes.count(True))
```


* (1) 제곱근을 기준으로 곱의 대칭이 이루어지므로 제곱근까지만 순회한다.
* (2) `i`에 2부터 곱하면서 False 처리한다.


풀이 2
----



```python
from sys import stdin

def get_prime(num):
    arr = [True] * (num + 1)
    for i in range(2, int(num ** 0.5) + 1) :
      if arr[i] :
        arr[i * 2 :: i] = [False] * (num // i - 1) # (1)
    return arr


arr = get_prime(123456 * 2)
while True :
  n = int(stdin.readline())
  if n == 0 :
    break

  primes = arr[n + 1 : 2 * n + 1]
  print(primes.count(True))
```


* (1) `i * 2`부터 `i` 간격으로 False 처리한다. `i`를 제외한 모든 배수를 선택하므로 `num // i - 1` 개수를 선택한다.
