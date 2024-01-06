[Baekjoon-Python] 9020 : 골드바흐의 추측
=
<https://www.acmicpc.net/problem/9020>


접근
--


1. `n`을 2로 나누어 두 개의 숫자로 만든다.
2. 두 수가 소수일 때까지 반복한다.
3. 하나라도 소수가 아니면 1씩 더하고 뺀다.


풀이
--



``` Python
from sys import stdin

def is_prime(num) :
  if num == 1 :
    return False

  for i in range(2, int(num ** 0.5) + 1) : # (1)
    if num % i == 0 :
      return False

  return True


T = int(stdin.readline())
for _ in range(T) :
  n = int(stdin.readline())
  num1, num2 = n // 2, n // 2

  while True :
    if is_prime(num1) and is_prime(num2) :
      print(num1, num2)
      break

    num1 -= 1
    num2 += 1
```


* (1) 제곱근을 기준으로 곱의 대칭이 이루어지므로 제곱근까지만 순회한다.
