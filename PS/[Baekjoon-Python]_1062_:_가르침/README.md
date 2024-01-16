[Baekjoon-Python] 1062 : 가르침
=
<https://www.acmicpc.net/problem/1062>


접근
--


1. 비트마스크를 적용하기 위해 알파벳을 아스키코드 - 97로 치환한다.
2. "anta", "tica"를 구성하는 `a, c, i, n, t`도 K개에 포함된다.
3. 알파벳을 K개 조합해서 비트 연산으로 단어를 몇 개 읽을 수 있는지 계산한다.


풀이
--



```python
from sys import stdin
from itertools import combinations

n, k = map(int, stdin.readline().split())
if k < 5: # (1)
    print(0)
elif k == 26: # (2)
    print(n)
else:
    k -= 5 # (3)
    no_learned = set()
    words = []
    for _ in range(n):
        w = 0
        for i in set(stdin.readline().rstrip()) - {"a", "c", "i", "n", "t"}:
            alphabet = 1 << ord(i) - 97 # (4)
            w |= alphabet
            no_learned.add(alphabet)
        words.append(w)

    if len(no_learned) <= k: # (5)
        print(n)
    else:
        ans = 0
        for comb in combinations(no_learned, k): # (6)
            tmp = 0
            for c in comb:
                tmp |= c

            cnt = 0
            for word in words:
                if word & tmp == word: # (7)
                    cnt += 1
            ans = max(ans, cnt)
        print(ans)
```


* (1) K가 5보다 작으면 모든 단어를 읽을 수 없다.
* (2) K가 26이면 모든 알파벳을 배웠기 때문에 모든 단어를 읽을 수 있다.
* (3) `a, c, i, n, t`는 중복되기 때문에 제외한다.
* (4) 알파벳의 아스키코드 - 97만큼 시프트 연산한다. `a = 1 << 0` ~ `z = 1 << 25`가 된다.
* (5) 단어에 포함된 알파벳 개수가 K개 이하면 모든 단어를 읽을 수 있다.
* (6) 조합으로 알파벳에서 K개를 선택한다.
* (7) 선택한 알파벳으로 읽을 수 있는 단어 개수를 계산한다.
