MySQL Replication 구성하기 - 1 with Docker
=
<p>과거에 진행했던 코인 모의투자 프로젝트에서 겪었던 문제와 Replication을 구성한 내용을 작성해보려고 한다.</p>
<h2>1. 배경</h2>
<p>맡았던 도메인은 사용자의 매수, 매도 주문이었고 기능 중 하나는 주문이 체결될 때마다 거래 내역을 생성해서 데이터베이스에 저장하는 것이었다. 코인의 거래량 자체가 적거나 실시간으로 거래량이 치솟아도 사용자가 걸어둔 미체결 주문량이 적으면 문제가 없었지만, 반대의 경우 거래 내역을 조회할 때 레이턴시가 길어지는 문제가 발생했다. 단주매매처럼 트래픽이 급격하게 증가하면 3초가 넘기도 했다.<br>insert 트랜잭션이 커넥션을 많이 점유해서 병목이 생긴 것은 아닐까 싶었지만 커넥션풀 사이즈를 조정해도 큰 변화는 없었다. 그래서 read, write 쿼리에 따라 부하를 분산할 수 있는 replication을 검토하게 되었고 write가 많은 프로젝트 특징때문에 async 방식을 선택했다.</p>
<p><a href="https://given-dev.tistory.com/112">MySQL Replication 구조</a>에서 replication에 대한 내용을 확인할 수 있다.</p>
<h3>1.1. version</h3>
<ul>
<li>MySQL 8.0.32</li>
<li>Docker 23.0.1</li>
<li>Ubuntu 22.04.2</li>
</ul>
<h3>1.2. 디렉토리 구조</h3>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/brIIaC/btsEcrZA4RV/x8KEMCO2tT8gPbV47cruV0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/brIIaC/btsEcrZA4RV/x8KEMCO2tT8gPbV47cruV0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbrIIaC%2FbtsEcrZA4RV%2Fx8KEMCO2tT8gPbV47cruV0%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<h2>2. docker-compose</h2>
<p>Master에 데이터가 존재하면 <code>mysqldump</code>를 사용해서 Slave와 싱크를 맞춘 후에 replication을 설정해야 한다. 개발 환경에서 진행했기 때문에 데이터 덤프를 건너뛰고 docker와 쉘 스크립트를 이용해서 replication 설정을 자동화하는 것에 초점을 두었다.</p>
<pre><code class="yml">version: "3"
services:
 db-master:
 container\_name: mysql-master
 build:
 context: ./mysql/master/
 dockerfile: Dockerfile
 restart: always
 environment:
 MYSQL\_ROOT\_PASSWORD: ${MYSQL\_ROOT\_PASSWORD}
 MYSQL\_USER\_PASSWORD: ${MYSQL\_USER\_PASSWORD}
 MYSQL\_DB: ${MYSQL\_DB}
 ports:
 - "13306:3306"
 volumes:
 - master\_vol:/var/lib/mysql
 - ./mysql/master/scripts:/docker-entrypoint-initdb.d
 networks:
 net-mysql:
 ipv4\_address: 172.28.0.2

 db-slave:
 container\_name: mysql-slave
 build:
 context: ./mysql/slave
 dockerfile: Dockerfile
 restart: always
 environment:
 MYSQL\_ROOT\_PASSWORD: ${MYSQL\_ROOT\_PASSWORD}
 MYSQL\_USER\_PASSWORD: ${MYSQL\_USER\_PASSWORD}
 MYSQL\_DB: ${MYSQL\_DB}
 ports:
 - "13307:3306"
 volumes:
 - slave\_vol:/var/lib/mysql
 - ./mysql/slave/scripts:/docker-entrypoint-initdb.d
 networks:
 net-mysql:
 ipv4\_address: 172.28.0.3
 depends\_on:
 - db-master

volumes:
 master\_vol:
 slave\_vol:

networks:
 net-mysql:
 driver: bridge
 ipam:
 config:
 - subnet: 172.28.0.0/16</code></pre>
