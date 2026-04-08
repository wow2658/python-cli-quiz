def check_answer(quiz, user_answer_int):
    """사용자 입력이 정답인지 판정"""
    return quiz["answer"] == user_answer_int

def calculate_score(score, total_q):
    """100점 만점 기준으로 점수 환산"""
    if total_q == 0: return 0
    return int((score / total_q) * 100)

def create_quiz_entry(question, choices, answer_int):
    """새로운 퀴즈 딕셔너리 객체 생성"""
    return {
        "question": question,
        "choices": choices,
        "answer": answer_int
    }