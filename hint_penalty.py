from dataclasses import dataclass, field

@dataclass
class HintPenaltyCalculator:
    """기본 감점 수치를 설정합니다. (기본값: 0.5점)"""
    # [dataclass 적용] 외부에서 주입받는 감점 수치 (기본값 제공)
    penalty_points: float = 0.5
    # field(init=False): 힌트 사용 기록은 내부 상태이므로 밖에서 주입받지 않고 직접 초기화함.
    used_hints_indices: set = field(init=False)

    def __post_init__(self):
        # [dataclass 후처리] 힌트를 사용한 문제의 인덱스를 기록할 빈 세트를 생성
        self.used_hints_indices = set()

    def get_hint(self, quiz_index: int, hint_text: str) -> str:
        """힌트를 요청받으면 반환하고, 해당 문제의 인덱스를 사용 기록에 추가합니다."""
        if not hint_text:
            return "등록된 힌트가 없습니다."
        
        self.used_hints_indices.add(quiz_index)
        return hint_text

    def calculate_penalty_deduction(self, correct_indices: list) -> float:
        """정답을 맞춘 문제 중, 힌트를 사용한 문제 수에 비례하여 총 감점액을 계산합니다."""
        deduction = 0.0
        for idx in correct_indices:
            if idx in self.used_hints_indices:
                deduction += self.penalty_points
        return deduction
    
    def reset(self):
        """새 게임 시작 시 힌트 사용 기록을 초기화합니다."""
        self.used_hints_indices.clear()