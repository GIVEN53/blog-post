Map 인터페이스와 구현체 파악하기 (1) - Map 인터페이스
=
우테코 미션에서 Map 자료구조를 사용하면서 Map 인터페이스의 여러 구현체를 접했다. 알고 있는 것보다 구현체 종류가 많아서 각각의 특징이 궁금해졌다. 그래서 Map 인터페이스부터 시작해서 구현체는 어떤 것들이 있는지 알아보려고 한다.


Map 인터페이스
---------


Map은 key, value 쌍으로 구성된 entry를 저장하는 자료구조이다. key로 value를 얻을 수 있고, key는 중복될 수 없지만 value는 중복될 수 있다. Map의 고유한 특성과 동작때문에 다른 Collection 프레임워크(List, Queue, Set)와 달리 **Collection 인터페이스를 상속하지 않는다.**


![](https://blog.kakaocdn.net/dn/CJeEE/btsGwPCQ5D2/mlpGVh4xXkRhB1m4yEYsik/img.png)



### 주요 메서드


자주 사용하는 메서드부터 알아보자.


#### V put(K key, V value)


key, value를 저장한다. **이미 key가 존재하면 이전 값은 value로 대체**된다. 처음 저장하는 key면 null, 이미 존재하는 key면 이전 값을 리턴한다.



```java
Map map = new HashMap<>();
System.out.println(map.put(1, "hello")); // null
System.out.println(map); // {1=hello}

System.out.println(map.put(1, "world")); // hello
System.out.println(map); // {1=world}
```


#### V get(Object key)


key에 매핑된 값을 리턴한다. key가 존재하지 않으면 null을 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.get(1)); // hello
System.out.println(map.get(2)); // null
```


#### V remove(Object key)


key를 삭제하고 key와 매핑된 값을 리턴한다. key가 존재하지 않으면 null을 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.remove(1)); // hello
System.out.println(map); // {}
System.out.println(map.remove(1)); // null
```


#### boolean containsKey(Object key)


key의 존재 여부를 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.containsKey(1)); // true
System.out.println(map.containsKey(2)); // false
```


#### int size()


키\-값 매핑 개수를 리턴한다. 개수가 `Integer.MAX_VALUE`보다 크면 `Integer.MAX_VALUE`를 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.size()); // 1
```


#### Set keySet()


모든 키를 Set에 담아서 리턴한다. Map에 변경사항이 발생하면 Set에도 그대로 반영된다. **remove**를 지원하고 요소를 삭제하면 Map에서 해당 키도 삭제된다. 반대로 **add**는 지원하지 않는다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
map.put(2, "world");
Set keySet = map.keySet();
keySet.remove(1);
System.out.println(map); // {2=world}

map.put(3, "hi");
System.out.println(keySet); // [2, 3]
keySet.add(1); // throw UnsupportedOperationException
```


#### Collection values()


모든 값을 Collection에 담아서 리턴한다. Map에 변경사항이 발생하면 Collection에도 그대로 반영된다. **remove**를 지원하고 요소를 삭제하면 Map에서 해당 값과 매핑된 키도 삭제된다. 반대로 **add**는 지원하지 않는다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
map.put(2, "world");
Collection values = map.values();
values.remove("hello");
System.out.println(map); // {2=world}

map.put(3, "hi");
System.out.println(values); // [world, hi]
values.add("hello"); // throw UnsupportedOperationException
```


#### Set\> entrySet()


모든 키\-값 entry를 Set에 담아서 리턴한다. Map에 변경사항이 발생하면 Set에도 그대로 반영된다. **remove**를 지원하고 요소를 삭제하면 Map에서 해당 entry도 삭제된다. 반대로 **add**는 지원하지 않는다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
map.put(2, "world");
Set> entries = map.entrySet();
entries.remove(Map.entry(1, "hello"));
System.out.println(map); // {2=world}

map.put(3, "hi");
System.out.println(entries); // [2=world, 3=hi]
entries.add(Map.entry(1, "hello")); // throw UnsupportedOperationException
```


### Java 8 이후 추가된 메서드


기존 구현체와의 호환성을 유지하면서 인터페이스를 확장하기 위해 **default 메서드**로 구현되어 있다. default로 추가하지 않으면 Map의 모든 구현체를 수정해야 하기 때문이다.


#### V putIfAbsent(K key, V value)


key가 존재하지 않으면 key, value를 저장한다. 내부적으로 `get()`과 `put()`을 호출한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
map.putIfAbsent(1, "world");
System.out.println(map); // {1=hello}

map.putIfAbsent(2, "world");
System.out.println(map); // {1=hello, 2=world}
```


#### V getOrDefault(Object key, V defaultValue)