<ul>
<li><strong>services</strong>: 컨테이너를 정의한다.</li>
<li><strong>build</strong>: Dockerfile로 이미지를 빌드할 경우 파일 경로와 파일명을 입력한다.</li>
<li><strong>restart</strong>: 컨테이너의 재시작 정책을 사용한다. <a href="https://docs.docker.com/config/containers/start-containers-automatically/">Docker Documentation</a></li>
<li><strong>environment</strong>: 환경 변수를 설정한다. <code>MYSQL\_ROOT\_PASSWORD</code>는 필수이다. <a href="https://hub.docker.com/\_/mysql/">MySQL Dockerhub</a></li>
<li><strong>ports</strong>: 포트를 바인딩한다. <code>host\_port:container\_port</code></li>
<li><strong>volumes</strong>: 볼륨 마운트, 바인드 마운트를 설정한다.<ul>
<li>volume mount: <code>volume\_name:container\_path</code></li>
<li>bind mount: <code>host\_path:container\_path</code></li>
</ul>
</li>
<li><strong>networks</strong>: 컨테이너에서 사용할 ip를 설정한다.</li>
</ul>
<h3>2.1. docker-entrypoint-initdb.d</h3>
<p><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/cZNsVu/btsEfm5jiQ1/6sxW6WBmiaT9GMY6ZHYUx0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/cZNsVu/btsEfm5jiQ1/6sxW6WBmiaT9GMY6ZHYUx0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcZNsVu%2FbtsEfm5jiQ1%2F6sxW6WBmiaT9GMY6ZHYUx0%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<p>MySQL 이미지의 layer를 보면 <code>/usr/local/bin/docker-entrypoint.sh</code> 스크립트가 entrypoint이고, 정의된 코드는 아래와 같다.</p>
<pre><code class="bash">declare -g DATABASE\_ALREADY\_EXISTS
if [ -d "$DATADIR/mysql" ]; then
 DATABASE\_ALREADY\_EXISTS='true'
fi

# Some Logic...

if [ -z "$DATABASE\_ALREADY\_EXISTS" ]; then
 docker\_verify\_minimum\_env

 # check dir permissions to reduce likelihood of half-initialized database
 ls /docker-entrypoint-initdb.d/ > /dev/null
 docker\_init\_database\_dir "$@"
 mysql\_note "Starting temporary server"
 docker\_temp\_server\_start "$@"
 mysql\_note "Temporary server started."
 mysql\_socket\_fix
 docker\_setup\_db
 docker\_process\_init\_files /docker-entrypoint-initdb.d/\*
 mysql\_expire\_root\_user
 mysql\_note "Stopping temporary server"
 docker\_temp\_server\_stop
 mysql\_note "Temporary server stopped"
 echo
 mysql\_note "MySQL init process done. Ready for start up."
 echo
else
 mysql\_socket\_fix
fi</code></pre>
<p><code>/var/lib/mysql</code> 디렉토리가 존재하지 않으면, 즉 컨테이너를 처음 생성하면 <code>/docker-entrypoint-initdb.d</code> 디렉토리 내의 파일들을 실행하게 된다.<br>따라서 replication을 설정하는 스크립트 파일을 <code>/docker-entrypoint-initdb.d</code>로 바인드 마운트해서 최초 한 번만 스크립트를 실행하도록 한다.</p>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>Shell Script 조건식 연산자<br><code>-d</code>: 디렉토리면 true<br><code>-z</code>: 문자열이 null or 길이가 0이면 true</p>
</span></p></blockquote><h2>3. Master 설정</h2>
<h3>3.1. my.cnf</h3>
<pre><code class="vim">[mysqld]
server-id=1
log-bin=mysql-bin
expire\_logs\_days=10
binlog\_cache\_size=2M
max\_binlog\_size=100M
lower\_case\_table\_names=1
log\_error=/var/log/mysql/error.log</code></pre>
<ul>
<li><strong>server-id</strong>: MySQL 서버가 각자 갖고 있는 고유한 식별 값이다. Slave의 server-id와 달라야 한다.</li>
<li><strong>log-bin</strong>: Binary Log의 파일명이다. 절대 경로를 추가해서 다른 디렉토리를 지정할 수 있다.</li>
<li><strong>expire\_logs\_days</strong>: Binary Log의 보관 주기를 설정한다.</li>
<li><strong>binlog\_cache\_size</strong>: Binary Log의 변경 이벤트를 보관할 메모리 버퍼 사이즈를 설정한다.</li>
<li><strong>max\_binlog\_size</strong>: Binary Log의 최대 사이즈를 설정한다.</li>
<li><strong>lower\_case\_table\_names</strong>: 1일 경우 대소문자를 구분하지 않는다.</li>
<li><strong>log\_error</strong>: 에러를 기록할 log 파일을 설정한다.</li>
</ul>
<p>추가적으로 필요한 파라미터가 있으면 <a href="https://dev.mysql.com/doc/refman/8.0/en/replication-options.html">MySQL Documentation</a>에서 확인할 수 있다.</p>
<h3>3.2. Dockerfile</h3>
<pre><code class="docker">FROM mysql:8.0.32-debian

