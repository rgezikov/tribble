import os
import random
import yaml


def main():

    file_name = os.path.join(os.path.dirname(__file__), "imperfektikoe-1.yaml")
    with open(file_name) as inf:
        data = yaml.safe_load(inf)

    questions = data['questions']
    random.shuffle(questions)

    max_len = max([len(x[0]) for x in questions])

    total_questions = len(questions)
    current_question = 1
    all_done = True
    for question in questions:
        question_len = len(question[0])
        question_str = question[0] + ' ' * (max_len - question_len)
        answer = input(f"({current_question}/{total_questions}) {question_str}: ")
        answer = answer.lower().strip().replace(" ", "").replace(",", "")
        correct_answer = question[1].lower().strip().replace(" ", "").replace(",", "")
        if answer == correct_answer:
            print("Correct!")
            current_question += 1
        else:
            print(f"Wrong! Correct answer: {correct_answer}")
            all_done = False
            break

    if not all_done:
        print("You did NOT pass the test. Train more!")
    else:
        print("You pass the test SUCCESSFULLY. Well done!")


if __name__ == "__main__":
    main()