key가 존재하면 매핑된 값을 리턴하고, 존재하지 않으면 defaultValue를 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.getOrDefault(1, "world")); // hello
System.out.println(map.getOrDefault(2, "world")); // world
```


#### boolean remove(Object key, Object value)


key\-value entry를 제거한다. key에 매핑된 값이 value와 일치하지 않거나 key가 존재하지 않으면 제거하지 않고 false를 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.remove(1, "world")); // false
System.out.println(map.remove(2, "world")); // false
System.out.println(map); // {1=hello}

System.out.println(map.remove(1, "hello")); // true
System.out.println(map); // {}
```


#### boolean replace(K key, V oldValue, V newValue)


key의 oldValue를 newValue로 변경한다. key에 매핑된 값이 oldValue와 일치하지 않거나 key가 존재하지 않으면 변경하지 않고 false를 리턴한다. 이외에는 `put()`을 호출하고 true를 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.replace(1, "world", "hi")); // false
System.out.println(map.replace(2, "hello", "hi")); // false
System.out.println(map); // {1=hello}

System.out.println(map.replace(1, "hello", "hi")); // true
System.out.println(map); // {1=hi}
```


#### V replace(K key, V value)


key에 매핑된 값을 value로 변경한다. key가 존재할 때만 `put()`을 호출한 후 이전 값을 리턴하고, 존재하지 않으면 null을 리턴한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.replace(1, "world")); // hello
System.out.println(map.replace(2, "world")); // null
System.out.println(map); // {1=world}
```


#### V computeIfAbsent(K key, Function super K, ? extends V mappingFunction)


**key가 존재하지 않으면** key로 function을 수행하여 값을 도출한다. 값이 null이 아니면 저장하고, null이면 저장하지 않는다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.computeIfAbsent(1, k -> "world" + k)); // hello
System.out.println(map.computeIfAbsent(2, k -> "world" + k)); // world2
System.out.println(map); // {1=hello, 2=world2}

System.out.println(map.computeIfAbsent(3, k -> null)); // null
System.out.println(map); // {1=hello, 2=world2}
```


#### V computeIfPresent(K key, BiFunction super K, ? super V, ? extends V remappingFunction)


**key가 존재하면** key, 매핑된 값으로 function을 수행하여 새로운 값을 도출한다. 새로운 값이 null이 아니면 저장하고, null이면 key를 제거한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.computeIfPresent(1, (k, v) -> v + " world" + k)); // hello world1
System.out.println(map.computeIfPresent(2, (k, v) -> v + " world" + k)); // null
System.out.println(map); // {1=hello world1}

System.out.println(map.computeIfPresent(1, (k, v) -> null)); // null
System.out.println(map); // {}
```


#### V compute(K key, BiFunction super K, ? super V, ? extends V remappingFunction)


**key의 존재 유무와 관계없이** key, 매핑된 값으로 function을 수행하여 새로운 값을 도출한다. 새로운 값이 null이 아니면 저장하고, null이면서 key가 존재하면 key를 제거한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.compute(1, (k, v) -> v + " world" + k)); // hello world1
System.out.println(map.compute(2, (k, v) -> v + " world" + k)); // null world2
System.out.println(map); // {1=hello world1, 2=null world2}

System.out.println(map.compute(1, (k, v) -> null)); // null
System.out.println(map); // {2=null world2}
```


#### V merge(K key, V value, BiFunction super V, ? super V, ? extends V remappingFunction)


**key가 존재하지 않으면** function을 수행하지 않고 key, value를 저장한다. **key가 존재하면** key와 매핑된 값과 value로 function을 수행하여 새로운 값을 도출한다. 새로운 값이 null이 아니면 저장하고, null이면 key를 제거한다.



```java
Map map = new HashMap<>();
map.put(1, "hello");
System.out.println(map.merge(1, " world", (oldValue, value) -> oldValue + value + "!")); // hello world!
System.out.println(map.merge(2, "world", String::concat)); // world
System.out.println(map); // {1=hello world!, 2=world}

System.out.println(map.merge(2, "world", (oldValue, value) -> null)); // null
System.out.println(map); // {1=hello world!}
```


구현체 다이어그램
---------



### Non\-Thread Safe


![](https://blog.kakaocdn.net/dn/JdGU7/btsGAfJGVpT/CzcZUDcUvkkBfUQAX3nZ4K/img.png)



### Thread Safe


![](https://blog.kakaocdn.net/dn/o5icW/btsGBxP4kss/mwEFxhKwTBygpb5Ej8MMqk/img.png)



### Collections Inner Class


![](https://blog.kakaocdn.net/dn/dopUuT/btsGCtTIPur/YCwn45KnGInH0dEaVeamu1/img.png)



Reference
---------


<https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Map.html>



