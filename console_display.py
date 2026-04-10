class ConsoleDisplay:
    """사용자 터미널 입출력을 전담하는 UI 클래스입니다."""

    # ==========================================
    # 1. 공통 메뉴 및 메시지 출력
    # ==========================================
    @staticmethod
    def show_main_menu():
        print("\n========================================")
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 및 삭제")
        print("4. 점수 및 기록 확인")
        print("5. 종료")
        print("========================================")

    @staticmethod
    def get_user_input(prompt: str) -> str:
        """기본 입력 함수 (공백 제거)"""
        return input(prompt).strip()

    @staticmethod
    def show_error(message: str):
        print(f"⚠️ {message}")

    @staticmethod
    def show_success(message: str):
        print(f"✅ {message}")

    @staticmethod
    def show_message(message: str):
        print(message)

    # ==========================================
    # 2. 퀴즈 진행 (플레이) UI
    # ==========================================
    @staticmethod
    def get_question_count(max_count: int):
        """풀고 싶은 문제 수를 사용자로부터 입력받습니다."""
        print(f"\n📂 현재 등록된 퀴즈는 총 {max_count}문제입니다.")
        while True:
            ans = input(f"▶️ 풀고 싶은 문제 수를 입력하세요 (1~{max_count}, 전체 풀기는 엔터, 취소는 'q'): ").strip()
            
            if ans.lower() == 'q':
                return None  # 취소 시그널
            if not ans:
                return max_count  # 그냥 엔터 치면 전체 다 풀기
                
            if ans.isdecimal():
                count = int(ans)
                if 1 <= count <= max_count:
                    return count
            
            ConsoleDisplay.show_error(f"1에서 {max_count} 사이의 숫자를 입력하거나 'q'를 눌러 취소해주세요.")
            
    @staticmethod
    def show_quiz_question(current_idx: int, total_count: int, question: str, choices: list):
        """퀴즈 1문제의 질문과 선택지를 화면에 출력합니다."""
        print("\n" + "-" * 40)
        
        print(f"📝 [문제 {current_idx}/{total_count}]")
        print(question + "\n")
        
        for idx, choice in enumerate(choices, 1):
            print(f"  {idx}. {choice}")
        print("-" * 40)

    @staticmethod
    def get_quiz_answer() -> str:
        """사용자로부터 정답 번호 또는 힌트 요청을 입력받습니다."""
        print("\n💡 힌트가 필요하면 'h'를 입력하세요.")
        return input("▶️ 정답 번호를 입력하세요: ").strip().lower()

    # ==========================================
    # 3. 퀴즈 추가 UI
    # ==========================================
    @staticmethod
    def get_new_quiz_data() -> dict:
        """새로운 퀴즈를 추가하기 위한 데이터를 사용자로부터 순차적으로 입력받습니다."""
        print("\n📌 [새 퀴즈 추가]")
        
        question = input("문제를 입력하세요: ").strip()
        if not question:
            ConsoleDisplay.show_error("빈 문제는 추가할 수 없습니다.")
            return None

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if not choice:
                ConsoleDisplay.show_error(f"선택지 {i}가 비어있습니다. 처음부터 다시 시도해주세요.")
                return None
            choices.append(choice)

        ans_str = input("정답 번호 (1-4): ").strip()
        if not ans_str.isdecimal() or not (1 <= int(ans_str) <= 4):
            ConsoleDisplay.show_error("1에서 4 사이의 숫자로 입력해야 합니다.")
            return None

        hint = input("힌트를 입력하세요 (없으면 엔터): ").strip()
        
        return {
            "question": question,
            "choices": choices,
            "answer": int(ans_str),
            "hint": hint if hint else None
        }

    # ==========================================
    # 4. 목록 조회 및 기록 확인 UI
    # ==========================================
    @staticmethod
    def show_quiz_list(quizzes: list):
        """현재 등록된 퀴즈 목록을 출력합니다."""
        if not quizzes:
            ConsoleDisplay.show_error("등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 [등록된 퀴즈 목록] (총 {len(quizzes)}개)")
        print("=" * 40)
        for i, quiz in enumerate(quizzes, 1):
            # quiz 객체의 속성에 직접 접근합니다 (quiz.py 구조 반영)
            print(f"[{i}] {quiz.question}")
        print("=" * 40)

    @staticmethod
    def show_score_board(best_score: float, history_records: list):
        """최고 점수와 최근 플레이 기록을 출력합니다."""
        print("\n" + "=" * 40)
        print(f"🏆 현재 최고 점수: {best_score}점")
        print("-" * 40)
        print("📜 [최근 플레이 기록]")
        
        if not history_records:
            print("  아직 플레이 기록이 없습니다.")
        else:
            # 최근 기록 5개만 역순으로 출력
            for record in reversed(history_records[-5:]):
                print(f"  [{record['timestamp']}] {record['total_questions']}문제 중 {record['correct_answers']}개 정답 (최종 {record['final_score']}점)")
        print("=" * 40)