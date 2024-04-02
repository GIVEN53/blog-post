MySQL Replication 구조
=
<h1>Replication</h1>
<p>두 개 이상의 데이터베이스를 Master, Slave 구조로 활용하여 Master 노드의 데이터를 Slave 노드로 복제, 동기화하는 기술이다.<br>Write 쿼리(<code>INSERT</code>, <code>UPATE</code>, <code>DELETE</code>)는 Master 노드에서 처리하고, Read 쿼리(<code>SELECT</code>)는 Slave 노드에서 처리한다.<br>MySQL 8.0부터는 Master/Slave를 Source, Replica로 명명하고 있다.</p>
<h3>사용 목적</h3>
<ol>
<li><strong>부하 분산</strong>: Read/Write 쿼리에 따라 Master, Slave의 부하를 분산하고, 쿼리의 약 80%가 읽기 작업이기 때문에 Slave를 Scale-Out하여 읽기 성능을 높일 수 있다.</li>
<li><strong>데이터 백업</strong>: Slave로 데이터가 복제되기 때문에 Master에 문제가 발생했을 때 피해를 최소화할 수 있다.</li>
<li><strong>지리적 분산</strong>: 글로벌 서비스의 경우 데이터베이스를 국가나 지역별로 분산 배치하여 빠르게 접근할 수 있다.</li>
</ol>
<h3>주의 사항</h3>
<ol>
<li>Master와 Slave 서버의 버전이 다를 경우 Slave 버전이 상위 버전이어야 한다.</li>
<li>서버 가동 시 Master -> Slave 순으로 가동해야 한다.</li>
</ol>
<h2>1. Replication 동작 방식</h2>
<p>Replication은 2개의 Log 파일과 3개의 쓰레드로 동작하며 기본적으로 <strong>비동기(async)</strong> 복제 방식을 사용한다.</p>
<h3>1.1. Async</h3>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="768" data-origin-height="513"><span data-url="https://blog.kakaocdn.net/dn/X3fsE/btsD7mqmT3N/BDRHpAvqhEMh4jvAfG5kn1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/X3fsE/btsD7mqmT3N/BDRHpAvqhEMh4jvAfG5kn1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FX3fsE%2FbtsD7mqmT3N%2FBDRHpAvqhEMh4jvAfG5kn1%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="768" data-origin-height="513"/></span></figure>
</p>
<p>Master에 commit된 내용이 Slave에 정상적으로 복제되었는지 확인하지 않고 Master의 트랜잭션을 종료 및 결과를 반환한다.</p>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>Client Commit -> Binlog Flush/Commit -> <strong>Engine Commit</strong> -> <strong>Client Commit OK Response</strong> -> <strong>Binlog dump Send Event without ACK Request</strong> -> Record Relay Log</p>
</span></p></blockquote><h4>장점</h4>
<ol>
<li>동기식 복제(sync)보다 쓰기 속도가 빠르다.</li>
<li>Slave에 장애가 발생해도 영향을 받지 않는다.</li>
<li>복제할 쿼리 양이 많아 Slave의 성능이 저하되어도 Master와는 무관하다.</li>
</ol>
<h4>단점</h4>
<ol>
<li>동기화를 보장하지 않아서 데이터 정합성이 깨질 수 있다.</li>
</ol>
<h4>1.1.1. Binary Log</h4>
<p>DDL, DML로 스키마 또는 데이터를 생성, 업데이트했을 때 변경된 이벤트를 저장하는 이진 파일이다. Replication 구성이나 특정 시점으로 복구할 때 사용한다.</p>
<h4>1.1.2. Binary Log Dump Thread(= Master Thread)</h4>
<p>Master와 Slave가 연결되면(START SLAVE) Binary Log Dump Thread를 생성한다. 여러 개의 Slave가 연결되어도 하나의 쓰레드만 생성된다. 해당 쓰레드는 Slave I/O Thread로부터 요청이 오면 Master의 Binary Log를 읽어서 Slave로 전송한다.</p>
<h4>1.1.3. Slave I/O Thread</h4>
<p>Slave에서 START SLAVE 명령어가 실행되면 Slave는 Master와 연결하고 I/O Thread를 생성한다. 해당 쓰레드는 offset을 기억하고 있다가 Master에게 다음 이벤트를 요청한다. Master의 Binary Log Dump Thread가 이벤트를 전송하면 Slave의 Relay Log에 저장한다.</p>
<h4>1.1.4. Relay Log</h4>
<p>전달받은 Binary Log를 Slave에 기록하기 위한 로그 파일이다. Master의 Binary Log Format과 정확하게 일치하며 인덱스 파일도 똑같이 존재한다. Slave는 3개의 조건 중 하나를 만족하면 새로운 Relay Log 파일을 생성한다.</p>
<ol>
<li>Slave I/O Thread가 시작될 때</li>
<li>로그가 flush될 때</li>
<li>로그 파일의 크기가 너무 커질 때 (<code>max\_relay\_log\_size</code> 파라미터의 영향을 받는다.)</li>
</ol>
<h4>1.1.5. Slave SQL Thread</h4>
<p>Relay Log에 저장된 이벤트를 읽어서 Slave의 스토리지 엔진에 반영하고, 이벤트를 모두 실행한 후 더 이상 필요하지 않으면 Relay Log 파일을 자동으로 삭제한다.<br>보통 <code>mysqldump</code>로 데이터를 백업해서 아카이브를 만드는데, mysqldump는 MySQL이 쿼리를 실행하고 있을 때 실행되면 데이터 정합성이 깨지는 문제가 발생한다. 그러나 replication을 사용할 경우 Slave SQL thread만 정지시키면 되기 때문에 안전하게 백업을 만들 수 있다.</p>
<pre><code class="sql">STOP SLAVE SQL\_THREAD;
-- from MySQL 8.0.22:
STOP REPLICA SQL\_THREAD;</code></pre>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>Master에서는 여러 쓰레드로부터 변경이 발생하지만 Slave에서는 하나의 SQL Thread가 DB 반영 작업을 수행하기 때문에 병목이 발생할 수 있다. 이를 해결하기 위해 MySQL 5.6부터 <code>DATABASE</code> 기반의 MTS(Multi Threaded Slave 또는 MTR: Multi Threaded Replication)기능이 추가됐으며, MySQL 5.7에서는 5.6 버전의 단점을 개선하여 <code>LOGICAL\_CLOCK</code> 기반으로 병렬 복제할 수 있게 되었다.</p>
</span></p></blockquote><p>Slave에서 <code>log-slave-updates</code> 파라미터를 활성화하면 SQL Thread에서 수행되는 이벤트를 자신의 Binary Log에도 기록할 수 있다. <a href="https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar\_log\_replica\_updates">MySQL Documentation</a><br>예를 들어 <code>A -> B -> C</code>의 replication을 구성할 경우 B는 A의 Slave이면서 C의 Master 역할을 수행함으로써 <strong>Chained Replication</strong>을 적용할 수 있다.</p>
<pre><code class="bash">[mysqld]
log-slave-updates=ON
# from MySQL 8.0.26:
log-replica-updates=ON</code></pre>
<h3>1.2. Semi-sync</h3>
<p>MySQL 5.5부터 도입됐으며 Master에서 Slave로 전송된 이벤트가 Relay Log에 정상적으로 기록되었다는 ACK을 회신한 후에 Client에게 트랜잭션의 결과를 반환한다. 따라서 Slave 스토리지 엔진의 데이터 동기화를 보장하는 것이 아닌, 최소 1대 이상의 Slave에 Relay Log 동기화를 보장한다.<br><strong>Binary Log의 전송 시기</strong>에 따라 After Commit(v5.5), After Sync(v5.7) 방식으로 나뉜다.</p>
<h4>장점</h4>
<ol>
<li>비동기 복제(async)보다 동기화를 보장한다.</li>
<li>동기 복제(sync)보다 성능 저하가 적다.</li>
</ol>
<h4>단점</h4>
<ol>
<li>ACK 응답을 위해 네트워크 통신이 한 번 더 발생한다.</li>
<li>Slave로부터 응답이 지연될 경우 쓰기 속도가 저하된다.</li>
</ol>
<p>Async와 Semi-sync 방식은 성능과 데이터 정합성 중에서 trade off가 있다. 데이터에 민감한 금융, 결제와 관련된 서비스는 Semi-sync를 고려해 볼 수 있다.</p>
<h4>1.2.1. After Commit</h4>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="616" data-origin-height="386"><span data-url="https://blog.kakaocdn.net/dn/b0emFN/btsD8Av7WNH/2n6h7hX3n3aF7Rh4XPsD2K/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/b0emFN/btsD8Av7WNH/2n6h7hX3n3aF7Rh4XPsD2K/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb0emFN%2FbtsD8Av7WNH%2F2n6h7hX3n3aF7Rh4XPsD2K%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="616" data-origin-height="386"/></span></figure>
</p>
<p>MySQL 5.5에서 추가되었고, Master의 Engine Commit이 수행된 후에 Slave의 Relay Log에 이벤트가 기록된다. 기록이 완료되면 Master에게 ACK를 회신하고 Client에게 결과를 반환한다.</p>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>Client Commit -> Binlog Flush/Commit -> <strong>Engine Commit</strong> -> <strong>Binlog dump Send Event with ACK Request</strong> -> <strong>Record Relay Log</strong> -> <strong>ACK</strong> -> <strong>Client Commit OK Response</strong></p>
</span></p></blockquote><p>Master에서 commit 후 Binary Log를 전송하기 전에 Master에서 crash 또는 Slave에서 Relay Log를 기록하기 전에 Slave에서 crash 되면 데이터의 정합성을 보장하기 어려운 단점이 있다.</p>
<h4>1.2.2. After Sync</h4>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="620" data-origin-height="380"><span data-url="https://blog.kakaocdn.net/dn/beb60y/btsD6u32pNF/ltg8fCT6s5dcKKJkrDg8LK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/beb60y/btsD6u32pNF/ltg8fCT6s5dcKKJkrDg8LK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbeb60y%2FbtsD6u32pNF%2Fltg8fCT6s5dcKKJkrDg8LK%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="620" data-origin-height="380"/></span></figure>
</p>
<p>MySQL 5.7에서 추가된 Loss-Less Replication이다. <code>rpl\_semi\_sync\_master\_wait\_point</code> 파라미터로 Semi-Sync 방식을 정할 수 있고 기본값은 After Sync이다.<br>Slave의 Relay Log에 이벤트가 기록되고 ACK를 회신한 후에 Master의 Engine Commit을 수행하도록 수정되었다.</p>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p>Client Commit -> Binlog Flush/Commit -> <strong>Binlog dump Send Event with ACK Request</strong> -> <strong>Record Relay Log</strong> -> <strong>ACK</strong> -> <strong>Engine Commit</strong> -> <strong>Client Commit OK Response</strong></p>
</span></p></blockquote><p>Slave의 Engine Commit을 보장하지 않지만 Relay Log를 정상적으로 기록했다는 것은 보장할 수 있다. 그리고 After Commit 방식과는 달리 ACK를 회신하지 않으면 Master에서 commit을 수행하지 않기 때문에 crash가 발생해도 정합성을 유지할 수 있다.<br>여러 Slave 중 하나의 Slave만 ACK를 회신하면 Master는 해당 트랜잭션을 완료하기 때문에 최소한의 데이터 정합성을 확보하면서 특정 Slave에서 지연이 발생해도 ACK를 빠르게 회신하는 Slave가 하나라도 있으면 Master의 쓰기 지연 시간은 줄어든다.</p>
<h2>2. Replication Format</h2>
<p>Binary Log에 변경된 이벤트를 기록할 때 format을 설정할 수 있으며 3가지 종류가 있다.</p>
<pre><code class="bash"># my.cnf
[mysqld]
binlog\_format=STATEMENT | ROW | MIXED</code></pre>
<pre><code class="sql">-- mysql client

