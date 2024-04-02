[Baekjoon-Python] 9251 : LCS
=
<p><a href="https://www.acmicpc.net/problem/9251">https://www.acmicpc.net/problem/9251</a></p>
<h2>접근</h2>
<ol>
<li>첫 번째 문자열의 알파벳을 두 번째 문자열과 비교하면서 공통 부분 수열 길이를 메모이제이션한다.</li>
</ol>
<h2>풀이</h2>
<pre><code class="python">from sys import stdin

letter\_1 = stdin.readline().rstrip()
letter\_2 = stdin.readline().rstrip()
dp = [0] \* len(letter\_2)
for let\_1 in letter\_1:
 cnt = 0 # (1)
 for i, let\_2 in enumerate(letter\_2):
 if dp[i] > cnt: # (2)
 cnt = dp[i]
 elif let\_1 == let\_2: # (3)
 dp[i] = cnt + 1

print(max(dp))</code></pre>
<ul>
<li>(1) cnt는 전 인덱스까지의 공통 부분 수열 길이이다.</li>
<li>(2) dp 값이 더 크면 cnt를 변경한다.</li>
<li>(3) 두 알파벳이 같으면 1을 더한 값을 dp에 저장한다.</li>
</ul>
<h3>예시</h3>
<p><code>ACAYKP</code>, <code>CAPCAK</code> 두 문자열이 있다.</p>
<ol>
<li>첫 알파벳이기 때문에 cnt는 증가하지 않는다. 첫 번째, 두 번째 A는 1이 된다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/wAFje/btsDRHHfleP/lgdHASqzZNxigYJ0y3mDx1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/wAFje/btsDRHHfleP/lgdHASqzZNxigYJ0y3mDx1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FwAFje%2FbtsDRHHfleP%2FlgdHASqzZNxigYJ0y3mDx1%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="2">
<li>cnt는 첫 번째 A에서 1이 되어 두 번째 C는 2가 된다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/ng3uX/btsDKRdkBS2/bodCFKXmonpE0wlTTkVMA0/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/ng3uX/btsDKRdkBS2/bodCFKXmonpE0wlTTkVMA0/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fng3uX%2FbtsDKRdkBS2%2FbodCFKXmonpE0wlTTkVMA0%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="3">
<li>cnt는 첫 번째 C에서 1이 되어 첫 번째 A는 2, 두 번째 C에서 2가 되어 두 번째 A는 3이 된다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/mDcFz/btsDJVtKai7/Oo2yQf8NKrMsLm6K6lqpY1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/mDcFz/btsDJVtKai7/Oo2yQf8NKrMsLm6K6lqpY1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FmDcFz%2FbtsDJVtKai7%2FOo2yQf8NKrMsLm6K6lqpY1%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="4">
<li>Y는 같은 알파벳이 없다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/l7zap/btsDQ70uzX1/tWBQ6aRJe79CFqOuRwbRg1/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/l7zap/btsDQ70uzX1/tWBQ6aRJe79CFqOuRwbRg1/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fl7zap%2FbtsDQ70uzX1%2FtWBQ6aRJe79CFqOuRwbRg1%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="5">
<li>cnt는 두 번째 A에서 3이 되어 K는 4가 된다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/byCQvV/btsDRlEgCTO/iI1W8lxRJ8bOzONXPwW8Tk/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/byCQvV/btsDRlEgCTO/iI1W8lxRJ8bOzONXPwW8Tk/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbyCQvV%2FbtsDRlEgCTO%2FiI1W8lxRJ8bOzONXPwW8Tk%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>
<ol start="6">
<li>cnt는 첫 번째 A에서 2가 되어 P는 3이 된다.</li>
</ol>
<p><figure class="imageblock alignCenter" width="80%"><span data-url="https://blog.kakaocdn.net/dn/bXTE1b/btsDJUVVUsb/CVomtjjwgu8KlblrccLA6K/img.png" data-lightbox="lightbox"><img src="https://blog.kakaocdn.net/dn/bXTE1b/btsDJUVVUsb/CVomtjjwgu8KlblrccLA6K/img.png" srcset="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbXTE1b%2FbtsDJUVVUsb%2FCVomtjjwgu8KlblrccLA6K%2Fimg.png" width="80%" onerror="this.onerror=null; this.src='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png'; this.srcset='//t1.daumcdn.net/tistory\_admin/static/images/no-image-v1.png';"/></span></figure>
</p>