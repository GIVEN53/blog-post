[Programmers-Java] 지형 이동
=
<https://school.programmers.co.kr/learn/courses/30/lessons/62050>


접근
--


1. 높이 갭으로 비용을 계산하고 우선순위 큐에 삽입한다.
2. 높이 갭이 `height`보다 작거나 같으면 비용은 0이다.
3. 사다리없이 이동할 수 있는 모든 격자를 탐색한 후 가장 비용이 낮은 다음 노드를 꺼내게 된다.


풀이
--



```java
import java.util.*;

class Solution {
    public int solution(int[][] land, int height) {
        int n = land.length;
        int[] directions = { 1, 0, -1, 0 };

        PriorityQueue pq = new PriorityQueue<>((o1, o2) -> o1.cost - o2.cost); // (1)
        boolean[][] visited = new boolean[n][n];
        pq.offer(new Node(0, 0, 0)); // (2)
        int totalCost = 0;
        while (!pq.isEmpty()) {
            Node now = pq.poll();
            if (visited[now.r][now.c]) {
                continue;
            }
            totalCost += now.cost;
            visited[now.r][now.c] = true; // (3)

            for (int i = 0; i < 4; i++) {
                int nr = now.r + directions[i];
                int nc = now.c + directions[3 - i];

                if (nr < 0 || n <= nr || nc < 0 || n <= nc) {
                    continue;
                }
                int heightGap = Math.abs(land[now.r][now.c] - land[nr][nc]);
                if (heightGap <= height) {
                    pq.offer(new Node(0, nr, nc));
                } else {
                    pq.offer(new Node(heightGap, nr, nc));
                }
            }
        }
        return totalCost;
    }

    class Node {
        final int cost;
        final int r;
        final int c;

        public Node(int cost, int r, int c) {
            this.cost = cost;
            this.r = r;
            this.c = c;
        }
    }
}
```


* (1) 비용이 낮은 순으로 정렬한다.
* (2) `(0, 0)`부터 탐색하지만 시작점을 어디로 잡아도 상관없다.
* (3) 큐에서 처음 꺼낸 노드만 방문 처리하고 비용을 더한다.
	+ `(1, 1)` -> `(1, 2)`의 비용이 5, `(2, 2)` -> `(1, 2)`의 비용이 3이라면 3의 비용만 더하고 5는 무시된다.