-- global value
SET GLOBAL binlog\_format = 'STATEMENT' | 'ROW' | 'MIXED';
-- session value
SET SESSION binlog\_format = 'STATEMENT' | 'ROW' | 'MIXED';</code></pre>
<h3>2.1. SBR(Statement Based Replication)</h3>
<p>가장 전통적인 방식으로 Master에서 실행한 쿼리를 그대로 Binary Log에 저장한다. Slave는 Binary Log에 작성된 쿼리를 실행시켜서 복제를 진행한다.<br>하나의 쿼리가 많은 row를 변경하더라도 쿼리 하나만 저장하기 때문에 로그 파일의 크기가 작아 저장공간 확보에 유리하고 빠르게 수행할 수 있다.</p>
<blockquote data-ke-style="style1"><p data-ke-size="size16"><span style="font-family: 'Noto Serif KR';"><p><a href="https://dev.mysql.com/doc/refman/8.0/en/replication-rbr-safe-unsafe.html">Unsafe Statements</a>은 쿼리의 결과가 항상 동일하지 않은 동작을 의미하며 이를 복제할 때 문제가 발생할 수 있다. 예를 들어 서버의 현재 시간을 포함한 INSERT 쿼리를 slave에서 실행하면 master와 저장된 값이 달리지기 때문이다. 이처럼 올바르게 복제할 수 없을 경우 <code>[Warning] Statement is not safe to log in statement format.</code>와 같은 경고가 표시된다.</p>
</span></p></blockquote><h3>2.2. RBR(Row Based Replication)</h3>
<p>개별 테이블의 행이 어떻게 영향을 받는지 Before/After row image로 Binary Log에 저장한다. 즉, 쿼리의 결과를 저장하며 MySQL 5.7.7부터 기본값이 되었다.</p>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="1640" data-origin-height="66"><span data-url="https://blog.kakaocdn.net/dn/C0BEb/btsEa7GXVyj/RPZVgbCGEOHAWC8BkmybHK/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/C0BEb/btsEa7GXVyj/RPZVgbCGEOHAWC8BkmybHK/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FC0BEb%2FbtsEa7GXVyj%2FRPZVgbCGEOHAWC8BkmybHK%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="1640" data-origin-height="66"/></span></figure>
</p>
<p>가장 안전하게 복제할 수 있지만 많은 행이 변경될 경우 저장해야 하는 데이터가 많아져 로그 파일의 크기가 커지는 단점이 있다.</p>
<h3>2.3. MBR(Mixed Based Replication)</h3>
<p>SBR과 RBR의 단점을 보완한 방식으로 기본적으로 SBR로 동작하다가 Unsafe Statements를 만나면 RBR로 동작한다.</p>
<p><figure class="imageblock alignCenter" data-ke-mobileStyle="widthOrigin" data-origin-width="1840" data-origin-height="304"><span data-url="https://blog.kakaocdn.net/dn/devEbP/btsEbDew8BW/igeyVyFa9cP5JYpEJfuz4k/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/devEbP/btsEbDew8BW/igeyVyFa9cP5JYpEJfuz4k/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdevEbP%2FbtsEbDew8BW%2FigeyVyFa9cP5JYpEJfuz4k%2Fimg.png" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';" data-origin-width="1840" data-origin-height="304"/></span></figure>
</p>
<p>MySQL 8.0.34부터 <code>binlog\_format</code> 파라미터는 deprecated되고, row 기반 방식이 유일한 format이 될 것이라고 한다.</p>
<h2>3. 복제 지연</h2>
<p>Master는 여러 쓰레드가 병렬적으로 write를 수행하고 있지만, Slave는 단일 스레드를 사용하여 직렬화되기 때문에 Master와 Slave 사이에 지연 시간이 발생한다.</p>
<h3>3.1. Long Query</h3>
<ul>
<li>SBR 방식의 경우 쿼리의 소요 시간만큼 Slave에서 복제 지연 발생</li>
</ul>
<h4>해결 방법</h4>
<ul>
<li>RBR 또는 MBR 방식으로 변경</li>
<li>쿼리 튜닝이나 인덱스를 활용하여 쿼리 성능 자체를 향상</li>
</ul>
<h3>3.2. Write 쿼리량 증가</h3>
<ul>
<li>특정 배치 작업으로 인해 write 쿼리 증가</li>
<li>서비스 트래픽 증가 -> 트래픽이 몰리는 시간대는 갭이 커졌다가 한가한 시간대에 다시 좁혀지는 상황이 반복되면서 Master와의 복제 갭을 따라잡지 못할 수 있다.</li>
</ul>
<h4>해결 방법</h4>
<ul>
<li>MTR(Multi Threaded Replication)을 설정하여 worker 쓰레드 개수를 늘려서 처리 속도를 향상</li>
<li>sharding 또는 비즈니스 도메인을 분리하여 경량화</li>
</ul>
<h3>3.3. Slave의 로드 증가</h3>
<ul>
<li>Slave의 read 트래픽 증가하거나 배치 또는 백업으로 인해 Slave의 사용량이 증가하여 처리 성능 지연</li>
</ul>
<h4>해결 방법</h4>
<ul>
<li>조회에 대한 트래픽을 감당할 Slave가 부족하다는 의미이기 때문에 Slave를 추가 구성</li>
</ul>
<h3>3.4. Lock 이슈</h3>
<ul>
<li>Slave에서 락(metadata lock 등)이 걸려서 쿼리가 제대로 수행되지 않는 경우</li>
</ul>
<h4>해결 방법</h4>
<ul>
<li>Lock의 원인을 찾아서 해결</li>
</ul>
<h2>Reference</h2>
<p><a href="https://dev.mysql.com/doc/refman/8.0/en/replication.html">https://dev.mysql.com/doc/refman/8.0/en/replication.html</a><br><a href="https://hoing.io/archives/3111">https://hoing.io/archives/3111</a><br><a href="https://myinfrabox.tistory.com/20">https://myinfrabox.tistory.com/20</a><br><a href="http://cloudrain21.com/mysql-replication">http://cloudrain21.com/mysql-replication</a></p>