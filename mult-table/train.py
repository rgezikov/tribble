#!/usr/bin/env python3

import argparse
import random
from  datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Учим таблицу умножения')
parser.add_argument('-e', dest='examples', required=True, type=int, help='Количество примеров')
parser.add_argument('--min', dest='min', type=int, required=True, help='Минимальное число')
parser.add_argument('--max', dest='max', type=int, required=True, help='Максимальное число')
args = parser.parse_args()

total_examples = args.examples

wrong_examples = []
total_time = timedelta()
correct_counter = 0
for example in range(total_examples):
    print("\nПример № {}".format(example + 1))
    a = random.randint(args.min, args.max)
    b = random.randint(2, 9)
    if args.max % 10 != 0 and args.min % 10 != 0:
        while (a * b) % 10 == 0:
            b = random.randint(2, 9)
    print("Сколько будет {} * {}?".format(a, b))
    start = datetime.utcnow()
    answer = int(input("Ответ:"))
    total_time = total_time + (datetime.utcnow() - start)
    if a * b == answer:
        correct_counter += 1
    else:
        wrong_examples.append([a, b, answer])

print("\n\nВсего примеров: {}.\nРешено правильно:{}.\nЗатрачено времени: {} секунд.".
      format(total_examples, correct_counter, round(total_time.total_seconds())))

if len(wrong_examples) > 0:
    print("\nПримеры с ошибками:")
    for we in wrong_examples:
        print("{} * {} = {}, а не {}".format(we[0],we[1], we[0] * we[1], we[2]))
else:
    print("Все примеры решены верно.")
