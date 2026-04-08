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
    """현재 메모리의 상태(data)를 json 파일에 안전하게 덮어씁니다."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        # ensure_ascii=False: 한글 깨짐 방지, indent=4: 예쁘게 줄바꿈 처리
        json.dump(data, f, ensure_ascii=False, indent=4)

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

        # 메뉴 분기점
        if choice == 1:
            print("\n[안내] 퀴즈 풀기 기능은 Step 3에서 구현할 예정입니다.")
        elif choice == 2:
            print("\n[안내] 퀴즈 추가 기능은 Step 4에서 구현할 예정입니다.")
        elif choice == 3:
            print("\n[안내] 퀴즈 목록 기능은 Step 4에서 구현할 예정입니다.")
        elif choice == 4:
            print("\n[안내] 점수 확인 기능은 Step 5에서 구현할 예정입니다.")
        elif choice == 5:
            print("\n데이터를 저장하고 프로그램을 정상 종료합니다. 수고하셨습니다!")
            save_data(app_data)  # <-- 5번 누르고 정상 종료 시에도 저장!
            break

if __name__ == "__main__":
    main()