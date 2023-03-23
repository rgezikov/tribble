import argparse
import os
import random
import yaml

def parse_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file_name', required=True, help='Input file')
    parser.add_argument('-m', dest='mode', required=True, default='learning', help='Mode (learning, exam)')
    args = parser.parse_args()
    return args

def main():
    args = parse_params()

    with open(args.file_name) as inf:
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
        if args.mode == 'exam':
            answer = input(f"({current_question}/{total_questions}) {question_str}: ")
        else:
            answer = input(f"{question_str} ?")

        answer = answer.lower().strip().replace(" ", "").replace(",", "")
        correct_answer = question[1].lower().strip().replace(" ", "").replace(",", "")
        if answer == correct_answer:
            print("Correct!")
            current_question += 1
        else:
            if args.mode == 'learning':
                print(f"Correct answer: {question[1]}")
            else:
                print(f"Wrong!")
            all_done = False
            if args.mode == 'exam':
                break

    if args.mode == 'exam':
        if not all_done:
            print("You did NOT pass the test. Train more!")
        else:
            print("You pass the test SUCCESSFULLY. Well done!")


if __name__ == "__main__":
    main()