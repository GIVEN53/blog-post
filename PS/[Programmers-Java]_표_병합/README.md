[Programmers-Java] 표 병합
=
<https://school.programmers.co.kr/learn/courses/30/lessons/150366>


접근
--


1. UPDATE: 부모 셀을 찾아 업데이트한다.
2. MERGE: 유니온-파인드를 사용하여 두 셀을 합친다.
3. UNMERGE: 부모 셀을 바라보는 셀들을 자신을 바라보도록 변경한다.
4. PRINT: 부모 셀의 값을 출력한다.


풀이
--



```java
import java.util.*;

class Solution {
    private static List result = new ArrayList<>();
    private static final String EMPTY = "EMPTY";
    private static int[] parents = new int[2501];
    private static String[] table = new String[2501];

    public String[] solution(String[] commands) {
        for (int i = 1; i < parents.length; i++) {
            parents[i] = i;
        }

        for (String command : commands) {
            String[] splitCommand = command.split(" ");
            switch (splitCommand[0]) { // (1)
                case "UPDATE" -> doUpdate(splitCommand);
                case "MERGE" -> doMerge(splitCommand);
                case "UNMERGE" -> doUnmerge(splitCommand);
                case "PRINT" -> doPrint(splitCommand);
            }
        }
        return result.toArray(new String[0]);
    }

    private void doUpdate(String[] commands) {
        if (commands.length == 4) { // (2)
            updateIndexValue(commands);
        }
        if (commands.length == 3) { // (3)
            updateValue(commands);
        }
    }

    private void updateIndexValue(String[] commands) {
        int r = Integer.parseInt(commands[1]);
        int c = Integer.parseInt(commands[2]);
        String value = commands[3];

        int parent = find(getIndex(r, c)); // (4)
        table[parent] = value;
    }

    private int getIndex(int r, int c) { // (5)
        return 50 * (r - 1) + c;
    }

    private void updateValue(String[] commands) {
        String value1 = commands[1];
        String value2 = commands[2];
        for (int i = 1; i < parents.length; i++) {
            if (value1.equals(table[i])) { // (6)
                table[i] = value2;
            }
        }
    }

    private void doMerge(String[] commands) { // (7)
        int r1 = Integer.parseInt(commands[1]);
        int c1 = Integer.parseInt(commands[2]);
        int r2 = Integer.parseInt(commands[3]);
        int c2 = Integer.parseInt(commands[4]);

        union(getIndex(r1, c1), getIndex(r2, c2));
    }

    private int find(int x) {
        if (parents[x] != x) {
            parents[x] = find(parents[x]);
        }
        return parents[x];
    }

    private void union(int a, int b) {
        a = find(a);
        b = find(b);
        if (a != b) {
            table[a] = getValue(a, b);
            table[b] = null;
            parents[b] = a;
        }
    }

    private String getValue(int a, int b) {
        String value1 = table[a];
        String value2 = table[b];
        if (value1 != null) {
            return value1;
        }
        return value2;
    }

    private void doUnmerge(String[] commands) { // (8)
        int r = Integer.parseInt(commands[1]);
        int c = Integer.parseInt(commands[2]);

        for (int i = 1; i < parents.length; i++) {
            find(i); // (9)
        }

        int parent = parents[getIndex(r, c)];
        String value = table[parent];
        for (int i = 1; i < parents.length; i++) {
            if (parents[i] == parent) {
                parents[i] = i;
                table[i] = null;
            }
        }
        table[getIndex(r, c)] = value;
    }

    private void doPrint(String[] commands) { // (10)
        int r = Integer.parseInt(commands[1]);
        int c = Integer.parseInt(commands[2]);

        int parent = find(getIndex(r, c));
        String value = table[parent];
        if (value == null) {
            result.add(EMPTY);
        } else {
            result.add(value);
        }
    }
}
```


* (1) 명령어에 따라 분기한다.
* (2) `UPDATE r c value` 명령어를 처리한다.
* (3) `UPDATE value1 value2` 명령어를 처리한다.
* (4) 부모 인덱스를 찾아 값을 변경한다.
* (5) 2차원 배열의 인덱스를 1차원 배열의 인덱스로 변경하여 리턴한다.
* (6) value1과 같은 값을 가진 셀을 찾아서 value2로 변경한다.
* (7) 두 셀을 병합한다.
* (8) 병합을 해제한다.
* (9) 부모 인덱스가 업데이트되지 않은 셀이 존재할 수 있기 때문에 순회하면서 업데이트한다.
* (10) 셀의 값을 출력한다.
