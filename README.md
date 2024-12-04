# Quiz Application

This application allows users to add and manage quiz questions, practice, and test their knowledge. The program supports multiple modes, as described below.

## Modes

### 1. Adding Questions
- Users can add two types of questions:
  1. **Quiz Questions:** Requires selecting one correct answer from multiple options.
  2. **Free-Form Questions:** Requires the user to input a text answer, which is compared to the expected answer.
- Questions are saved to a file to persist between sessions.
- A minimum of 5 questions must be added before accessing **Practice** or **Test** modes.

### 2. Statistics Viewing
- Displays all questions currently in the system, including:
  - Unique ID number.
  - Active/disabled status.
  - Question text.
  - Number of times the question was shown in practice/tests.
  - Percentage of correct answers.

### 3. Disable/Enable Questions
- Users can toggle the status (active/disabled) of a question by its ID.
- The question details are shown for confirmation before making changes.

### 4. Practice Mode
- Offers non-stop practice questions.
- Questions answered incorrectly appear more frequently, while those answered correctly appear less often.
- Probabilities persist between sessions.

### 5. Test Mode
- Users can take a test with a specified number of questions.
- Questions are chosen randomly and do not repeat within a single test.
- At the end of the test, the user is shown their score.
- Scores, along with the date and time, are saved in `results.txt`.

## File Structure
- quiz.py
- README.md
- results.txt
- questions.json
- test_quiz.py
- LICENSE

