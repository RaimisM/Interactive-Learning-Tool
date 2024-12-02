import json
import random
import sys

class Question:
    def __init__(self, question_id, text, answer, question_type, options=None, active=True):
        self.question_id = question_id
        self.text = text
        self.answer = answer
        self.question_type = question_type
        self.options = options
        self.active = active
class QuestionMode:
    def __init__(self, filename="questions.json"):
        self.filename = filename
        self.questions = self.load_questions()

        def load_questions(self):
            with open(self.filename, "r") as file:
                return json.load(file)
            
        def save_questions(self):
            with open(self.filename, "w") as file:
                json.dump(self.questions, file)
        
        def add_question(self, question, answer):
            self.questions.append({"question": question, "answer": answer})
            self.save_questions()
        
        def get_question(self):
            return random.choice(self.questions)
        
        def check_answer(self, question, answer):
            return question["answer"] == answer
        
        def find_question_by_id(self, id):
            return self.questions[id]
        
class StatisticsMode:
    def __init__(self, question_mode):
        self.question_mode = question_mode

    def show_statistics(self):
        correct = 0
        total = 0
        for question in self.question_mode.questions:
            if question["active"]:
                total += 1
                if question["correct"]:
                    correct += 1
        return correct, total
    
class PracticeMode:
    def __init__(self, queastion_mode):
        self.question_mode = question_mode
        
    def practice(self):
        active_question = self.question_mode.get_question()
        if len(active question) < 5:
            print("Add at least 5 active questions to start practice mode")
            return
        
        while True:
            question = random.choice(active_question)
            print(f"Question: {question.text}")
            if question.question_type == "multiple_choice":
                print("Options:", ", ".join(question.options))
            answer = input("Enter your answer: ").strip().lower()
            if answer == "exit":
                break
            
            question.show_count += 1
            if answer == question.answer:
                print("Correct!")
                question.correct_count += 1
            else:
                print(f"Wrong! The correct answer is {question.answer}")
        
        self.question_mode.save_questions()

class TestMode:
    def __init__(self, question_mode, results_file="results.txt"):
        self.question_mode = question_mode
        self.results_file = results_file

    def start(self):
        active_questions = [question for question in self.question_mode.questions if question["active"]]
        if len(active_questions) < 5:
            print("Add at least 5 active questions to start test mode")
            return
        
        correct = 0
        total = 0
        for question in active_questions:
            print(f"Question: {question.text}")
            if question.question_type == "multiple_choice":
                print("Options:", ", ".join(question.options))
            answer = input("Enter your answer: ").strip().lower()
            if self.question_mode.check_answer(question, answer):
                print("Correct!")
                question["correct"] = True
                correct += 1
            else:
                print(f"Wrong! The correct answer is {question['answer']}")
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
            question_type = input("Enter the question type (multiple_choice or free_form): ").strip().lower()
            text = input("Enter the question: ").strip()
            if question_type == "multiple_choice":
                options = input("Enter the options separated by commas: ").split(",")
                answer = input("Enter the answer: ").strip().lower()
                question = Question(question_id, text, answer, question_type, options)
            elif question_type == "free_form":
                answer = input("Enter the answer: ").strip().lower()
                question = Question(question_id, text, answer, question_type)
            else:
                sys.exit("Invalid question type")

            self.question_mode.add_question(question)
            print("Question added successfully!")

        def toggle_question(self):
            question_id = int(input("Enter the question id: "))
            question = self.question_mode.find_question_by_id(question_id)
            if question:
                question["active"] = not question["active"]
                self.question_mode.save_questions()
                print(f"Question {question_id} is now {'active' if question['active'] else 'disabled'}")
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

            