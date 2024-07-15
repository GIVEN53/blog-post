[Programmers-Java] 양과 늑대
=
<https://school.programmers.co.kr/learn/courses/30/lessons/92343>


접근
--


1. 트리를 bfs 탐색한다.
2. 비트마스킹으로 중복 경로 탐색을 제거한다.
3. 경로에 포함된 노드의 왼쪽, 오른쪽 자식 노드를 추가해 나간다.


풀이
--



```java
import java.util.*;

class Solution {
    private int n;
    private int[] info;
    private int[] left = new int[17];
    private int[] right = new int[17];
    private boolean[] visited = new boolean[1 << 17];

    public int solution(int[] info, int[][] edges) {
        this.n = info.length;
        this.info = info;

        Arrays.fill(left, -1);
        Arrays.fill(right, -1);
        for (int[] edge : edges) {
            int parent = edge[0];
            int child = edge[1];
            if (left[parent] == -1) { // (1)
                left[parent] = child;
            } else {
                right[parent] = child;
            }
        }

        return bfs(0);
    }

    private int bfs(int start) {
        Queue q = new LinkedList<>();
        q.offer(1 << start);
        int ans = 0;
        while (!q.isEmpty()) {
            int now = q.poll();
            if (visited[now]) { // (2)
                continue;
            }
            visited[now] = true;

            int sheep = 0;
            int wolf = 0;
            for (int i = 0; i < n; i++) { // (3)
                if ((1 << i & now) == 0) {
                    continue;
                }

                if (info[i] == 0) {
                    sheep++;
                } else {
                    wolf++;
                }
            }
            if (sheep <= wolf) { // (4) 
                continue;
            }
            ans = Math.max(ans, sheep); // (5)

            for (int i = 0; i < n; i++) { // (6)
                if ((1 << i & now) == 0) {
                    continue;
                }
                if (left[i] != -1) {
                    q.offer(1 << left[i] | now);
                }
                if (right[i] != -1) {
                    q.offer(1 << right[i] | now);
                }
            }
        }
        return ans;
    }
}
```


* (1\) 부모 노드의 왼쪽 자식 노드와 오른쪽 자식 노드를 저장한다.
* (2\) 이미 방문한 경로는 건너뛴다.
* (3\) 현재 경로를 지나온 노드의 양, 늑대 마릿수를 구한다.
* (4\) 양이 늑대에게 모두 잡아먹히는 경로이기 때문에 더 이상 탐색하지 않는다.
* (5\) 양의 최대 마릿수를 갱신한다.
* (6\) 현재 경로를 지나온 노드의 왼쪽 자식 노드와 오른쪽 자식 노드를 추가해서 큐에 삽입한다.
