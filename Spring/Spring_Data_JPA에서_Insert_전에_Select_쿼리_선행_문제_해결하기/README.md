Spring Data JPA에서 Insert 전에 Select 쿼리 선행 문제 해결하기
=
<h2>배경</h2>
<pre><code class="language-java">@Entity(name = "users")
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
}</code></pre>
<p>User 엔티티의 <code>@Id</code>는 OAuth 서버에서 전달받은 key를 PK로 할당하고 있기 때문에 <code>@GeneratedValue</code> 어노테이션은 사용하지 않았다.<br><br></p>
<pre><code class="language-java">@Service
@RequiredArgsConstructor
public class UserSignupService {
 private final UserRepository userRepository;
 private final UserMapper userMapper;

 public LoginResponse signUp(SignUpRequest signUpRequest) {
 // logic ...

 return userMapper.toEntity(userRepository.save(user));
 }
}</code></pre>
<pre><code class="language-bash">[Hibernate] 
 select
 u1\_0.oauth\_id,
 u1\_0.activity\_amount,
 u1\_0.birthday,
 u1\_0.created\_at,
 u1\_0.diabetes\_year,
 u1\_0.diabetic,
 u1\_0.gender,
 u1\_0.height,
 u1\_0.injection,
 u1\_0.medicine,
 u1\_0.nickname,
 u1\_0.oauth\_provider,
 u1\_0.profile\_image\_path,
 u1\_0.recommended\_calorie,
 u1\_0.role,
 u1\_0.status,
 u1\_0.updated\_at 
 from
 users u1\_0 
 where
 u1\_0.oauth\_id=?

TRACE 17218 --- [ main] org.hibernate.orm.jdbc.bind : binding parameter [1] as [VARCHAR] - [22222222]
TRACE 17218 --- [ main] o.s.t.i.TransactionInterceptor : Completing transaction for [org.springframework.data.jpa.repository.support.SimpleJpaRepository.save]
TRACE 17218 --- [ main] o.s.t.i.TransactionInterceptor : Completing transaction for [com.coniverse.dangjang.domain.user.service.UserSignupService.signUp]

[Hibernate] 
 /\* insert for
 com.coniverse.dangjang.domain.user.entity.User \*/insert 
 into
 users (activity\_amount,birthday,created\_at,diabetes\_year,diabetic,gender,height,injection,medicine,nickname,oauth\_provider,profile\_image\_path,recommended\_calorie,role,status,updated\_at,oauth\_id) 
 values
 (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)</code></pre>
