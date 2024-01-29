[Programmers-Java] 무인도 여행
=
<https://school.programmers.co.kr/learn/courses/30/lessons/154540>


접근
--


1. 무인도를 bfs 탐색한다.
2. 탐색할 때 무인도 칸에 적힌 숫자를 합한다.
3. 합을 리스트에 추가한 후 오름차순 정렬한다.


풀이
--



```java
import java.util.*;

class Solution {
    private List<Integer> date = new ArrayList<>();
    private int[] direction = {1, 0, -1, 0};
    private int n;
    private int m;
    private boolean[][] visited;

    public int[] solution(String[] maps) {
        this.n = maps.length;
        this.m = maps[0].length();
        this.visited = new boolean[n][m];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                char now = maps[i].charAt(j);
                if (now != 'X' && !visited[i][j]) { // (1)
                    bfs(now - '0', i, j, maps);
                }
            }
        }

        if (date.size() == 0) {
            return new int[] {-1};
        }
        return date.stream()
                .mapToInt(i -> i)
                .sorted()
                .toArray(); // (2)
    }

    private void bfs(int sum, int r, int c, String[] maps) {
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[] {r, c});
        visited[r][c] = true;

        while (!q.isEmpty()) {
            int[] now = q.poll();

            for (int i = 0; i < 4; i++) { // (3)
                int nr = now[0] + direction[i];
                int nc = now[1] + direction[3 - i];

                if (isOutOfRange(nr, nc) || visited[nr][nc]) {
                    continue;
                }

                char next = maps[nr].charAt(nc);
                if (next == 'X') {
                    continue;
                }
                visited[nr][nc] = true; // (4)
                sum += next - '0';
                q.offer(new int[] {nr, nc});
            }
        }

        date.add(sum);
    }

    private boolean isOutOfRange(int r, int c) {
        return r < 0 || r >= n || c < 0 || c >= m;
    }
}
```


* (1) 무인도이고 방문하지 않았을 경우 현재 좌표에서 bfs 탐색한다.
* (2) 리스트를 오름차순 정렬하여 배열로 변환한다.
* (3) 상하좌우를 탐색하면서 다음 좌표가 범위를 벗어났거나, 이미 방문했거나, 바다이면 건너뛴다.
* (4) 다음 좌표의 방문 처리와 적힌 숫자를 합하고 큐에 삽입한다.
