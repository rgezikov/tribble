import argparse
import random

g_number = ['single', 'plural']
person = ['first', 'second', 'third']
g_gender = ['male', 'female', 'thing']
verbs = ['to be', 'to do', 'to have', 'to go']
polarity = ['positive', 'negative']
sentence_type = ['statement', 'question']
questions = ['', 'What', 'Where', 'Why', 'Who', 'When', 'How', 'Which', 'Whose', 'How much/many', 'How + <>']
tense = ['past simple', 'present simple', 'future simple']


def get_random(arr):
    idx = random.randint(0, len(arr) - 1)
    return arr[idx]


def generate_task():
    n = get_random(g_number)
    p = get_random(person)
    g = get_random(g_gender) if (n == 'single' and p == 'third') else ''
    subject = " ".join([x for x in (n, p, g,) if x])
    v = get_random(verbs)
    pl = get_random(polarity)
    t = get_random(sentence_type)
    q = get_random(questions) if t == 'question' else ''
    tn = get_random(tense)
    return [subject, v, pl, t, q, tn]


def main():
    parser = argparse.ArgumentParser(description='Tasks generator')
    parser.add_argument('-n', dest='num_tasks', required=False, type=int, default=10, help='Number of tasks')
    args = parser.parse_args()

    for task_num in range(args.num_tasks):
        task = [x for x in generate_task() if x]
        print(f"#{(task_num + 1):02d}. {', '.join(task)}")


if __name__ == "__main__":
    main()