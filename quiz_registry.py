from quiz import Quiz

class QuizRegistry:
    def __init__(self, app_data: dict):
        # file_io에서 불러온 원본 데이터를 참조합니다.
        self.app_data = app_data
        # 딕셔너리 리스트를 Quiz 객체 리스트로 변환하여 메모리에 올립니다.
        self.quizzes = [Quiz.from_dict(q) for q in app_data.get("quizzes", [])]

    def add_quiz(self, quiz_item: Quiz) -> None:
        """새로운 퀴즈를 목록에 추가합니다."""
        self.quizzes.append(quiz_item)
        self._sync_to_app_data()

    def delete_quiz(self, index: int) -> bool:
        """
        지정된 인덱스(0부터 시작)의 퀴즈를 삭제합니다.
        성공 시 True, 범위를 벗어나면 False를 반환합니다.
        """
        if 0 <= index < len(self.quizzes):
            del self.quizzes[index]
            self._sync_to_app_data()
            return True
        return False

    def get_all_quizzes(self) -> list:
        """현재 등록된 모든 Quiz 객체 리스트를 반환합니다."""
        return self.quizzes

    def _sync_to_app_data(self) -> None:
        """메모리의 Quiz 객체 상태를 다시 딕셔너리로 변환해 app_data에 덮어씁니다."""
        self.app_data["quizzes"] = [q.to_dict() for q in self.quizzes]