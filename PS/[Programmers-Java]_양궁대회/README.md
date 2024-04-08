[Programmers-Java] 양궁대회
=
<https://school.programmers.co.kr/learn/courses/30/lessons/92342>


접근
--


1. 라이언의 화살을 dfs 탐색한다.
2. 과녁에 맞췄지만 어피치보다 개수가 적어서 점수를 얻지 못하는 경우도 탐색해야 한다.
3. 어피치의 총 점수를 구하고 라이언의 점수를 빼 나간다.


풀이
--



```java
import java.util.*;

class Solution {
    private int[] ryan = new int[11];
    private int[] apeach;
    private List candidates = new ArrayList<>();
    private int maxDiff;

    public int[] solution(int n, int[] info) {
        this.apeach = info;
        dfs(n, 0, -getApeachScore());

        if (maxDiff == 0) {
            return new int[] {-1};
        }
        return selectRyan();
    }

    private int getApeachScore() { // (1)
        int score = 0;
        for (int i = 0; i < 11; i++) {
            if (apeach[i] > 0) {
                score += 10 - i;
            }
        }
        return score;
    }

    private void dfs(int arrow, int i, int scoreDiff) {
        if (arrow == 0) { // (2)
            registerCandidate(scoreDiff);
            return;
        }
        if (i == 11) { // (3)
            return;
        }

        for (int cnt = apeach[i] + 1; cnt > -1; cnt--) { // (4)
            ryan[i] = cnt;
            dfs(arrow - cnt, i + 1, calculateScoreDiff(i, scoreDiff));
            ryan[i] = 0;
        }
    }

    private int calculateScoreDiff(int i, int prevScoreDiff) {
        if (ryan[i] <= apeach[i]) { // (5)
            return prevScoreDiff;
        }
        if (apeach[i] == 0) { // (6)
            return prevScoreDiff + (10 - i);
        }
        return prevScoreDiff + (10 - i) * 2; // (7)
    }

    private void registerCandidate(int scoreDiff) { // (8)
        if (scoreDiff < maxDiff) {
            return;
        }

        if (scoreDiff > maxDiff) {
            maxDiff = scoreDiff;
            candidates.clear();
        }
        candidates.add(ryan.clone());
    }

    private int[] selectRyan() { // (9)
        for (int i = 10; i > -1; i--) {
            if (candidates.size() == 1) {
                break;
            }

            int maxArrow = 0;
            List tmp = new ArrayList<>();
            for (int[] candidate : candidates) {
                if (candidate[i] > maxArrow) {
                    maxArrow = candidate[i];
                    tmp.clear();
                    tmp.add(candidate);
                } else if (candidate[i] == maxArrow) {
                    tmp.add(candidate);
                }
            }
            candidates = tmp;
        }
        return candidates.get(0);
    }
}
```


* (1) 어피치의 총 점수를 계산한다.
* (2) 화살을 모두 소비했을 경우 후보 과녁 결과를 저장한다.
* (3) 과녁을 벗어났을 경우 리턴한다.
* (4) 라이언이 i번째 과녁에서 점수를 얻으려면 어피치보다 한 발을 더 맞춰야 한다. 따라서 어치피의 화살 개수 + 1부터 시작한다.
* (5) 어피치가 점수를 얻는 경우이면 이전 점수 차이를 그대로 리턴한다.
* (6) 어피치 점수가 0이면 이전 점수 차이에 라이언의 점수만 더한다.
* (7) 나머지는 어피치가 점수를 잃고 라이언이 점수를 얻는 경우이기 때문에 이전 점수 차이에 라이언의 점수 \* 2를 더한다.
* (8) 최대 점수 차이를 갱신하고 후보 과녁 결과를 저장한다.
* (9) 0점 과녁부터 순회하면서 가장 낮은 점수를 더 많이 맞힌 개수를 기준으로 정렬하여 첫 번째 과녁 결과를 리턴한다.
