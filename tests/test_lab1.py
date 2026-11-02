import json, pytest
from pathlib import Path
from actualwork.lab1.needleman_wunsch import get_score_and_alignment

@pytest.fixture(scope="module")
def test_data():
    json_path = Path(__file__).parent / "lab1_test_cases.json"
    with json_path.open(encoding="utf-8") as f:
        return json.load(f)

def test_needleman(test_data):
    for case in test_data["cases"].values():
        score, seq1, seq2 = get_score_and_alignment(*case["input"], *case["penalty"])
        true_score, true_seq1, true_seq2 = case["output"]
        assert(score == true_score)
        assert(any([seq == true_seq1 for seq in seq1])) # ПЕРЕДЕЛАТЬ!
        assert(any([seq == true_seq2 for seq in seq2])) # ПЕРЕДЕЛАТЬ!