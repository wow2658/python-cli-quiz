# 🐳 파이썬 CLI 퀴즈 게임 (주제: Docker Compose & Git 인프라 구축)

## 1. 프로젝트 개요 및 주제 선정
본 프로젝트는 **Python 객체지향 설계(OOP) 및 파일 데이터 영속성**의 실전 적용을 목적으로 개발된 콘솔 기반 퀴즈 애플리케이션임.

- **퀴즈 주제:** Docker Compose 기초 및 멀티 컨테이너 네트워크, Git SSH 키 설정, 운영 명령어(`up`, `down` 등)
- **선정 이유:** Python 프로그래밍 기본기를 검증함과 동시에, 인프라 자동화 도구(Docker) 및 버전 관리 시스템(Git)의 핵심 개념을 문제화하여 SW 워크스테이션 구축 지식을 내재화하기 위함. 기본 탑재된 5개의 퀴즈 문항 역시 해당 지식을 검증할 수 있도록 구성됨.

---

## 2. 개발 및 실행 환경
- **Language:** Python 3.12.13 (외부 라이브러리 미사용, 표준 라이브러리만 활용)
- **OS:** macOS (Zsh 환경)
- **IDE:** Visual Studio Code 1.112.0
- **Virtualization:** Docker (Host OS의 도커 실행기-Docker Desktop, OrbStack 등-와 무관하게 100% 동일한 Linux 및 Python 3.12.13 실행 환경 보장)
- **VCS:** Git CLI (v2.53.0) & GitHub
- **특이사항:** 본 프로젝트는 실제 2인 팀 개발이 아닌, 'Windows & Mac 환경에서의 실무 협업 시나리오'를 가정하여 인프라 설계 및 형상 관리를 학습한 결과물임. OS 차이로 인한 의존성 및 경로 충돌을 방지하고자 `Dockerfile`과 `docker-compose.yml`을 구성하여 컨테이너화된 환경을 선제 구축함. 또한, Git의 구동 원리를 체화하기 위해 GUI 툴에 의존하지 않고 모든 작업을 순수 터미널 명령어(CLI)로 수행함.

---

## 3. 프로젝트 파일 구조
```text
python-cli-quiz/
├── docker-compose.yml # Docker 멀티 컨테이너 실행 명세서
├── Dockerfile         # Python 3.11 기반 독립 실행 환경 구축용 이미지 빌드 파일
├── main.py            # 프로그램 실행의 진입점 (Entry Point)
├── quiz.py            # Quiz 클래스 (데이터 모델)
├── quiz_game.py       # QuizGame 클래스 (시스템 제어 및 로직)
├── state.json         # 퀴즈 목록 및 최고 점수가 저장되는 데이터베이스 파일 (볼륨 마운트)
├── README.md          # 프로젝트 설명서
├── .gitignore         # Git 추적 제외 목록
└── docs/
    └── screenshots/   # 실행 결과 및 검증 증빙 이미지 폴더
```

---

## 4. 프로그램 실행 및 핵심 기능
본 프로그램은 로컬 환경에 Python을 직접 설치할 필요 없이, Docker Compose를 통해 격리된 환경에서 안전하게 실행됨.

### 실행 방법 (Interactive Mode)
```bash
# 초기 빌드 및 퀴즈 게임 실행 (사용자 키보드 입력 활성화)
docker compose run --rm quiz-app
```
*(※ `up -d` 대신 `run --rm`을 채택한 이유: 사용자의 `input()` 입력을 실시간으로 대기하는 대화형 CLI 특성상, STDIN 통신을 완벽히 지원하고 종료 시 컨테이너 찌꺼기를 남기지 않기 위함)*

### 핵심 기능 명세
1. **메뉴 시스템:** 퀴즈 풀기, 추가, 목록, 점수 확인, 종료의 5가지 메뉴 제공.
2. **퀴즈 플레이 및 정답 판정:** 저장된 퀴즈를 순차 출제하고 정답/오답을 판정함.
3. **입력 오류 및 안전 종료 방어 로직:**
   - 비정상적인 값 입력 시 프로그램 종료 없이 예외 메시지 출력 후 재입력을 요구함.
   - `Ctrl+C` (KeyboardInterrupt) 등 발생 시, 현재 상태를 `state.json`에 강제 저장한 뒤 안전하게 프로세스를 종료함.

---

## 5. 객체 지향 코드 구조 및 설계
역할을 2개의 핵심 클래스로 엄격히 분리하여 설계함.

