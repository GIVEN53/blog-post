[Programmers-Java] 가장 큰 정사각형 찾기
=
<p><a href="https://school.programmers.co.kr/learn/courses/30/lessons/12905">https://school.programmers.co.kr/learn/courses/30/lessons/12905</a></p>
<h2>접근</h2>
<ol>
<li>행 + 1, 열 + 1 크기의 배열을 생성한다.</li>
<li>표에서 1이면 좌, 상, 좌상의 정사각형을 확인하고 그 중 최솟값 + 1을 계산한다.</li>
<li>정사각형의 한 변의 길이를 메모이제이션한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="java">class Solution {
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

 return maxSide \* maxSide;
 }
}</code></pre>
<ul>
<li>(1) 좌, 상, 좌상의 dp 값 중 최솟값에 1을 더한다.</li>
<li>(2) 정사각형의 한 변의 길이의 최댓값을 갱신한다.</li>
</ul>
<h3>예시</h3>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/cEKtTO/btsDRmSscuI/weBEdYcDLwFjPSOKrgPyP1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/cEKtTO/btsDRmSscuI/weBEdYcDLwFjPSOKrgPyP1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcEKtTO%2FbtsDRmSscuI%2FweBEdYcDLwFjPSOKrgPyP1%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
<br>위와 같은 board가 있다.<br><br></p>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/biOA0o/btsDXbuO8p0/BViHPNxKYJgevCYIqK0tDK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/biOA0o/btsDXbuO8p0/BViHPNxKYJgevCYIqK0tDK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbiOA0o%2FbtsDXbuO8p0%2FBViHPNxKYJgevCYIqK0tDK%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
<br>board 값이 1이면 좌, 상, 좌상의 dp 값 중 최솟값 + 1을 저장한다.<br><br></p>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/cZjQqZ/btsDRIgEVtt/FMnnjq1kOOg60P4zUGwAVK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/cZjQqZ/btsDRIgEVtt/FMnnjq1kOOg60P4zUGwAVK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcZjQqZ%2FbtsDRIgEVtt%2FFMnnjq1kOOg60P4zUGwAVK%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
<br>순회가 끝나면 dp는 위와 같고, 가장 큰 정사각형의 한 변의 길이는 3이 된다.</p>