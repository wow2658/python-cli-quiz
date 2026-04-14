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

<img width="369" height="168" alt="Screenshot 2026-04-10 at 8 34 38 PM" src="https://github.com/user-attachments/assets/67b889a1-6521-4490-8842-137e12a7d38d" />
<img width="637" height="62" alt="image" src="https://github.com/user-attachments/assets/b23ba498-50cc-4109-8270-f962e652d5ac" />



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

<p align="center">
  <img width="1120" height="742" alt="도커명령어 비교 Screenshot 2026-04-08 at 11 23 21 AM" src="https://github.com/user-attachments/assets/1fe15405-a6be-4a82-bce0-e848581b43c5" />
</p>


---

## 4. 프로젝트 아키텍처 및 객체 지향(OOP) 설계
거대한 `main.py` 구조를 탈피하고, 책임을 철저히 분리한 모듈형 아키텍처를 도입함.

### 📂 파일 구조 및 역할 분리
```text
python-cli-quiz/
├── 📂 [Entry Point]
│   └── 📜 main.py             # 객체 의존성 주입(DI) 및 애플리케이션 실행 전담 (진입점)
├── 📂 [Control Layer]
│   ├── 📜 terminal_runner.py  # 시스템 생명주기 루프 및 예외(Ctrl+C 등) 방어 전담
│   ├── 📜 menu_actions.py     # 메뉴별 동작(퀴즈 풀기, 추가, 조회, 종료)을 캡슐화한 커맨드 패턴
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
│   └── 📜 file_io.py          # state.json 파일 I/O 및 데이터 스키마 무결성 보증 전담
├── 📜 docker-compose.yml      # 멀티 컨테이너 실행 명세서
└── 📜 state.json              # 데이터베이스 파일 (볼륨 마운트)
```

### 🔄 핵심 실행 흐름도 (데이터 이동 흐름)
```text
[사용자 터미널] 
      ↕ (글자를 보여주고 입력을 받음)
[console_display] 
      ↕
[terminal_runner] (무한 루프 구동, 예외 방어 및 라우팅)
      ┣━ (1. 퀴즈 풀기) ━━━━▶ [menu_actions (PlayQuizAction)]
      ┃                             ┣━ [quiz_game] (진행 엔진 시작)
      ┃                             ┃      ┣━ (화면 렌더링) ━▶ [console_display]
      ┃                             ┃      ┣━ (정답 채점) ━━▶ [quiz_evaluator]
      ┃                             ┃      ┣━ (힌트 감점) ━━▶ [hint_penalty]
      ┃                             ┃      ┗━ (기록 생성) ━━▶ [score_history]
      ┃                             ┗━ (종료 및 결과 세이브) ━▶ [file_io]
      ┃
      ┗━ (5. 정상 종료) ━━━━▶ [menu_actions (ExitAction)]
                                    ┗━ (데이터 안전 보존) ━━▶ [file_io] ↔ (state.json)
```
핵심 데이터 영속화 흐름:
`[MenuAction] (각 기능 수행 완료)` ➔ `[file_io.save_data] (JSON 직렬화 및 임시 파일을 활용한 Atomic 저장)` ➔ `[state.json]`

### 💡 [참고] 데이터 구조 미리보기 (state.json)
퀴즈 마스터 데이터(정적)와 플레이어의 기록(동적)을 독립적인 키(Key)로 분리한 계층형 도메인 구조임.

```json
{
    "quizzes": [
        {
            "question": "[Easy] docker-compose.yml 파일에 정의된 모든 서비스를 백그라운드에서 실행하는 가장 기본적인 명령어는?",
            "choices": [
                "docker run -bg",
                "docker compose up -d",
                "docker start --all",
                "docker compose start -b"
            ],
            "answer": 2,
            "hint": "백그라운드(background)에서 실행한다는 뜻으로, 데몬(daemon) 모드의 첫 글자를 옵션으로 씁니다."
        }
    ],
    "best_score": 100.0,
    "history": [
        {
            "timestamp": "2026-04-10 12:30:00",
            "total_questions": 10,
            "correct_answers": 10,
            "final_score": 100.0
        }
    ]
}
```
---

## 5. 핵심 기능 및 데이터 영속성

### 🎮 주요 게임 기능
1. **기본 퀴즈 제공 및 랜덤 출제:** 초기 실행 시 `state.json`에 10개의 퀴즈 데이터가 기본 내장되어 있음. 출제 순서는 무작위(`random.shuffle`)로 섞임.
2. **힌트 및 감점 시스템:** 정답이 막힐 경우 `'h'`를 입력해 힌트를 열람할 수 있으며, 해당 문제 정답 시 최종 점수에서 페널티가 차감됨.
3. **히스토리 누적:** 플레이 시각, 정답률, 획득 점수가 객체화되어 영구 보존됨.
4. **중도 포기(Escape Hatch):** 언제든 `'q'`를 입력하면 메인 메뉴로 즉시 복귀함.
5. **예외 처리 방어:** 사용자의 공백, 문자, 범위를 벗어난 숫자 등 비정상 입력에 대해 크래시 없이 대응함.

