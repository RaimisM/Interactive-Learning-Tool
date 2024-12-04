from quiz import Question, QuestionMode
from unittest.mock import patch, mock_open

def main():
    test_to_dict()
    test_add_question()
    test_find_question_by_id()

def test_to_dict():
    question = Question(
        question_id=1,
        text="What keyword is used to define a function in Python?",
        answer="def",
        question_type="free_form",
        active=True,
        show_count=5,
        correct_count=3
    )
    expected = {
        "question_id": 1,
        "text": "What keyword is used to define a function in Python?",
        "answer": "def",
        "question_type": "free_form",
        "options": [],
        "active": True,
        "show_count": 5,
        "correct_count": 3,
    }
    assert question.to_dict() == expected

def test_add_question():
    with patch("builtins.open", mock_open(read_data="[]")) as mocked_file:
        question_mode = QuestionMode("test_questions.json")
        question = Question(
            question_id=1,
            text="Which data type is used to store a sequence of characters in Python?",
            answer="string",
            question_type="free_form",
            active=True,
        )
        question_mode.add_question(question)
        assert len(question_mode.questions) == 1
        assert question_mode.questions[0].text == "Which data type is used to store a sequence of characters in Python?"
        mocked_file().write.assert_called()

def test_find_question_by_id():
    question1 = Question(1, "What keyword is used to define a function in Python?", "def", "free_form")
    question2 = Question(2, "What is the output of print(2**3)?", "8", "free_form")
    question_mode = QuestionMode()
    question_mode.questions = [question1, question2]
    found_question = question_mode.find_question_by_id(1)
    assert found_question is not None
    assert found_question.text == "What keyword is used to define a function in Python?"

if __name__ == "__main__":
    main()