<p>User 객체를 저장하면 select 후 insert가 실행된다.<br><code>save()</code>를 호출할수록 불필요한 select 쿼리가 기하급수적으로 늘어날 것이고 결국 데이터베이스의 성능을 저하시키기 때문에 최적화가 필요하다고 판단했다.<br><br></p>
<h2>save()는 어떻게 동작할까?</h2>
<p>원인을 파악하기 위해 <code>save()</code>의 동작 방식을 살펴보았다.<br><code>save()</code> 메서드는 JpaRepository의 구현체인 <strong>SimpleJpaRepository</strong> 클래스에 구현되어 있다. </p>
<h3>SimpleJpaRepository</h3>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/dUAPCF/btsEGS2wkGh/370kGyTYDB5P4Wm3yIa0qk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/dUAPCF/btsEGS2wkGh/370kGyTYDB5P4Wm3yIa0qk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdUAPCF%2FbtsEGS2wkGh%2F370kGyTYDB5P4Wm3yIa0qk%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<p>주입된 <strong>JpaEntityInformation</strong>의 <code>isNew()</code>를 호출해서 전달받은 객체가 new 상태라면 영속화(<code>persist()</code>)하고, 관리 중인 상태라면 병합(<code>merge()</code>)한다.</p>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="675" data-origin-height="418"><span data-url="https://blog.kakaocdn.net/dn/IeHn9/btsExIssyhJ/KYkNsJhyNswXr2v6KGNO50/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/IeHn9/btsExIssyhJ/KYkNsJhyNswXr2v6KGNO50/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FIeHn9%2FbtsExIssyhJ%2FKYkNsJhyNswXr2v6KGNO50%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="675" data-origin-height="418"/></span></figure>
</p>
<p>JpaEntityInformation 인터페이스의 다이어그램이며, JpaMetamodelEntityInformation과 AbstractEntityInformation의 <code>isNew()</code> 메서드가 동작한다.</p>
<h3>JpaMetamodelEntityInformation</h3>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="807" data-origin-height="268"><span data-url="https://blog.kakaocdn.net/dn/7Lc9c/btsEtsYyJk4/m5ktcN4xRWEZOyBRFS0VIk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/7Lc9c/btsEtsYyJk4/m5ktcN4xRWEZOyBRFS0VIk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F7Lc9c%2FbtsEtsYyJk4%2Fm5ktcN4xRWEZOyBRFS0VIk%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="807" data-origin-height="268"/></span></figure>
</p>
<p><strong>JpaMetamodelEntityInformation</strong>는 <code>@Version</code> 어노테이션을 사용한 필드를 확인한다.</p>
<ul>
<li>관련 필드가 없거나 <code>@Version</code>이 사용된 필드가 primitive 타입이면 AbstractEntityInformation의 <code>isNew()</code>를 호출한다.</li>
<li><code>@Version</code>이 사용된 필드가 wrapper class이면 null인지 확인한다.</li>
</ul>
<h3>AbstractEntityInformation</h3>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="807" data-origin-height="328"><span data-url="https://blog.kakaocdn.net/dn/bJME5e/btsEtmRKv6W/T1tMZhUEo8TiLJqa9Bevm0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/bJME5e/btsEtmRKv6W/T1tMZhUEo8TiLJqa9Bevm0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbJME5e%2FbtsEtmRKv6W%2FT1tMZhUEo8TiLJqa9Bevm0%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="807" data-origin-height="328"/></span></figure>
</p>
<p><strong>AbstractEntityInformation</strong>는 <code>@Id</code> 어노테이션을 사용한 필드를 확인한다.</p>
<ul>
<li>primitive 타입이 아니라면 null인지 확인한다.</li>
<li>Number의 하위 타입이면 0인지 확인한다.</li>
</ul>
<h3><strong>원인</strong></h3>
<p><code>@GeneratedValue</code> 어노테이션으로 auto increment를 사용하면 데이터베이스에 저장될 때 id가 할당된다. 데이터베이스에 저장되기 전에 메모리에서 생성된 객체는 id가 비어있기 때문에 <code>isNew()</code>는 true이다. 그러나 <code>@Id</code> 필드에 값을 할당한 상태에서 객체를 저장할 경우 <code>isNew()</code>는 false이기 때문에 <code>em.merge()</code>를 호출하게 된다.</p>
<p><code>merge()</code>는 준영속 상태(Detached)의 엔티티를 영속 상태(Managed)로 만들기 위해 <strong>식별자 값으로 조회하고, 조회된 객체에 병합하거나 조회된 객체가 없으면 새로 생성해서 병합</strong>한다.<br>따라서 select로 객체를 조회하고, 조회된 객체가 없으므로 insert를 실행하게 된다.<br><br></p>
<h2>해결 방법1: 엔티티에서 Persistable<T> 인터페이스 구현</h2>
<pre><code class="language-java">@Entity(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User extends BaseEntity implements Persistable<String> {
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
}</code></pre>
<p><code>getId()</code>는 <code>@Id</code> 어노테이션의 필드, <code>isNew()</code>는 새로운 엔티티인지 여부를 리턴하도록 오버라이딩한다.</p>
<pre><code class="language-java">@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public class BaseEntity {
 @CreatedDate
 @Column(name = "CREATED\_AT", updatable = false, nullable = false)
 private LocalDateTime createdAt;

 @LastModifiedDate
 @Column(name = "UPDATED\_AT", nullable = false)
 private LocalDateTime updatedAt;
}</code></pre>
<p>JPA의 auditing을 사용하면 <code>isNew()</code>를 쉽게 오버라이딩할 수 있다. </p>
<h3>Persistable 인터페이스를 구현하는 이유</h3>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="697" data-origin-height="268"><span data-url="https://blog.kakaocdn.net/dn/kWsrX/btsEwIzwTdP/OkTXKH3h5PKRDC6AJCsHMK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/kWsrX/btsEwIzwTdP/OkTXKH3h5PKRDC6AJCsHMK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FkWsrX%2FbtsEwIzwTdP%2FOkTXKH3h5PKRDC6AJCsHMK%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="697" data-origin-height="268"/></span></figure>
<br><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="675" data-origin-height="418"><span data-url="https://blog.kakaocdn.net/dn/cdzAT8/btsEy6sDyKc/vXF7KU0dB2mezNm8WUyXxk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/cdzAT8/btsEy6sDyKc/vXF7KU0dB2mezNm8WUyXxk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcdzAT8%2FbtsEy6sDyKc%2FvXF7KU0dB2mezNm8WUyXxk%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="675" data-origin-height="418"/></span></figure>
</p>
<p>엔티티에서 <code>Persistable<T></code> 인터페이스를 구현하면 SimpleJpaRepository의 JpaEntityInformation를 <strong>JpaPersistableEntityInformation</strong>으로 주입하게 된다.</p>
<h3>JpaPersistableEntityInformation 주입 과정</h3>
<p>SimpleJpaRepository bean은 JpaRepositoryFactory에서 생성된다.</p>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/slfDq/btsEFN8uane/78MM2wT7eCqY3p7URKQKdk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/slfDq/btsEFN8uane/78MM2wT7eCqY3p7URKQKdk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FslfDq%2FbtsEFN8uane%2F78MM2wT7eCqY3p7URKQKdk%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<h4>1. getTargetRepository()</h4>
<p>JPA repository 객체를 생성한다.</p>
<h4>2. getEntityInformation()</h4>
<p><code>information.getDomainType()</code>에서 리턴한 User 클래스를 파라미터로 받는다.<br><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/RqkZE/btsEFdl3VBz/5B6wVhOHzs6hdx6rqtSdb1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/RqkZE/btsEFdl3VBz/5B6wVhOHzs6hdx6rqtSdb1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FRqkZE%2FbtsEFdl3VBz%2F5B6wVhOHzs6hdx6rqtSdb1%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="868" data-origin-height="583"><span data-url="https://blog.kakaocdn.net/dn/5kXpx/btsEqV713sI/BAVDvwXlkoR9WTYHYhLUtk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/5kXpx/btsEqV713sI/BAVDvwXlkoR9WTYHYhLUtk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F5kXpx%2FbtsEqV713sI%2FBAVDvwXlkoR9WTYHYhLUtk%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="868" data-origin-height="583"/></span></figure>
</p>
<h4>3. JpaEntityInformationSupport.getEntityInformation()</h4>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/dm62VN/btsEEXjxe5Z/K9z30VM8EXVMi7bdhDDssK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/dm62VN/btsEEXjxe5Z/K9z30VM8EXVMi7bdhDDssK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fdm62VN%2FbtsEEXjxe5Z%2FK9z30VM8EXVMi7bdhDDssK%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<p>User 클래스는 Persistable의 구현체이기 때문에 <strong>JpaPersistableEntityInformation</strong>을 리턴한다.</p>
<h4>4. repository 리턴</h4>
<p>JpaPersistableEntityInformation이 주입된 SimpleJpaRepository를 리턴한다. </p>
<p>SimpleJpaRepository에서 <code>save()</code>를 호출하면 <code>isNew()</code>는 엔티티에서 오버라이딩한 <code>isNew()</code>가 실행된다.</p>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="694" data-origin-height="494"><span data-url="https://blog.kakaocdn.net/dn/bufCDZ/btsEydy6ynb/fvTT2T0x6Uu69DRLIUKQ1k/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/bufCDZ/btsEydy6ynb/fvTT2T0x6Uu69DRLIUKQ1k/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbufCDZ%2FbtsEydy6ynb%2FfvTT2T0x6Uu69DRLIUKQ1k%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="694" data-origin-height="494"/></span></figure>
</p>
<br>

<h2>해결 방법2: @PrePersist, @PostLoad 어노테이션 사용</h2>
<pre><code class="language-java">@Entity(name = "users")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User implements Persistable<String> {
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
}</code></pre>
<p><strong>Persistable를 구현할 때 새로운 엔티티인지 판단할 필드가 없을 경우</strong> boolean 필드와 <code>@PrePersist</code>, <code>@PostLoad</code> 어노테이션으로 해결할 수 있다.</p>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p><code>@Transient</code>: 테이블의 컬럼과 매핑이 제외된다.<br><code>@PrePersist</code>: 엔티티가 비영속 상태(New)에서 영속 상태(Managed)가 되기 전에 실행한다.<br><code>@PostLoad</code>: 엔티티가 영속성 컨텍스트에 조회된 후에 또는 refresh를 호출한 후에 실행한다.</p>
</span></p></blockquote><p>객체가 생성됐을 때 boolean 필드를 true로 할당해서 <code>em.persist()</code>가 실행되도록 한다.<br>flush가 되기 전에 같은 트랜잭션에서 해당 객체를 다시 조회 후 변경하는 경우가 발생할 수 있기 때문에 <code>@PrePersist</code> 어노테이션을 사용한다.<br>다른 트랜잭션에서 엔티티를 조회할 때 새로운 엔티티로 판단하지 않도록 <code>@PostLoad</code> 어노테이션을 사용한다.</p>
<h3>결과</h3>
<pre><code class="language-bash">[Hibernate] 
 /\* insert for
 com.coniverse.dangjang.domain.user.entity.User \*/insert 
 into
 users (activity\_amount,birthday,created\_at,diabetes\_year,diabetic,gender,height,injection,medicine,nickname,oauth\_provider,profile\_image\_path,recommended\_calorie,role,status,updated\_at,oauth\_id) 
 values
 (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)</code></pre>
<p>select 쿼리 선행없이 insert 쿼리 하나만 발생하는 것을 확인할 수 있다.</p>
<h2>Reference</h2>
<p><a href="https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.entity-persistence.saving-entites">https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.entity-persistence.saving-entites</a><br><a href="https://junhyunny.github.io/spring-boot/jpa/junit/pre-persist-pre-update/">https://junhyunny.github.io/spring-boot/jpa/junit/pre-persist-pre-update/</a></p>