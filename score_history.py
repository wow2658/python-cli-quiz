import datetime
from dataclasses import dataclass, field

@dataclass
class ScoreRecord:
    # [dataclass 적용] 3개의 성적 데이터를 외부에서 주입받음.
    total_questions: int
    correct_answers: int
    final_score: float
    # field(init=False): 타임스탬프는 밖에서 넣어주는 것이 아니라 생성 시 자동으로 기록됨.
    timestamp: str = field(init=False)

    def __post_init__(self):
        # [dataclass 후처리] 인스턴스 생성 시점의 시간을 자동으로 기록
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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