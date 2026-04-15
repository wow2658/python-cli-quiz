from dataclasses import dataclass, field
from quiz import Quiz

@dataclass
class QuizRegistry:
    # [dataclass 적용] file_io에서 불러온 원본 데이터(보따리)를 복사하지 않고 그대로 참조(Reference)함.
    # (이로 인해 여기서 데이터를 수정하면 원본 app_data도 실시간으로 함께 변동됨)
    app_data: dict
    
    # field(init=False): "이건 밖(main)에서 주입받는 택배가 아니라, 내가 내부에서 직접 만들거야!"
    # 자동 생성되는 __init__의 매개변수 목록에서 quizzes를 제외하라는 지시임.
    quizzes: list = field(init=False)

    def __post_init__(self):
        # [dataclass 후처리] 자동 생성된 __init__이 끝난 직후, 곧바로 이 함수가 연달아 실행됨.
        # 원본 데이터 내부의 날것(딕셔너리) 리스트를 Quiz 객체 리스트로 변환하여 메모리에 적재함.
        # [학습용 압축풀기 코드] 기능적으로 아래 주석 코드와 100% 동일함:
        # temp_list = []
        # for q in self.app_data.get("quizzes", []):
        #     temp_list.append(Quiz.from_dict(q))
        # self.quizzes = temp_list
        self.quizzes = [Quiz.from_dict(q) for q in self.app_data.get("quizzes", [])]

    def add_quiz(self, quiz_item: Quiz) -> None:
        """새로운 퀴즈 객체를 내부 목록 끝에 추가함."""
        self.quizzes.append(quiz_item)
        # 리스트에 객체가 추가되었으므로 원본 app_data 딕셔너리 상태를 즉시 동기화함
        self._sync_to_app_data()

    def delete_quiz(self, index: int) -> bool:
        """
        지정된 인덱스(0부터 시작)의 퀴즈를 메모리에서 삭제함.
        보유 개수 내의 정상적인 인덱스일 경우 삭제 후 True 반환, 벗어나면 False 반환.
        """
        if 0 <= index < len(self.quizzes):
            del self.quizzes[index]
            # 리스트 객체가 삭제되었으므로 원본 app_data 딕셔너리 상태를 즉시 동기화함
            self._sync_to_app_data()
            return True
        return False

    def get_all_quizzes(self) -> list:
        """현재 메모리에 등록된 모든 Quiz 객체 리스트를 반환함."""
        return self.quizzes

    def _sync_to_app_data(self) -> None:
        """
        메모리 상의 Quiz 객체들을 저장하기 좋은 일반 딕셔너리로 분해해 원본 app_data에 덮어씀.
        (함수명 앞의 언더바(_)는 클래스 내부에서만 쓰는 Private 용도라는 암묵적 약속임)
        """
        # [학습용 압축풀기 코드] 기능적으로 아래 주석 코드와 100% 동일함:
        # temp_list = []
        # for q in self.quizzes:
        #     temp_list.append(q.to_dict())
        # self.app_data["quizzes"] = temp_list
        self.app_data["quizzes"] = [q.to_dict() for q in self.quizzes]