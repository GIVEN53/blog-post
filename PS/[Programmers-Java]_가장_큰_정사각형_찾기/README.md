[Programmers-Java] 가장 큰 정사각형 찾기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/12905>


접근
--


1. 행 + 1, 열 + 1 크기의 배열을 생성한다.
2. 표에서 1이면 좌, 상, 좌상의 정사각형을 확인하고 그 중 최솟값 + 1을 계산한다.
3. 정사각형의 한 변의 길이를 메모이제이션한다.


풀이
--



```java
class Solution {
    public int solution(int[][] board) {
        int row = board.length + 1;
        int col = board[0].length + 1;

        int maxSide = 0;
        int[][] dp = new int[row][col];
        for (int r = 1; r < row; r++) {
            for (int c = 1; c < col; c++) {
                if (board[r - 1][c - 1] == 1) {
                    dp[r][c] = Math.min(dp[r][c - 1], Math.min(dp[r - 1][c], dp[r - 1][c - 1])) + 1; // (1)
                    maxSide = Math.max(maxSide, dp[r][c]); // (2)
                }
            }
        }

        return maxSide * maxSide;
    }
}
```


* (1) 좌, 상, 좌상의 dp 값 중 최솟값에 1을 더한다.
* (2) 정사각형의 한 변의 길이의 최댓값을 갱신한다.


### 예시


![](https://blog.kakaocdn.net/dn/cEKtTO/btsDRmSscuI/weBEdYcDLwFjPSOKrgPyP1/img.png)  
위와 같은 board가 있다.  
  



![](https://blog.kakaocdn.net/dn/biOA0o/btsDXbuO8p0/BViHPNxKYJgevCYIqK0tDK/img.png)  
board 값이 1이면 좌, 상, 좌상의 dp 값 중 최솟값 + 1을 저장한다.  
  



![](https://blog.kakaocdn.net/dn/cZjQqZ/btsDRIgEVtt/FMnnjq1kOOg60P4zUGwAVK/img.png)  
순회가 끝나면 dp는 위와 같고, 가장 큰 정사각형의 한 변의 길이는 3이 된다.

