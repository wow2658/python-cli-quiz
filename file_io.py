import json
import os
import tempfile

STATE_FILE = "state.json"
DEFAULT_DATA = {
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
        },
        {
            "question": "[Easy] 파이썬에서 사용자의 입력값(문자열)이 숫자로만 이루어져 있는지 판별할 때 사용하는 문자열 메서드는? (힌트: 예외 처리 방어 로직에 썼던 것!)",
            "choices": [
                "isnumeric()",
                "isdigit()",
                "isnumber()",
                "is_int()"
            ],
            "answer": 2,
            "hint": "숫자(digit)인지(is) 물어보는 직관적인 이름의 파이썬 내장 문자열 함수입니다."
        },
        {
            "question": "[Medium] Git에서 방금 남긴 커밋 메시지에 오타를 발견했을 때, 새로운 커밋을 추가하지 않고 가장 최근 커밋을 '슬쩍' 수정하는 명령어는?",
            "choices": [
                "git commit --amend",
                "git reset --soft HEAD~1",
                "git revert HEAD",
                "git rebase -i"
            ],
            "answer": 1,
            "hint": "법안이나 문서를 '수정하다, 고치다'라는 뜻을 가진 영단어 amend를 옵션으로 사용합니다."
        },
        {
            "question": "[Hard] Docker Compose에서 Web 서비스가 DB 서비스의 '단순 컨테이너 생성'을 넘어, '완전히 부팅되어 접속 가능한 상태'가 된 후 실행되도록 정교하게 의존성을 제어하는 속성은?",
            "choices": [
                "depends_on: [ condition: service_started ]",
                "wait_for_it: db_service:3306",
                "depends_on: [ condition: service_healthy ]",
                "links: [ db_service: ready ]"
            ],
            "answer": 3,
            "hint": "단순 시작(started) 여부가 아니라, 컨테이너가 '건강하게(healthy)' 작동 중인지 확인하는 조건입니다."
        },
        {
            "question": "[Hard] 이미 원격 저장소(GitHub)에 푸시된 과거의 커밋 여러 개를 하나로 깔끔하게 합치거나, 특정 과거 커밋의 내용만 조작하고 싶을 때 사용하는 강력한 명령어는?",
            "choices": [
                "git reset --hard",
                "git cherry-pick",
                "git revert --no-commit",
                "git rebase -i"
            ],
            "answer": 4,
            "hint": "커밋의 베이스를 다시(re) 배치하며, 대화형(interactive) 모드로 진입하기 위해 '-i' 옵션을 씁니다."
        },
        {
            "question": "[Easy] Git에서 현재 작업 디렉토리의 변경 사항(수정/추가/삭제)을 확인할 때 사용하는 명령어는?",
            "choices": [
                "git log",
                "git diff",
                "git status",
                "git show"
            ],
            "answer": 3,
            "hint": "현재 '상태(status)'를 보여달라는 뜻의 영단어가 그대로 명령어입니다."
        },
        {
            "question": "[Easy] Docker에서 현재 실행 중인 컨테이너 목록만 확인하는 명령어는?",
            "choices": [
                "docker images",
                "docker ps",
                "docker ls --running",
                "docker container inspect"
            ],
            "answer": 2,
            "hint": "리눅스에서 실행 중인 프로세스(process)를 확인하는 명령어와 동일합니다."
        },
        {
            "question": "[Medium] 파이썬 CLI 프로그램에서 사용자가 Ctrl+C를 눌렀을 때 발생하는 예외(Exception)의 정확한 이름은?",
            "choices": [
                "SystemExit",
                "EOFError",
                "KeyboardInterrupt",
                "InterruptedError"
            ],
            "answer": 3,
            "hint": "키보드(Keyboard)로 인터럽트(Interrupt, 중단 요청)를 보낸다는 뜻이 이름에 그대로 담겨 있습니다."
        },
        {
            "question": "[Medium] Dockerfile에서 컨테이너가 실행될 때 기본으로 수행할 명령어를 지정하되, docker run 시 인자를 넘기면 덮어쓸 수 있게 하는 명령어는?",
            "choices": [
                "RUN",
                "ENTRYPOINT",
                "CMD",
                "EXEC"
            ],
            "answer": 3,
            "hint": "ENTRYPOINT는 고정 실행이고, 이것은 '기본 명령(Command)'이라는 뜻으로 덮어쓰기가 가능합니다."
        },
        {
            "question": "[Hard] Git에서 실수로 스테이징(git add)까지 한 파일을 커밋하지 않고 스테이징 영역에서만 제거하되, 작업 디렉토리의 수정 내용은 그대로 보존하는 명령어는?",
            "choices": [
                "git rm --cached 파일명",
                "git reset HEAD 파일명",
                "git checkout -- 파일명",
                "git stash 파일명"
            ],
            "answer": 2,
            "hint": "HEAD(최신 커밋) 시점으로 스테이징 영역만 되돌린다(reset)는 의미입니다. 작업 디렉토리는 건드리지 않습니다."
        }
    ],
    "best_score": 0.0,
    "history": []
}

def load_data():
    if not os.path.exists(STATE_FILE):
        print(f"\n[안내] 저장된 데이터({STATE_FILE})가 없습니다. 기본 데이터로 초기화합니다.")
        return DEFAULT_DATA.copy()
    
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            quiz_count = len(data.get("quizzes", []))
            best_score = data.get("best_score", 0)
            print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {best_score}점)")
            return data
    except json.JSONDecodeError:
        print(f"\n⚠️ 데이터 파일({STATE_FILE})이 손상되었습니다. 기본 퀴즈 데이터로 복구합니다.")
        return DEFAULT_DATA.copy()

def save_data(data):
    # Atomic Save: 저장 중 크래시로 인한 파일 증발 원천 차단
    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(STATE_FILE)))
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.close(fd)
    os.replace(temp_path, STATE_FILE)