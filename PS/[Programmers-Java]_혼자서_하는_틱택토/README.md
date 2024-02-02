[Programmers-Java] 혼자서 하는 틱택토
=
<https://school.programmers.co.kr/learn/courses/30/lessons/160585>


접근
--


1. 행, 열, 대각선의 o와 x의 개수를 센다.
2. 각각의 개수 중 3이 있으면 해당 표시가 승리한다.
3. 게임이 불가능한 경우
	1. o, x 둘 다 승리
	2. o가 승리했지만 o 개수가 x 개수보다 한 개 더 많지 않음
	3. x가 승리했지만 x 개수가 o 개수와 같지 않음
	4. o 개수와 x 개수의 차이가 0 또는 1이 아님


풀이
--



```java
class Solution {
    public int solution(String[] board) {
        int[] o = new int[8]; // (1)
        int[] x = new int[8];
        int oCnt = 0;
        int xCnt = 0;
        for (int i = 0; i < board.length; i++) {
            String[] b = board[i].split("");
            for (int j = 0; j < b.length; j++) {
                if (b[j].equals("O")) {
                    o[i]++;
                    o[3 + j]++;
                    findDiagonal(i, j, o);
                } else if (b[j].equals("X")) {
                    x[i]++;
                    x[3 + j]++;
                    findDiagonal(i, j, x);
                }
            }
            oCnt += o[i];
            xCnt += x[i];
        }

        boolean oWin = isWin(o);
        boolean xWin = isWin(x);
        if (oWin && xWin) { // (2)
            return 0;
        } else if (oWin && oCnt != xCnt + 1) {
            return 0;
        } else if (xWin && oCnt != xCnt) {
            return 0;
        } else if (oCnt > 1 + xCnt || oCnt < xCnt) {
            return 0;
        }
        return 1;
    }

    private void findDiagonal(int i, int j, int[] arr) {
        if (i == 1 && j == 1) { // (3)
            arr[6]++;
            arr[7]++;
        } else if (i == j) { // (4)
            arr[6]++;
        } else if (Math.abs(i - j) == 2) { // (5)
            arr[7]++;
        }
    }

    private boolean isWin(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == 3) { // (6)
                return true;
            }
        }
        return false;
    }
}
```


* (1) 배열의 인덱스는 `0:1행, 1:2행, 2:3행, 3:1열, 4:2열, 5:3열, 6:우하향 대각선, 7:우상향 대각선`에서 해당 표시의 개수를 의미한다.
* (2) 게임이 불가능한 경우를 확인한다.
* (3) `(1, 1)`은 게임판의 가운데이다. 우하향, 우상향 대각선 모두 만들 수 있다.
* (4) `(0, 0)`, `(2, 2)`는 우하향 대각선을 만들 수 있다.
* (5) `(0, 2)`, `(2, 0)`은 우상향 대각선을 만들 수 있다.
* (6) 3개가 같은 표시이면 해당 표시가 승리한다.
