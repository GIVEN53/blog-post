[Baekjoon-Python] 1339 : 단어 수학
=
<https://www.acmicpc.net/problem/1339>


접근
--


1. 알파벳마다 `10^자릿수`만큼 더한다.
2. 내림차순으로 정렬하여 9부터 곱하면서 결과에 더한다.


풀이
--



```python
from sys import stdin
from collections import defaultdict

alphabets_dict = defaultdict(int)
for _ in range(int(stdin.readline())) :
  alphabets = stdin.readline().rstrip()
  for j in range(len(alphabets)) :
      alphabets_dict[alphabets[j]] += 10 ** (len(alphabets) - j - 1)

scores = sorted(alphabets_dict.values(), reverse=True)

res = 0
num = 9
for score in scores :
  res += num * score
  num -= 1

print(res)
```


예를 들어 `ABCD`라면 dictionary에는 `{'A' : 1000, 'B' : 100, 'C' : 10, 'D' : 1}`로 저장된다. 이후 `BCDDD`가 주어지면 `{'A' : 1000, 'B' : 10100, 'C' : 1010, 'D' : 112}`이 된다.