USER root
COPY ./master.cnf /etc/mysql/my.cnf
RUN mkdir /var/log/mysql && touch /var/log/mysql/error.log && chmod -R 777 /var/log/mysql/</code></pre>
<ul>
<li>FROM: build할 이미지</li>
<li>USER: 커맨드를 수행할 OS user</li>
<li>COPY: host의 파일이나 디렉토리를 컨테이너로 복사</li>
<li>RUN: 컨테이너에서 수행할 커맨드</li>
</ul>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p><code>my.cnf</code>의 우선 순위</p>
<ol>
<li>/etc/my.cnf</li>
<li>/etc/mysql/my.cnf</li>
<li>/usr/local/etc/my.cnf</li>
<li>~/my.cnf</li>
</ol>
</span></p></blockquote><h3>3.3. entrypoint</h3>
<p><code>./mysql/master/scripts/</code>경로에 생성한 스크립트 파일이다. 컨테이너의 <code>/docker-entrypoint-initdb.d</code> 경로로 마운트되고 컨테이너가 최초 생성될 때 스크립트를 실행한다.</p>
<pre><code class="bash">#!/bin/bash
# (1)
set -e

# (2)
until mysqladmin -u root -p"${MYSQL\_ROOT\_PASSWORD}" ping; do
 echo "# waiting for mysql - $(date)"
 sleep 3
done

# (3)
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "CREATE USER 'replUser'@'172.28.0.%' IDENTIFIED BY '${MYSQL\_USER\_PASSWORD}'"
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "GRANT ALL PRIVILEGES ON \*.\* TO 'replUser'@'172.28.0.%' WITH GRANT OPTION"
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "GRANT REPLICATION SLAVE ON \*.\* TO 'replUser'@'172.28.0.%'"
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "FLUSH PRIVILEGES"</code></pre>
<ul>
<li>(1) 쉘 스크립트에서 에러가 발생하면 즉시 스크립트를 종료한다.</li>
<li>(2) MySQL 서버가 완전히 실행되기 전에 script가 먼저 실행되기 때문에 에러가 발생한다. 따라서 서버가 정상 실행될 때까지 ping 명령어로 확인하면서 기다린다.</li>
<li>(3) replication 권한이 부여된 사용자를 생성한다.</li>
</ul>
<h2>4. Slave 설정</h2>
<h3>4.1. my.cnf</h3>
<pre><code class="vim">[mysqld]
server-id=2
log-bin=mysql-bin
relay\_log=/var/lib/mysql/mysql-relay-bin
#log\_replica\_updates=ON
expire\_logs\_days=10
binlog\_cache\_size=2M
max\_binlog\_size=100M
read\_only=ON
lower\_case\_table\_names=1
log\_error=/var/log/mysql/error.log</code></pre>
<ul>
<li><strong>server-id</strong>: Master의 server-id와 다른 값을 사용한다.</li>
<li><strong>relay\_log</strong>: Relay Log의 경로이다.</li>
<li><strong>log\_replica\_updates</strong>: Master로부터 전달받은 Binary Log를 Slave의 Binary Log에도 기록할지 여부를 설정하며 기본값은 ON이다.<br> MySQL 8.0.26 이전 릴리즈는 <code>log\_slave\_updates</code>을 사용하고 기본값은 OFF이다.</li>
<li><strong>read\_only</strong>: 읽기만 허용한다.</li>
</ul>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>server-id는 Binary Log에 쌓이는 이벤트들이 어떤 서버에서 발생한 이벤트인지 식별하기 위해 사용된다. Master와 값이 동일할 경우 Master에서 발생한 이벤트여도 Slave에서 발생한 이벤트로 보고 동기화를 진행하지 않는다. 따라서 replication 구성에 포함된 서버들은 각자 고유한 server-id를 갖도록 설정해야 한다.</p>
</span></p></blockquote><h3>4.2. Dockerfile</h3>
<pre><code class="docker">FROM mysql:8.0.32-debian

