from abc import ABC, abstractmethod
import file_io
from console_display import ConsoleDisplay
from quiz import Quiz

class MenuAction(ABC):
    @abstractmethod
    def execute(self) -> bool:
        """
        메뉴 동작을 실행합니다.
        루프를 계속 돌려야 하면 True, 종료해야 하면 False를 반환합니다.
        """
        pass

class PlayQuizAction(MenuAction):
    def __init__(self, app_data, registry, game):
        self.app_data = app_data
        self.registry = registry
        self.game = game

    def execute(self) -> bool:
        quizzes = self.registry.get_all_quizzes()
        if not quizzes:
            ConsoleDisplay.show_error("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return True
            
        q_count = ConsoleDisplay.get_question_count(len(quizzes))
        
        if q_count is None:
            ConsoleDisplay.show_message("\n👋 퀴즈 풀기를 취소하고 메인 메뉴로 돌아갑니다.")
            return True

        record = self.game.play(question_count=q_count, randomize=True) 
        
        if record:
            self.app_data["history"].append(record.to_dict())
            
            if record.final_score > self.app_data["best_score"]:
                ConsoleDisplay.show_success(f"🎉 최고 점수 갱신! ({self.app_data['best_score']}점 -> {record.final_score}점)")
                self.app_data["best_score"] = record.final_score
            
            file_io.save_data(self.app_data)
            
        return True

class AddQuizAction(MenuAction):
    def __init__(self, registry):
        self.registry = registry

    def execute(self) -> bool:
        new_quiz_data = ConsoleDisplay.get_new_quiz_data()
        if new_quiz_data:
            new_quiz = Quiz.from_dict(new_quiz_data)
            self.registry.add_quiz(new_quiz)
            ConsoleDisplay.show_success("퀴즈가 성공적으로 추가 및 저장되었습니다!")
        return True

class ListDeleteQuizAction(MenuAction):
    def __init__(self, registry):
        self.registry = registry

    def execute(self) -> bool:
        quizzes = self.registry.get_all_quizzes()
        ConsoleDisplay.show_quiz_list(quizzes)
        
        if quizzes:
            del_choice = ConsoleDisplay.get_user_input("\n🗑️ 삭제할 퀴즈 번호를 입력하세요 (취소하려면 그냥 엔터): ")
            if del_choice.isdecimal():
                target_index = int(del_choice) - 1 
                if self.registry.delete_quiz(target_index):
                    ConsoleDisplay.show_success("퀴즈가 삭제되었습니다.")
                else:
                    ConsoleDisplay.show_error("존재하지 않는 번호입니다.")
        return True

class ViewScoreAction(MenuAction):
    def __init__(self, app_data):
        self.app_data = app_data

    def execute(self) -> bool:
        ConsoleDisplay.show_score_board(self.app_data["best_score"], self.app_data["history"])
        return True

class ExitAction(MenuAction):
    def __init__(self, app_data):
        self.app_data = app_data

    def execute(self) -> bool:
        ConsoleDisplay.show_message("\n데이터를 안전하게 저장하고 프로그램을 종료합니다. 수고하셨습니다!")
        file_io.save_data(self.app_data)
        return False
