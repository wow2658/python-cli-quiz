import random
from console_display import ConsoleDisplay
from hint_penalty import HintPenaltyCalculator
from score_history import ScoreRecord
import quiz_evaluator

class QuizGame:
    def __init__(self, registry):
        # 퀴즈 목록을 들고 있는 레지스트리 객체를 주입받습니다 (의존성 주입)
        self.registry = registry

    def play(self, question_count: int = None, randomize: bool = False) -> ScoreRecord:
        """
        퀴즈 게임 1회차를 실행합니다.
        - question_count: 풀고 싶은 문제 수 (기본값: 전체)
        - randomize: 랜덤 출제 여부 (기본값: False)
        """
        quizzes = self.registry.get_all_quizzes()
        if not quizzes:
            ConsoleDisplay.show_error("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return None

        # 원본 데이터를 훼손하지 않기 위해 얕은 복사본으로 플레이 리스트 생성
        play_list = quizzes[:]
        
        if randomize:
            random.shuffle(play_list)
            
        if question_count and 0 < question_count < len(play_list):
            play_list = play_list[:question_count]

        hint_calc = HintPenaltyCalculator(penalty_points=5.0) # 힌트 1회당 5점 감점
        correct_count = 0
        correct_indices = []

        ConsoleDisplay.show_message(f"\n🚀 퀴즈를 시작합니다! (총 {len(play_list)}문제)")

        for i, current_quiz in enumerate(play_list, 1):
            ConsoleDisplay.show_quiz_question(i, len(play_list), current_quiz.question, current_quiz.choices)
            
            # 올바른 정답이 들어올 때까지 무한 루프
            while True:
                ans_str = ConsoleDisplay.get_quiz_answer()
                
                # 힌트 처리 로직
                if ans_str == 'h':
                    hint_msg = hint_calc.get_hint(i, current_quiz.hint)
                    ConsoleDisplay.show_message(f"\n💡 [힌트] {hint_msg}")
                    continue
                    
                if not ans_str.isdigit():
                    ConsoleDisplay.show_error("숫자 또는 힌트('h')만 입력해주세요.")
                    continue
                    
                ans_int = int(ans_str)
                if not (1 <= ans_int <= len(current_quiz.choices)):
                    ConsoleDisplay.show_error(f"1에서 {len(current_quiz.choices)} 사이의 번호를 선택해주세요.")
                    continue
                    
                break # 정상적인 숫자가 입력되면 루프 탈출

            # 채점기 연동
            if quiz_evaluator.check_answer(current_quiz, ans_int):
                ConsoleDisplay.show_success("정답입니다!")
                correct_count += 1
                correct_indices.append(i) # 힌트 감점을 위해 맞춘 문제의 인덱스 기억
            else:
                ConsoleDisplay.show_error(f"틀렸습니다! (정답: {current_quiz.answer}번)")

        # 최종 점수 정산
        penalty = hint_calc.calculate_penalty_deduction(correct_indices)
        final_score = quiz_evaluator.calculate_score(correct_count, len(play_list), penalty)
        
        ConsoleDisplay.show_message("\n" + "="*40)
        ConsoleDisplay.show_message(f"🏆 게임 종료! {len(play_list)}문제 중 {correct_count}문제 정답!")
        if penalty > 0:
            ConsoleDisplay.show_message(f"📉 힌트 사용으로 인한 감점: -{penalty}점")
        ConsoleDisplay.show_message(f"✨ 최종 점수: {final_score}점")
        ConsoleDisplay.show_message("="*40)
        
        # 게임 결과를 기록 객체로 만들어 반환
        return ScoreRecord(len(play_list), correct_count, final_score)