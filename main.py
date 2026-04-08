# main.py
import sys

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
    while True:
        display_menu()
        
        # [방어 1 & 2]: Ctrl+C (KeyboardInterrupt) 및 Ctrl+D (EOFError) 강제 종료 방어
        try:
            raw_input = input("선택: ")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 비정상 종료 시그널이 감지되었습니다.")
            print("데이터를 안전하게 보존한 후 프로그램을 종료합니다.")
            # TODO: Step 2에서 여기에 state.json 저장 로직을 추가할 예정
            sys.exit(0) # 안전한 종료

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
            print("\n프로그램을 정상 종료합니다. 수고하셨습니다!")
            break

if __name__ == "__main__":
    main()