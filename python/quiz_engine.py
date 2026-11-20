"""Doremon.ai Python learning engine — runs locally with Python 3.10+.

The GitHub Pages frontend runs Python through Pyodide; this module is a
standalone Python quiz for learners who want to practice in a terminal.
No third-party dependencies or personal information required.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Question:
    prompt: str
    options: tuple[str, str, str]
    correct: int
    explanation: str

QUESTIONS = [
    Question('What does print() do?', ('Displays text', 'Saves a file', 'Starts a loop'), 0, 'print displays output.'),
    Question('What is 7 * 3?', ('10', '21', '73'), 1, '* multiplies numbers.'),
    Question('Which creates a list?', ('(1, 2)', '[1, 2]', '{1: 2}'), 1, 'Lists use square brackets.'),
    Question('What is len("robot")?', ('4', '5', '6'), 1, 'robot contains five letters.'),
    Question('Which keyword defines a function?', ('def', 'func', 'function'), 0, 'Python functions begin with def.'),
    Question('What is 2 ** 4?', ('8', '16', '24'), 1, '** is exponentiation.'),
    Question('What does range(3) yield?', ('0, 1, 2', '1, 2, 3', '0, 1, 2, 3'), 0, 'The stop value is excluded.'),
    Question('Which is a comment?', ('// hello', '# hello', '<!-- hello -->'), 1, 'Python comments start with #.'),
    Question('What is 9 // 2?', ('4', '4.5', '5'), 0, '// performs floor division.'),
    Question('Which value is Boolean?', ('"yes"', 'True', '100'), 1, 'True and False are Booleans.'),
]

def grade(question: Question, choice: int) -> bool:
    """Return whether a zero-based option index is correct."""
    return choice == question.correct

def play() -> int:
    print('🤖 Welcome to Doremon.ai Python Challenge!')
    score = 0
    for number, question in enumerate(QUESTIONS, 1):
        print(f'\\n{number}. {question.prompt}')
        for index, option in enumerate(question.options, 1):
            print(f'  {index}. {option}')
        while True:
            answer = input('Choose 1, 2, or 3 (q to quit): ').strip().lower()
            if answer == 'q':
                return score
            if answer in ('1', '2', '3'):
                break
            print('Please choose 1, 2, or 3.')
        if grade(question, int(answer) - 1):
            score += 1
            print('Correct! 🎉')
        else:
            print('Not quite — keep learning!')
        print(question.explanation)
    print(f'\\nFinal score: {score}/{len(QUESTIONS)}')
    return score

if __name__ == '__main__':
    play()
