def check_answer(quiz_item, user_answer: int) -> bool:
    """
    사용자가 낸 답안(user_answer)과 실제 객체(quiz_item)가 가진 정답(.answer)이 일치하는지 판별함.
    비교 연산자(==)는 알아서 참/거짓(True/False)을 반환하므로, if문을 쓰지 않고도 한 줄로 깔끔하게 진위를 판별할 수 있음.
    """
    return quiz_item.answer == user_answer

def calculate_score(correct_count: int, total_count: int, penalty: float = 0.0) -> float:
    """맞은 개수와 힌트 페널티를 종합하여 100점 만점 기준의 백분율 점수를 계산함."""
    
    # [안전 장치 1] ZeroDivisionError(0으로 나누기) 방어막
    # 만약 문제 수가 0개일 때 강제로 계산하면 컴퓨터 아키텍처 특성상 치명적 에러가 발생함.
    # 따라서 값이 0이면 아래 계산식을 타지 못하게 즉시 0점을 뱉고 함수를 빠져나감 (Early Return).
    if total_count == 0:
        return 0.0
        
    # 기본 점수 산출: (맞은 개수 / 총 개수) * 100
    base_score = (correct_count / total_count) * 100
    
    # [안전 장치 2] 점수 음수(마이너스) 방어막 (max 함수)
    # 파이썬 내장함수 max(a, b)는 두 값 중 더 큰 숫자를 고르는 기능임.
    # 힌트를 너무 많이 써서 페널티를 맞은 결과가 음수(-10점 등)가 되더라도,
    # 0.0과 -10.0을 비교해서 더 큰 0.0을 고르도록 강제하여 "최하점은 무조건 0점"이 되게 락(Lock)을 검.
    final_score = max(0.0, base_score - penalty)
    
    # [안전 장치 3] 부동소수점 자릿수 폭주 방어막 (round 함수)
    # 컴퓨터의 나눗셈은 83.333333... 처럼 끝없이 이어질 수 있어 화면(UI)이 매우 지저분해짐.
    # round(값, 자릿수) 함수를 통해 깔끔하게 소수점 첫째 자리(1)까지만 반올림하여 반환함.
    return round(final_score, 1)