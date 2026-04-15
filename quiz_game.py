import random
from dataclasses import dataclass
from console_display import ConsoleDisplay
from hint_penalty import HintPenaltyCalculator
from score_history import ScoreRecord
import quiz_evaluator

@dataclass
class QuizGame:
    # [dataclass 적용] 퀴즈 게임의 핵심 로직(진행, 셔플, 채점, 결과 반환)을 총괄하는 게임 엔진 클래스임.
    # 퀴즈들을 보관하고 있는 '퀴즈 관리국(registry)' 객체를 외부로부터 주입받음.
    # 이를 통해 메모리/DB 관리 역할과 게임 진행이라는 역할을 서로 완벽하게 분리(디커플링)함.
    registry: 'QuizRegistry'

    def play(self, question_count: int = None, randomize: bool = False) -> ScoreRecord:
        """
        퀴즈 게임 1판(1사이클)을 실행함.
        입력받은 횟수만큼 문제를 출제하고, 다 끝나면 성적표(ScoreRecord 객체)를 반환함.
        """
        # 1. 퀴즈 관리국에서 전체 퀴즈 리스트를 퍼옴.
        quizzes = self.registry.get_all_quizzes()
        if not quizzes:
            ConsoleDisplay.show_error("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요!")
            return None # 조기 종료 (Early Return)

        # [학습] 리스트의 얕은 복사본(Shallow Copy) 기법 등장 ( [:] )
        # 게임을 하다가 문제 순서를 섞거나 지울 일이 생기는데, 만약 원본 주소(quizzes)를 바로 갖다 쓰면
        # 관리국 내부의 진짜 원본 데이터 순서까지 뒤죽박죽 섞여버리는 대참사가 일어남.
        # 이를 막기 위해 원본은 안전하게 둔 채 내용물 배열만 새롭게 복사해서 플레이 전용 리스트(play_list)를 만듦.
        play_list = quizzes[:]
        
        if randomize:
            # random 패키지를 사용해, 방금 만든 '복사본' 리스트 내부의 순서를 무작위로 마구 섞음
            random.shuffle(play_list)
            
        # 만약 유저가 전체 문제를 다 안 풀고 5문제만 풀겠다고 넘겼다면 (question_count가 있고, 총 길이보다 작다면)
        if question_count and 0 < question_count < len(play_list):
            # 맨 앞에서부터 요청한 개수만큼 슬라이싱(:)으로 싹둑 잘라서 플레이 리스트 길이를 줄임
            play_list = play_list[:question_count]

        # 힌트를 한 번 쓸 때마다 -5점을 깎는 페널티 계산기(독립적인 특수 모듈) 객체를 가동(생성)시킴
        hint_calc = HintPenaltyCalculator(penalty_points=5.0)
        correct_count = 0 
        
        # [살생부 기능] "정답을 맞춘 문제 중 힌트를 쓴 문제"에만 나중에 감점을 때리기 위해, 
        # 일단 정답을 맞출 때마다 그 문제 번호를 적어 두는 리스트임.
        correct_indices = [] 

        ConsoleDisplay.show_message(f"\n🚀 퀴즈를 시작합니다! (총 {len(play_list)}문제)")

        # [자동 번호표 기계] enumerate를 써서 1번부터 인덱스(i)와 리스트 내용(current_quiz)을 차례대로 뽑아냄
        for i, current_quiz in enumerate(play_list, 1):
            # 뷰 담당자(ConsoleDisplay)를 호출해 화면에 문항을 예쁘게 그려줌
            ConsoleDisplay.show_quiz_question(i, len(play_list), current_quiz.question, current_quiz.choices)
            
            # [입력 방어막] 사용자가 제대로 된 입력(1번~4번 사이 등)을 칠 때까지 무한정 뺑뺑이 돌리는 루프임.
            while True:
                ans_str = ConsoleDisplay.get_quiz_answer()
                
                # 🔥 특수 로직: 'q'를 치면 게임을 통째로 포기해 버림
                if ans_str == 'q':
                    ConsoleDisplay.show_message("\n👋 퀴즈를 중도 포기하셨습니다. 메인 메뉴로 돌아갑니다.")
                    # return None으로 던져버리면, 이 게임을 호출한 상위(MenuAction)단에서 
                    # 성적(record)이 안 왔네? 하고 하드디스크에 기록조차 남기지 않고 깔끔히 메인으로 돌아감.
                    return None
                
                # 🔥 특수 로직: 'h'를 치면 힌트 출력기능이 발동됨
                if ans_str == 'h':
                    # 페널티 계산기에게 "나 i번 문제 힌트 좀 볼래!" 라고 요청하고 힌트 문구를 받아옴
                    hint_msg = hint_calc.get_hint(i, current_quiz.hint)
                    ConsoleDisplay.show_message(f"\n💡 [힌트] {hint_msg}")
                    continue # 힌트만 보고 통과시켜주는 것이 아니므로, 위로 올려보내 다시 정답(숫자)을 치게 만듦.
                    
                # 입력값이 아직 숫자가 아니면 (이상한 문자 등을 썼을 때 튕겨냄)
                if not ans_str.isdecimal():
                    ConsoleDisplay.show_error("숫자 또는 힌트('h'), 포기('q')만 입력해주세요.")
                    continue
                    
                ans_int = int(ans_str)
                # 입력한 숫자가 객체가 가진 선택지 전체 길이(1~4번 등) 범위를 완전히 벗어나면 (예: 99번을 입력)
                if not (1 <= ans_int <= len(current_quiz.choices)):
                    ConsoleDisplay.show_error(f"1에서 {len(current_quiz.choices)} 사이의 번호를 선택해주세요.")
                    continue
                    
                # 위 온갖 깐깐한 조건들을 돌파했다면 드디어 이 무한 방어벽 루프를 부수고(break) 채점 단계로 진입함!
                break 

            # 채점 전담반(quiz_evaluator)에 '문제본체객체'와 '유저입력값'을 넘겨서 일치 진위를 판별함
            if quiz_evaluator.check_answer(current_quiz, ans_int):
                ConsoleDisplay.show_success("정답입니다!")
                correct_count += 1
                correct_indices.append(i) # 어? 정답 맞췄네? 나중에 힌트 감점 때리기 위해 번호를 살생부에 적어둠
            else:
                ConsoleDisplay.show_error(f"틀렸습니다! (정답: {current_quiz.answer}번)")

        # ==== 모든 for문(퀴즈 1바퀴 반복)이 모조리 끝난 후 내려오는 최종 정산 구역 ====
        
        # 페널티 계산기에게 아까 차곡차곡 적었던 살생부(정답을 맞춘 문제 번호 리스트)를 넘겨줘서 최종 감점할 수치를 뜯어냄
        penalty = hint_calc.calculate_penalty_deduction(correct_indices)
        
        # 다시 채점 전담반에게 방금 받아온 penalty 점수를 넘겨서 최종 100점 만점 기준의 점수 계산을 위임함 (아까 본 그 방어막 함수)
        final_score = quiz_evaluator.calculate_score(correct_count, len(play_list), penalty)
        
        # 뷰 담당자에게 최종 스코어보드를 화면에 뿌리라고 지시함 (출력 노동 위임)
        ConsoleDisplay.show_message("\n" + "="*40)
        ConsoleDisplay.show_message(f"🏆 게임 종료! {len(play_list)}문제 중 {correct_count}문제 정답!")
        if penalty > 0:
            ConsoleDisplay.show_message(f"📉 힌트 사용으로 인한 감점: -{penalty}점") # 힌트를 써서 감점된 전적이 있으면 추가로 띄움
        ConsoleDisplay.show_message(f"✨ 최종 점수: {final_score}점")
        ConsoleDisplay.show_message("="*40)
        
        # [데이터 포장] 낱갈래로 흩어져 계산되던 결과들(총 갯수, 맞춘 갯수, 내점수 등)을
        # 오직 '성적표 객체 구조체(ScoreRecord)'로 예쁘게 포장해서 바깥(MenuAction)으로 툭 던져서 넘겨줌!
        return ScoreRecord(len(play_list), correct_count, final_score)