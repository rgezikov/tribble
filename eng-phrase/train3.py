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

    all_done = True
    for question in questions:
        question_len = len(question[0])
        question_str = question[0] + ' ' * (max_len - question_len)
        answer = input(f"{question_str}: ")
        correct_answer = question[1].lower()
        if answer.strip().lower() == correct_answer:
            print("Correct!")
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