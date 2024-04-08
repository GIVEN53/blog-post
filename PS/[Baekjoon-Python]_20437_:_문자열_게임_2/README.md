[Baekjoon-Python] 20437 : 문자열 게임 2
=
<https://www.acmicpc.net/problem/20437>


접근
--


1. 알파벳의 `ASCII - 97`을 인덱스로 사용한다.
2. 알파벳마다 문자열의 인덱스를 저장한다.
3. 알파벳을 순회하면서 k개 포함하는 인덱스 2개를 찾고, 문자열의 길이를 구한다.
4. 최소 길이, 최대 길이를 갱신한다.


풀이
--



```python
from sys import stdin


def play():
    min_len, max_len = 1e9, 0
    for alpha in alphabet:
        if len(alpha) < k: # (1)
            continue
        for i in range(len(alpha) - k + 1): 
            length = alpha[i + k - 1] - alpha[i] + 1 # (2)
            if length < min_len:
                min_len = length
            if length > max_len:
                max_len = length
    if max_len == 0: # (3)
        print(-1)
    else:
        print(min_len, max_len)


t = int(stdin.readline())
for _ in range(t):
    w, k = stdin.readline().rstrip(), int(stdin.readline())
    alphabet = [[] for _ in range(26)] # (4)
    for j, word in enumerate(w):
        i = ord(word) - 97
        alphabet[i].append(j)
    play()
```


* (1) k개보다 적은 알파벳은 건너뛴다.
* (2) 해당 알파벳이 k개 포함하는 문자열 길이를 구한다.
* (3) 알파벳이 전부 k보다 개수가 적을 경우 최대 길이 또는 최소 길이는 갱신되지 않는다.
* (4) `a: 0 ~ z: 25`로 인덱스를 지정하고 알파벳마다 문자열의 인덱스를 저장한다.
