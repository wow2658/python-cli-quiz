import sys
import file_io
from console_display import ConsoleDisplay

class TerminalRunner:
    def __init__(self, actions: dict, app_data: dict):
        self.actions = actions
        self.app_data = app_data

    def run(self):
        while True:
            ConsoleDisplay.show_main_menu()
            
            try:
                choice_str = ConsoleDisplay.get_user_input("▶️ 메뉴 선택 (1-5): ")
                
                if not choice_str.isdecimal():
                    ConsoleDisplay.show_error("숫자로 입력해주세요.")
                    continue
                    
                choice = int(choice_str)
                action = self.actions.get(choice)

                if action:
                    should_continue = action.execute()
                    if not should_continue:
                        break
                else:
                    ConsoleDisplay.show_error("1에서 5 사이의 숫자를 선택해주세요.")

            except KeyboardInterrupt:
                try:
                    confirm = ConsoleDisplay.get_user_input("\n\n⚠️ 정말로 프로그램을 종료하시겠습니까? (y/n): ").lower()
                    
                    if confirm == 'y':
                        ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                        file_io.save_data(self.app_data)
                        sys.exit(0)
                    else:
                        ConsoleDisplay.show_message("종료를 취소하고 메인 메뉴로 돌아갑니다.")
                        continue
                        
                except (KeyboardInterrupt, EOFError):
                    ConsoleDisplay.show_message("\n강제 종료가 확정되었습니다. 안전하게 보존 후 종료합니다...")
                    file_io.save_data(self.app_data)
                    sys.exit(0)

            except EOFError:
                ConsoleDisplay.show_error("\n\n입력 스트림이 끊어졌습니다(EOF).")
                ConsoleDisplay.show_message("터미널(tty) 재연결을 시도합니다...")
                
                try:
                    import os
                    sys.stdin.close()
                    sys.stdin = open('/dev/tty', 'r')
                    ConsoleDisplay.show_success("✅ 터미널 복구 성공! 퀴즈 게임을 계속 진행합니다.\n")
                    continue
                    
                except Exception as e:
                    ConsoleDisplay.show_error(f"터미널 복구 실패: {e}")
                    ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                    file_io.save_data(self.app_data)
                    sys.exit(0)
