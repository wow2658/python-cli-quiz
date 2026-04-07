class Quiz:
    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def check_answer(self, user_input: int) -> bool:
        """사용자가 입력한 번호가 정답인지 확인하는 메서드"""
        return self.answer == user_input

# ==========================================
# 아래부터는 푸시 전 작동 확인을 위한 임시 테스트 코드입니다.
# ==========================================
if __name__ == "__main__":
    # 1. 가짜 퀴즈 1개를 생성해 봅니다.
    test_quiz = Quiz(
        question="Docker 컨테이너를 백그라운드에서 실행하는 옵션은?", 
        choices=["-a", "-b", "-d", "-f"], 
        answer=3
    )
    
    # 2. 데이터가 잘 들어갔는지 출력해 봅니다.
    print(f"📝 문제: {test_quiz.question}")
    print(f"👉 선택지: {test_quiz.choices}")
    
    # 3. 채점 로직이 잘 돌아가는지 테스트합니다.
    print(f"✅ 정답(3)을 입력했을 때 결과: {test_quiz.check_answer(3)}")
    print(f"❌ 오답(1)을 입력했을 때 결과: {test_quiz.check_answer(1)}")