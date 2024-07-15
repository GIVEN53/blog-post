[Programmers-Java] 단체사진 찍기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/1835>


접근
--


1. 순열로 배치의 경우의 수를 구한다.
2. 배치가 조건에 모두 부합하는지 확인한다.


풀이
--



```java
class Solution {
    private String[] members = new String[] { "A", "C", "F", "J", "M", "N", "R", "T" };
    private boolean[] visited = new boolean[8];
    private int answer;

    public int solution(int n, String[] data) {
        answer = 0;
        createPermutation("", data);
        return answer;
    }

    private void createPermutation(String result, String[] data) {
        if (result.length() == 8) { // (1)
            for (String condition : data) {
                if (!validate(result, condition)) {
                    return;
                }
            }
            answer++;
            return;
        }

        for (int i = 0; i < 8; i++) { // (2)
            if (visited[i]) {
                continue;
            }
            visited[i] = true;
            createPermutation(result + members[i], data);
            visited[i] = false;
        }
    }

    private boolean validate(String lines, String condition) {
        char operator = condition.charAt(3);
        char friend1 = condition.charAt(0);
        char friend2 = condition.charAt(2);
        int interval = Character.getNumericValue(condition.charAt(4));

        int differenceIndex = Math.abs(lines.indexOf(friend1) - lines.indexOf(friend2)) - 1; // (3)

        switch (operator) {
            case '=' -> {
                if (differenceIndex == interval) {
                    return true;
                }
            }
            case '>' -> {
                if (differenceIndex > interval) {
                    return true;
                }
            }
            case '<' -> {
                if (differenceIndex < interval) {
                    return true;
                }
            }
        }
        return false;
    }
}
```


* (1\) 8명을 모두 선택했으면 조건을 순회하면서 모든 조건을 만족하는지 확인한다.
* (2\) 순열로 배치를 구한다.
* (3\) 배치에서 두 친구의 간격을 계산한다.
