[Programmers-Java] 코딩 테스트 공부
=
<https://school.programmers.co.kr/learn/courses/30/lessons/118668>


접근
--


1. 초기 알고력, 코딩력과 모든 문제를 풀 수 있는 알고력, 코딩력 중 최댓값을 구한다.
2. 2차원 배열을 생성하여 최댓값까지 알고력과 코딩력을 메모이제이션한다.
3. `dp[알고력][코딩력] = 시간`이고 알고력과 코딩력의 점화식은  
`dp[알고력 + 1][코딩력] = min(dp[알고력 + 1][코딩력], dp[알고력][코딩력] + 1)`  
`dp[알고력][코딩력 + 1] = min(dp[알고력][코딩력 + 1], dp[알고력][코딩력] + 1)`
4. 문제를 풀었을 경우  
`dp[알고력 + alp_rwd][코딩력 + cop_rwd] = min(dp[알고력 + alp_rwd][코딩력 + cop_rwd], dp[알고력][코딩력] + cost)`
5. **문제를 풀었을 때 최대 알고력, 코딩력보다 커질 수 있다.**


풀이
--



```java
import java.util.Arrays;

class Solution {
    public int solution(int alp, int cop, int[][] problems) {
        int maxAlp = alp;
        int maxCop = cop;
        for (int[] problem : problems) { // (1)
            maxAlp = Math.max(maxAlp, problem[0]);
            maxCop = Math.max(maxCop, problem[1]);
        }
        if (alp == maxAlp && cop == maxCop) { // (2)
            return 0;
        }

        int[][] dp = new int[maxAlp + 2][maxCop + 2]; // (3)
        for (int[] d : dp) {
            Arrays.fill(d, Integer.MAX_VALUE);
        }
        dp[alp][cop] = 0;

        for (int i = alp; i < dp.length - 1; i++) { // (4)
            for (int j = cop; j < dp[0].length - 1; j++) {
                dp[i + 1][j] = Math.min(dp[i + 1][j], dp[i][j] + 1); // (5)
                dp[i][j + 1] = Math.min(dp[i][j + 1], dp[i][j] + 1);

                for (int[] problem : problems) { // (6)
                    if (i >= problem[0] && j >= problem[1]) { // (7)
                        int nextAlp = Math.min(i + problem[2], maxAlp);
                        int nextCop = Math.min(j + problem[3], maxCop);

                        dp[nextAlp][nextCop] = Math.min(dp[nextAlp][nextCop], dp[i][j] + problem[4]);
                    }
                }
            }
        }
        return dp[maxAlp][maxCop];
    }
}
```


* (1) 문제의 최대 알고력과 최대 코딩력을 갱신한다.
* (2) 초기 알고력, 코딩력으로 모든 문제를 풀 수 있으면 0을 리턴한다.
* (3) dp는 2차원 배열이고 각각의 인덱스는 알고력과 코딩력이다.
* (4) 초기 알고력, 코딩력부터 순회하면서 공부를 하고 문제를 풀어 다음 알고력, 코딩력 시간을 갱신한다.
* (5) 다음 알고력과 코딩력의 최소 시간을 갱신한다.
* (6) 문제를 순회하면서 현재 알고력, 코딩력으로 문제를 풀 수 있는지 확인한다.
* (7) 문제를 풀었을 때 다음 알고력 또는 코딩력이 최대 알고력 또는 코딩력보다 커질 수 있다. 최대보다 커지더라도 문제를 모두 풀 수 있기 때문에 dp 인덱스 이내로 조정한다.
