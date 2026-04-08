import sys
import file_io
from console_display import ConsoleDisplay
from quiz_registry import QuizRegistry
from quiz_game import QuizGame
from quiz import Quiz

def main():
    # 1. 파일에서 기존 데이터 로드 (없으면 빈 딕셔너리 반환)
    app_data = file_io.load_data()
    if "history" not in app_data:
        app_data["history"] = []
    if "best_score" not in app_data:
        app_data["best_score"] = 0.0

    # 2. 객체 의존성 주입 및 조립 (Dependency Injection)
    registry = QuizRegistry(app_data)
    game = QuizGame(registry)

    # 3. 메인 무한 루프 시작
    while True:
        ConsoleDisplay.show_main_menu()
        
        try:
            choice_str = ConsoleDisplay.get_user_input("▶️ 메뉴 선택 (1-5): ")
            
            if not choice_str.isdigit():
                ConsoleDisplay.show_error("숫자로 입력해주세요.")
                continue
                
            choice = int(choice_str)

            # [1] 퀴즈 풀기
            if choice == 1:
                # 보너스 기획 반영: 랜덤 출제 활성화 (문제 수 지정도 여기서 인자로 넘길 수 있음)
                record = game.play(randomize=True) 
                
                if record:
                    # 기록 저장
                    app_data["history"].append(record.to_dict())
                    
                    # 최고 점수 갱신 확인
                    if record.final_score > app_data["best_score"]:
                        ConsoleDisplay.show_success(f"🎉 최고 점수 갱신! ({app_data['best_score']}점 -> {record.final_score}점)")
                        app_data["best_score"] = record.final_score
                    
                    # 1회차 끝날 때마다 안전하게 디스크에 저장
                    file_io.save_data(app_data)

            # [2] 퀴즈 추가
            elif choice == 2:
                new_quiz_data = ConsoleDisplay.get_new_quiz_data()
                if new_quiz_data:
                    new_quiz = Quiz.from_dict(new_quiz_data)
                    registry.add_quiz(new_quiz)
                    ConsoleDisplay.show_success("퀴즈가 성공적으로 추가 및 저장되었습니다!")

            # [3] 퀴즈 목록 및 삭제
            elif choice == 3:
                quizzes = registry.get_all_quizzes()
                ConsoleDisplay.show_quiz_list(quizzes)
                
                if quizzes:
                    del_choice = ConsoleDisplay.get_user_input("\n🗑️ 삭제할 퀴즈 번호를 입력하세요 (취소하려면 그냥 엔터): ")
                    if del_choice.isdigit():
                        # 화면에 보이는 번호(1부터 시작)를 실제 인덱스(0부터 시작)로 보정
                        target_index = int(del_choice) - 1 
                        if registry.delete_quiz(target_index):
                            ConsoleDisplay.show_success("퀴즈가 삭제되었습니다.")
                        else:
                            ConsoleDisplay.show_error("존재하지 않는 번호입니다.")

            # [4] 점수 및 기록 확인
            elif choice == 4:
                ConsoleDisplay.show_score_board(app_data["best_score"], app_data["history"])

            # [5] 정상 종료
            elif choice == 5:
                ConsoleDisplay.show_message("\n데이터를 안전하게 저장하고 프로그램을 종료합니다. 수고하셨습니다!")
                file_io.save_data(app_data)
                break

            else:
                ConsoleDisplay.show_error("1에서 5 사이의 숫자를 선택해주세요.")

        # 사용자의 강제 종료(Ctrl+C)를 감지하여 데이터 증발 방어
        except (KeyboardInterrupt, EOFError):
            ConsoleDisplay.show_error("\n\n비정상 종료 시그널이 감지되었습니다.")
            ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
            file_io.save_data(app_data)
            sys.exit(0)

if __name__ == "__main__":
    main()