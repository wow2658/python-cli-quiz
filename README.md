# 🐳 파이썬 CLI 퀴즈 게임 (주제: Docker Compose & Git 인프라 구축)

## 1. 프로젝트 개요 및 주제 선정
본 프로젝트는 **Python 객체지향 설계(OOP) 및 파일 데이터 영속성**의 실전 적용을 목적으로 개발된 콘솔 기반 퀴즈 애플리케이션임. 


- **퀴즈 주제:** Docker Compose 기초 및 멀티 컨테이너 네트워크, Git SSH 키 설정, 운영 명령어(`up`, `down` 등)
- **선정 이유:** Python 프로그래밍 기본기를 검증함과 동시에, 인프라 자동화 도구(Docker) 및 버전 관리 시스템(Git)의 핵심 개념을 문제화하여 SW 워크스테이션 구축 지식을 내재화하기 위함.

---

## 2. 개발 및 실행 환경
- **Language:** Python 3.12.13 (외부 라이브러리 미사용, 표준 라이브러리만 활용)
- **OS:** macOS (Zsh 환경) & Windows 11
- **Virtualization:** Docker (Windows/Mac 다른 기종 간 100% 동일한 Linux 실행 환경 보장)
- **VCS:** Git CLI (Mac) & TortoiseGit (Windows) & GitHub

### 🛠 하이브리드 실무 협업 시나리오 검증
본 프로젝트는 'Windows + GUI vs Mac + CLI 환경에서의 실무 협업 시나리오'를 가정하여 인프라를 설계함. 
Mac 환경(개발자 B)은 Git의 원리 체화를 위해 순수 터미널 명령어(CLI)를 활용하고, Windows 환경(개발자 A)은 실무 생산성을 위해 GUI 툴(TortoiseGit)을 활용하는 하이브리드 워크플로우를 성공적으로 검증함.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f929a4ab-78fb-493f-95b7-8ef5a2b17707" width="833" alt="하이브리드 Git 워크플로우">
</p>

---

## 3. 사전 요구사항 및 빠른 시작 (Quick Start)

