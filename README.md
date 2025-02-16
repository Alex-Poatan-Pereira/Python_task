#### Middleware란 무엇인가?(with Decorators)
1. **Middleware**는  Django의 요청(Request)과 응답(Response) 사이에서 특정 로직을 수행하는 컴포넌트.  
`settings.py`에서 `MIDDLEWARE` 설정을 확인
>

2. **Middleware**와 **Decorators**의 **차이**
**Middleware**는 전역적으로 모든 요청과 응답을 처리(Django 전체에서 작동)   
보안, 로깅, 데이터 변환 등의 역할을 수행하는 컴포넌트.
**Decorator**는 특정 함수나 클래스에만 적용하는 방식(view 함수에서 주로 사용)   
로그인 제한, 권한 체크 등에 사용

----
#### Django란?
**Django는 Python 기반의 웹 프레임워크로, 빠르고 효율적인 웹 개발을 가능하게 해주는 풀스택 프레임워크**

Django의 특징
- MTV Pattern
    - Model
        데이터와 관련된 로직을 처리.
        데이터 구조 정의, 데이터베이서 기록을 관리
        >

    - Template
        레이아웃과 화면상의 로직을 처리
        >
    - View
        메인 비지니스 로직을 담당.
        클라이언트의 요청에 대해 처리를 분기하는 역할
>

- Django ORM
SQL을 직접 사용하지 않고 Python 클래스로 데이터베이스를 다룰 수 있음.
>

- Django DRF를 이용해 REST API 개발 가능
----
#### JWT란 무엇인가요?
**사용자 인증과 정보 교환을 위한 토큰 기반 인증 방식**
- 처리방식
    1. 클라이언트가 ID/PW를 서버로 보냄
    2. 서버에서 ID/PW를 검증하고 유효하다면 일정한 형식으로 서명 처리된 Token을 응답
    3. 이후 클라이언트는 모든 요청 헤더에 토큰을 담아 서버로 요청을 전송
    4. 서버는 해당 토큰의 유효성을 검증하고 유저의 신원과 권한을 확인 후 요청을 처리
>
- 세션(Session)과의 차이
    - 세션이란 세션 DB를 이용해서 유저의 정보를 기억하며,
Session ID라고 하는 랜덤한 Key를 쿠키에 담아서 Auth에 활용,
쿠키를 사용해서 Session ID를 주고 받는 것
    - 따라서 세션 DB가 존재하지 않으며 **DB가 필요하지 않음**
    - **토큰 자체**가 하나의 인증 데이터
    - 서버는 토큰이 **유효한지만** 검증하여 처리
>
- 장점
    서버에서 관리하는 데이터가 없으므로 **복잡한 처리 로직이 필요하지 않음**
    **세션이나 DB없이** 유저를 인증하는것이 가능
>
- 단점
    세션 테이블이 없기 때문에 **일방적으로 로그인을 무효화** 하는 등의 처리가 **불가능**
    Token 자체가 데이터를 담고 있는 정보이므로 **탈취당할시 보안이 취약**
>
- 단점 보완 방법
        1. **블랙리스트(Blacklist)** 또는 토큰 **저장 방식 변경**(세션 테이블(DB)에 저장하고, 로그아웃 시 삭제)   
        2. 토큰 만료 시간을 짧게 설정하고 **Refresh Token 활용**
>
- JWT 구조
    - Header
        토큰의 타입(jwt) 또는 서명 부분의 생성에 어떤 알고리즘(alg)이 사용되었는지 등을 저장
    - Payload
        토근 발급자, 토큰 대상자, 토큰 만료시간, 활성날짜, 발급시간 등 유저 정보를 담아서 인증
    - Signature
        Header + Payload + 서버의 비밀키 값을 HEADER에 명시된 암호 알고리즘 방식으로 생성한 값 
        서명의 유효여부 + 유효기간 내의 토큰인지 확인하여 Auth 과정을 처리
>
- Access Token과 Refresh Token
    - Access Token 
        **요청**할 때 **인증**을 위해 **헤더**에 포함해야하는 토큰
        매 요청시 보내는 토큰이므로 보안이 취약
    - Refresh Token
        **Access Token이 만료**되었을때 새로 Access Token을 발급받기 위한 Token
        Access Token 보다 **긴 유효기간**
        Refresh Token까지 만료되었다면
다시 인증(로그인) 과정이 필요합니다.

----
#### Access / Refresh Token 발행과 검증에 관한 테스트 시나리오 작성하기
1. 회원가입 & 로그인 → Access / Refresh Token 발급 확인
- 응답 코드: 200 OK
- 응답 데이터에 **access, refresh 토큰**이 포함되어 있어야 함
>

2.  Access Token을 사용하여 보호된 API 접근 가능 여부 확인
- **Authorization 헤더에 Bearer {access_token}을 추가**하여 보호된 API 호출
- 정상적으로 응답이 오는지 확인 (200 OK)
- **만료된 Access Token**을 사용하면 **401 Unauthorized**가 반환되는지 확인
>
3. Access Token 만료 후 Refresh Token을 사용하여 새로운 Access Token 발급 테스트
- **Access Token이 만료**된 후 Refresh Token으로 새로운 Access Token을 요청
- 응답 코드: 200 OK
- 응답 데이터에 새로운 access 토큰이 포함되어 있어야 함
>

4. 잘못된 Refresh Token 사용 시 인증 실패 테스트
- **존재하지 않는 Refresh Token**을 사용하여 Access Token 갱신 요청
- 응답 코드: 401 Unauthorized
- refresh 토큰이 유효하지 않다는 메시지가 반환되어야 함
>
5. 로그아웃 시 Refresh Token 블랙리스트 추가 테스트
- **Refresh Token을 사용하여 로그아웃** 요청
- **Refresh Token이 블랙리스트에 등록되었는지 확인
- 응답 코드: 205 Reset Content
>
6. 블랙리스트된 Refresh Token을 사용한 Access Token 갱신 차단
- **블랙리스트에 등록된 Refresh Token**을 사용하여 Access Token 갱신 요청
- 응답 코드: 401 Unauthorized
- refresh 토큰이 블랙리스트에 등록되었음을 나타내는 메시지가 반환되어야 함