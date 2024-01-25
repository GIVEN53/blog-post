[Programmers-Java] 도넛과 막대 그래프
=
<https://school.programmers.co.kr/learn/courses/30/lessons/258711>


접근
--


1. **생성한 정점**은 들어오는 간선이 없고 나가는 간선이 2개 이상있다.
2. **도넛**의 모든 정점은 들어오는 간선과 나가는 간선이 1개씩 있다.
3. **막대**의 마지막 정점은 나가는 간선이 없다.
4. **8자**의 정점 중 한 개는 나가는 간선이 2개있다.
5. 생성한 정점과의 간선을 포함하여 특징을 정리하면 다음과 같다.




|  | in 간선 | out 간선 |
| --- | --- | --- |
| 생성한 정점 | 0 | > 1 |
| 도넛 (모든 정점) | >= 1 | 1 |
| 막대 (마지막 정점) | >= 1 | 0 |
| 8자 (한 정점) | >= 2 | 2 |


풀이
--



```java
import java.util.*;

class Solution {
    public int[] solution(int[][] edges) {
        Map<Integer, Integer> out = new HashMap<>();
        Map<Integer, Integer> in = new HashMap<>();
        int[] answer = new int[4];

        for (int[] edge : edges) { // (1)
            out.put(edge[0], out.getOrDefault(edge[0], 0) + 1);
            in.put(edge[1], in.getOrDefault(edge[1], 0) + 1);
        }

        for (int node : out.keySet()) {
            if (out.get(node) > 1) { // (2)
                if (!in.containsKey(node)) {
                    answer[0] = node;
                } else {
                    answer[3] += 1;
                }
            }
        }

        for (int node : in.keySet()) {
            if (!out.containsKey(node)) { // (3)
                answer[2] += 1;
            }
        }
        answer[1] = out.get(answer[0]) - answer[2] - answer[3]; // (4)
        return answer;
    }
}
```


* (1) a -> b 간선이라면 in에 b를, out에 a를 저장한다.
* (2) out 간선 개수가 2개 이상인 정점 중에서 in 간선이 없으면 생성한 정점이고, 있으면 8자 그래프이다.
* (3) in 간선이 있는 정점 중에서 out 간선이 없으면 막대 그래프이다.
* (4) 도넛 그래프 개수는 `생성한 정점의 out 간선 개수 - 막대 그래프 개수 - 8자 그래프 개수`이다.
