[Programmers-Java] 테이블 해시 함수
=
<https://school.programmers.co.kr/learn/courses/30/lessons/147354>


접근
--


1. 튜플을 정렬한다.
2. i번째 행의 값은 i로 나눈 나머지를 구하고 모두 더한다.
3. 범위 내의 값들을 누적하여 XOR 연산한다.


풀이
--



```java
import java.util.Arrays;
import java.util.stream.IntStream;

class Solution {
    public int solution(int[][] data, int col, int row_begin, int row_end) {
        int[][] sortedData = sort(data, col - 1); // (1)
        return IntStream.range(row_begin - 1, row_end) // (2)
            .map(i -> modAndSum(i + 1, sortedData[i])) // (3)
            .reduce(0, (a, b) -> a ^ b); // (4)
    }

    private int[][] sort(int[][] data, int col) {
        Arrays.sort(data, (o1, o2) -> {
            if (o1[col] == o2[col]) {
                return o2[0] - o1[0];
            }
                return o1[col] - o2[col];
            });
        return data;
    }

    private int modAndSum(int modNum, final int[] data) {
        return Arrays.stream(data)
            .map(d -> d % modNum)
            .sum();
    }
}
```


* (1\) 튜플을 정렬한다.
* (2\) `row_begin ~ row_end`의 인덱스만 순회한다.
* (3\) i로 나눈 나머지의 합을 구한다.
* (4\) XOR 연산한다.
