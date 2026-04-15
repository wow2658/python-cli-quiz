from abc import ABC, abstractmethod
from dataclasses import dataclass
import file_io
from console_display import ConsoleDisplay
from quiz import Quiz

# [학습] ABC(Abstract Base Class) 기법: 일종의 '노예 계약서' 혹은 '공통 규격서' 역할을 함.
# 이 클래스를 상속받는 모든 자식 클래스들은 반드시 아래에 명시된 형태의 메서드를 똑같이 만들어야만 프로그램이 작동하게 강제함.
class MenuAction(ABC):
    @abstractmethod
    def execute(self) -> bool:
        """
        메뉴 동작을 실행함.
        메인 무한 루프(while True)를 계속 돌려야 하면 True, 프로그램을 종료해야 하면 False를 반환함.
        """
        pass

# [학습] 위 MenuAction 규격서를 상속받은 첫 번째 자식 클래스 (1. 퀴즈 풀기)
@dataclass
class PlayQuizAction(MenuAction):
    # [dataclass 적용] 퀴즈 풀기 모드는 데이터 갱신도 해야 하고, 문제 목록도 알아야 하고, 게임 로직도 돌려야 해서
    # 가장 많은 3개의 도구(의존성)를 외부(main.py)로부터 골고루 주입받음.
    app_data: dict
    registry: 'QuizRegistry'
    game: 'QuizGame'

    # 노예 계약서(ABC)에 적힌 규약대로 무조건 똑같은 이름(execute)으로 함수를 구현해야 함!
    def execute(self) -> bool:
        # 1. 퀴즈 저장소에서 전체 목록 퍼오기
        quizzes = self.registry.get_all_quizzes()
        if not quizzes:
            ConsoleDisplay.show_error("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return True # 에러가 났어도 프로그램이 꺼지면 안 되므로 True를 반환해 화면을 메인 메뉴로 되돌림
            
        # 2. 뷰(ConsoleDisplay)를 호출해 화면에 UI를 띄우고 풀고싶은 문제 개수를 입력받음
        q_count = ConsoleDisplay.get_question_count(len(quizzes))
        
        # 'q'를 눌러 취소(None 반환)했을 때의 조기 종료 처리 (Early Return)
        if q_count is None:
            ConsoleDisplay.show_message("\n👋 퀴즈 풀기를 취소하고 메인 메뉴로 돌아갑니다.")
            return True

        # 3. 게임 엔진에 개수를 넘겨주며 실제 플레이 시작. 끝난 뒤 꽉 찬 결과지(record 객체)를 반환받음
        record = self.game.play(question_count=q_count, randomize=True) 
        
        if record:
            # 방금 끝난 게임 기록을 딕셔너리로 분해(직렬화)해서 전체 데이터 배열(history) 마지막 꼬리에 갖다 붙임
            self.app_data["history"].append(record.to_dict())
            
            # [최고 점수 갱신 로직] 이번 판 성적이 역사상 최고 점수보다 높으면 신기록을 갱신함!
            if record.final_score > self.app_data["best_score"]:
                ConsoleDisplay.show_success(f"🎉 최고 점수 갱신! ({self.app_data['best_score']}점 -> {record.final_score}점)")
                self.app_data["best_score"] = record.final_score
            
            # 이 메뉴에서는 신기록, 플레이 내역 등 핵심 데이터가 변동되었으므로 하드디스크 파일에 안전하게 오토 세이브(Atomic Save)
            file_io.save_data(self.app_data)
            
        return True # 하나의 게임 사이클이 무사히 끝났으니 메인 메뉴 루프를 계속 돌리라는 신호

@dataclass
class AddQuizAction(MenuAction):
    # [dataclass 적용] 퀴즈 추가 모드는 '퀴즈 관리국(registry)' 관련 권한 하나만 있으면 되므로 딱 하나만 주입받음
    registry: 'QuizRegistry'

    def execute(self) -> bool:
        # 화면 담당자(ConsoleDisplay)에게 새 퀴즈 입력을 받아오라고 지시
        new_quiz_data = ConsoleDisplay.get_new_quiz_data()
        
        if new_quiz_data:
            # 받아온 날것의 딕셔너리 데이터를 '보조 공장장(.from_dict)'에게 넘겨 세련된 Quiz 객체로 조립함
            new_quiz = Quiz.from_dict(new_quiz_data)
            # 깔끔하게 조립된 객체를 퀴즈 관리국에 정식 등록!
            self.registry.add_quiz(new_quiz)
            ConsoleDisplay.show_success("퀴즈가 성공적으로 추가 및 저장되었습니다!")
        return True

@dataclass
class ListDeleteQuizAction(MenuAction):
    # [dataclass 적용] 목록 조회 및 삭제 역시 '퀴즈 관리국(registry)'의 데이터만 만지므로 registry만 있으면 됨
    registry: 'QuizRegistry'

    def execute(self) -> bool:
        quizzes = self.registry.get_all_quizzes()
        ConsoleDisplay.show_quiz_list(quizzes)
        
        if quizzes:
            # 1. 삭제할 번호를 콘솔 기기에서 문자열로 입력받음
            del_choice = ConsoleDisplay.get_user_input("\n🗑️ 삭제할 퀴즈 번호를 입력하세요 (취소하려면 그냥 엔터): ")
            
            # 2. 만약 정상적인 숫자를 쳤다면 (isdecimal 검증 통과)
            if del_choice.isdecimal():
                # [★디버깅 주의] 화면에는 사람이 보기 편하라고 1, 2, 3번으로 번호표(enumerate)를 띄웠지만,
                # 컴퓨터 메모리(리스트 인덱스)는 무조건 0, 1, 2번부터 시작함.
                # 따라서 컴퓨터가 엉뚱한 걸 지우지 않도록 입력된 숫자에서 1을 꼭 빼주어야 함 (-1 연산 필수!)
                target_index = int(del_choice) - 1 
                
                # 위에서 도출된 컴퓨터용 인덱스로 삭제를 시도하고, 반환 성공 여부(True/False)에 따라 다르게 UI 출력
                if self.registry.delete_quiz(target_index):
                    ConsoleDisplay.show_success("퀴즈가 삭제되었습니다.")
                else:
                    ConsoleDisplay.show_error("존재하지 않는 번호입니다.")
        return True

@dataclass
class ViewScoreAction(MenuAction):
    # [dataclass 적용] 이 모드는 뭘 저장하거나 목록을 뺄 일이 없고, 오직 눈팅용이므로 '원본 데이터 보따리(app_data)'만 주입받음.
    app_data: dict

    def execute(self) -> bool:
        # 뷰 전담반(ConsoleDisplay)에 원본 보따리 중 최고점수와 히스토리 전용 데이터만 떼어서 던져줌 (=알아서 예쁘게 그려라)
        ConsoleDisplay.show_score_board(self.app_data["best_score"], self.app_data["history"])
        return True

@dataclass
class ExitAction(MenuAction):
    # [dataclass 적용] 종료 시 데이터 저장을 위해 원본 데이터 보따리만 주입받음.
    app_data: dict

    def execute(self) -> bool:
        ConsoleDisplay.show_message("\n데이터를 안전하게 저장하고 프로그램을 종료합니다. 수고하셨습니다!")
        # [종료 전 최후 오토 세이브]: 다른 메뉴를 도는 동안 메모리에만 떠있었을지 모르는 모든 잔여 데이터를 지금 디스크에 강제 저장함
        file_io.save_data(self.app_data)
        
        # [★엔진 기믹의 핵심] 이 수많은 클래스 중에서 오직 얘 혼자 유일하게 False를 반환함!
        # 이 False가 바구니에 담겨 TerminalRunner(지휘자)에게 전달되면,
        # 지휘자는 메인 무한 루프(while True)를 드디어 깨부수고 프로그램을 윈도우상에서 완전히 셧다운시킴.
        return False
