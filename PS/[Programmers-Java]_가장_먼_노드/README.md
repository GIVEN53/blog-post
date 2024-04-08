[Programmers-Java] 가장 먼 노드
=
<https://school.programmers.co.kr/learn/courses/30/lessons/49189>


접근
--


1. 다익스트라 알고리즘을 사용하여 1번 노드에서 모든 노드까지의 거리를 구한다.


풀이
--



```java
import java.util.*;

class Solution {
    private List[] graph;
    private int[] distances;
    private static final int INF = Integer.MAX_VALUE;

    public int solution(int n, int[][] edge) {
        init(n);
        for (int[] e : edge) {
            graph[e[0]].add(new Node(e[1], 1));
            graph[e[1]].add(new Node(e[0], 1));
        }

        dijkstra();
        int max = 0;
        int cnt = 0;
        for (int dist : distances) { // (1)
            if (dist == INF) {
                continue;
            }
            if (max < dist) {
                max = dist;
                cnt = 1;
            } else if (max == dist) {
                cnt++;
            }
        }
        return cnt;
    }

    private void init(int n) {
        graph = new List[n + 1];
        for (int i = 1; i <= n; i++) {
            graph[i] = new ArrayList<>();
        }

        distances = new int[n + 1];
        Arrays.fill(distances, INF);
        distances[1] = 0;
    }

    private void dijkstra() {
        PriorityQueue pq = new PriorityQueue<>();
        pq.offer(new Node(1, 0));

        while (!pq.isEmpty()) {
            Node now = pq.poll();
            int v = now.vertex;
            int c = now.cost;

            if (distances[v] < c) {
                continue;
            }

            for (Node next : graph[v]) {
                int nextCost = c + next.cost;
                if (nextCost < distances[next.vertex]) {
                    distances[next.vertex] = nextCost;
                    pq.offer(new Node(next.vertex, nextCost));
                }
            }

        }
    }

    class Node implements Comparable {
        int vertex;
        int cost;

        Node(int vertex, int cost) {
            this.vertex = vertex;
            this.cost = cost;
        }

        @Override
        public int compareTo(Node o) {
            return Integer.compare(this.cost, o.cost);
        }
    }
}
```


* (1) 모든 노드까지의 거리를 계산한 후 최대 거리인 노드의 개수를 구한다.