USER root
COPY ./slave.cnf /etc/mysql/my.cnf
RUN mkdir /var/log/mysql && touch /var/log/mysql/error.log && chmod -R 777 /var/log/mysql/</code></pre>
<p>Master의 Dockerfile과 동일하다.</p>
<h3>4.3. entrypoint</h3>
<p><code>./mysql/slave/scripts/</code>경로에 있는 스크립트 파일이다. 컨테이너의 <code>/docker-entrypoint-initdb.d</code> 경로로 마운트되고 컨테이너가 최초 생성될 때 스크립트를 실행한다.</p>
<pre><code class="bash">#!/bin/bash
set -e

# (1)
until mysqladmin -u root -p"${MYSQL\_ROOT\_PASSWORD}" -h 172.28.0.2 ping; do
 echo "# waiting for master - $(date)"
 sleep 3
done

# (2)
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "CREATE USER 'replUser'@'172.28.0.%' IDENTIFIED BY '${MYSQL\_USER\_PASSWORD}'"
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "GRANT ALL PRIVILEGES ON \*.\* TO 'replUser'@'172.28.0.%' WITH GRANT OPTION"
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "FLUSH PRIVILEGES"

# (3)
source\_log\_file=$(mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -h 172.28.0.2 -e "SHOW MASTER STATUS\G" | grep mysql-bin)
re="[a-z]\*-bin.[0-9]\*"
if [[ $source\_log\_file =~ $re ]];then
 source\_log\_file=${BASH\_REMATCH[0]}
fi

# (4)
source\_log\_pos=$(mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -h 172.28.0.2 -e "SHOW MASTER STATUS\G" | grep Position)
re="[0-9]+"
if [[ $source\_log\_pos =~ $re ]];then
 source\_log\_pos=${BASH\_REMATCH[0]}
fi

# (5)
sql="CHANGE REPLICATION SOURCE TO SOURCE\_HOST='172.28.0.2', SOURCE\_USER='replUser', SOURCE\_PASSWORD='${MYSQL\_USER\_PASSWORD}', SOURCE\_LOG\_FILE='${source\_log\_file}', SOURCE\_LOG\_POS=${source\_log\_pos}, GET\_SOURCE\_PUBLIC\_KEY=1"

mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "${sql}"
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -e "START REPLICA"