### 📋 Prerequisites (사전 준비)
본 프로그램을 실행하려면 로컬 PC에 아래 도구들이 설치되어 있어야 함. (Python은 직접 설치할 필요 없음)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 또는 [OrbStack](https://orbstack.dev/) (Mac 환경 가벼운 컨테이너 구동용으로 권장)
- [Git](https://git-scm.com/)

### 🚀 실행 방법 (Interactive Mode)
```bash
# 1. 저장소 클론 및 디렉터리 이동
git clone [자신의_레포지토리_주소]
cd python-cli-quiz

# 2. 도커 이미지 빌드 및 퀴즈 게임 실행 (사용자 키보드 입력 활성화)
docker compose run --rm quiz-app
```

**💡 기술적 의사결정: 실행 명령어 채택 배경 (`up -d` vs `run --rm`)**
본 프로젝트는 백그라운드에서 상시 구동되는 웹 서버가 아닌, 사용자의 키보드 입력(`input()`)을 실시간으로 대기해야 하는 **대화형 CLI 프로그램**임.
* **STDIN/TTY 자동 할당:** `run` 명령어는 내부적으로 `-it` (Interactive & TTY) 옵션을 내포하여, 사용자의 키보드 입력이 즉각적으로 컨테이너 내부에 전달되도록 통신 채널을 오픈함.
* **컨테이너 라이프사이클 최적화 (`--rm`):** 1회성 플레이가 목적이므로, 게임 종료 시 불필요한 컨테이너 가비지를 즉시 파기하여 호스트 컴퓨터의 스토리지 낭비를 원천 차단함.

---

## 4. 프로젝트 아키텍처 및 객체 지향(OOP) 설계
거대한 `main.py` 구조를 탈피하고, 책임을 철저히 분리한 모듈형 아키텍처를 도입함.

### 📂 파일 구조 및 역할 분리
```text
python-cli-quiz/
├── 📂 [Entry Point]
│   └── 📜 main.py             # 객체 의존성 주입(DI) 및 메뉴 라우팅 담당 (진입점)
├── 📂 [Control Layer] 
│   ├── 📜 console_display.py  # 화면 출력(print)과 사용자 입력(input) 전담 (UI 격리)
│   └── 📜 quiz_game.py        # 퀴즈 플레이 엔진 (랜덤 출제, 게임 루프 제어)
├── 📂 [Business Logic] 
│   ├── 📜 quiz_registry.py    # 메모리 내 퀴즈 목록의 CRUD 전담
│   ├── 📜 hint_penalty.py     # 힌트 사용 기록 및 감점 비즈니스 로직
│   └── 📜 quiz_evaluator.py   # 순수 채점 및 퍼센티지 점수 계산기 (Stateless)
├── 📂 [Data Model] 
│   ├── 📜 quiz.py             # 퀴즈 1문제의 형태 (질문, 선택지, 정답, 힌트) DTO
│   └── 📜 score_history.py    # 1회차 게임 종료 후의 기록물 객체
├── 📂 [Infrastructure]
│   └── 📜 file_io.py          # state.json 파일 I/O 전담
├── 📜 docker-compose.yml      # 멀티 컨테이너 실행 명세서
└── 📜 state.json              # 데이터베이스 파일 (볼륨 마운트)
```

### 🔄 핵심 실행 흐름도 (데이터 이동 흐름)
```text
[사용자 터미널] 
      ↕ (글자를 보여주고 입력을 받음)
[console_display] 
      ↕
   [main] 
      ┣━ (1. 퀴즈 풀기) ━▶ [quiz_game] (진행 엔진)
      ┃                      ┣━ (화면 렌더링) ━▶ [console_display]
      ┃                      ┣━ (정답 채점) ━━▶ [quiz_evaluator]
      ┃                      ┣━ (힌트 감점) ━━▶ [hint_penalty]
      ┃                      ┗━ (기록 생성) ━━▶ [score_history]
      ┃
      ┗━ (종료 후 저장) ━▶ [file_io] ↔ (state.json)
```

---

## 5. 핵심 기능 및 데이터 영속성

### 🎮 주요 게임 기능
1. **문제 수 선택 및 랜덤 출제:** 원하는 문제 수를 지정할 수 있으며, 출제 순서는 매번 무작위(`random.shuffle`)로 섞임.
2. **힌트 및 감점 시스템:** 막힐 경우 `'h'`를 입력해 힌트를 열람할 수 있으나, 정답 시 최종 점수에서 페널티가 차감됨.
3. **히스토리 누적:** 매 플레이 시각과 정답률, 획득 점수가 객체화되어 영구 보존됨.
4. **중도 포기(Escape Hatch):** 문제 추가나 퀴즈 진행 도중 언제든 `'q'`를 입력하면 즉시 메인 메뉴로 안전하게 복귀함.

### 💾 데이터 파일 동기화 (Volume Mount)
* `docker-compose.yml` 내 볼륨 마운트(`.:/app`)를 설정하여, 도커 컨테이너가 파기되더라도 최고 점수와 퀴즈 데이터(`state.json`)는 내 컴퓨터에 영구 보존됨.
* 반대로, 호스트 PC에서 메모장으로 `state.json`에 퀴즈를 직접 타이핑해 넣으면, 도커 컨테이너를 다시 빌드하지 않아도 게임에 즉각 반영됨.

---

## 6. Git 워크플로우 (간소화된 Git Flow)
2인 협업 상황을 가정하여, 실무 표준에 가까운 **간소화된 Git Flow(Simplified Git Flow)** 전략을 도입함.

### 🌿 브랜치 전략
- **`main` (Production):** 제품 배포용 무결점 상태 보장 (직접 푸시 지양).
- **`dev` (Development):** 개발된 기능이 모이는 통합 테스트 브랜치.
- **`feature/...` (Feature):** 개별 기능 개발을 위한 격리 브랜치. 완료 시 `dev`로 PR 병합.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4e61d7a7-9e1b-4ab4-9b29-53326cc478d7" width="1500" alt="Git 브랜치 전략">
</p>

---

## 7. 시스템 검증 및 테스트 결과
> 아래 경로에 실행 및 검증 증빙 스크린샷을 첨부함.

- [ ] 메인 메뉴 화면 (`docs/screenshots/menu.png`)
- [ ] 퀴즈 풀기 및 정답 판정 (`docs/screenshots/play.png`)
- [ ] 새로운 퀴즈 추가 (`docs/screenshots/add_quiz.png`)
- [ ] 최고 점수 확인 (`docs/screenshots/score.png`)
- [ ] 비정상 입력 방어 (`docs/screenshots/error_handling.png`)
- [ ] 브랜치 병합 기록 (`docs/screenshots/git_log.png`)

---

## [부록] 핵심 예외 처리 및 트러블슈팅 (Troubleshooting)

### 1. `isdigit()`의 맹점(위첨자 버그) 발견 및 `isdecimal()` 고도화
* **이슈 발견:** 사용자 입력 검증을 위해 `str.isdigit()`을 사용했으나, 테스트 중 사용자가 **위첨자(예: `²`, `³`)나 분수(`½`)** 등을 입력할 경우 `isdigit()`이 이를 숫자로 취급하여 `True`를 반환하는 맹점을 발견함.
* **치명적 크래시(Crash) 원인:** `isdigit()`의 검증을 통과한 위첨자 문자열(`"²"`)이 곧바로 `int()` 함수로 전달되면서 형변환에 실패(`ValueError`), 프로그램 전체가 비정상 종료되는 치명적인 버그로 이어짐을 확인함.
* **해결 및 고도화:** 문자열 검증 메서드를 순수 아라비아 숫자(0-9)만을 엄격하게 판별하는 **`str.isdecimal()`**로 전면 교체함. 이를 통해 악의적이거나 비정상적인 유니코드 입력으로 인한 런타임 크래시를 완벽하게 차단함.

### 2. 시스템 시그널 제어 및 Graceful Shutdown (`KeyboardInterrupt` & `EOFError`)
CLI 환경에서 사용자의 강제 종료로 인한 데이터 유실을 방지하기 위한 필수 예외 처리임.

* **`Ctrl + C` (KeyboardInterrupt - 시그널 인터럽트):** * 파이썬 프로세스에 중단 요청(SIGINT) 시그널이 전송됨. 즉시 파기하지 않고, `input()`을 통해 사용자에게 "정말로 종료하시겠습니까? (y/n)"를 다시 묻는 안전장치(Confirmation)를 구현함.
* **`Ctrl + D` (EOFError - 입력 스트림 단절) 및 복구 강제 도입:**
  * **발생 원인:** 키보드와 파이썬을 연결하는 입력 통신 케이블(stdin) 자체가 물리적으로 단절되는(End Of File) 현상임.
  * **스트림 재연결(Recovery):** 단순히 즉각 종료하는 것을 넘어, 운영체제 레벨에서 `sys.stdin = open('/dev/tty', 'r')`를 강제 호출하여 끊어진 터미널 통신을 복구(재연결)하는 방어 로직을 실험적으로 구현함. 복구에 성공하면 메인 루프로 복귀하고, 실패할 경우에만 `save_data()`를 호출하여 안전하게 프로세스를 파기(Graceful Shutdown)하도록 이중 방어선을 구축함.

### 3. [한계점] OS 레벨 프로세스 제어 단축키 방어 불가 사유
* **`Alt + F4` / `Cmd + Q` / 터미널 탭 닫기:** 운영체제의 창 관리자나 터미널 에뮬레이터 자체에 전달되는 절대 파기 명령이므로, 파이썬 코드 레벨(`try-except`)에서는 제어권을 탈취할 수 없음. 이는 CLI 프로그램의 태생적 한계이므로, 본 시스템에서는 콘솔 내부 시그널 및 스트림 통제(항목 2번)를 최대 방어선으로 규정함.