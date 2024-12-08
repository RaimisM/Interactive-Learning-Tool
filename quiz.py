import json
import random
import os
from datetime import datetime

class Question:
    def __init__(self, question_id, text, answer, question_type, options=None, active=True, show_count=0, correct_count=0):
        self._question_id = question_id
        self._text = text
        self._answer = answer
        self._question_type = question_type
        self._options = options or []
        self._active = active
        self._show_count = show_count
        self._correct_count = correct_count

    @property
    def question_id(self):
        return self._question_id
    
    @question_id.setter
    def question_id(self, value):
        self._question_id = value

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value

    @property
    def answer(self):
        return self._answer
    
    @answer.setter
    def answer(self, value):
        self._answer = value

    @property
    def question_type(self):
        return self._question_type
    
    @question_type.setter
    def question_type(self, value):
        self._question_type = value

    @property
    def options(self):
        return self._options
    
    @options.setter
    def options(self, value):
        self._options = value

    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        self._active = value

    @property
    def show_count(self):
        return self._show_count
    
    @show_count.setter
    def show_count(self, value):
        self._show_count = value

    @property
    def correct_count(self):
        return self._correct_count
    
    @correct_count.setter
    def correct_count(self, value):
        self._correct_count = value

    def add_show_count(self):
        self._show_count += 1

    def add_correct_count(self):
        self._correct_count += 1

    def calculate_correct_rate(self):
        return (self._correct_count / self._show_count * 100) if self._show_count > 0 else 0

    def is_answer_correct(self, answer):
        if self._question_type == "multiple_choice":
            correct_letter = chr(97 + self._options.index(self._answer))
            return answer == correct_letter.lower()
        elif self._question_type == "free_form":
            return answer.strip().lower() == self._answer.lower()
        return False

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "text": self.text,
            "answer": self.answer,
            "question_type": self.question_type,
            "options": self.options,
            "active": self.active,
            "show_count": self.show_count,
            "correct_count": self.correct_count
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question_id=data.get("question_id"),
            text=data.get("text"),
            answer=data.get("answer"),
            question_type=data.get("question_type"),
            options=data.get("options", []),
            active=data.get("active", True),
            show_count=data.get("show_count", 0),
            correct_count=data.get("correct_count", 0),
        )

class QuestionMode:
    def __init__(self, filename="questions.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file)
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with open(self.filename, "r") as file:
                return [Question(**question) for question in json.load(file)]
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []
            
    def save_questions(self):
        with open(self.filename, "w") as file:
            json.dump([question.to_dict() for question in self.questions], file, indent=4)
        
    def add_question(self, question):
        self.questions.append(question)
        self.save_questions()
        
    def get_question(self):
        return random.choice(self.questions)
        
    def check_answer(self, question, answer):
        return question.answer == answer
        
    def find_question_by_id(self, question_id):
        for question in self.questions:
            if question.question_id == question_id:
                return question
        return None
        
class StatisticsMode:
    def __init__(self, question_mode):
        self.question_mode = question_mode

    def show_statistics(self):
        for question in self.question_mode.questions:
            if question.show_count > 0:
                correct_rate = question.correct_count / question.show_count * 100
            else:
                correct_rate = 0

            print(f"Question ID: {question.question_id}")
            print(f"Active: {'Yes' if question.active else 'No'}")
            print(f"Question Text: {question.text}")
            print(f"Times Shown: {question.show_count}")
            print(f"Correct Answer Percentage: {correct_rate:.2f}%")
            print("-" * 40)

class Answer:
    @staticmethod
    def question_answering(question, answer, question_mode):
        question.add_show_count()

        if question.question_type == "multiple_choice":
            if question.answer not in question.options:
                raise ValueError(f"Answer '{question.answer}' is not in the options {question.options}")
            correct_letter = chr(97 + question.options.index(question.answer))

            if question.is_answer_correct(answer):
                print(f"\033[32mCorrect!\033[0m Answer is {correct_letter}) {question.answer}")
                question.add_correct_count()
            else:
                print(f"\033[91mWrong!\033[0m The correct answer is {correct_letter}) {question.answer}")

        elif question.question_type == "free_form":
            if question.is_answer_correct(answer):
                print("\033[32mCorrect!\033[0m")
                question.add_correct_count()
            else:
                print(f"\033[91mWrong!\033[0m The correct answer is {question.answer}")

        question_mode.save_questions()

class PracticeMode:
    def __init__(self, question_mode):
        self.question_mode = question_mode

    def practice(self):
        active_questions = [question for question in self.question_mode.questions if question.active]
        if len(active_questions) < 5:
            print("Add at least 5 active questions to start practice mode")
            return

        while True:
            weights = [max(1, question.show_count - question.correct_count) for question in active_questions]
            question = random.choices(active_questions, weights=weights, k=1)[0]
            print(f"Question:\n\033[1m{question.text}\033[0m")

            if question.question_type == "multiple_choice":
                for i, option in enumerate(question.options):
                    print(f"\t{chr(97 + i)}. {option}")
                answer = input("Enter your answer (a, b, c, d or type 'exit' to quit): ").strip().lower()
            elif question.question_type == "free_form":
                answer = input("Type your answer (or type 'exit' to quit): ").strip()

            if answer == "exit":
                print("Exiting practice mode")
                return

            Answer.question_answering(question, answer, self.question_mode)

class TestMode:
    def __init__(self, question_mode, results_file="results.txt"):
        self.question_mode = question_mode
        self.results_file = results_file

    def start(self):
        active_questions = [question for question in self.question_mode.questions if question.active]
        if len(active_questions) < 5:
            print("Add at least 5 active questions to start test mode")
            return

        while True:
            try:
                number_questions = int(input(f"Enter the number of questions you want to solve (min 5 - max {len(active_questions)}): "))
                if number_questions < 5 or number_questions > len(active_questions):
                    print(f"Please enter a number between 5 and {len(active_questions)}")
                else:
                    break
            except ValueError:
                print("Invalid number")

        active_questions = random.sample(active_questions, number_questions)

        correct = 0
        total = 0
        for question in active_questions:
            print(f"Question:\n\033[1m{question.text}\033[0m")
            if question.question_type == "multiple_choice":
                for i, option in enumerate(question.options):
                    print(f"\t{chr(97 + i)}. {option}")
                answer = input("Enter your answer (a, b, c, d): ").strip().lower()
            elif question.question_type == "free_form":
                answer = input("Type your answer: ").strip().lower()

            is_correct = question.is_answer_correct(answer)
            Answer.question_answering(question, answer, self.question_mode)

            total += 1
            if is_correct:
                correct += 1

        score = f"{correct}/{total}"
        print(f"\033[93mYour score is {score}\033[0m")
        print("\033[93mThank you for taking the test!\033[0m")
        print("-" * 40)
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.results_file, "a") as file:
            file.write(f"{time} - Score: {score}\n")

