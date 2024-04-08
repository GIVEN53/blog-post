[Programmers-Java] 등산코스 정하기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/118669>


접근
--


1. 출입구의 강도를 0으로 설정한다.
2. 출입구와 연결된 등산로를 우선순위 큐에 삽입하여 탐색한다.
3. 다음 지점의 강도는 현재 지점까지의 강도와 다음 지점과 연결된 등산로의 강도 중 최댓값이다.
4. 산봉우리까지의 모든 코스를 탐색한다. 산봉우리에서 내려오는 것은 생각하지 않는다.  
 예를 들어 `1 (출입구) -> 2 -> 5 (산봉우리)` 코스의 강도가 최솟값이면 해당 코스로 내려오면 된다.
5. 어떤 지점에서 현재 코스의 강도가 이전 코스의 강도보다 크면 현재 코스를 탐색하지 않는다.


풀이
--



```java
import java.util.*;

class Solution {
    private static int MAX = Integer.MAX_VALUE;

    public int[] solution(int n, int[][] paths, int[] gates, int[] summits) {
        Map[] mountain = generateMountain(n, paths);
        boolean[] isSummit = findSummit(n, summits);

        int[] intensity = new int[n + 1];
        Arrays.fill(intensity, MAX);

        PriorityQueue pq = new PriorityQueue<>();
        for (int gate : gates) { // (1)
            intensity[gate] = 0;
            for (int key : mountain[gate].keySet()) {
                pq.offer(new Node(key, mountain[gate].get(key)));
            }
        }

        while (!pq.isEmpty()) {
            Node now = pq.poll();
            if (now.time >= intensity[now.vertex]) { // (2)
                continue;
            }
            intensity[now.vertex] = now.time;
            if (isSummit[now.vertex]) { // (3)
                continue;
            }
            for (int next_vertex : mountain[now.vertex].keySet()) { // (4)
                int next_time = mountain[now.vertex].get(next_vertex);
                pq.offer(new Node(next_vertex, Math.max(now.time, next_time))); // (5)
            }
        }

        Arrays.sort(summits); // (6)
        int[] answer = {0, MAX};
        for (int summit : summits) {
            int time = intensity[summit];
            if (time < answer[1]) {
                answer[0] = summit;
                answer[1] = time;
            }
        }
        return answer;
    }

    private Map[] generateMountain(int n, int[][] paths) {
        Map[] mountain = new Map[n + 1];
        for (int i = 1; i < mountain.length; i++) {
            mountain[i] = new HashMap<>();
        }
        for (int[] path : paths) { // (7)
            int start = path[0];
            int end = path[1];
            int w = path[2];
            mountain[start].put(end, w);
            mountain[end].put(start, w);
        }

        return mountain;
    }

    private boolean[] findSummit(int n, int[] summits) { // (8)
        boolean[] isSummit = new boolean[n + 1];

        for (int s : summits) {
            isSummit[s] = true;
        }

        return isSummit;
    }
}

class Node implements Comparable {
    int vertex;
    int time;

    Node(int vertex, int time) {
        this.vertex = vertex;
        this.time = time;
    }

    @Override
    public int compareTo(Node node) {
        return this.time - node.time;
    }
}
```


* (1) 출입구의 강도를 0으로 변경하고, 출입구와 연결된 등산로 정보를 우선순위 큐에 삽입한다.
* (2) 현재 지점을 이미 지나간 코스가 있을 때 비교하게 된다. 현재 코스에서 현재 지점까지의 최대 강도가 이전 코스에서 현재 지점까지의 최대 강도보다 크면 탐색을 하지 않는다.
* (3) 현재 지점이 산봉우리이면 현재 지점까지의 최대 강도만 저장하고 탐색을 하지 않는다.
* (4) 현재 지점의 다음 등산로를 순회한다.
* (5) 현재 지점까지의 최대 강도와 다음 등산로의 강도 중 최댓값을 우선순위 큐에 삽입한다.
* (6) 강도가 같은 산봉우리가 여러 개라면 산봉우리의 번호가 가장 낮아야 하기 때문에 오름차순 정렬한다. 그리고 순회하면서 강도가 가장 낮은 산봉우리를 찾는다.
* (7) 각 지점에 연결된 등산로 정보를 저장한다.
* (8) 산봉우리의 인덱스를 true로 변경한다.
