# ats_ckonlpy
> 금융거래의 적요 텍스트 분석을 위한 한국어 형태소 분석기 라이브러리 이며, KoNLPy의 customized version입니다. 본 코드는 [lovit](https://github.com/lovit/customized_konlpy) 님의 코드를 기반으로 작성하였으며 [pypi](https://pypi.org/project/ats-ckonlpy/)에 배포되어 있습니다.


![](./png/image.png)

## 설치 방법

윈도우:

1. 자바 설치 (JDK, oracle.com )
[JDK](https://www.oracle.com/java/technologies/downloads/) 에 접속해서 본인 os에 맞는 자바를 설치합니다. 

2. jpype 설치
[jpype](https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype) 로 접속해서 본인 os와 사용하는 환경의 파이썬 버젼과 맞는 jpype를 다운받고 pip 명령어로 설치합니다.
```sh
# ex-윈도우
pip install JPype1-1.4.0-cp38-cp38-win_amd64.whl
```

3. 환경변수 편집

- '시스템 환경 변수 편집'에 들어가서 '시스템 변수' JAVA_HOME이라는 변수로 1.에서 설치한 자바 경로를 설정합니다. 
ex) C:\Program Files\Java\jdk-19

- 그 후 Path를 편집해서 %JAVA_HOME%\bin\server를 추가해줍니다. 
※ 이전 버젼에서는 %JAVA_HOME%\bin 여기까지만 저장하라고 되어있을텐데 19버젼부터는 server란 경로가 추가되었고 이 안에 jvm.dll 파일이 들어있으니 주의해야 합니다.


4. install
이제 해당 패키지를 설치해줍니다.
```sh
git clone https://github.com/whfh3900/ats_ckonlpy.git
cd ats_ckonlpy
python setup.py install
```

5. pip install
마지막으로 재부팅하여 아래 코드를 통해 정상적으로 실행되는지 확인합니다.
```python
from ckonlpy.tag import Twitter
twitter = Twitter()
```


## 사용 예제

konlpy에는 한국어를 위한 많은 분석기법을 제공하지만 여기에서는 품사 태깅 기능만을 보여줍니다. 
```python
from ckonlpy.tag import Twitter, Postprocessor
post = Postprocessor(Twitter())
post.pos("신한이경진") # [('신한', 'Nic'), ('이경진', 'Name')]
```
'신한'은 금융용어 말뭉치에 의해 Nic이란 품사로 '이경진'은 사람이름이므로 Name이란 품사로 태깅되는 것을 볼 수 있습니다.

_더 많은 예제와 사용법은 [customized KoNLPy](https://github.com/lovit/customized_konlpy) 를 참고하세요._



## 정보

최승언 – [@velog](https://velog.io/@csu5216) – csu5216@gmail.com

라이센스: GNU General Public License v3.0

[LICENSE](https://github.com/lovit/customized_konlpy/blob/master/LICENSE)
