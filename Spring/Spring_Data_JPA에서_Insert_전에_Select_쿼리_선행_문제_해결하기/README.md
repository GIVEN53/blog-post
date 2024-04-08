Spring Data JPA에서 Insert 전에 Select 쿼리 선행 문제 해결하기
=
배경
--



```java
@Entity(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User extends BaseEntity {
    @Id
    private String oauthId;

    @Enumerated(EnumType.STRING)
    private OauthProvider oauthProvider;

    @Column(nullable = false, unique = true, length = 8)
    private String nickname;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 5)
    private Gender gender;

    @Column(nullable = false)
    private LocalDate birthday;

    // field ...
}
```


User 엔티티의 `@Id`는 OAuth 서버에서 전달받은 key를 PK로 할당하고 있기 때문에 `@GeneratedValue` 어노테이션은 사용하지 않았다.  
  




```java
@Service
@RequiredArgsConstructor
public class UserSignupService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;

    public LoginResponse signUp(SignUpRequest signUpRequest) {
        // logic ...

        return userMapper.toEntity(userRepository.save(user));
    }
}
```



```bash
[Hibernate] 
    select
        u1_0.oauth_id,
        u1_0.activity_amount,
        u1_0.birthday,
        u1_0.created_at,
        u1_0.diabetes_year,
        u1_0.diabetic,
        u1_0.gender,
        u1_0.height,
        u1_0.injection,
        u1_0.medicine,
        u1_0.nickname,
        u1_0.oauth_provider,
        u1_0.profile_image_path,
        u1_0.recommended_calorie,
        u1_0.role,
        u1_0.status,
        u1_0.updated_at 
    from
        users u1_0 
    where
        u1_0.oauth_id=?

TRACE 17218 --- [           main] org.hibernate.orm.jdbc.bind              : binding parameter [1] as [VARCHAR] - [22222222]
TRACE 17218 --- [           main] o.s.t.i.TransactionInterceptor           : Completing transaction for [org.springframework.data.jpa.repository.support.SimpleJpaRepository.save]
TRACE 17218 --- [           main] o.s.t.i.TransactionInterceptor           : Completing transaction for [com.coniverse.dangjang.domain.user.service.UserSignupService.signUp]

[Hibernate] 
    /* insert for
        com.coniverse.dangjang.domain.user.entity.User */insert 
    into
        users (activity_amount,birthday,created_at,diabetes_year,diabetic,gender,height,injection,medicine,nickname,oauth_provider,profile_image_path,recommended_calorie,role,status,updated_at,oauth_id) 
    values
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
```


User 객체를 저장하면 select 후 insert가 실행된다.  
`save()`를 호출할수록 불필요한 select 쿼리가 기하급수적으로 늘어날 것이고 결국 데이터베이스의 성능을 저하시키기 때문에 최적화가 필요하다고 판단했다.  
  



save()는 어떻게 동작할까?
-----------------


원인을 파악하기 위해 `save()`의 동작 방식을 살펴보았다.  
`save()` 메서드는 JpaRepository의 구현체인 **SimpleJpaRepository** 클래스에 구현되어 있다. 


### SimpleJpaRepository


