# LIKELION 9th Apply Crawler

🦁 LikeLion Applicant Crawler by Inha University 🦁

## 제작자

- 19학번 전자공학과 김재원

## 👨🏻‍💻 개요

- 멋쟁이사자처럼 지원자 정보 자동 추합 크롤링(Crawling) 프로그램

## 🔨기술 스택

- BeautifulSoup

## 사용 전, 환경 세팅

1. 환경변수에 APPLY_USERNAME과 APPLY_PASSWORD값 저장

## 사용법

### 1. 깃 클론

- `git clone https://github.com/minsgy/LIKELION_Apply_Crawling.git`

### 2. 가상 환경 생성 및 실행 후, 종속성 다운로드

- `python -m venv <가상환경 이름>`
- `. <가상환경 이름>/script/activate`, mac:`. <가상환경 이름>/bin/activate`
- `pip install -r requirements.txt`

### 3.기본 세팅

학교 별 아이디. 비밀번호 설정 필요

1. 환경변수에 APPLY_USERNAME과 APPLY_PASSWORD값 저장

- 예시 : `export APPLY_USERNAME='34@likelion.org'`

### 4. 사용 방법

- `from crawler import getApplicants`
- python 코드에서 getApplicants 를 부를 경우 자동으로 로그인 후 Dictionary의 List 로 반환.
- 여기서부턴 학교별 상황에 맞게;;;