### 💾 데이터 파일 동기화 (Volume Mount)
* `docker-compose.yml` 내 볼륨 마운트(`.:/app`)를 설정하여, 도커 컨테이너가 파기되더라도 최고 점수와 퀴즈 데이터(`state.json`)는 내 컴퓨터에 영구 보존됨.
* 반대로, 호스트 PC에서 메모장으로 `state.json`에 퀴즈를 직접 타이핑해 넣으면, 도커 컨테이너를 다시 빌드하지 않아도 게임에 즉각 반영됨.

---

## 6. Git 워크플로우 및 형상 관리 전략

### 🌿 브랜치 분리 이유와 병합(Merge)의 의미
* **브랜치 분리 이유:** 안정적으로 구동되는 배포용 `main` 브랜치에 직접 코드를 작성하지 않고, 새로운 기능 개발이나 리팩토링은 `feature/...` 등의 별도 브랜치를 생성(분리)하여 진행. 이는 개발 중인 불완전한 코드나 버그가 기존의 정상적인 서비스에 악영향을 미치는 것을 물리적으로 격리(차단)하기 위함.
* **병합(Merge)의 의미:** 격리된 브랜치에서 기능 구현과 테스트가 완전히 끝나 안전성이 검증되었을 때만 코드를 원본에 합치는 병합 작업을 수행. 이를 통해 `main` 브랜치는 언제나 에러 없는 100% 무결성 상태를 유지.
* **적용된 구조:**
  * `main` (Production): 언제나 배포 가능한 무결점 상태 (직접 푸시 절대 지양)
  * `dev` (Development): 다음 배포를 위해 기능들이 모이는 통합 테스트 브랜치
  * `feature/...`: 개별 기능 구현을 위한 격리 브랜치 (완료 시 `dev`로 PR 병합)
 
* **커밋 단위 및 규칙:** 기능 단위로 커밋을 분할하며, `[Feat]`, `[Fix]`, `[Docs]`, `[Refactor]` 접두사를 명시하여 목적을 직관적으로 파악하도록 강제함.

  <p align="center">
  <img src="https://github.com/user-attachments/assets/4e61d7a7-9e1b-4ab4-9b29-53326cc478d7" width="1500" alt="Git 브랜치 전략">
</p>


### 📝 커밋 단위 분할 및 메시지 규칙
* **커밋 단위 분할의 목적:** 모든 변경 사항을 퇴근할 때 한 번에 뭉뚱그려 커밋하지 않고, 논리적인 기능 단위(예: UI 추가, 파일 I/O 구현, 버그 수정 등)로 잘게 쪼개어 커밋했습니다. 이를 통해 추후 치명적인 오류가 발생하더라도 전체를 되돌릴 필요 없이, 문제의 원인이 되는 특정 시점의 커밋만 정밀하게 추적하여 안전하게 롤백(Rollback)할 수 있습니다.
* **커밋 메시지 컨벤션:** 직관적인 협업을 위해 접두사를 명시하여, 팀원이나 리뷰어가 히스토리만 보고도 어떤 작업이 이루어졌는지 즉각 파악할 수 있도록 규칙을 강제했습니다.
  * `Feat:` 퀴즈 출제 등 새로운 기능 추가
  * `Fix:` 채점 점수 오류 등 버그 수정
  * `Docs:` README 파일 등 문서 작성 및 수정
  * `Refactor:` 기능 변화 없이 클래스 분리 등 내부 아키텍처 구조 개선

### 📸 작업 증빙 및 시연 결과 (스크린샷)
> **평가 요구사항 증빙 자료:** (아래 괄호 안의 위치에 실제 스냅샷 이미지 링크 삽입 필요)

- [x] **GitHub 원격 저장소 커밋 (10개 이상):** https://github.com/wow2658/python-cli-quiz.git)]
- [x] **`git log --oneline --graph` 병합 내역:**
      
<img width="2558" height="836" alt="image" src="https://github.com/user-attachments/assets/8f1a130a-1ce2-46b2-9671-2f9846ef4533" />

- [x] **Git 기초 명령어 7종(init, add, commit, push, pull, checkout, clone) 실습 내역** 

clone

