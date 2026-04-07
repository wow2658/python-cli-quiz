from quiz import Quiz

class QuizGame:
    def __init__(self, quiz_list: list):
        self.quiz_list = quiz_list
        self.score = 0
        self.current_index = 0

    def next_quiz(self) -> Quiz:
        """다음 문제를 반환 (더 이상 없으면 None)"""
        if self.current_index < len(self.quiz_list):
            quiz = self.quiz_list[self.current_index]
            self.current_index += 1
            return quiz
        return None

    def add_score(self):
        self.score += 1

    def get_final_score(self) -> str:
        return f"최종 점수: {self.score} / {len(self.quiz_list)}"