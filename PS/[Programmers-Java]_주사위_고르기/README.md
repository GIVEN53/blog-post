[Programmers-Java] 주사위 고르기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/258709>


접근
--


1. n은 최대 10이다.
2. n개의 주사위 중 `n / 2`개를 뽑는 조합 nCn/2 \= 252
3. 뽑은 `n / 2`개의 주사위로 얻을 수 있는 점수의 개수 6n/2 \= 7,776
4. A와 B의 점수를 비교하여 나올 수 있는 승패 결과의 개수 7,7762 \= 6n \= 60,466,176
5. `252 * 60,466,176 = 약 152억`이기 때문에 시간복잡도를 줄여야 한다.
6. A가 몇 번 이기는지를 이분 탐색으로 구하면 `252 * 7,776 * log7,776 = 약 25,474,176`으로 시간 내에 해결할 수 있다.


풀이
--



```java
import java.util.*;

class Solution {
    private int n;
    private List diceComb = new ArrayList<>();

    public int[] solution(int[][] dice) {
        this.n = dice.length;
        combineDice(0, 0, new int[n / 2]); // (1)

        int[] answer = {};
        int maxWinCnt = 0;
        for (int[] aComb : diceComb) {
            List aScores = new ArrayList<>();
            combineScores(0, 0, aComb, aScores, dice); // (2)
            Collections.sort(aScores);

            int[] bComb = getBComb(aComb);
            List bScores = new ArrayList<>();
            combineScores(0, 0, bComb, bScores, dice); // (3)
            Collections.sort(bScores);

            int winCnt = getWinCntOfA(aScores, bScores); // (4)
            if (maxWinCnt < winCnt) {
                maxWinCnt = winCnt;
                answer = aComb;
            }
        }

        for (int i = 0; i < answer.length; i++) {
            answer[i]++; // (5)
        }
        return answer;
    }

    private void combineDice(int start, int cnt, int[] numbers) { 
        if (cnt == n / 2) { // (6)
            diceComb.add(numbers.clone());
            return;
        }

        for (int i = start; i < n; i++) {
            numbers[cnt] = i;
            combineDice(i + 1, cnt + 1, numbers);
        }
    }

    private int[] getBComb(int[] aComb) { // (7)
        boolean[] isA = new boolean[n];
        for (int num : aComb) {
            isA[num] = true; // (8)
        }

        int b = 0;
        int[] bComb = new int[n / 2];
        for (int i = 0; i < n; i++) {
            if (!isA[i]) {
                bComb[b] = i;
                b++;
            }
        }

        return bComb;
    }

    private void combineScores(int cnt, int sum, int[] comb, List scores, int[][] dice) {
        if (cnt == n / 2) { // (9)
            scores.add(sum);
            return;
        }

        for (int i = 0; i < 6; i++) {
            combineScores(cnt + 1, sum + dice[comb[cnt]][i], comb, scores, dice);
        }
    }

    private int getWinCntOfA(List aScores, List bScores) {
        int winCnt = 0;
        for (int s : aScores) { // (10)
            int start = 0;
            int end = bScores.size() - 1;
            while (start <= end) {
                int mid = (start + end) / 2;

                if (s > bScores.get(mid)) {
                    start = mid + 1;
                } else {
                    end = mid - 1;
                }
            }
            winCnt += start;
        }
        return winCnt;
    }
}
```


* (1\) `n / 2`개의 주사위를 선택하는 조합을 구한다.
* (2\) A의 주사위로 얻을 수 있는 점수를 구한다.
* (3\) B의 주사위로 얻을 수 있는 점수를 구한다.
* (4\) A의 몇 번 이기는지 구한다.
* (5\) 현재 주사위 번호가 0부터 시작하기 때문에 1씩 더해준다.
* (6\) `n / 2`개의 주사위를 모두 골랐을 경우 주사위 번호 조합을 리스트에 추가한다.
* (7\) B가 가져간 나머지 `n / 2`개의 주사위 번호를 가져온다.
* (8\) A가 가져간 주사위 번호를 true 처리한다.
* (9\) `n / 2`개의 주사위를 모두 굴렸을 경우 나오는 점수를 리스트에 추가한다.
* (10\) 이분 탐색하여 A의 점수로 이길 수 있는 B의 점수의 개수를 구한다.