<img width="477" height="332" alt="Screenshot 2026-04-07 at 2 12 34 PM" src="https://github.com/user-attachments/assets/e520e910-0bb9-4ee5-9fdb-e922bde0a1a0" />
<img width="616" height="471" alt="image" src="https://github.com/user-attachments/assets/7beb0df6-3aa8-4551-9054-06be30463b32" />



init

<img width="760" height="138" alt="image" src="https://github.com/user-attachments/assets/1192c8f9-e633-4f7d-b858-b4f9ff6fdf8a" />

add

<img width="697" height="567" alt="깃애드Screenshot 2026-04-06 at 8 21 58 PM" src="https://github.com/user-attachments/assets/7a7aa5a3-80e0-4327-b3f7-f019e0d0a807" />


commit

<img width="540" height="184" alt="image" src="https://github.com/user-attachments/assets/30d01867-ad49-4dca-9c75-2f2f1c4c22bc" />

push

<img width="1000" height="430" alt="image" src="https://github.com/user-attachments/assets/d73044fe-0cd4-43c0-8819-6792bfde76ab" />

pull

<img width="607" height="153" alt="image" src="https://github.com/user-attachments/assets/f08e0799-fe4c-4874-a751-5bd9c34e61b8" />

checkout

<img width="550" height="113" alt="image" src="https://github.com/user-attachments/assets/627b9ac2-55ab-4e54-a1f8-8e1fd6bbdec8" />




- [x] **프로그램 메뉴 정상 출력 확인:** 
      
 <img width="427" height="180" alt="image" src="https://github.com/user-attachments/assets/f4e73834-ea36-4a1c-95c0-1284c89e3756" />
 
- [x] **퀴즈 정답/오답 및 예외(공백/문자) 방어 판정:**
      
<img width="637" height="42" alt="image" src="https://github.com/user-attachments/assets/8afcd057-12ec-44c9-be4c-c8035b5c4d87" />
<img width="690" height="243" alt="image" src="https://github.com/user-attachments/assets/56c07757-9a12-462f-b22c-77174f03ae7c" />
<img width="699" height="294" alt="image" src="https://github.com/user-attachments/assets/4a5923fc-77eb-487c-b4c6-30a198ab2b2c" />
<img width="527" height="189" alt="image" src="https://github.com/user-attachments/assets/160b2fec-946a-46ff-9616-49957222f2ce" />
<img width="364" height="116" alt="image" src="https://github.com/user-attachments/assets/a6d5bca5-ec9d-4655-8eb9-a562a8bd45f1" />



- [x] **컨테이너 재실행 후 추가된 퀴즈 및 점수 유지:** 
<img width="355" height="296" alt="image" src="https://github.com/user-attachments/assets/a6045741-46b3-42e5-aa9f-4c7db88bc5d7" />
<img width="310" height="205" alt="image" src="https://github.com/user-attachments/assets/5cedf4e9-bf19-4e27-ba6c-150d583aa1f1" />
<img width="521" height="1217" alt="image" src="https://github.com/user-attachments/assets/33a0ae39-79d5-4cd7-baf5-31bc74c38edf" />

---

## 7. 기술적 의사결정 기록 (Tech Decision Records)
> 객체 지향 설계 및 아키텍처 구성에 대한 심층 판단 근거임.

### 7.1. 패러다임: 함수(Function) 대신 클래스(Class)를 도입한 이유
* **데이터와 기능의 '세트 메뉴화' (상태와 행위의 응집)**: 함수만 사용해서 게임을 만들면, 현재 몇 점인지, 힌트를 몇 번 썼는지 같은 '데이터'를 이 함수 저 함수로 계속 넘겨주거나(매개변수 전달), 어디서든 접근할 수 있는 위험한 공용 변수(전역 변수)를 써야함. 클래스를 도입하면 QuizGame이라는 하나의 상자 안에 데이터(점수, 힌트 횟수)와 기능(채점하기)을 한데 묶어서 자기 자신을 스스로 관리하게 만들 수 있어 코드가 훨씬 깔끔해짐.
  
<p align="center">
<img width="860" height="562" alt="image" src="https://github.com/user-attachments/assets/96cd4ab8-3845-4f9a-99b7-4f52b87112c8" />
</p>

<p align="center">
<img width="911" height="1198" alt="image" src="https://github.com/user-attachments/assets/34753707-6150-4005-8ef2-aae8354d4fae" />
</p>

<p align="center">
  <img width="800" height="171" alt="image" src="https://github.com/user-attachments/assets/ac01bdbe-5086-4c59-8eee-df1975753699" />
</p>
  
