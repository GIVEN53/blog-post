MySQL Replication 구성하기 - 2 with Spring JPA
=
[MySQL Replication 구성하기 - 1 with Docker](https://given-dev.tistory.com/113)에서 데이터베이스의 replication을 구성했다.  
write는 Master, read는 Slave에서 처리하도록 쿼리를 분산하는 것은 애플리케이션 레벨에서 구현해야 한다.  
일반적인 방법은 `@Transactional` 어노테이션의 `readOnly` 속성에 따라 분기하는 것이다.  
![](https://blog.kakaocdn.net/dn/KlGn4/btsEfohUDdr/21RsV1wL1r6kex9AwRqWL1/img.png)


### version


* Java 11.0.18
* Spring 2.7.8


1. Data Source
--------------


![](https://blog.kakaocdn.net/dn/csOJN5/btsEft4A7x3/4aJAr85u8KhrcE7k2Y2700/img.png)


Data Source는 DB Connection과 관련된 인터페이스이며 데이터베이스의 연결 정보를 저장하고 Connection Pool에 Connection을 등록, 관리하는 역할을 한다.  
JDBC는 Data Source 인터페이스를 통해 Connection을 획득, 반납하는 방식으로 데이터베이스와 통신하게 된다.  
Data Source 인터페이스의 구현체는 여러 가지가 있으며 Spring Boot 2.0부터 `HikariCP`가 표준이다.


Data Source가 한 개일 경우 auto configuration으로 Data Source가 자동으로 생성된다. 그러나 replication을 사용하면 2개 이상의 Data Source가 필요하기 때문에 개발자가 직접 생성해야 한다. 


### 1.1. property 설정



```yml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: ${master_username}
    password: ${master_password}
    url: jdbc:mysql://${master_host}:13306/${db_name}?useSSL=false&allowPublicKeyRetrieval=true&useUnicode=true&serverTimezone=Asia/Seoul
    slaves:
      slave1:
        name: slave1
        driver-class-name: com.mysql.cj.jdbc.Driver
        username: ${slave_username}
        password: ${slave_password}
        url: jdbc:mysql://${slave_host}:13307/${db_name}?useSSL=false&allowPublicKeyRetrieval=true&useUnicode=true&serverTimezone=Asia/Seoul

  jpa:
    database-platform: org.hibernate.dialect.MySQL5InnoDBDialect
    properties:
      hibernate:
        format_sql: true
        show_sql: true
        physical_naming_strategy: org.springframework.boot.orm.jpa.hibernate.SpringPhysicalNamingStrategy
        hbm2ddl:
          auto: create
      defer-datasource-initialization: true
```


`application.properties` 또는 `application.yml`에 데이터베이스 정보를 입력한다.



```bash
Caused by: com.mysql.jdbc.exceptions.jdbc4.MySQLNonTransientConnectionException: Public Key Retrieval is not allowed
```


MySQL 8.0부터 보안적인 이슈로 userSSL 옵션에 대한 추가적인 설정이 필요하다. MySQL의 SSL 접속을 끄기위해 `useSSL=false`를 기본적으로 세팅하게 되는데 `allowPublicKeyRetrieval=true`도 추가해주어야 한다.


### 1.2. build.gradle



```gradle
dependencies {
    // ...

    annotationProcessor 'org.springframework.boot:spring-boot-configuration-processor'
}
```


`@ConfigurationProperties` 어노테이션을 사용하기 위해 의존성을 추가한다.


### 1.3. POJO mapping



```java
@Getter
@Setter
@Component
@ConfigurationProperties(prefix = "spring.datasource")
public class ReplicationDataSourceProperties {
  private String driverClassName;
  private String username;
  private String password;
  private String url;
  private final Map<String, Slave> slaves = new HashMap<>();

  @Getter
  @Setter
  public static class Slave {
    private String name;
    private String driverClassName;
    private String username;
    private String password;
    private String url;
  }
}
```


prefix와 매칭되는 프로퍼티들을 자바 객체로 매핑한다.


2. Routing Data Source
----------------------


![](https://blog.kakaocdn.net/dn/PrXw0/btsEj8rbpSJ/G1tUptTVafzTccG50zZRe1/img.png)


`AbstractRoutingDataSource`는 Spring JDBC에 포함되어 있는 클래스로, lookup key를 기반으로 동적으로 타겟 Data Source를 변경한다.  
이 클래스를 상속해서 `determineCurrentLookupKey()`를 구현해야 한다.


### 2.1. 구현



```java
@Slf4j
public class ReplicationRoutingSource extends AbstractRoutingDataSource {
  private SlaveNames<String> slaveNames;

  // (1)
  @Override
  public void setTargetDataSources(Map<Object, Object> targetDataSources) {
    super.setTargetDataSources(targetDataSources);

    List<String> slaveNames = targetDataSources.keySet()
        .stream()
        .map(Object::toString)
        .filter(str -> str.contains(DataSourceType.SLAVE.getName()))
        .collect(Collectors.toList());

    this.slaveNames = new SlaveNames<>(slaveNames);
  }

  // (2)
  @Override
  protected Object determineCurrentLookupKey() {
    boolean isReadOnly = TransactionSynchronizationManager.isCurrentTransactionReadOnly();

    if (isReadOnly) {
      String nextSlaveName = slaveNames.getNext();
      log.info("Slave connected: {}", nextSlaveName);
      return nextSlaveName;
    }
    log.info("Master connected");
    return DataSourceType.MASTER.getName();
  }

  // (3)
  private static class SlaveNames<T> {
    private final List<T> values;
    private int index = 0;

    private SlaveNames(List<T> values) {
      this.values = values;
    }

    private T getNext() {
      if (index >= values.size() - 1) {
        index = -1;
      }
      return values.get(++index);
    }
  }
}
```


* (1) Data Source들을 targetDataSource에 할당하고 Slave의 Data Source명을 저장한다.
* (2) `TransactionSynchronizationManager`는 현재 요청에 할당된 쓰레드와 매핑된 트랜잭션을 가져온다. 현재 트랜잭션이 `@Transactional(readOnly=true)`면 Slave, `@Transactional`이면 Master의 Data Source명을 리턴한다.
* (3) 여러 개의 Slave를 사용할 경우 부하를 분산한다.


3. Bean 생성
----------



```java
@Configuration
@RequiredArgsConstructor
public class ReplicationDatasourceConfig {
  private final JpaProperties jpaProperties;
  private final ReplicationDataSourceProperties dataSourceProperties;

  @Bean
  public DataSource routingDataSource() {
    Map<Object, Object> targetDataSources = new HashMap<>();

    DataSource masterDataSource = createDataSource(
        dataSourceProperties.getDriverClassName(),
        dataSourceProperties.getUsername(),
        dataSourceProperties.getPassword(),
        dataSourceProperties.getUrl()
    );
    targetDataSources.put(DataSourceType.MASTER.getName(), masterDataSource);

    for (ReplicationDataSourceProperties.Slave slave : dataSourceProperties.getSlaves().values()) {
      DataSource slaveDataSource = createDataSource(
          slave.getDriverClassName(),
          slave.getUsername(),
          slave.getPassword(),
          slave.getUrl()
      );
      targetDataSources.put(slave.getName(), slaveDataSource);
    }

    ReplicationRoutingSource routingDataSource = new ReplicationRoutingSource();
    routingDataSource.setTargetDataSources(targetDataSources);
    routingDataSource.setDefaultTargetDataSource(masterDataSource);

    return routingDataSource;
  }

  private DataSource createDataSource(String driverClassName, String userName, String password, String uri) {
    return DataSourceBuilder.create()
        .type(HikariDataSource.class)
        .driverClassName(driverClassName)
        .username(userName)
        .password(password)
        .url(uri)
        .build();
  }

  @Bean
  public DataSource lazyRoutingDataSource(@Qualifier("routingDataSource") DataSource routingDataSource) {
    return new LazyConnectionDataSourceProxy(routingDataSource);
  }

  @Bean
  public LocalContainerEntityManagerFactoryBean entityManagerFactory(@Qualifier("lazyRoutingDataSource") DataSource dataSource) {
    EntityManagerFactoryBuilder entityManagerFactoryBuilder = createEntityManagerFactoryBuilder(jpaProperties);
    return entityManagerFactoryBuilder.dataSource(dataSource)
        .packages("com.foo")
        .build();
  }

  private EntityManagerFactoryBuilder createEntityManagerFactoryBuilder(JpaProperties jpaProperties) {
    return new EntityManagerFactoryBuilder(new HibernateJpaVendorAdapter(), jpaProperties.getProperties(), null);
  }

  @Bean
  public PlatformTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
    JpaTransactionManager transactionManager = new JpaTransactionManager();
    transactionManager.setEntityManagerFactory(entityManagerFactory);
    return transactionManager;
  }
}
```


### 3.1. routingDataSource()


Master와 Slave의 Data Source를 생성하고 구현한 Routing Data Source에 할당한다.


### 3.2. lazyRoutingDataSource()


Spring은 트랜잭션 시작 시점에(쿼리를 실행하기 전에) Data Source에서 Connection을 획득한다. 즉, 현재 스레드에 매핑된 트랜잭션을 가져올 수 없어서 `DefaultTargetDataSource`로 할당한 Master의 Connection만 얻게 된다.



> TransactionManager 식별 -> Data Source에서 Connection 획득 -> 트랜잭션 동기화

따라서 `LazyConnectionDataSourceProxy` 객체를 사용해서 쿼리를 실행할 때 Connection을 가져올 수 있도록 구현해야 한다.



> TransactionManager 식별 -> Connection Proxy 객체 획득 -> 트랜잭션 동기화 -> 실제 쿼리 호출 시 getConnection() -> determineCurrentLookupKey() 호출

### 3.3. entityManagerFactory()


직접 생성한 Data Source와 JPA 설정을 EntityManagerFactory에 주입한다.  
packages는 엔티티가 위치한 패키지 경로를 지정한다.


### 3.4. transactionManager()


트랜잭션 관리를 도와주는 transactionManager를 등록한다. `PlatformTransactionManager` 인터페이스로 추상화되어 있다.


4. Test
-------



```java
@SpringBootTest
public class DataSourceTest {
  public final String TEST_METHOD = "determineCurrentLookupKey";

  @Test
  @DisplayName("Master Data Source")
  @Transactional
  void masterDataSourceTest(@Qualifier("routingDataSource") DataSource routingDataSource) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method determineCurrentLookupKey = AbstractRoutingDataSource.class.getDeclaredMethod(TEST_METHOD);
    determineCurrentLookupKey.setAccessible(true);

    String dataSourceType = (String) determineCurrentLookupKey.invoke(routingDataSource);

    assertThat(dataSourceType).isEqualTo(DataSourceType.MASTER.getName());
  }

  @Test
  @DisplayName("Slave Data Source")
  @Transactional(readOnly = true)
  void slaveDataSourceTest(@Qualifier("routingDataSource") DataSource routingDataSource) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Method determineCurrentLookupKey = AbstractRoutingDataSource.class.getDeclaredMethod(TEST_METHOD);
    determineCurrentLookupKey.setAccessible(true);

    String dataSourceType = (String) determineCurrentLookupKey.invoke(routingDataSource);

    assertThat(dataSourceType).contains(DataSourceType.SLAVE.getName());
  }
}
```


`determineCurrentLookupKey()` 메서드가 `@Transactional(readOnly = true | false)`에 따라 Data Source를 분기해서 처리하는지 테스트한다.  
![](https://blog.kakaocdn.net/dn/EQYjD/btsEf7G4X7Z/ByxPcqYSo5b00NcY1yoPn0/img.png)


### 4.1. 로그 확인


![](https://blog.kakaocdn.net/dn/NZ23q/btsEhUAkmi2/2WGEkCF1yznPk8DTdm7Vsk/img.png)  
데이터를 저장하면 Master의 Connection을 획득한다.


![](https://blog.kakaocdn.net/dn/bcJFmP/btsEkgbrMgH/lkh0gs4xbgChUKvUUPLtp0/img.png)  
데이터를 조회하면 Slave의 Connection을 획득한다.


Reference
---------


<https://docs.spring.io/spring-boot/docs/current/reference/html/data.html#data.sql.datasource>  
<https://tecoble.techcourse.co.kr/post/2023-06-28-JDBC-DataSource/>  
<https://docs.spring.io/spring-boot/docs/current/reference/html/howto.html#howto.data-access>  
<https://runebook.dev/en/docs/spring_boot/howto?page=11>  
<https://lemontia.tistory.com/967>  
<https://vladmihalcea.com/read-write-read-only-transaction-routing-spring/>