class Quiz:
    def __init__(self):
        self.question_mode = QuestionMode()
        self.statistics_mode = StatisticsMode(self.question_mode)
        self.practice_mode = PracticeMode(self.question_mode)
        self.test_mode = TestMode(self.question_mode)

    def add_question(self):
        question_id = len(self.question_mode.questions) + 1
        question_type = input("Select the question type: \n 1. Multiple Choice \n 2. Free Form\n").strip().lower()

        if question_type not in ["1", "2"]:
            print("Invalid choice. For multiple choice, type '1'. For free form, type '2'")
            return

        text = input("Enter the question: ").strip()
        if not text:
            print("Question cannot be empty")
            return

        if question_type == "1":
            while True:
                options = input("Enter four options separated by commas: ").strip().split(",")
                if len(options) != 4:
                    print("Please provide exactly 4 options")
                else:
                    break
            answer = input("Enter the answer: ").strip().lower()
            if answer not in options:
                print("Answer should be one of the options")
                return
            question = Question(question_id, text, answer, "multiple_choice", options)
        
        elif question_type == "2":
            while True:
                answer = input("Enter the answer: ").strip().lower()
                if answer == "":
                    print("Answer can not be empty")
                else:
                    question = Question(question_id, text, answer, "free_form")
                    break
        
        self.question_mode.add_question(question)
        print("Question added successfully!\n")
    
    def toggle_question(self):
        print(f"Active questions ID: {', '.join(str(question.question_id) for question in self.question_mode.questions if question.active)}")
        print(f"Disabled questions ID: {', '.join(str(question.question_id) for question in self.question_mode.questions if not question.active)}")
        
        try:
            question_id = int(input("Enter the question ID: "))
        except ValueError:
            print("Invalid question ID")
            return
        question = self.question_mode.find_question_by_id(question_id)
        if question:
            print(f"Question ID: {question.question_id}")
            print(f"Question Text: {question.text}")
            print(f"Answer: {question.answer}")
            while True:
                confirmation = input(f"Are you sure you want to {'disable' if question.active else 'enable'} this question? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    question.active = not question.active
                    self.question_mode.save_questions()
                    print(f"Question {question_id} is now {'active' if question.active else 'disabled'}")
                    break
                elif confirmation == "no":
                    print("Action cancelled")
                    break
                else:
                    print("Invalid input. Please type 'yes' or 'no'")
        else:
            print("Question not found")

class Panel:
    def __init__(self, quiz):
        self.quiz = quiz

    def display(self):
        while True:
            print("-" * 40)
            print("Select an option:")
            print("1. Add question")
            print("2. Activate/Disable question")
            print("3. Practice mode")
            print("4. Test mode")
            print("5. Show statistics")
            print("6. Exit")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.quiz.add_question()
            elif choice == "2":
                self.quiz.toggle_question()
            elif choice == "3":
                self.quiz.practice_mode.practice()
            elif choice == "4":
                self.quiz.test_mode.start()
            elif choice == "5":
                self.quiz.statistics_mode.show_statistics()
            elif choice == "6":
                print("Goodbye!")
                break

if __name__ == "__main__":
    quiz = Quiz()
    panel = Panel(quiz)
    panel.display()
    question = Question()
    question._active = False
 ##############################################################
 #
 # link to pair programing exercise: https://github.com/RaimisM/war_card_game.git 