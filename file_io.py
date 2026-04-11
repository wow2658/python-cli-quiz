import json
import os
import tempfile

STATE_FILE = "state.json"
DEFAULT_DATA = {
    "quizzes": [
        {
            "question": "Python의 창시자는?",
            "choices": ["Guido", "Linus", "Bjarne", "James"],
            "answer": 1
        },
        {
            "question": "Docker 컨테이너를 백그라운드에서 실행하는 옵션은?",
            "choices": ["-a", "-b", "-d", "-f"],
            "answer": 3
        }
    ],
    "best_score": 0
}

def load_data():
    if not os.path.exists(STATE_FILE):
        print(f"\n[안내] 저장된 데이터({STATE_FILE})가 없습니다. 기본 데이터로 초기화합니다.")
        data = DEFAULT_DATA.copy()
    else:
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                quiz_count = len(data.get("quizzes", []))
                best_score = data.get("best_score", 0)
                print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {best_score}점)")
        except json.JSONDecodeError:
            print(f"\n⚠️ 데이터 파일({STATE_FILE})이 손상되었습니다. 기본 퀴즈 데이터로 복구합니다.")
            data = DEFAULT_DATA.copy()
            
    # 스키마 무결성 보장 (필수 키가 없으면 기본값 세팅)
    if "history" not in data:
        data["history"] = []
    if "best_score" not in data:
        data["best_score"] = 0.0
        
    return data

def save_data(data):
    # Atomic Save: 저장 중 크래시로 인한 파일 증발 원천 차단
    fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(os.path.abspath(STATE_FILE)))
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.close(fd)
    os.replace(temp_path, STATE_FILE)