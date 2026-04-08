# main.py
import sys
import json
import os

STATE_FILE = "state.json"

# 파일이 없거나 손상되었을 때 사용할 '최소 요구' 기본 데이터
DEFAULT_DATA = {
    "quizzes": [
        {
            "question": "Python의 창시자는?",
            "choices": ["Guido", "Linus", "Bjarne", "James"],
            "answer": 1
        },
        {
            "question": "Docker 컨테이너를 백그라운드에서 실행하는 옵션은?",
            "choices": ["-a", "-b", "-d", "-f"],
            "answer": 3
        }
    ],
    "best_score": 0
}

def load_data():
    """상태 파일을 읽어오거나, 없거나 손상되었을 경우 기본값으로 초기화합니다."""
    # 1. 파일이 아예 없는 경우 (최초 실행)
    if not os.path.exists(STATE_FILE):
        print(f"\n[안내] 저장된 데이터({STATE_FILE})가 없습니다. 기본 데이터로 초기화합니다.")
        return DEFAULT_DATA.copy()
    
    # 2. 파일이 있는 경우 읽기 시도
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            quiz_count = len(data.get("quizzes", []))
            best_score = data.get("best_score", 0)
            print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {best_score}점)")
            return data
            
    # 3. 파일 내용이 깨졌거나 JSON 형식이 아닌 경우 (손상 방어)
    except json.JSONDecodeError:
        print(f"\n⚠️ 데이터 파일({STATE_FILE})이 손상되었습니다. 기본 퀴즈 데이터로 복구합니다.")
        return DEFAULT_DATA.copy()

def save_data(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def play_quiz(app_data):
    quizzes = app_data.get("quizzes", [])
    
    # 퀴즈가 하나도 없을 경우 방어
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
        return

    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")
    score = 0

    for i, quiz in enumerate(quizzes, 1):
        print("\n" + "-"*40)
        print(f"[문제 {i}]")
        print(quiz["question"] + "\n")

        # 선택지 예쁘게 출력
        choices = quiz.get("choices", [])
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")

        # [핵심]: 각 문제마다 사용자가 올바른 정답을 낼 때까지 무한 방어 루프
        while True:
            try:
                raw_ans = input("\n✅ 정답 번호를 입력하세요: ")
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 퀴즈 도중 강제 종료 시그널이 감지되었습니다.")
                print("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                save_data(app_data)
                sys.exit(0)

            ans_str = raw_ans.strip()
            
            if not ans_str:
                print("⚠️ 값을 입력하지 않았습니다.")
                continue
            if not ans_str.isdigit():
                print("⚠️ 숫자로만 입력해주세요.")
                continue

            ans_int = int(ans_str)
            if ans_int < 1 or ans_int > len(choices):
                print(f"⚠️ 1에서 {len(choices)} 사이의 번호를 선택해주세요.")
                continue

            # 정상 입력 검증 통과 -> 정답 판정
            if ans_int == quiz["answer"]:
                print("🎉 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다! (정답: {quiz['answer']}번)")
            
            break # while 방어 루프를 탈출하고 다음 문제(for문)로 넘어감

    # 결과 출력
    total_q = len(quizzes)
    calc_score = int((score / total_q) * 100) # 100점 만점 환산
    print("\n" + "="*40)
    print(f"🏆 결과: {total_q}문제 중 {score}문제 정답! ({calc_score}점)")
    print("="*40)

# ==========================================
# [Step 4 추가 1]: 퀴즈 추가 엔진
# ==========================================
def add_quiz(app_data):
    print("\n📌 새로운 퀴즈를 추가합니다.")
    try:
        # 문제 입력 방어
        while True:
            question = input("문제를 입력하세요: ").strip()
            if not question:
                print("⚠️ 빈 문제는 추가할 수 없습니다. 다시 입력해주세요.")
                continue
            break

        # 선택지 입력 방어 (무조건 4개 입력받도록 고정)
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if not choice:
                    print(f"⚠️ 빈 선택지는 추가할 수 없습니다. 선택지 {i}를 다시 입력해주세요.")
                    continue
                choices.append(choice)
                break

        # 정답 번호 입력 방어
        while True:
            ans_str = input("정답 번호 (1-4): ").strip()
            if not ans_str.isdigit():
                print("⚠️ 숫자로만 입력해주세요.")
                continue
            ans_int = int(ans_str)
            if ans_int < 1 or ans_int > 4:
                print("⚠️ 1에서 4 사이의 번호를 선택해주세요.")
                continue
            break

        # 딕셔너리 조립 및 메모리 반영
        new_quiz = {
            "question": question,
            "choices": choices,
            "answer": ans_int
        }
        
        if "quizzes" not in app_data:
            app_data["quizzes"] = []
            
        app_data["quizzes"].append(new_quiz)
        
        # [핵심] 입력이 끝나는 즉시 json 파일에 물리적으로 덮어씀 (데이터 보장)
        save_data(app_data)
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 퀴즈 추가 도중 강제 종료 시그널이 감지되었습니다.")
        save_data(app_data)
        sys.exit(0)

# ==========================================
# [Step 4 추가 2]: 퀴즈 목록 조회 엔진
# ==========================================
def list_quizzes(app_data):
    quizzes = app_data.get("quizzes", [])
    
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다.")
        return

    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("-" * 40)
    for i, quiz in enumerate(quizzes, 1):
        print(f"[{i}] {quiz['question']}")
    print("-" * 40)

def display_menu():
    print("\n========================================")
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("========================================")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("========================================")

def main():
    # [Step 2 핵심]: 프로그램 시작 시 무조건 데이터를 메모리에 적재함
    app_data = load_data()

    while True:
        display_menu()
        
        # [방어 1 & 2]: Ctrl+C (KeyboardInterrupt) 및 Ctrl+D (EOFError) 강제 종료 방어
        try:
            raw_input = input("선택: ")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 비정상 종료 시그널이 감지되었습니다.")
            print("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
            save_data(app_data)  # <-- 강제 종료 직전 구조대 역할!
            sys.exit(0)

        # [방어 3]: 입력 앞뒤 공백 제거 (예: "  1 " -> "1")
        choice = raw_input.strip()

        # [방어 4]: 빈 입력 (그냥 엔터) 방어
        if not choice:
            print("⚠️ 값을 입력하지 않았습니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        # [방어 5]: 숫자가 아닌 입력 (예: abc, 1.5, -1) 방어
        if not choice.isdigit():
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue
            
        choice = int(choice)

        # [방어 6]: 허용 범위 밖 숫자 (예: 메뉴 9, 0) 방어
        if choice < 1 or choice > 5:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        # 메뉴 분기점 연동 완료
        if choice == 1:
            play_quiz(app_data)
        elif choice == 2:
            add_quiz(app_data)   # <-- 새로 만든 추가 함수 연결!
        elif choice == 3:
            list_quizzes(app_data) # <-- 새로 만든 목록 조회 함수 연결!
        elif choice == 4:
            print("\n[안내] 점수 확인 기능은 Step 5에서 구현할 예정입니다.")
        elif choice == 5:
            print("\n데이터를 저장하고 프로그램을 정상 종료합니다. 수고하셨습니다!")
            save_data(app_data)
            break

if __name__ == "__main__":
    main()