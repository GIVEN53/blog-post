[Programmers-Java] 배달
=
<https://school.programmers.co.kr/learn/courses/30/lessons/12978>


접근
--


1. 다익스트라 알고리즘을 사용하여 1번 마을에서 각 마을에 도착하는 최소 시간을 구한다.
2. K 시간 이하로 도착하는 마을의 개수를 구한다.


풀이
--



```java
import java.util.*;

class Solution {
    private int[][] board;
    private int[] distance;

    public int solution(int N, int[][] road, int K) {
        board = new int[N][N];
        for (int[] r : road) {
            int a = r[0] - 1;
            int b = r[1] - 1;
            int c = r[2];
            if (board[a][b] == 0 || (board[a][b] != 0 && board[a][b] > c)) { // (1)
                board[a][b] = c;
                board[b][a] = c;
            }
        }
        distance = new int[N];
        Arrays.fill(distance, (int) 1e9);
        distance[0] = 0;
        dijkstra(new int[] {0, 0}, N, K);

        return (int) Arrays.stream(distance)
                .filter(d -> d <= K)
                .count();
    }

    private void dijkstra(int[] start, int N, int K) {
        PriorityQueue q = new PriorityQueue<>((a, b) -> a[0] - b[0]);
        q.offer(start);

        while (!q.isEmpty()) {
            int[] now = q.poll();
            int city = now[0];
            int time = now[1];

            for (int i = 0; i < N; i++) {
                int nextTime = time + board[city][i];
                if (nextTime > K || board[city][i] == 0) {
                    continue;
                }
                if (nextTime < distance[i]) {
                    distance[i] = nextTime;
                    q.offer(new int[] {i, nextTime});
                }
            }
        }
    }
}
```


* (1) 도로가 여러 개 존재할 수 있기 때문에 최솟값을 저장한다.
