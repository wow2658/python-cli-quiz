from dataclasses import dataclass

@dataclass
class Quiz:
    # [dataclass 적용] 파이썬이 아래 선언을 보고 __init__(생성자)을 100% 자동 생성함!
    # 기존의 def __init__(...): self.question = question 같은 반복 코드가 완전히 소멸됨.
    question: str
    choices: list
    answer: int
    hint: str = None  # 선택적 기능으로 추가 (기본값 설정 완료)

    def to_dict(self) -> dict:
        """
        [ 저장하기 공정: 완성품 객체 -> 날것의 부품(딕셔너리)으로 분해]
        하드디스크(파일)에는 멋지게 완성된 파이썬 객체(레고 성)를 그대로 넣을 수 없음.
        그래서 파일 저장을 위해 현재 메모리에 떠있는 복잡한 객체 상태를,
        파일 저장이 가능한 형태인 날것의 파이썬 딕셔너리(해체된 레고 블록)로 완전히 부숴서 분해(직렬화)하여 내보냄.
        이후 메인 로직(json.dump)에서 이 딕셔너리를 납작한 JSON 텍스트로 변환해 박스(파일)에 담아 보관함.
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

    # @classmethod 데코레이터: 기본 공장장(__init__)을 도와주는 보조 공장장 역할.
    # 외부에서 낱개 재료를 주지 않고 "데이터 보따리(딕셔너리)" 포장째로 툭 던져놔도,
    # 알아서 보따리를 푼 뒤 내부 조립공에게 넘겨 객체를 찍어내게 하는 똑똑한 대체 생성자(조립 공장)임.
    @classmethod
    def from_dict(cls, data: dict):
        """
        [ 불러오기 공정: 날것의 부품 보따리 -> 멋진 완성품(객체)으로 조립]
        JSON 상자를 뜯어 막 꺼내온 날것의 파이썬 딕셔너리 데이터(data, 분해된 블록들)를 보따리째로 넘겨받음.
        이 딕셔너리를 재료로 삼아, 우리 프로그램에서 써먹을 수 있는 완벽한 완성품(Quiz 객체)으로 조립(복원)해서 반환함.
        """
        # cls는 이 클래스 자체(Quiz)를 의미함. 즉 Quiz(...) 를 호출하는 것과 100% 동일함.
        return cls(
            # .get()을 사용하여 과거 데이터에 특정 키값이 누락되어 있어도 프로그램이 죽지 않도록 방어하고 기본값을 세팅함.
            question=data.get("question", ""),
            choices=data.get("choices", []),
            answer=data.get("answer", 1),
            hint=data.get("hint")
        )