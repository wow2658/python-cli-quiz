def check_answer(quiz_item, user_answer: int) -> bool:
    """사용자의 입력이 퀴즈의 정답과 일치하는지 검증합니다."""
    return quiz_item.answer == user_answer

def calculate_score(correct_count: int, total_count: int, penalty: float = 0.0) -> float:
    """
    백분율 기반 점수를 계산하고 힌트 페널티를 적용합니다.
    최하 점수는 0점 미만으로 내려가지 않습니다.
    """
    if total_count == 0:
        return 0.0
        
    base_score = (correct_count / total_count) * 100
    final_score = max(0.0, base_score - penalty)
    
    return round(final_score, 1)