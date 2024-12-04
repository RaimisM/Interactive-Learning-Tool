import json
import random
import os

class Question:
    def __init__(self, question_id, text, answer, question_type, options=None, active=True, show_count=0, correct_count=0):
        self.question_id = question_id
        self.text = text
        self.answer = answer
        self.question_type = question_type
        self.options = options or []
        self.active = active
        self.show_count = show_count
        self.correct_count = correct_count

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
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            return []
            
    def save_questions(self):
        with open(self.filename, "w") as file:
            json.dump([question.__dict__ for question in self.questions], file, indent=4)
        
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
        correct = 0
        total = 0
        for question in self.question_mode.questions:
            if question.active:
                total += 1
                if question.correct:
                    correct += 1
        return correct, total
    
class PracticeMode:
    def __init__(self, question_mode):
        self.question_mode = question_mode
        
    def practice(self):
        active_question = [question for question in self.question_mode.questions if question.active]
        if len(active_question) < 5:
            print("Add at least 5 active questions to start practice mode")
            return
        
        while True:
            question = random.choice(active_question)
            print(f"\nQuestion:\n{question.text}")

            if question.question_type == "multiple_choice":
                for i, option in enumerate(question.options):
                    print(f"\t{chr(97 + i)}. {option}")
                answer = input("Enter your answer (A, B, C, D or type 'exit' to quit): ").strip().lower()
            elif question.question_type == "free_form":
                answer = input("Type your answer (or type 'exit' to quit): ").strip()
            if answer == "exit":
                return
            
            question.show_count += 1
            if question.question_type == "multiple_choice":
                if question.answer not in question.options:
                    raise ValueError(f"Answer '{question.answer}' is not in the options {question.options}")
                correct_letter = chr(97 + question.options.index(question.answer))
                if answer == correct_letter:
                    print(f"Correct! Answer is {correct_letter}) {question.answer}")
                    question.correct_count += 1
                else:
                    print(f"Wrong! The correct answer is {correct_letter}) {question.answer}")
            elif question.question_type == "free_form":
                if answer.strip().lower() == question.answer.lower():
                    print("Correct!")
                    question.correct_count += 1
                else:
                    print(f"Wrong! The correct answer is: {question.answer}")
            self.question_mode.save_questions()

class TestMode:
    def __init__(self, question_mode, results_file="results.txt"):
        self.question_mode = question_mode
        self.results_file = results_file

    def start(self):
        active_questions = [question for question in self.question_mode.questions if question.active]
        if len(active_questions) < 5:
            print("Add at least 5 active questions to start test mode")
            return
        
        correct = 0
        total = 0
        for question in active_questions:
            print(f"Question: {question.text}")
            if question.question_type == "multiple_choice":
                for idx, option in enumerate(question.options):
                    print(f"{chr(97 + idx)}. {option}")
                answer = input("Enter your answer (A, B, C, D): ").strip().lower()
            elif question.question_type == "free_form":
                answer = input("Type your answer: ").strip().lower()

            if question.question_type == "multiple_choice":
                if question.answer not in question.options:
                    raise ValueError(f"Answer '{question.answer}' is not in the options {question.options}")
                correct_letter = chr(97 + question.options.index(question.answer))
                if answer == correct_letter.lower():
                    print(f"Correct! Answer is {correct_letter}) {question.answer}")
                    question.correct_count += 1
                    correct += 1
                else:
                    print(f"Wrong! The correct answer is {question.answer}")
            elif question.question_type == "free_form":
                if answer == question.answer:
                    print("Correct!")
                    question.correct_count += 1
                    correct += 1
                else:
                    print(f"Wrong! The correct answer is {question.answer}")

            question.show_count += 1
            total += 1
        
        self.question_mode.save_questions()
        score = f"{correct}/{total}"
        print(f"Your score is {score}")
        with open(self.results_file, "a") as file:
            file.write(f"{correct}/{total}\n")


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

        if question_type == "1":
            while True:
                options = input("Enter four options separated by commas: ").split(",")
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
            answer = input("Enter the answer: ").strip().lower()
            question = Question(question_id, text, answer, "free_form")
        
        self.question_mode.add_question(question)
        print("Question added successfully!\n")
    
    def toggle_question(self):
        question_id = int(input("Enter the question id: "))
        question = self.question_mode.find_question_by_id(question_id)
        if question:
            question.active = not question.active
            self.question_mode.save_questions()
            print(f"Question {question_id} is now {'active' if question.active else 'disabled'}")
        else:
            print("Question not found")

class Panel:
    def __init__(self, quiz):
        self.quiz = quiz

    def display(self):
        while True:
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

            