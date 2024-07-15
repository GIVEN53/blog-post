MySQL Replication 구성하기 - 1 with Docker
=
과거에 진행했던 코인 모의투자 프로젝트에서 겪었던 문제와 Replication을 구성한 내용을 작성해보려고 한다.


1\. 배경
------


맡았던 도메인은 사용자의 매수, 매도 주문이었고 기능 중 하나는 주문이 체결될 때마다 거래 내역을 생성해서 데이터베이스에 저장하는 것이었다. 코인의 거래량 자체가 적거나 실시간으로 거래량이 치솟아도 사용자가 걸어둔 미체결 주문량이 적으면 문제가 없었지만, 반대의 경우 거래 내역을 조회할 때 레이턴시가 길어지는 문제가 발생했다. 단주매매처럼 트래픽이 급격하게 증가하면 3초가 넘기도 했다.  
insert 트랜잭션이 커넥션을 많이 점유해서 병목이 생긴 것은 아닐까 싶었지만 커넥션풀 사이즈를 조정해도 큰 변화는 없었다. 그래서 read, write 쿼리에 따라 부하를 분산할 수 있는 replication을 검토하게 되었고 write가 많은 프로젝트 특징때문에 async 방식을 선택했다.


[MySQL Replication 구조](https://given-dev.tistory.com/112)에서 replication에 대한 내용을 확인할 수 있다.


### 1\.1\. version


* MySQL 8\.0\.32
* Docker 23\.0\.1
* Ubuntu 22\.04\.2


### 1\.2\. 디렉토리 구조


![](https://blog.kakaocdn.net/dn/brIIaC/btsEcrZA4RV/x8KEMCO2tT8gPbV47cruV0/img.png)



2\. docker\-compose
-------------------


Master에 데이터가 존재하면 `mysqldump`를 사용해서 Slave와 싱크를 맞춘 후에 replication을 설정해야 한다. 개발 환경에서 진행했기 때문에 데이터 덤프를 건너뛰고 docker와 쉘 스크립트를 이용해서 replication 설정을 자동화하는 것에 초점을 두었다.



```yml
version: "3"
services:
  db-master:
    container_name: mysql-master
    build:
      context: ./mysql/master/
      dockerfile: Dockerfile
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_USER_PASSWORD: ${MYSQL_USER_PASSWORD}
      MYSQL_DB: ${MYSQL_DB}
    ports:
      - "13306:3306"
    volumes:
      - master_vol:/var/lib/mysql
      - ./mysql/master/scripts:/docker-entrypoint-initdb.d
    networks:
      net-mysql:
        ipv4_address: 172.28.0.2

  db-slave:
    container_name: mysql-slave
    build:
      context: ./mysql/slave
      dockerfile: Dockerfile
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_USER_PASSWORD: ${MYSQL_USER_PASSWORD}
      MYSQL_DB: ${MYSQL_DB}
    ports:
      - "13307:3306"
    volumes:
      - slave_vol:/var/lib/mysql
      - ./mysql/slave/scripts:/docker-entrypoint-initdb.d
    networks:
      net-mysql:
        ipv4_address: 172.28.0.3
    depends_on:
      - db-master

volumes:
  master_vol:
  slave_vol:

networks:
  net-mysql:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```


* **services**: 컨테이너를 정의한다.
* **build**: Dockerfile로 이미지를 빌드할 경우 파일 경로와 파일명을 입력한다.
* **restart**: 컨테이너의 재시작 정책을 사용한다. [Docker Documentation](https://docs.docker.com/config/containers/start-containers-automatically/)
* **environment**: 환경 변수를 설정한다. `MYSQL_ROOT_PASSWORD`는 필수이다. [MySQL Dockerhub](https://hub.docker.com/_/mysql/)
* **ports**: 포트를 바인딩한다. `host_port:container_port`
* **volumes**: 볼륨 마운트, 바인드 마운트를 설정한다.
	+ volume mount: `volume_name:container_path`
	+ bind mount: `host_path:container_path`
* **networks**: 컨테이너에서 사용할 ip를 설정한다.


### 2\.1\. docker\-entrypoint\-initdb.d


![](https://blog.kakaocdn.net/dn/cZNsVu/btsEfm5jiQ1/6sxW6WBmiaT9GMY6ZHYUx0/img.png)



MySQL 이미지의 layer를 보면 `/usr/local/bin/docker-entrypoint.sh` 스크립트가 entrypoint이고, 정의된 코드는 아래와 같다.



```bash
declare -g DATABASE_ALREADY_EXISTS
if [ -d "$DATADIR/mysql" ]; then
    DATABASE_ALREADY_EXISTS='true'
fi

# Some Logic...

if [ -z "$DATABASE_ALREADY_EXISTS" ]; then
    docker_verify_minimum_env

    # check dir permissions to reduce likelihood of half-initialized database
    ls /docker-entrypoint-initdb.d/ > /dev/null
    docker_init_database_dir "$@"
    mysql_note "Starting temporary server"
    docker_temp_server_start "$@"
    mysql_note "Temporary server started."
    mysql_socket_fix
    docker_setup_db
    docker_process_init_files /docker-entrypoint-initdb.d/*
    mysql_expire_root_user
    mysql_note "Stopping temporary server"
    docker_temp_server_stop
    mysql_note "Temporary server stopped"
    echo
    mysql_note "MySQL init process done. Ready for start up."
    echo
else
    mysql_socket_fix
fi
```


`/var/lib/mysql` 디렉토리가 존재하지 않으면, 즉 컨테이너를 처음 생성하면 `/docker-entrypoint-initdb.d` 디렉토리 내의 파일들을 실행하게 된다.  
따라서 replication을 설정하는 스크립트 파일을 `/docker-entrypoint-initdb.d`로 바인드 마운트해서 최초 한 번만 스크립트를 실행하도록 한다.



> Shell Script 조건식 연산자  
> `-d`: 디렉토리면 true  
> `-z`: 문자열이 null or 길이가 0이면 true

3\. Master 설정
-------------


### 3\.1\. my.cnf



```vim
[mysqld]
server-id=1
log-bin=mysql-bin
expire_logs_days=10
binlog_cache_size=2M
max_binlog_size=100M
lower_case_table_names=1
log_error=/var/log/mysql/error.log
```


* **server\-id**: MySQL 서버가 각자 갖고 있는 고유한 식별 값이다. Slave의 server\-id와 달라야 한다.
* **log\-bin**: Binary Log의 파일명이다. 절대 경로를 추가해서 다른 디렉토리를 지정할 수 있다.
* **expire\_logs\_days**: Binary Log의 보관 주기를 설정한다.
* **binlog\_cache\_size**: Binary Log의 변경 이벤트를 보관할 메모리 버퍼 사이즈를 설정한다.
* **max\_binlog\_size**: Binary Log의 최대 사이즈를 설정한다.
* **lower\_case\_table\_names**: 1일 경우 대소문자를 구분하지 않는다.
* **log\_error**: 에러를 기록할 log 파일을 설정한다.


추가적으로 필요한 파라미터가 있으면 [MySQL Documentation](https://dev.mysql.com/doc/refman/8.0/en/replication-options.html)에서 확인할 수 있다.


### 3\.2\. Dockerfile



```docker
FROM mysql:8.0.32-debian

USER root
COPY ./master.cnf /etc/mysql/my.cnf
RUN mkdir /var/log/mysql && touch /var/log/mysql/error.log && chmod -R 777 /var/log/mysql/
```


* FROM: build할 이미지
* USER: 커맨드를 수행할 OS user
* COPY: host의 파일이나 디렉토리를 컨테이너로 복사
* RUN: 컨테이너에서 수행할 커맨드



> `my.cnf`의 우선 순위
> 
> 
> 1. /etc/my.cnf
> 2. /etc/mysql/my.cnf
> 3. /usr/local/etc/my.cnf
> 4. \~/my.cnf

### 3\.3\. entrypoint


`./mysql/master/scripts/`경로에 생성한 스크립트 파일이다. 컨테이너의 `/docker-entrypoint-initdb.d` 경로로 마운트되고 컨테이너가 최초 생성될 때 스크립트를 실행한다.



```bash
#!/bin/bash
# (1)
set -e

# (2)
until mysqladmin -u root -p"${MYSQL_ROOT_PASSWORD}" ping; do
  echo "# waiting for mysql - $(date)"
  sleep 3
done

# (3)
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER 'replUser'@'172.28.0.%' IDENTIFIED BY '${MYSQL_USER_PASSWORD}'"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON *.* TO 'replUser'@'172.28.0.%' WITH GRANT OPTION"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT REPLICATION SLAVE ON *.* TO 'replUser'@'172.28.0.%'"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES"
```


* (1\) 쉘 스크립트에서 에러가 발생하면 즉시 스크립트를 종료한다.
* (2\) MySQL 서버가 완전히 실행되기 전에 script가 먼저 실행되기 때문에 에러가 발생한다. 따라서 서버가 정상 실행될 때까지 ping 명령어로 확인하면서 기다린다.
* (3\) replication 권한이 부여된 사용자를 생성한다.


4\. Slave 설정
------------


### 4\.1\. my.cnf



```vim
[mysqld]
server-id=2
log-bin=mysql-bin
relay_log=/var/lib/mysql/mysql-relay-bin
#log_replica_updates=ON
expire_logs_days=10
binlog_cache_size=2M
max_binlog_size=100M
read_only=ON
lower_case_table_names=1
log_error=/var/log/mysql/error.log
```


* **server\-id**: Master의 server\-id와 다른 값을 사용한다.
* **relay\_log**: Relay Log의 경로이다.
* **log\_replica\_updates**: Master로부터 전달받은 Binary Log를 Slave의 Binary Log에도 기록할지 여부를 설정하며 기본값은 ON이다.  
 MySQL 8\.0\.26 이전 릴리즈는 `log_slave_updates`을 사용하고 기본값은 OFF이다.
* **read\_only**: 읽기만 허용한다.



> server\-id는 Binary Log에 쌓이는 이벤트들이 어떤 서버에서 발생한 이벤트인지 식별하기 위해 사용된다. Master와 값이 동일할 경우 Master에서 발생한 이벤트여도 Slave에서 발생한 이벤트로 보고 동기화를 진행하지 않는다. 따라서 replication 구성에 포함된 서버들은 각자 고유한 server\-id를 갖도록 설정해야 한다.

### 4\.2\. Dockerfile



```docker
FROM mysql:8.0.32-debian

USER root
COPY ./slave.cnf /etc/mysql/my.cnf
RUN mkdir /var/log/mysql && touch /var/log/mysql/error.log && chmod -R 777 /var/log/mysql/
```


Master의 Dockerfile과 동일하다.


### 4\.3\. entrypoint


`./mysql/slave/scripts/`경로에 있는 스크립트 파일이다. 컨테이너의 `/docker-entrypoint-initdb.d` 경로로 마운트되고 컨테이너가 최초 생성될 때 스크립트를 실행한다.



```bash
#!/bin/bash
set -e

# (1)
until mysqladmin -u root -p"${MYSQL_ROOT_PASSWORD}" -h 172.28.0.2 ping; do
  echo "# waiting for master - $(date)"
  sleep 3
done

# (2)
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER 'replUser'@'172.28.0.%' IDENTIFIED BY '${MYSQL_USER_PASSWORD}'"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON *.* TO 'replUser'@'172.28.0.%' WITH GRANT OPTION"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES"

# (3)
source_log_file=$(mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -h 172.28.0.2 -e "SHOW MASTER STATUS\G" | grep mysql-bin)
re="[a-z]*-bin.[0-9]*"
if [[ $source_log_file =~ $re ]];then
  source_log_file=${BASH_REMATCH[0]}
fi

# (4)
source_log_pos=$(mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -h 172.28.0.2 -e "SHOW MASTER STATUS\G" | grep Position)
re="[0-9]+"
if [[ $source_log_pos =~ $re ]];then
  source_log_pos=${BASH_REMATCH[0]}
fi

# (5)
sql="CHANGE REPLICATION SOURCE TO SOURCE_HOST='172.28.0.2', SOURCE_USER='replUser', SOURCE_PASSWORD='${MYSQL_USER_PASSWORD}', SOURCE_LOG_FILE='${source_log_file}', SOURCE_LOG_POS=${source_log_pos}, GET_SOURCE_PUBLIC_KEY=1"

mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "${sql}"
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "START REPLICA"

# (6)
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -h 172.28.0.2 -e "CREATE DATABASE ${MYSQL_DB}"
```


* (1\) Slave에서 Master로 접근하기 때문에 Master가 완전히 실행될 때까지 기다린다.
* (2\) Slave의 사용자를 생성한다.
* (3\) Master에 접속해서 Binary Log 파일명을 변수에 저장한다.
* (4\) Master에 접속해서 Binary Log의 현재 위치를 변수에 저장한다.

```sql
SHOW MASTER STATUS\G;
```


Slave에 Master 정보를 등록하려면 Master에서 위 명령어를 실행해서 File과 Position 값을 가져와야 한다.  
![](https://blog.kakaocdn.net/dn/brdZrF/btsEaWlOogf/4zkqKLyiK7cSII23WillsK/img.png)




- (5\) Slave에서 Master의 정보를 입력하고 replication을 시작한다.

```sql
CHANGE MASTER TO
MASTER_HOST='호스트명 or ip',
MASTER_USER='replication 유저명',
MASTER_PASSWORD='패스워드',
MASTER_LOG_FILE='Binary Log 파일명',
MASTER_LOG_POS=Binary Log 현재 위치,
GET_MASTER_PUBLIC_KEY=1;
-- or from MySQL 8.0.23:
CHANGE REPLICATION SOURCE TO
SOURCE_HOST='호스트명 or ip',
SOURCE_USER='replication 유저명',
SOURCE_PASSWORD='패스워드',
SOURCE_LOG_FILE='Binary Log 파일명',
SOURCE_LOG_POS=Binary Log 현재 위치,
GET_SOURCE_PUBLIC_KEY=1;

START SLAVE;
-- or from MySQL 8.0.22:
START REPLICA;
```


MySQL 8\.0부터 caching\_sha2\_password 플러그인이 기본값이다.  
caching\_sha2\_password 플러그인으로 인증하는 사용자 계정을 사용할 때 Master와 SSL 기반의 보안 연결을 적용하지 않으면 아래와 같은 에러가 발생한다.



```bash
error connecting to master 'replUser@172.28.0.2:3306' - retry-time: 60 retries: 1 message:
Authentication plugin 'caching_sha2_password' reported error: Authentication requires secure connection.
```


해결하려면 `GET_SOURCE_PUBLIC_KEY`을 사용해서 RSA key pair 기반의 암호 교환을 활성화해야 한다.



- (6\) Master에 접속해서 데이터베이스를 생성한다.
> Master에 데이터베이스를 먼저 생성하고 replication을 설정하면 position이 데이터베이스 생성 후의 위치로 저장되기 때문에 Slave에 데이터베이스가 생성되지 않는다.


5\. 결과
------



```bash
docker-compose up -d
```


`docker-compose.yml`에 정의된 컨테이너를 생성한다.



```sql
SHOW SLAVE STATUS\G;
-- or from MySQL 8.0.22:
SHOW REPLICA STATUS\G;
```


Slave에 접속해서 명령어를 실행하면 성공적으로 연결되었음을 확인할 수 있다.  
![](https://blog.kakaocdn.net/dn/DLA21/btsEdVMNbAn/CY1xY4f5oLUXIpL1YHIGH0/img.png)



Reference
---------


[https://dev.mysql.com/doc/refman/8\.0/en/replication\-howto.html](https://dev.mysql.com/doc/refman/8.0/en/replication-howto.html)  
[https://dev.mysql.com/doc/refman/8\.0/en/sql\-replication\-statements.html](https://dev.mysql.com/doc/refman/8.0/en/sql-replication-statements.html)  
[https://huisam.tistory.com/entry/mysql\-replication](https://huisam.tistory.com/entry/mysql-replication)

