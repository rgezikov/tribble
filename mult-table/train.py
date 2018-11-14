from  datetime import datetime, timedelta
import random

total_examples = 10

wrong_examples = []
total_time = timedelta()
correct_counter = 0
for example in range(total_examples):
    print("\nПример № {}".format(example + 1))
    a = random.randint(2, 5)
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