* **부서별 역할 나누기 (책임의 분리):** 모든 코드가 한 곳에 섞여 있으면, 단순히 "출력되는 글자" 하나를 바꾸려다 "채점 로직"이 고장 날 수 있음. 화면에 글자를 띄우는 역할(UI), 게임을 진행하는 역할(Engine), 파일에 저장하는 역할(I/O)을 각각의 클래스로 부서 나누듯 격리함. 덕분에 나중에 터미널 화면을 웹 브라우저나 앱으로 바꾸더라도, 핵심 채점 엔진은 한 줄도 고치지 않고 그대로 재사용할 수 있음.

### 7.2. 데이터베이스: JSON 채택 이유 및 구조 설계
* **채택 사유:** 별도의 DB 엔진 설치 없이 내장 `json` 모듈로 객체 직렬화/역직렬화가 가능하여 CLI 경량 환경에 최적화됨. 사람이 직접 읽고 수정(Human-readable)하기도 용이함.
* **구조 설계의 이유 (`{"quizzes": [], "best_score": 0, "history": []}`):** 퀴즈 마스터 데이터(정적)와 유저 플레이 기록(동적)을 하나의 파일 내에서 논리적 도메인으로 분할함. 이를 통해 앱 로드 시 각 키보드별로 적절한 클래스 객체에 매핑하기 쉬워짐.
* **파일 I/O 예외 처리(`try/except`)의 필수성:** 파일 시스템은 외부 자원임. 권한 부족, 디스크 용량, 경로 누락 등으로 언제든 접근에 실패할 수 있으므로, 크래시 방지를 위해 `try/except` 처리가 반드시 요구됨.
* **파일 손상 복구 로직 (Resilience):** 강제 종료 등으로 `state.json`이 파괴되어 `JSONDecodeError`가 발생할 경우, 프로그램이 죽지 않고 메모리에 하드코딩된 `DEFAULT_DATA`를 반환하여 기본 퀴즈 세트로 서비스를 자동 초기화/복구하도록 설계함.
* **[한계점] 데이터 1,000건 이상 증가 시:** JSON은 전체 파일을 메모리에 적재하여 수정 후 통째로 덮어쓰는 구조임. 데이터가 대규모로 커지면 메모리 오버헤드가 급증하고 탐색 속도가 저하됨. 이 시점부터는 SQLite와 같은 임베디드 RDBMS로 마이그레이션해야 함.

<img width="885" height="1103" alt="image" src="https://github.com/user-attachments/assets/a547028c-8e00-4595-93da-9ec6b5c72926" />

<img width="886" height="342" alt="image" src="https://github.com/user-attachments/assets/71b408de-42c0-41ad-8632-385086707cb1" />



### 7.3. 시스템 안정성 제어 및 요구사항 변경 대응
* **Graceful Shutdown (`Ctrl+C`, `EOF`):** 터미널 환경에서 `KeyboardInterrupt` 시 즉각 종료하지 않고 `y/n` 재확인 프롬프트를 띄움. 물리적 단절(`EOFError`) 발생 시에도 즉시 파기하지 않고, `sys.stdin = open('/dev/tty', 'r')`를 호출해 OS 레벨 터미널 재연결을 시도하거나, 불가피할 시 메모리의 데이터를 안전하게 저장(`save_data()`)한 뒤 종료함.
* **확장성 (요구사항 변경 시 타격 범위):** 만약 "정답 채점 방식"이나 "선택지 개수" 규칙이 변경될 경우, 전체 구조를 수정할 필요 없이 순수 비즈니스 로직을 담당하는 `quiz_evaluator.py` 내부 함수와 `console_display.py`의 출력 포맷 일부만 수정하면 됨. 데이터 구조 로직(`quiz.py`)과 게임 진행 엔진(`quiz_game.py`)은 OCP(개방-폐쇄 원칙)에 따라 수정 없이 그대로 재사용 가능함.

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

### 4. 수정한 코드를 커밋하지 않고 다른 브랜치로 안전하게 옮기기
* **상황:** 배포용 `main` 브랜치에서 실수로 코드를 대량으로 수정해버렸으나, 해당 내용을 `main`에 직접 올리지 않고 `feature` 등 별도의 격리된 브랜치를 생성하여 커밋하고 싶을 때 발생함.
* **해결 원리:** Git은 `git commit` 도장을 찍기 전(Working Directory 상태)의 변경 사항들은 현재 브랜치의 DB에 영구 귀속시키지 않고 현재 작업 책상 위에만 임시로 올려둠.
* **조치 방법:** 수정한 파일들이 널려있는 상태 그대로 `git switch -c <새로운-브랜치-이름>` 명령어를 실행함. Git이 수정된 짐(코드)들을 잃어버리지 않고 그대로 들고 새 브랜치로 이동(Switch)해 줌. 이후 `git add .` 와 `git commit`을 순차적으로 수행하면, 원본 `main` 브랜치는 깨끗하게 보호된 채 새 브랜치에만 작업 내역이 안전하게 박제됨.