### 📌 `Quiz` 클래스 (데이터 객체)
- **역할:** 개별 퀴즈의 속성(문제, 선택지 4개, 정답)과 퀴즈 출력, 정답 확인 메서드를 캡슐화.

### 📌 `QuizGame` 클래스 (시스템 매니저)
- **역할:** 전체 게임 루프, 메뉴 입출력, 퀴즈 리스트 관리, 최고 점수 갱신 및 파일 I/O 통합 관리.

### 💡 기술적 의사결정
- **함수형이 아닌 클래스 채택:** 데이터와 제어 로직을 객체 단위로 묶어 응집도를 높이고 전역 변수 남용을 차단함. 책임 분리를 통해 향후 채점 로직이나 입출력 포맷이 변경되어도 상호 간섭을 최소화함.

---

## 6. 데이터 영속성 및 파일 I/O 설계

### 💡 기술적 의사결정
- **Docker Volume Mount 동기화:** `docker-compose.yml` 내 볼륨 마운트(`.:/app`)를 설정하여, 컨테이너 내부에서 발생한 상태 변화(`state.json` 갱신)가 호스트 PC에도 실시간 영구 저장되도록 파이프라인을 구축함.
- **예외 처리(`try/except`) 적용:** 파일 누락 또는 JSON 구조 손상 시 발생할 수 있는 런타임 에러를 방어함.
- **자가 복구(Self-Healing):** 손상이 감지되면 예외 메시지를 출력한 뒤, 기본 퀴즈 세트로 메모리를 복구하고 파일을 덮어써 프로그램의 가용성을 지속 보장함.

### 데이터 파일 (`state.json`) 스키마
```json
{
    "quizzes": [
        {
            "question": "Docker Compose에서 컨테이너를 백그라운드로 실행하는 옵션은?",
            "choices": ["-d", "-b", "-bg", "-v"],
            "answer": 1
        }
    ],
    "best_score": 5
}
```

---

## 7. Git 워크플로우 및 실무형 협업 시나리오
본 프로젝트는 2인 협업 상황(개발자 A: Windows, 개발자 B: Mac)을 가정하여, 실무 표준에 가까운 **간소화된 Git Flow(Simplified Git Flow)** 전략을 도입함.

### 7.1. 브랜치 전략 설계
- **`main` (Production):** 제품 배포용 무결점 상태 보장 (직접 푸시 지양).
- **`dev` (Development):** 개발된 기능이 모이는 통합 테스트 브랜치.
- **`feature/...` (Feature):** 개별 기능 개발을 위한 격리 브랜치. 완료 시 `dev`로 PR 병합.

### 7.2. 2인 협업 시나리오 명령어 흐름
**1. [공통] 통합 브랜치 세팅:** `main`에 Docker 환경 구축 완료 후 `dev` 브랜치 파생 및 원격 업로드 (`git checkout -b dev`)
**2. [개발자 A - Windows] `Quiz` 클래스 작업:** `dev`에서 `feature/quiz-class` 브랜치 생성 -> 코드 작성 -> 푸시 및 PR
**3. [개발자 B - Mac] `QuizGame` 클래스 작업:** `dev`에서 `feature/quiz-game` 브랜치 생성 -> 코드 작성 -> 푸시 및 PR
**4. [공통] 최종 통합 및 릴리즈:** `dev`에서 충돌 테스트 완료 후 `main`으로 최종 병합(`git merge dev`) 및 배포.

### 7.3. 원격 저장소 동기화 (Clone & Pull 실습)
- 상기 협업 완료 후, 별도의 실습용 로컬 디렉터리에 원격 저장소를 복제(`git clone`)함.
- 복제된 저장소에서 코드를 수정 및 푸시한 뒤, 기존 원본 디렉터리에서 `git pull origin main`을 수행하여 충돌 없이 변경 사항이 반영됨을 검증 완료함.

---

## 8. 시스템 검증 및 테스트 결과
> 아래 경로에 실행 및 검증 증빙 스크린샷을 첨부함.

- [ ] 메인 메뉴 화면 (`docs/screenshots/menu.png`)
- [ ] 퀴즈 풀기 및 정답 판정 (`docs/screenshots/play.png`)
- [ ] 새로운 퀴즈 추가 (`docs/screenshots/add_quiz.png`)
- [ ] 최고 점수 확인 (`docs/screenshots/score.png`)
- [ ] 비정상 입력 방어 (`docs/screenshots/error_handling.png`)
- [ ] 브랜치 병합 기록 (`docs/screenshots/git_log.png`)