class Quiz:
    def __init__(self, question: str, choices: list, answer: int, hint: str = None):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint  # 선택적 기능으로 추가 (기본값 None)

    def to_dict(self) -> dict:
        """파일 저장을 위해 객체를 딕셔너리로 직렬화합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, data: dict):
        """딕셔너리 데이터에서 Quiz 객체를 복원합니다."""
        return cls(
            question=data.get("question", ""),
            choices=data.get("choices", []),
            answer=data.get("answer", 1),
            hint=data.get("hint")
        )