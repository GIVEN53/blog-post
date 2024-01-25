[Programmers-Java] n + 1 카드게임
=
<https://school.programmers.co.kr/learn/courses/30/lessons/258707>


접근
--


1. 임의의 카드 x와 매칭되는 카드는 하나밖에 없다.
2. 처음에 뽑은 `n / 3`개의 카드와 매칭되는 카드는 무조건 구매한다. 이 때 코인은 1개 필요하다.
3. 구매하지 않고 넘긴 카드라도 나중에 구매할 수 있다.
4. 페어가 없고 코인이 2개라면 구매하지 않고 넘긴 카드 중 페어가 되는 카드 2개를 구매한다.


풀이
--



```java
import java.util.*;

class Solution {
    private Set<Integer> myCards = new HashSet<>();
    private Set<Integer> tempCards = new HashSet<>();
    private int pair;
    private int round = 1;
    private int myCoin;
    private int n;

    public int solution(int coin, int[] cards) {
        this.myCoin = coin;
        this.n = cards.length;

        for (int i = 0; i < n / 3; i++) { // (1)
            myCards.add(cards[i]);
        }

        for (int card : myCards) { // (2)
            if (myCards.contains(n + 1 - card)) {
                pair++;
            }
        }
        pair /= 2;

        for (int i = n / 3; i < n; i += 2) { // (3)
            matchCard(cards[i]); // (4)
            matchCard(cards[i + 1]);

            if (pair < 1 && myCoin > 1) { // (5)
                for (int card : tempCards) {
                    if (tempCards.contains(n + 1 - card)) {
                        pair++;
                        myCoin -= 2;
                        tempCards.remove(card); // (6)
                        break;
                    }
                }
            }

            if (pair < 1) { // (7)
                break;
            }
            round++;
            pair--;
        }

        return round;
    }

    private void matchCard(int card) {
        if (myCoin > 0 && myCards.contains(n + 1 - card)) { // (8)
            myCoin--;
            pair++;
            return;
        }
        tempCards.add(card); // (9)
    }
}
```


* (1) 카드 `n / 3`장을 먼저 뽑는다.
* (2) 처음에 뽑은 카드 중에서 페어 개수를 구한다.
* (3) 카드 뭉치를 두 장씩 순회한다.
* (4) 뽑은 두 개의 카드를 처음에 뽑은 카드와 페어가 되는지 확인한다.
* (5) 페어가 없고 코인이 2개 이상이면 구매하지 않고 넘긴 카드 중에서 페어가 되는 카드 2개를 구매한다.
* (6) 임의의 수와 다른 수를 합해서 n + 1이 되는 경우는 하나뿐이므로 페어가 되는 카드 중 하나를 삭제해서 다음에 또 구매하지 않도록 한다.
* (7) 페어가 없으면 다음 라운드를 진행할 수 없기 때문에 탈출한다.
* (8) 코인이 1개 이상 있고, 가지고 있는 카드와 페어가 되면 해당 카드를 구매한다.
* (9) 이외에는 카드를 넘긴다.
