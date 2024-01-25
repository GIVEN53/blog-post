[Programmers-Java] 붕대 감기
=
<https://school.programmers.co.kr/learn/courses/30/lessons/250137>


접근
--


1. 공격을 순회하면서 현재 초와 같으면 피해를 입는다.
2. 같지 않으면 붕대를 감는다.
3. 회복 후 체력이 최대 체력보다 큰지 확인한다.
4. 공격의 최대 공격 시간만큼 반복하기 때문에 시간복잡도는 `O(1000)`이다.


풀이
--



```java
class Solution {
    private int currentHealth;
    private int sec = 1;
    private int successStreak;

    public int solution(int[] bandage, int health, int[][] attacks) {
        currentHealth = health;
        int i = 0;
        while (i < attacks.length) {
            if (sec == attacks[i][0]) { // (1)
                attackByMonster(attacks[i][1]);
                i++;
            } else { // (2)
                recover(bandage, health);
            }

            if (currentHealth <= 0) { // (3)
                return -1;
            }
            sec += 1;
        }
        return currentHealth;
    }

    private void attackByMonster(int damage) { // (4)
        currentHealth -= damage;
        successStreak = 0;
    }

    private void recover(int[] bandage, int health) {
        currentHealth += bandage[1]; // (5)
        successStreak++;
        if (successStreak == bandage[0]) { // (6)
            currentHealth += bandage[2];
            successStreak = 0;
        }

        if (currentHealth > health) { // (7)
            currentHealth = health;
        }
    }
}
```


* (1) 현재 초에 몬스터의 공격이 있으면 피해를 입는다.
* (2) 공격이 없으면 회복한다.
* (3) 현재 체력이 0 이하이면 죽는다.
* (4) 몬스터의 피해량만큼 체력이 줄어들고 연속 성공 횟수를 초기화한다.
* (5) 초당 회복량 만큼 회복하고 연속 성공 횟수가 1 증가한다.
* (6) t초 연속 성공했을 경우 추가 회복량만큼 회복하고 연속 성공 횟수를 초기화한다.
* (7) 현재 체력이 최대 채력보다 커질 수 없다.
