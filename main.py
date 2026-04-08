import sys
import file_io
import quiz_evaluator
def play_quiz(app_data):
    quizzes = app_data.get("quizzes", [])
    
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
        return

    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)")
    score = 0

    for i, quiz in enumerate(quizzes, 1):
        print("\n" + "-"*40)
        print(f"[문제 {i}]")
        print(quiz["question"] + "\n")

        choices = quiz.get("choices", [])
        for idx, choice in enumerate(choices, 1):
            print(f"{idx}. {choice}")

        while True:
            try:
                raw_ans = input("\n✅ 정답 번호를 입력하세요: ")
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 퀴즈 도중 강제 종료 시그널이 감지되었습니다.")
                print("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                file_io.save_data(app_data)
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

            # quiz_core 연동 로직
            if quiz_evaluator.check_answer(quiz, ans_int):
                print("🎉 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다! (정답: {quiz['answer']}번)")
            break 

    total_q = len(quizzes)
    calc_score = quiz_evaluator.calculate_score(score, total_q)
    
    print("\n" + "="*40)
    print(f"🏆 결과: {total_q}문제 중 {score}문제 정답! ({calc_score}점)")
    
    current_best = app_data.get("best_score", 0)
    if calc_score > current_best:
        print(f"🎉 새로운 최고 점수입니다! (기존: {current_best}점 -> 갱신: {calc_score}점)")
        app_data["best_score"] = calc_score
        file_io.save_data(app_data) 
    print("="*40)

def add_quiz(app_data):
    print("\n📌 새로운 퀴즈를 추가합니다.")
    try:
        while True:
            question = input("문제를 입력하세요: ").strip()
            if not question:
                print("⚠️ 빈 문제는 추가할 수 없습니다. 다시 입력해주세요.")
                continue
            break

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if not choice:
                    print(f"⚠️ 빈 선택지는 추가할 수 없습니다. 선택지 {i}를 다시 입력해주세요.")
                    continue
                choices.append(choice)
                break

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

        # quiz_core 연동 로직
        new_quiz = quiz_evaluator.create_quiz_entry(question, choices, ans_int)
        
        if "quizzes" not in app_data:
            app_data["quizzes"] = []
            
        app_data["quizzes"].append(new_quiz)
        file_io.save_data(app_data)
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 퀴즈 추가 도중 강제 종료 시그널이 감지되었습니다.")
        file_io.save_data(app_data)
        sys.exit(0)

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

def show_score(app_data):
    best_score = app_data.get("best_score", 0)
    quizzes = app_data.get("quizzes", [])
    
    print("\n" + "="*40)
    print(f"🏆 현재 최고 점수: {best_score}점")
    print(f"📂 등록된 총 문제 수: {len(quizzes)}개")
    print("="*40)

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
    app_data = file_io.load_data()

    while True:
        display_menu()
        
        try:
            raw_input = input("선택: ")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 비정상 종료 시그널이 감지되었습니다.")
            print("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
            file_io.save_data(app_data)
            sys.exit(0)

        choice = raw_input.strip()

        if not choice:
            print("⚠️ 값을 입력하지 않았습니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        if not choice.isdigit():
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue
            
        choice = int(choice)

        if choice < 1 or choice > 5:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        if choice == 1:
            play_quiz(app_data)
        elif choice == 2:
            add_quiz(app_data)   
        elif choice == 3:
            list_quizzes(app_data) 
        elif choice == 4:
            show_score(app_data)
        elif choice == 5:
            print("\n데이터를 저장하고 프로그램을 정상 종료합니다. 수고하셨습니다!")
            file_io.save_data(app_data)
            break

if __name__ == "__main__":
    main()