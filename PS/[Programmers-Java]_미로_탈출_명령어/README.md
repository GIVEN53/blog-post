[Programmers-Java] 미로 탈출 명령어
=
<https://school.programmers.co.kr/learn/courses/30/lessons/150365>


접근
--


1. 두 점 p, q가 있을 때 맨해튼 거리는 `|p1 - q1| + |p2 - q2|`로 구한다.
2. 맨해튼 거리가 3이고 k가 2라면 k 거리로 탈출 지점에 도달할 수 없다. 즉, `맨해튼 거리 <= k`가 성립되어야 한다.
3. dfs 탐색해서 탈출 지점까지 거리를 구한다.


풀이
--



```java
class Solution {
    private static final int[] row = {1, 0, 0, -1};
    private static final int[] col = {0, -1, 1, 0};
    private String answer = "impossible";
    private int r;
    private int c;
    private int n;
    private int m;
    private int k;

    public String solution(int n, int m, int x, int y, int r, int c, int k) {
        this.r = r;
        this.c = c;
        this.n = n;
        this.m = m;
        this.k = k;

        if (getManhattanDist(x, y) > k) { // (1)
            return answer;
        }
        dfs(0, x, y, "");
        return answer;
    }

    private void dfs(int moveDist, int x, int y, String command) {
        if (!answer.equals("impossible")) return; // (2)
        if (k - moveDist < getManhattanDist(x, y)) return; // (3)
        if ((k - moveDist - getManhattanDist(x, y)) % 2 != 0) return; // (4)

        if (moveDist == k) { // (5)
            answer = command;
            return;
        }

        for (int i = 0; i < 4; i++) {
            int nx = x + row[i];
            int ny = y + col[i];
            char newCommand = getCommand(i);
            if (isOutOfRange(nx, ny)) {
                continue;
            }
            dfs(moveDist + 1, nx, ny, command + newCommand);
        }
    }

    private int getManhattanDist(int x, int y) { // (6)
        return Math.abs(r - x) + Math.abs(c - y);
    }

    private char getCommand(int i) { // (7)
        return switch (i) {
            case 0 -> 'd';
            case 1 -> 'l';
            case 2 -> 'r';
            default -> 'u';
        };
    }

    private boolean isOutOfRange(int x, int y) {
        return x < 1 || y < 1 || x > n || y > m;
    }
}
```


* (1) 출발 위치와 탈출 지점 사이의 맨해튼 거리가 k보다 크면 어떤 방식으로도 k 거리로 탈출 지점에 도달할 수 없다.
* (2) 이미 미로를 탈출했을 경우 더 이상 탐색하지 않는다.
* (3) 남은 이동 거리가 맨해튼 거리보다 작으면 탈출 지점에 도달할 수 없다.
* (4) `남은 이동 거리 - 맨해튼 거리`가 홀수면 탈출 지점에 도달할 수 없다. 같은 격자를 두 번 이상 방문할 수 있기 때문에 짝수는 가능하다.
* (5) 이외의 경우 이동 거리와 k가 같으면 변수 값을 현재까지의 문자열로 변경한다.
* (6) 맨해튼 거리를 구한다.
* (7) dfs 탐색에서 인덱스를 0부터 순회하고 해당 메서드에서 문자열을 사전 순으로 리턴하기 때문에 가장 먼저 찾은 탈출 경로는 사전 순으로 가장 빠른 경로이다.
