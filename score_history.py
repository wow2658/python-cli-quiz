import datetime

class ScoreRecord:
    def __init__(self, total_questions: int, correct_answers: int, final_score: float):
        # 인스턴스 생성 시점의 시간을 자동으로 기록
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.final_score = final_score

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "final_score": self.final_score
        }

    @classmethod
    def from_dict(cls, data: dict):
        # 과거 기록 복원 시 사용
        record = cls(
            total_questions=data.get("total_questions", 0),
            correct_answers=data.get("correct_answers", 0),
            final_score=data.get("final_score", 0.0)
        )
        record.timestamp = data.get("timestamp", "Unknown Date")
        return record