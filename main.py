from quiz import Quiz
from quiz_game import QuizGame

def main():
    # 1. 문제 팩 준비
    questions = [
        Quiz("Docker 컨테이너를 백그라운드에서 실행하는 옵션은?", ["-a", "-b", "-d", "-f"], 3),
        Quiz("Git에서 브랜치를 생성하고 바로 이동하는 명령어는?", ["git checkout -b", "git branch -m", "git fetch", "git pull"], 1),
        Quiz("파이썬에서 클래스의 생성자(초기화) 메서드 이름은?", ["__start__", "__init__", "__main__", "__create__"], 2)
    ]

    # 2. 게임 엔진에 문제 팩 장전
    game = QuizGame(questions)
    
    print("🎮 개발자 CLI 퀴즈 게임을 시작합니다!\n" + "="*40)
    
    # 3. 게임 루프 시작
    while True:
        current_quiz = game.next_quiz()
        if current_quiz is None:
            break
        
        print(f"\n📝 문제: {current_quiz.question}")
        print(f"👉 선택지: {current_quiz.choices}")
        
        try:
            user_ans = int(input("✅ 정답 번호를 입력하세요: "))
            if current_quiz.check_answer(user_ans):
                print("🎉 정답입니다!")
                game.add_score()
            else:
                print("❌ 틀렸습니다!")
        except ValueError:
            print("⚠️ 숫자로만 입력해주세요!")

    # 4. 최종 결과 출력
    print("\n" + "="*40)
    print(game.get_final_score())

if __name__ == "__main__":
    main()