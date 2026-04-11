import file_io
from quiz_registry import QuizRegistry
from quiz_game import QuizGame
from menu_actions import (
    PlayQuizAction, 
    AddQuizAction, 
    ListDeleteQuizAction, 
    ViewScoreAction, 
    ExitAction
)
from terminal_runner import TerminalRunner

def main():
    # 1. 파일에서 기존 데이터 로드 (스키마 검증은 file_io가 자체 보장함)
    app_data = file_io.load_data()

    # 2. 필수 시스템 의존성(Dependency) 객체 조립
    registry = QuizRegistry(app_data)
    game = QuizGame(registry)

    # 3. 메뉴 액션(행동) 매핑 - Command 패턴
    actions = {
        1: PlayQuizAction(app_data, registry, game),
        2: AddQuizAction(registry),
        3: ListDeleteQuizAction(registry),
        4: ViewScoreAction(app_data),
        5: ExitAction(app_data)
    }

    # 4. 애플리케이션 수명주기 전담 객체(Runner) 실행
    runner = TerminalRunner(actions, app_data)
    runner.run()

if __name__ == "__main__":
    main()