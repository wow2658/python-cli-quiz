import sys
from dataclasses import dataclass
import file_io
from console_display import ConsoleDisplay

@dataclass
class TerminalRunner:
    # [dataclass 적용] 애플리케이션의 메인 루프(심장)와 생명 주기를 전담하는 지휘자(Runner) 클래스임.
    # 파이썬의 일급 객체 특성을 활용하여, 바깥(main.py)에서 조립 완료된
    # {숫자: 액션객체} 형태의 '행동 딕셔너리'를 통째로 주입받음 (Command 패턴 적용).
    actions: dict
    app_data: dict

    def run(self):
        # 1. 무한 루프 가동: 사용자가 명시적으로 정상 종료하기 전까지 프로그램을 죽지 않게 살려둠.
        while True:
            ConsoleDisplay.show_main_menu()
            
            # 여기서부터 치명적 에러(Ctrl+C 등) 방해 공작이 발생할 수 있으므로 예외 처리 방어막(try)을 펼침.
            try:
                choice_str = ConsoleDisplay.get_user_input("▶️ 메뉴 선택 (1-5): ")
                
                # 입력값이 '0~9' 숫자로만 이루어져 있는지 1차 검증 (문자인 경우 다시 처음으로 올림)
                if not choice_str.isdecimal():
                    ConsoleDisplay.show_error("숫자로 입력해주세요.")
                    continue
                    
                choice = int(choice_str)
                # 입력된 번호에 매칭되는 행동 객체를 actions 딕셔너리에서 꺼내옴.
                action = self.actions.get(choice)

                if action:
                    # 지휘자(Runner)는 어떤 로직인지 알 필요 없이 그저 "실행(execute)해!"라고 무지성 명령만 내림.
                    # 각 Action 객체는 자기 일을 무사히 마치면 루프를 계속할지(True), 종료할지(False)를 반환함.
                    should_continue = action.execute()
                    if not should_continue:
                        break # 반환값이 False(ExitAction)면 그제야 무한 루프를 파괴하고 정상 종료함.
                else:
                    ConsoleDisplay.show_error("1에서 5 사이의 숫자를 선택해주세요.")

            # 2. 첫 번째 방어선: 키보드 강제 종료 (Ctrl+C) 방어 및 확인 로직
            except KeyboardInterrupt:
                try:
                    # 실수로 종료 단축키를 눌렀을 상황을 대비해 y/n으로 재검증을 시도함.
                    confirm = ConsoleDisplay.get_user_input("\n\n⚠️ 정말로 프로그램을 종료하시겠습니까? (y/n): ").lower()
                    
                    if confirm == 'y':
                        ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                        # 확정 시, 지금까지의 모든 메모리 딕셔너리 데이터를 하드디스크에 안전하게 굽고(저장) 종료함.
                        file_io.save_data(self.app_data)
                        sys.exit(0) # 운영체제에게 정상(코드 0) 종료됨을 알리며 프로세스 소멸.
                    else:
                        ConsoleDisplay.show_message("종료를 취소하고 메인 메뉴로 돌아갑니다.")
                        continue # 종료 취소 시 무한 루프 상단으로 복귀.
                        
                # "종료할래?" 묻고 있는데 거기다 대고 또 Ctrl+C를 연타하는 악성/극단적 종료 시도를 방어하는 2차 중첩 방어막임.
                except (KeyboardInterrupt, EOFError):
                    ConsoleDisplay.show_message("\n강제 종료가 확정되었습니다. 안전하게 보존 후 종료합니다...")
                    # 묻지도 따지지도 않고 가장 우선적으로 파일 저장부터 시키고 치명적 폭파시킴.
                    file_io.save_data(self.app_data)
                    sys.exit(0)

            # 3. 두 번째 방어선: 터미널 붕괴/파이프라인 단절 (EOF) 방어 및 심폐소생술 (고급 기법)
            except EOFError:
                # 사용자가 터미널(CMD) 창 자체를 X 버튼으로 닫거나, 통신 케이블이 뽑혀 입력을 더 못 받는 치명적 상태임.
                ConsoleDisplay.show_error("\n\n입력 스트림이 끊어졌습니다(EOF).")
                ConsoleDisplay.show_message("터미널(tty) 재연결을 시도합니다...")
                
                try:
                    import os
                    sys.stdin.close()
                    # OS/리눅스 환경의 근원적 터미널 장비 파일인 '/dev/tty'를 강제로 열어
                    # 끊어지고 붕괴된 생명유지장치(입력 파이프스트림)를 억지로 다시 이어 붙이는 소생술 시도임.
                    sys.stdin = open('/dev/tty', 'r')
                    ConsoleDisplay.show_success("✅ 터미널 복구 성공! 퀴즈 게임을 계속 진행합니다.\n")
                    continue
                    
                except Exception as e:
                    # 윈도우 환경이거나 터미널이 완전히 박살나 복구(Except)마저 실패했다면 최후의 수단을 씀.
                    ConsoleDisplay.show_error(f"터미널 복구 실패: {e}")
                    ConsoleDisplay.show_message("데이터를 안전하게 보존한 후 프로그램을 종료합니다...")
                    # 죽는 그 순간(완전한 크래시 직전)까지도 유저의 데이터를 놓치지 않고 하드에 굽고 장렬하게 전사함.
                    file_io.save_data(self.app_data)
                    sys.exit(0)
