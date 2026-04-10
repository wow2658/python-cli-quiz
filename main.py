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
            
            if not choice_str.isdecimal():
                ConsoleDisplay.show_error("숫자로 입력해주세요.")
                continue
                
            choice = int(choice_str)

            # [1] 퀴즈 풀기
            if choice == 1:
                # 1. 퀴즈가 있는지 먼저 확인
                quizzes = registry.get_all_quizzes()
                if not quizzes:
                    ConsoleDisplay.show_error("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
                    continue
                    
                # 2. 문제 수 선택 UI 호출 (신규 추가)
                q_count = ConsoleDisplay.get_question_count(len(quizzes))
                
                # 'q'를 눌러 취소한 경우 메인 메뉴로 복귀
                if q_count is None:
                    ConsoleDisplay.show_message("\n👋 퀴즈 풀기를 취소하고 메인 메뉴로 돌아갑니다.")
                    continue

                # 3. 입력받은 문제 수(question_count)를 전달하여 게임 실행
                record = game.play(question_count=q_count, randomize=True) 
                
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
                    if del_choice.isdecimal():
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

        # =========================================================
        # 🔥 업데이트된 예외 처리 로직: 실수 방지 안전장치 추가
        # =========================================================
        # 1. Control+C (KeyboardInterrupt) 처리: y/n 확인 절차
        except KeyboardInterrupt:
            try:
                # 이미 입력 중이던 줄에서 벗어나기 위해 줄바꿈(\n\n) 추가
                confirm = ConsoleDisplay.get_user_input("\n\n⚠️ 정말로 프로그램을 종료하시겠습니까? (y/n): ").lower()
                
                if confirm == 'y':
                    ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                    file_io.save_data(app_data)
                    sys.exit(0)
                else:
                    ConsoleDisplay.show_message("종료를 취소하고 메인 메뉴로 돌아갑니다.")
                    continue
                    
            # 확인 창이 떠있는데 거기서 또 Control+C나 Control+D를 누르면 진짜 종료로 간주
            except (KeyboardInterrupt, EOFError):
                ConsoleDisplay.show_message("\n강제 종료가 확정되었습니다. 안전하게 보존 후 종료합니다...")
                file_io.save_data(app_data)
                sys.exit(0)

        # 2. Control+D (EOFError) 처리: 터미널 재연결(복구) 도전!
        except EOFError:
            ConsoleDisplay.show_error("\n\n입력 스트림이 끊어졌습니다(EOF).")
            ConsoleDisplay.show_message("터미널(tty) 재연결을 시도합니다...")
            
            try:
                import os
                # 끊어진 기존 stdin을 닫고, 리눅스/맥의 기본 터미널 장치로 강제 연결
                sys.stdin.close()
                sys.stdin = open('/dev/tty', 'r')
                ConsoleDisplay.show_success("✅ 터미널 복구 성공! 퀴즈 게임을 계속 진행합니다.\n")
                continue # 메인 루프의 처음(메뉴 출력)으로 무사 복귀
                
            except Exception as e:
                # 윈도우 환경이거나 권한 문제로 복구 실패 시, 안전하게 저장 후 종료
                ConsoleDisplay.show_error(f"터미널 복구 실패: {e}")
                ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                file_io.save_data(app_data)
                sys.exit(0)

if __name__ == "__main__":
    main()