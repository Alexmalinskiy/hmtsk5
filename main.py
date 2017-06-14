def main():
    print_greeting()
    data, work_indexes, exam_index, sex_index, exp_index = read_journal()
    while True:
        command = input_command()
        if command == "q":
            print("Сеанс завершён")
            break
        elif command == "m":
            calc_avg_mark(data, work_indexes, exam_index)
        elif command == "s":
            calc_avg_sex(data, work_indexes, exam_index, sex_index)
        elif command == "e":
            calc_avg_exp(data, work_indexes, exam_index, exp_index)
        elif command == "t":
            calc_best_students(data,work_indexes,exam_index)
        else:
            print("Неверная команда! Попробуйте ещё раз")


def print_greeting():
# приветствие и список команд
    print("Добро пожаловать в онлайн-дневник!")
    print("----------------------------------")
    print("Перечень доступных команд: \nm - Вывести среднюю оценку по группе"
          "\ns - Вывести среднюю оценку в разрезе пола \ne - Вывести среднюю оценку в разрезе опыта"
          "\nt - Вывести лучшего студента \nq - Выйти из программы")


def read_journal():
# считываем файл в списки и определяем список индексов контрольных работ и экзамена
    file = open("journal.txt", encoding='utf8')
    data = [line.strip().replace("\\n", "").split(";") for line in file]

    work_indexes = [j for j, x in enumerate(data[0]) if "др" in data[0][j].lower()]
    exam_index = [j for j, x in enumerate(data[0]) if "экзамен" in data[0][j].lower()]
    sex_index = [j for j, x in enumerate(data[0]) if "пол" in data[0][j].lower()]
    exp_index = [j for j, x in enumerate(data[0]) if "опыт" in data[0][j].lower()]

    return data, work_indexes, exam_index, sex_index, exp_index


def input_command():
    print("Введите команду")
    command = input()
    return command.lower()


def calc_avg_mark(data, work_indexes, exam_index):
    total_homework_sum = 0
    total_ex_sum = 0
    for i, student in enumerate(data):
        if i == 0:
            continue
        total_homework_sum += sum([int(y) for k, y in enumerate(student) if k in work_indexes])
        total_ex_sum += sum([int(y) for k, y in enumerate(student) if k in exam_index])
    avg_homework = round(total_homework_sum / (len(work_indexes) * (len(data) - 1)),1)
    avg_ex = round(total_ex_sum / (len(data) - 1), 1)
    print("Средняя оценка за домашние задания по группе: ", avg_homework)
    print("Средняя оценка за экзамен по группе: ", avg_ex)


def calc_avg_sex(data, work_indexes, exam_index, sex_index):
    total_homework_male = []
    total_homework_female = []
    total_ex_sum_male = 0
    total_ex_sum_female = 0
    for i, student in enumerate(data):
        if i == 0:
            continue
        if student[sex_index[0]].lower() == "м":
            total_homework_male.append(sum([int(y) for k, y in enumerate(student) if k in work_indexes]))
            total_ex_sum_male += sum([int(y) for k, y in enumerate(student) if k in exam_index])
        else:
            total_homework_female.append(sum([int(y) for k, y in enumerate(student) if k in work_indexes]))
            total_ex_sum_female += sum([int(y) for k, y in enumerate(student) if k in exam_index])

    avg_homework_male = round(sum(total_homework_male) / (len(work_indexes) * len(total_homework_male)),1)
    avg_ex_male = round(total_ex_sum_male / len(total_homework_male), 1)
    avg_homework_female = round(sum(total_homework_female) / (len(work_indexes) * len(total_homework_female)),1)
    avg_ex_female = round(total_ex_sum_female / len(total_homework_female), 1)

    print("Средняя оценка за домашние задания у мужчин: ", avg_homework_male)
    print("Средняя оценка за домашние экзамен у мужчин: ", avg_ex_male)
    print("Средняя оценка за домашние задания у женщин: ", avg_homework_female)
    print("Средняя оценка за домашние экзамен у женщин: ", avg_ex_female)


def calc_avg_exp(data, work_indexes, exam_index, exp_index):
    total_homework_exp = []
    total_homework_unexp = []
    total_ex_sum_exp = 0
    total_ex_sum_unexp = 0
    for i, student in enumerate(data):
        if i == 0:
            continue
        if student[exp_index[0]].lower() == "да":
            total_homework_exp.append(sum([int(y) for k, y in enumerate(student) if k in work_indexes]))
            total_ex_sum_exp += sum([int(y) for k, y in enumerate(student) if k in exam_index])
        else:
            total_homework_unexp.append(sum([int(y) for k, y in enumerate(student) if k in work_indexes]))
            total_ex_sum_unexp += sum([int(y) for k, y in enumerate(student) if k in exam_index])

    avg_homework_exp = round(sum(total_homework_exp) / (len(work_indexes) * len(total_homework_exp)), 1)
    avg_ex_exp = round(total_ex_sum_exp / len(total_homework_exp), 1)
    avg_homework_unexp = round(sum(total_homework_unexp) / (len(work_indexes) * len(total_homework_unexp)), 1)
    avg_ex_unexp = round(total_ex_sum_unexp / len(total_homework_unexp), 1)

    print("Средняя оценка за домашние задания у студентов с опытом: ", avg_homework_exp)
    print("Средняя оценка за домашние экзамен у студентов с опытом: ", avg_ex_exp)
    print("Средняя оценка за домашние задания у студентов без опыта: ", avg_homework_unexp)
    print("Средняя оценка за домашние экзамен у студентов без опыта: ", avg_ex_unexp)


def calc_best_students(data, work_indexes, exam_index, work_weight = 0.6, exam_weight = 0.4):
    max_total_points = 0
    max_indexes = []
    for i, student in enumerate(data):
        if i == 0:
            continue

        total_points_per_student = 0
        work_points_per_student = 0

        work_points_per_student = sum([int(y) for k, y in enumerate(student) if k in work_indexes])
        total_points_per_student += work_weight * round(work_points_per_student / len(work_indexes), 1)
        total_points_per_student += exam_weight * sum([int(y) for k, y in enumerate(student) if k in exam_index])

        if len(max_indexes) == 0:
            max_indexes.append(i)
            max_total_points = total_points_per_student
        else:
            if max_total_points < total_points_per_student:
                max_total_points = total_points_per_student
                max_indexes = [i]
            elif max_total_points == total_points_per_student:
                max_indexes.append(i)

    print_best_students(data, max_total_points, *max_indexes)


def print_best_students(data, max_total_points, *args):
    students = ""
    for i,arg in enumerate(args):
        if i == 0:
            students += data[arg][0] + " " + data[arg][1] + " " + data[arg][2]
        else:
            students += "," + data[arg][0] + " " + data[arg][1] + " " + data[arg][2]
    if students.count(",") == 0:
        print("Лучший студент:", students, "с интегральной оценкой", max_total_points)
    else:
        print("Лучшие студенты:", students, "с интегральной оценкой", max_total_points)


main()