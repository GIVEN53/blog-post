[Programmers-Java] 택배 배달과 수거하기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/150369>


접근
--


1. 마지막 집부터 배달과 수거를 마쳐야 한다.
2. 집을 뒤에서부터 순회하면서 배달과 수거를 마무리할 수 있는 왕복 횟수를 구한다.
3. 왕복하면서 남은 배달 상자 개수, 수거 상자 개수를 앞 집으로 이전한다.


풀이
--



```java
class Solution {
    public long solution(int cap, int n, int[] deliveries, int[] pickups) {
        long answer = 0;

        int d = 0;
        int p = 0;
        for (int i = n - 1; i > -1; i--) { // (1)
            int cnt = 0;
            d -= deliveries[i]; // (2)
            p -= pickups[i];
            while (d < 0 || p < 0) { // (3)
                d += cap;
                p += cap;
                cnt++;
            }

            answer += (i + 1) * 2 * cnt; // (4)
        }

        return answer;
    }
}
```


* (1) 마지막 집부터 순회한다.
* (2) 배달과 수거를 마친다.
* (3) cnt는 물류창고에서 해당 집까지 왕복한 횟수이다. 왕복할 때마다 `cap`개만큼 상자를 더 실을 수 있기 때문에 남은 배달 상자 개수와 수거 상자 개수에 더해준다.
* (4) 왕복한 거리를 구한다.
