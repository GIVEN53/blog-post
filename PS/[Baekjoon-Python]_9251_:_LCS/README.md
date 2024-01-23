[Baekjoon-Python] 9251 : LCS
=
<https://www.acmicpc.net/problem/9251>


접근
--


1. 첫 번째 문자열의 알파벳을 두 번째 문자열과 비교하면서 공통 부분 수열 길이를 메모이제이션한다.


풀이
--



```python
from sys import stdin

letter_1 = stdin.readline().rstrip()
letter_2 = stdin.readline().rstrip()
dp = [0] * len(letter_2)
for let_1 in letter_1:
    cnt = 0 # (1)
    for i, let_2 in enumerate(letter_2):
        if dp[i] > cnt: # (2)
            cnt = dp[i]
        elif let_1 == let_2: # (3)
            dp[i] = cnt + 1

print(max(dp))
```


* (1) cnt는 전 인덱스까지의 공통 부분 수열 길이이다.
* (2) dp 값이 더 크면 cnt를 변경한다.
* (3) 두 알파벳이 같으면 1을 더한 값을 dp에 저장한다.


### 예시


`ACAYKP`, `CAPCAK` 두 문자열이 있다.


1. 첫 알파벳이기 때문에 cnt는 증가하지 않는다. 첫 번째, 두 번째 A는 1이 된다.


![](https://blog.kakaocdn.net/dn/wAFje/btsDRHHfleP/lgdHASqzZNxigYJ0y3mDx1/img.png)


2. cnt는 첫 번째 A에서 1이 되어 두 번째 C는 2가 된다.


![](https://blog.kakaocdn.net/dn/ng3uX/btsDKRdkBS2/bodCFKXmonpE0wlTTkVMA0/img.png)


3. cnt는 첫 번째 C에서 1이 되어 첫 번째 A는 2, 두 번째 C에서 2가 되어 두 번째 A는 3이 된다.


![](https://blog.kakaocdn.net/dn/mDcFz/btsDJVtKai7/Oo2yQf8NKrMsLm6K6lqpY1/img.png)


4. Y는 같은 알파벳이 없다.


![](https://blog.kakaocdn.net/dn/l7zap/btsDQ70uzX1/tWBQ6aRJe79CFqOuRwbRg1/img.png)


5. cnt는 두 번째 A에서 3이 되어 K는 4가 된다.


![](https://blog.kakaocdn.net/dn/byCQvV/btsDRlEgCTO/iI1W8lxRJ8bOzONXPwW8Tk/img.png)


6. cnt는 첫 번째 A에서 2가 되어 P는 3이 된다.


![](https://blog.kakaocdn.net/dn/bXTE1b/btsDJUVVUsb/CVomtjjwgu8KlblrccLA6K/img.png)

