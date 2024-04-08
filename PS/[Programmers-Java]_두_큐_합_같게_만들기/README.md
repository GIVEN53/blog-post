[Programmers-Java] 두 큐 합 같게 만들기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/118667>


접근
--


1. 큐의 합을 미리 계산한다.
2. 두 큐의 합을 비교하고 큰 큐에서 작은 큐로 원소를 이동시킨다.


풀이
--



```java
import java.util.*;

class Solution {
    public int solution(int[] queue1, int[] queue2) {
        long queue1Sum = Arrays.stream(queue1).sum();
        long queue2Sum = Arrays.stream(queue2).sum();
        if ((queue1Sum + queue2Sum) % 2 != 0) { // (1)
            return -1;
        }

        Queue q1 = generateQueue(queue1);
        Queue q2 = generateQueue(queue2);

        int cnt = 0;
        while (cnt < 600000) { // (2)
            if (queue1Sum > queue2Sum) { // (3)
                int num = q1.poll();
                queue1Sum -= num;
                q2.add(num);
                queue2Sum += num;
                cnt += 1;
            } else if (queue1Sum < queue2Sum) { // (4)
                int num = q2.poll();
                queue2Sum -= num;
                q1.add(num);
                queue1Sum += num;
                cnt += 1;
            } else { // (5)
                return cnt;
            }
        }
        return -1;
    }

    private Queue generateQueue(int[] arr) {
        Queue q = new LinkedList<>();
        for (int i : arr) {
            q.add(i);
        }
        return q;
    }
}
```


* (1) 두 배열의 합이 홀수면 -1을 리턴한다.
* (2) 큐의 최대 길이는 300,000이므로 두 큐의 길이의 합인 600,000을 탈출 조건으로 설정한다.
* (3) 큐1의 합이 큐2의 합보다 크면 큐1의 원소를 꺼내서 큐2에 삽입한다.
* (4) 큐2의 합이 큐1의 합보다 크면 큐2의 원소를 꺼내서 큐1에 삽입한다.
* (5) 두 큐의 합이 같으면 작업 횟수를 리턴한다.
