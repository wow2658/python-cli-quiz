# 1. README에 명시한 정확한 파이썬 버전의 경량화(slim) 이미지 사용
FROM python:3.12.13-slim

# 2. 컨테이너 내부의 작업 디렉터리 설정
WORKDIR /app

# 3. 호스트(내 컴퓨터)의 파일을 컨테이너 내부로 복사
COPY . /app

# 4. 컨테이너 실행 시 기본으로 작동할 명령어
CMD ["python", "main.py"]