# (6)
mysql -u root -p"${MYSQL\_ROOT\_PASSWORD}" -h 172.28.0.2 -e "CREATE DATABASE ${MYSQL\_DB}"</code></pre>
<ul>
<li>(1) Slave에서 Master로 접근하기 때문에 Master가 완전히 실행될 때까지 기다린다.</li>
<li>(2) Slave의 사용자를 생성한다.</li>
<li>(3) Master에 접속해서 Binary Log 파일명을 변수에 저장한다.</li>
<li>(4) Master에 접속해서 Binary Log의 현재 위치를 변수에 저장한다.<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><pre><code class="sql">SHOW MASTER STATUS\G;</code></pre>
<p>Slave에 Master 정보를 등록하려면 Master에서 위 명령어를 실행해서 File과 Position 값을 가져와야 한다.<br><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/brdZrF/btsEaWlOogf/4zkqKLyiK7cSII23WillsK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/brdZrF/btsEaWlOogf/4zkqKLyiK7cSII23WillsK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbrdZrF%2FbtsEaWlOogf%2F4zkqKLyiK7cSII23WillsK%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
</span></p></blockquote></li>
<li>(5) Slave에서 Master의 정보를 입력하고 replication을 시작한다.<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><pre><code class="sql">CHANGE MASTER TO
MASTER\_HOST='호스트명 or ip',
MASTER\_USER='replication 유저명',
MASTER\_PASSWORD='패스워드',
MASTER\_LOG\_FILE='Binary Log 파일명',
MASTER\_LOG\_POS=Binary Log 현재 위치,
GET\_MASTER\_PUBLIC\_KEY=1;
-- or from MySQL 8.0.23:
CHANGE REPLICATION SOURCE TO
SOURCE\_HOST='호스트명 or ip',
SOURCE\_USER='replication 유저명',
SOURCE\_PASSWORD='패스워드',
SOURCE\_LOG\_FILE='Binary Log 파일명',
SOURCE\_LOG\_POS=Binary Log 현재 위치,
GET\_SOURCE\_PUBLIC\_KEY=1;

START SLAVE;
-- or from MySQL 8.0.22:
START REPLICA;</code></pre>
<p>MySQL 8.0부터 caching\_sha2\_password 플러그인이 기본값이다.<br>caching\_sha2\_password 플러그인으로 인증하는 사용자 계정을 사용할 때 Master와 SSL 기반의 보안 연결을 적용하지 않으면 아래와 같은 에러가 발생한다.</p>
<pre><code class="bash">error connecting to master 'replUser@172.28.0.2:3306' - retry-time: 60 retries: 1 message:
Authentication plugin 'caching\_sha2\_password' reported error: Authentication requires secure connection.</code></pre>
<p>해결하려면 <code>GET\_SOURCE\_PUBLIC\_KEY</code>을 사용해서 RSA key pair 기반의 암호 교환을 활성화해야 한다.</p>
</span></p></blockquote></li>
<li>(6) Master에 접속해서 데이터베이스를 생성한다.<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>Master에 데이터베이스를 먼저 생성하고 replication을 설정하면 position이 데이터베이스 생성 후의 위치로 저장되기 때문에 Slave에 데이터베이스가 생성되지 않는다.</p>
</span></p></blockquote></li>
</ul>
<h2>5. 결과</h2>
<pre><code class="bash">docker-compose up -d</code></pre>
<p><code>docker-compose.yml</code>에 정의된 컨테이너를 생성한다.</p>
<pre><code class="sql">SHOW SLAVE STATUS\G;
-- or from MySQL 8.0.22:
SHOW REPLICA STATUS\G;</code></pre>
<p>Slave에 접속해서 명령어를 실행하면 성공적으로 연결되었음을 확인할 수 있다.<br><figure class="imageblock alignCenter" width="100%"><span data-url="https://blog.kakaocdn.net/dn/DLA21/btsEdVMNbAn/CY1xY4f5oLUXIpL1YHIGH0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/DLA21/btsEdVMNbAn/CY1xY4f5oLUXIpL1YHIGH0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FDLA21%2FbtsEdVMNbAn%2FCY1xY4f5oLUXIpL1YHIGH0%2Fimg.png" width="100%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<h2>Reference</h2>
<p><a href="https://dev.mysql.com/doc/refman/8.0/en/replication-howto.html">https://dev.mysql.com/doc/refman/8.0/en/replication-howto.html</a><br><a href="https://dev.mysql.com/doc/refman/8.0/en/sql-replication-statements.html">https://dev.mysql.com/doc/refman/8.0/en/sql-replication-statements.html</a><br><a href="https://huisam.tistory.com/entry/mysql-replication">https://huisam.tistory.com/entry/mysql-replication</a></p>