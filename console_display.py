class ConsoleDisplay:
    """
    애플리케이션의 뷰(View) 영역을 담당하는 전담 UI(사용자 인터페이스) 클래스임.
    내부적인 데이터 연산이나 파일 저장은 전혀 하지 않고 오직 화면 출력과 단순 입력만 수행함.
    """

    # ==========================================
    # 1. 공통 메뉴 및 메시지 출력
    # ==========================================
    # [★핵심] @staticmethod 데코레이터: 클래스를 객체화(인스턴스 생성)하지 않아도 '클래스명.함수명()'으로 즉시 사용할 수 있게 해줌.
    # self 매개변수가 들어가지 않으며, 상태 저장 없이 누구나 전역적으로 공유해서 쓰는 도구함(공중전화 박스) 같은 역할을 함.
    @staticmethod
    def show_main_menu():
        """메인 화면 UI를 렌더링함."""
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
        """기본 입력 함수. 사용자가 실수로 앞뒤에 넣은 공백을 제거(.strip())하여 반환함."""
        return input(prompt).strip()

    @staticmethod
    def show_error(message: str):
        """에러 메시지임을 시각적으로 분리하기 위해 이모지(⚠️)를 붙여 출력함."""
        print(f"⚠️ {message}")

    @staticmethod
    def show_success(message: str):
        """성공 메시지임을 시각적으로 분리하기 위해 이모지(✅)를 붙여 출력함."""
        print(f"✅ {message}")

    @staticmethod
    def show_message(message: str):
        """일반적인 안내성 시스템 메시지를 출력함."""
        print(message)

    # ==========================================
    # 2. 퀴즈 진행 (플레이) UI
    # ==========================================
    @staticmethod
    def get_question_count(max_count: int):
        """풀이할 문제 개수를 입력받고 꼼꼼하게 유효성을 검증(Validation)함."""
        print(f"\n📂 현재 등록된 퀴즈는 총 {max_count}문제입니다.")
        while True:
            ans = input(f"▶️ 풀고 싶은 문제 수를 입력하세요 (1~{max_count}, 전체 풀기는 엔터, 취소는 'q'): ").strip()
            
            if ans.lower() == 'q':
                return None  # 상위 함수가 알아채고 메인 메뉴로 복귀하도록 취소 시그널 반환
            if not ans:
                return max_count  # 무입력(엔터) 시 전체(최대 개수)로 세팅함
                
            if ans.isdecimal():
                count = int(ans)
                if 1 <= count <= max_count:
                    return count
            
            # 위 정상 조건들에 하나도 걸리지 못하면 에러를 띄우고 while문 첫줄로 무한히 올려보냄
            ConsoleDisplay.show_error(f"1에서 {max_count} 사이의 숫자를 입력하거나 'q'를 눌러 취소해주세요.")
            
    @staticmethod
    def show_quiz_question(current_idx: int, total_count: int, question: str, choices: list):
        """문제 제목과 4개의 선택지를 보기 좋게 나열하여 렌더링함."""
        print("\n" + "-" * 40)
        print(f"📝 [문제 {current_idx}/{total_count}]")
        print(question + "\n")
        
        # [학습] enumerate(리스트, 시작숫자): 단순히 요소만 뽑지 않고 번호(인덱스)표를 함께 뽑아주는 파이썬 내장 기능
        # [학습용 압축풀기 코드] 위 기능은 아래 원시적인 코드 구조를 우아하게 한 줄로 줄인 것임:
        # idx = 1
        # for choice in choices:
        #     print(f"  {idx}. {choice}")
        #     idx = idx + 1
        for idx, choice in enumerate(choices, 1):
            print(f"  {idx}. {choice}")
        print("-" * 40)

    @staticmethod
    def get_quiz_answer() -> str:
        """정답 번호 또는 힌트 요청(h) 키입력을 받음."""
        print("\n💡 힌트가 필요하면 'h'를 입력하세요.")
        return input("▶️ 정답 번호를 입력하세요: ").strip().lower()

    # ==========================================
    # 3. 퀴즈 추가 UI
    # ==========================================
    @staticmethod
    def get_new_quiz_data() -> dict:
        """새로운 퀴즈 추가를 위해 문제, 선택지, 정답, 힌트를 순차 입력받고 하나의 딕셔너리 보따리로 포장해 반환함."""
        print("\n📌 [새 퀴즈 추가]")
        
        question = input("문제를 입력하세요: ").strip()
        if not question:
            ConsoleDisplay.show_error("빈 문제는 추가할 수 없습니다.")
            return None # 하나라도 조건 미달 시 즉시 함수를 빠져나감 (Early Return)

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if not choice:
                ConsoleDisplay.show_error(f"선택지 {i}가 비어있습니다. 처음부터 다시 시도해주세요.")
                return None
            choices.append(choice)

        ans_str = input("정답 번호 (1-4): ").strip()
        # 입력이 문자가 섞이지 않은 순수 숫자인지 여부와, 지정된 1~4 범위 내에 있는지 이중 검증함
        if not ans_str.isdecimal() or not (1 <= int(ans_str) <= 4):
            ConsoleDisplay.show_error("1에서 4 사이의 숫자로 입력해야 합니다.")
            return None

        hint = input("힌트를 입력하세요 (없으면 엔터): ").strip()
        
        # 모든 폭탄 검증을 통과해야만 최종적으로 딕셔너리를 생성하여 반환함
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
        """메모리에 등록된 모든 퀴즈 목록을 순서대로 나열하여 출력함."""
        if not quizzes:
            ConsoleDisplay.show_error("등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 [등록된 퀴즈 목록] (총 {len(quizzes)}개)")
        print("=" * 40)
        # [학습용 압축풀기 코드] 위 enumerate 기능은 아래 원시적인 일반 for문 구조를 완전히 대체함:
        # i = 1
        # for quiz in quizzes:
        #     print(f"[{i}] {quiz.question}")
        #     i = i + 1
        for i, quiz in enumerate(quizzes, 1):
            # 외부에서 전달받은 멋진 quiz 객체 모델의 내부 속성값(.question)을 직접 접근하여 출력함
            # (만약 quiz가 날것의 딕셔너리였다면 quiz["question"] 형태로 번거롭게 써야 했음)
            print(f"[{i}] {quiz.question}")
        print("=" * 40)

    @staticmethod
    def show_score_board(best_score: float, history_records: list):
        """가장 높은 최고 점수와 큐(Queue/파이프) 형태로 관리되는 최근 플레이 기록을 출력함."""
        print("\n" + "=" * 40)
        print(f"🏆 현재 최고 점수: {best_score}점")
        print("-" * 40)
        print("📜 [최근 플레이 기록]")
        
        if not history_records:
            print("  아직 플레이 기록이 없습니다.")
        else:
            # [학습] 파이썬 리스트 슬라이싱(Slicing)과 뒤집기(reversed) 기법
            # 1. [-5:] 의 의미: 
            #    파이썬은 목록을 앞에서부터 0, 1, 2... 세는 기능뿐만 아니라, 맨 뒤에서부터 -1, -2... 로 역추적하는 기능도 있음.
            #    즉, [-5:]라는 문법은 "뒤에서 5번째(-5) 위치부터 맨 끝(:)까지 싹둑 잘라서 가져와라!"라는 뜻임.
            #    이 덕분에 게임을 100판을 했더라도 무조건 최신 기록 5개만 깔끔하게 퍼올릴 수 있음.
            
            # 2. reversed(...) 의 의미:
            #    데이터를 .append()로 밀어 넣으면 최신 데이터일수록 리스트의 맨 오른쪽 마지막 칸에 쌓임.
            #    퍼온 5개를 그대로 화면에 출력하면 과거 기록이 위에 뜨고, 방금 플레이한 최신 기록이 맨 아래로 내려가 버림.
            #    이것을 방지하기 위해 reversed()를 먹여서 순서를 180도 뒤집어주는 것임. (최신 기록이 모니터 최상단에 뜨게 됨)
            for record in reversed(history_records[-5:]):
                # (주의: record는 멋진 클래스 객체가 아니라, 게임이 끝나고 저장하기 쉽게 구운 '날것의 딕셔너리'임.
                #  그래서 점(record.timestamp)을 쓰지 못하고, 문자열 열쇠 꾸러미(record['timestamp']) 방식을 사용함)
                print(f"  [{record['timestamp']}] {record['total_questions']}문제 중 {record['correct_answers']}개 정답 (최종 {record['final_score']}점)")
        print("=" * 40)