![](https://blog.kakaocdn.net/dn/dUAPCF/btsEGS2wkGh/370kGyTYDB5P4Wm3yIa0qk/img.png)



주입된 **JpaEntityInformation**의 `isNew()`를 호출해서 전달받은 객체가 new 상태라면 영속화(`persist()`)하고, 관리 중인 상태라면 병합(`merge()`)한다.


![](https://blog.kakaocdn.net/dn/IeHn9/btsExIssyhJ/KYkNsJhyNswXr2v6KGNO50/img.png)



JpaEntityInformation 인터페이스의 다이어그램이며, JpaMetamodelEntityInformation과 AbstractEntityInformation의 `isNew()` 메서드가 동작한다.


### JpaMetamodelEntityInformation


![](https://blog.kakaocdn.net/dn/7Lc9c/btsEtsYyJk4/m5ktcN4xRWEZOyBRFS0VIk/img.png)



**JpaMetamodelEntityInformation**는 `@Version` 어노테이션을 사용한 필드를 확인한다.


* 관련 필드가 없거나 `@Version`이 사용된 필드가 primitive 타입이면 AbstractEntityInformation의 `isNew()`를 호출한다.
* `@Version`이 사용된 필드가 wrapper class이면 null인지 확인한다.


### AbstractEntityInformation


![](https://blog.kakaocdn.net/dn/bJME5e/btsEtmRKv6W/T1tMZhUEo8TiLJqa9Bevm0/img.png)



**AbstractEntityInformation**는 `@Id` 어노테이션을 사용한 필드를 확인한다.


* primitive 타입이 아니라면 null인지 확인한다.
* Number의 하위 타입이면 0인지 확인한다.


### **원인**


`@GeneratedValue` 어노테이션으로 auto increment를 사용하면 데이터베이스에 저장될 때 id가 할당된다. 데이터베이스에 저장되기 전에 메모리에서 생성된 객체는 id가 비어있기 때문에 `isNew()`는 true이다. 그러나 `@Id` 필드에 값을 할당한 상태에서 객체를 저장할 경우 `isNew()`는 false이기 때문에 `em.merge()`를 호출하게 된다.


`merge()`는 준영속 상태(Detached)의 엔티티를 영속 상태(Managed)로 만들기 위해 **식별자 값으로 조회하고, 조회된 객체에 병합하거나 조회된 객체가 없으면 새로 생성해서 병합**한다.  
따라서 select로 객체를 조회하고, 조회된 객체가 없으므로 insert를 실행하게 된다.  
  



해결 방법1: 엔티티에서 Persistable 인터페이스 구현
----------------------------------



```java
@Entity(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User extends BaseEntity implements Persistable {
    @Id
    private String oauthId;

    @Enumerated(EnumType.STRING)
    private OauthProvider oauthProvider;

    @Column(nullable = false, unique = true, length = 8)
    private String nickname;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 5)
    private Gender gender;

    @Column(nullable = false)
    private LocalDate birthday;

    // field ...

    @Override
    public String getId() {
        return this.oauthId;
    }

    @Override
    public boolean isNew() {
        return this.getCreatedAt() == null;
    }
}
```


`getId()`는 `@Id` 어노테이션의 필드, `isNew()`는 새로운 엔티티인지 여부를 리턴하도록 오버라이딩한다.



```java
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public class BaseEntity {
    @CreatedDate
    @Column(name = "CREATED_AT", updatable = false, nullable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "UPDATED_AT", nullable = false)
    private LocalDateTime updatedAt;
}
```


JPA의 auditing을 사용하면 `isNew()`를 쉽게 오버라이딩할 수 있다. 


### Persistable 인터페이스를 구현하는 이유


![](https://blog.kakaocdn.net/dn/kWsrX/btsEwIzwTdP/OkTXKH3h5PKRDC6AJCsHMK/img.png)
  
![](https://blog.kakaocdn.net/dn/cdzAT8/btsEy6sDyKc/vXF7KU0dB2mezNm8WUyXxk/img.png)



엔티티에서 `Persistable` 인터페이스를 구현하면 SimpleJpaRepository의 JpaEntityInformation를 **JpaPersistableEntityInformation**으로 주입하게 된다.


### JpaPersistableEntityInformation 주입 과정


SimpleJpaRepository bean은 JpaRepositoryFactory에서 생성된다.


![](https://blog.kakaocdn.net/dn/slfDq/btsEFN8uane/78MM2wT7eCqY3p7URKQKdk/img.png)



#### 1. getTargetRepository()


JPA repository 객체를 생성한다.


#### 2. getEntityInformation()


`information.getDomainType()`에서 리턴한 User 클래스를 파라미터로 받는다.  
![](https://blog.kakaocdn.net/dn/RqkZE/btsEFdl3VBz/5B6wVhOHzs6hdx6rqtSdb1/img.png)



![](https://blog.kakaocdn.net/dn/5kXpx/btsEqV713sI/BAVDvwXlkoR9WTYHYhLUtk/img.png)



#### 3. JpaEntityInformationSupport.getEntityInformation()


![](https://blog.kakaocdn.net/dn/dm62VN/btsEEXjxe5Z/K9z30VM8EXVMi7bdhDDssK/img.png)



User 클래스는 Persistable의 구현체이기 때문에 **JpaPersistableEntityInformation**을 리턴한다.


#### 4. repository 리턴


JpaPersistableEntityInformation이 주입된 SimpleJpaRepository를 리턴한다. 


SimpleJpaRepository에서 `save()`를 호출하면 `isNew()`는 엔티티에서 오버라이딩한 `isNew()`가 실행된다.


![](https://blog.kakaocdn.net/dn/bufCDZ/btsEydy6ynb/fvTT2T0x6Uu69DRLIUKQ1k/img.png)



  

해결 방법2: @PrePersist, @PostLoad 어노테이션 사용
---------------------------------------



```java
@Entity(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User implements Persistable {
    @Id
    private String oauthId;

    // field ...

    @Transient
    private boolean isNew = true;

    @Override
    public String getId() {
        return this.oauthId;
    }

    @Override
    public boolean isNew() {
        return this.isNew;
    }

    @PrePersist
    @PostLoad
    void markNotNew() {
        this.isNew = false;
    }
}
```


**Persistable를 구현할 때 새로운 엔티티인지 판단할 필드가 없을 경우** boolean 필드와 `@PrePersist`, `@PostLoad` 어노테이션으로 해결할 수 있다.



> `@Transient`: 테이블의 컬럼과 매핑이 제외된다.  
> `@PrePersist`: 엔티티가 비영속 상태(New)에서 영속 상태(Managed)가 되기 전에 실행한다.  
> `@PostLoad`: 엔티티가 영속성 컨텍스트에 조회된 후에 또는 refresh를 호출한 후에 실행한다.

객체가 생성됐을 때 boolean 필드를 true로 할당해서 `em.persist()`가 실행되도록 한다.  
flush가 되기 전에 같은 트랜잭션에서 해당 객체를 다시 조회 후 변경하는 경우가 발생할 수 있기 때문에 `@PrePersist` 어노테이션을 사용한다.  
다른 트랜잭션에서 엔티티를 조회할 때 새로운 엔티티로 판단하지 않도록 `@PostLoad` 어노테이션을 사용한다.


### 결과



```bash
[Hibernate] 
    /* insert for
        com.coniverse.dangjang.domain.user.entity.User */insert 
    into
        users (activity_amount,birthday,created_at,diabetes_year,diabetic,gender,height,injection,medicine,nickname,oauth_provider,profile_image_path,recommended_calorie,role,status,updated_at,oauth_id) 
    values
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
```


select 쿼리 선행없이 insert 쿼리 하나만 발생하는 것을 확인할 수 있다.


Reference
---------


<https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.entity-persistence.saving-entites>  
<https://junhyunny.github.io/spring-boot/jpa/junit/pre-persist-pre-update/>

