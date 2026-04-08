# 🐳 파이썬 CLI 퀴즈 게임 (주제: Docker Compose & Git 인프라 구축)

## 1. 프로젝트 개요 및 주제 선정
본 프로젝트는 **Python 객체지향 설계(OOP) 및 파일 데이터 영속성**의 실전 적용을 목적으로 개발된 콘솔 기반 퀴즈 애플리케이션임.

- **퀴즈 주제:** Docker Compose 기초 및 멀티 컨테이너 네트워크, Git SSH 키 설정, 운영 명령어(`up`, `down` 등)
- **선정 이유:** Python 프로그래밍 기본기를 검증함과 동시에, 인프라 자동화 도구(Docker) 및 버전 관리 시스템(Git)의 핵심 개념을 문제화하여 SW 워크스테이션 구축 지식을 내재화하기 위함. 기본 탑재된 5개의 퀴즈 문항 역시 해당 지식을 검증할 수 있도록 구성됨.

---

## 2. 개발 및 실행 환경
- **Language:** Python 3.12.13 (외부 라이브러리 미사용, 표준 라이브러리만 활용)
- **OS:** macOS (Zsh 환경) & Windows 11
- **IDE:** Visual Studio Code 1.112.0
- **Virtualization:** Docker (Windows/Mac 이기종 간 100% 동일한 Linux 실행 환경 보장)
- **VCS:** Git CLI (Mac) & TortoiseGit (Windows) & GitHub
- **특이사항:** 본 프로젝트는 'Windows + GUI vs Mac + CLI 환경에서의 실무 협업 시나리오'를 가정하여 인프라를 설계함. Mac 환경(개발자 B)은 Git의 원리 체화를 위해 순수 터미널 명령어(CLI)를 활용하고, Windows 환경(개발자 A)은 실무 생산성을 위해 GUI 툴(TortoiseGit)을 활용하는 하이브리드 워크플로우를 성공적으로 검증함.


<p align="center">
  <img src="https://github.com/user-attachments/assets/f929a4ab-78fb-493f-95b7-8ef5a2b17707" width="833" alt="하이브리드 Git 워크플로우">
</p>

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

**💡 실행 명령어 채택 배경 (`up -d` vs `run --rm`)**
본 프로젝트는 백그라운드에서 상시 구동되는 웹 서버(`up -d`)가 아닌, 사용자의 키보드 입력(`input()`)을 실시간으로 대기하고 반응해야 하는 **대화형 CLI 프로그램**임. 이를 위해 `run --rm` 명령어를 채택하여 다음과 같은 기술적 이점을 확보함.
* **STDIN/TTY 자동 할당:** `docker compose run` 명령어는 내부적으로 `-it` (Interactive & TTY) 옵션을 기본적으로 내포하여 실행됨. 이를 통해 터미널과 컨테이너 간의 STDIN(표준 입력) 통신 채널이 열려, 사용자의 키보드 입력이 즉각적으로 프로그램에 전달됨.
* **컨테이너 라이프사이클 최적화 (`--rm`):** 1회성 플레이(테스트)가 목적이므로, 게임 종료 시 불필요한 컨테이너 찌꺼기(가비지)를 즉시 자동 파기하여 호스트의 스토리지 낭비를 원천 차단함.

  
<p align="center">
  <img width="1120" height="742" alt="도커명령어 비교 Screenshot 2026-04-08 at 11 23 21 AM" src="https://github.com/user-attachments/assets/1fe15405-a6be-4a82-bce0-e848581b43c5" />
</p>

### 핵심 기능 명세
1. **메뉴 시스템:** 퀴즈 풀기, 추가, 목록, 점수 확인, 종료의 5가지 직관적인 CLI 메뉴 제공.
2. **퀴즈 플레이 및 정답 판정:** 저장된 퀴즈를 순차적으로 출제하고 실시간으로 정답/오답을 판정하여 피드백 제공.
3. **예외 처리 및 안전 종료 방어 로직 (Fail-Safe):**
   - **입력 오류 방어:** 타입 불일치 등 비정상적인 값 입력 시, 프로그램이 크래시(Crash)되지 않고 예외 메시지 출력 후 안전하게 재입력을 요구하는 견고한 루프를 유지함.
   - **강제 종료 대응 (`Ctrl+C`):** `KeyboardInterrupt` 등 예기치 않은 종료 시그널이 발생하더라도, 메모리에 있는 현재 진행 상태와 데이터를 `state.json`에 강제 동기화(저장)한 뒤 프로세스를 안전하게 종료(Graceful Shutdown)하여 데이터 유실을 방지함.
---

## 5. 객체 지향 코드 구조 및 설계
역할을 2개의 핵심 클래스로 엄격히 분리하여 설계함.

### 📌 `Quiz` 클래스 (데이터 객체)
- **역할:** 개별 퀴즈의 속성(문제, 선택지 4개, 정답)과 퀴즈 출력, 정답 확인 메서드를 캡슐화.

### 📌 `QuizGame` 클래스 (시스템 매니저)
- **역할:** 전체 게임 루프, 메뉴 입출력, 퀴즈 리스트 관리, 최고 점수 갱신 및 파일 I/O 통합 관리.

### 💡 기술적 의사결정
- **함수형이 아닌 클래스 채택:** 데이터와 제어 로직을 객체 단위로 묶어 응집도를 높이고 전역 변수 남용을 차단함. 책임 분리를 통해 향후 채점 로직이나 입출력 포맷이 변경되어도 상호 간섭을 최소화함.

<p align="center">
  <img src="https://github.com/user-attachments/assets/761189d5-cbfc-47eb-ad06-185825217e1d" width="490" alt="객체지향 시스템 아키텍처 (UML)">
</p>

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

<p align="center">
  <img src="https://github.com/user-attachments/assets/4e61d7a7-9e1b-4ab4-9b29-53326cc478d7" width="1500" alt="Git 브랜치 전략">
</p>

### 7.2. 2인 협업 시나리오 흐름 (Hybrid Workflow)
**1. [공통] 통합 브랜치 세팅:** `main`에 Docker 환경 구축 완료 후 `dev` 브랜치 파생 및 원격 업로드
**2. [개발자 A - Windows/GUI] `Quiz` 클래스 작업:** - TortoiseGit을 활용하여 `feature/quiz-class` 브랜치 생성 및 체크아웃
   - `quiz.py` 작성 후 GUI 환경에서 커밋 및 푸시 (Upstream 연동)
   - GitHub PR(Pull Request) 생성
**3. [개발자 B - Mac/CLI] `QuizGame` 클래스 작업:** - 터미널(CLI)을 활용하여 `feature/quiz-game` 브랜치 생성 (`git checkout -b`)
   - `quiz_game.py` 작성 후 터미널에서 커밋 및 푸시 (`git commit`, `git push`)
   - GitHub PR(Pull Request) 생성
**4. [공통] 최종 통합 및 릴리즈:** `dev` 브랜치에서 충돌 테스트 완료 후 `main`으로 최종 병합 및 배포.

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
