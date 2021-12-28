import math
from typing import Callable, List, Tuple

from homework_2 import get_values_table, print_values_table


def pretty_print(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def print_results(results_table: List[List[float]]):
    print("Таблица результатов:")
    header = ["x_k", "f(x_k)", "f'(x_k)_ЧД", "f'(x_k)_Т - f'(x_k)_ЧД", "f''(x_k)_ЧД", "f''(x_k)_Т - f''(x_k)_ЧД"]
    pretty_print([header] + results_table)


def print_numerical_derivation_results(
    values_table: List[Tuple[float, float]],  # (x_k, f(x_k)) for k in 1..m
    f: Callable,
    df: Callable,
    ddf: Callable,
):
    h = values_table[1][0] - values_table[0][0]
    print(f"h = {h}")

    first_derivatives = [
        (-3 * values_table[0][1] + 4 * values_table[1][1] - values_table[2][1]) / (2 * h)
    ] + [
        (values_table[i + 1][1] - values_table[i - 1][1]) / (2 * h) for i in range(1, len(values_table) - 1)
    ] + [
        (3 * values_table[-1][1] - 4 * values_table[-2][1] + values_table[-3][1]) / (2 * h)
    ]

    second_derivatives = [
        0.0
    ] + [
        (values_table[i + 1][1] - 2 * values_table[i][1] + values_table[i - 1][1]) / (h ** 2) for i in range(1, len(values_table) - 1)
    ] + [
        0.0
    ]

    print_results([
        [
            values_table[i][0],
            values_table[i][1],
            first_derivatives[i],
            abs(df(values_table[i][0]) - first_derivatives[i]),
            second_derivatives[i],
            abs(ddf(values_table[i][0]) - second_derivatives[i]),
        ] for i in range(len(values_table))
    ])


def make_numerical_derivation(f: Callable, df: Callable, ddf: Callable):
    m = int(input("Введите значение m\n"))
    a = float(input("Введите начало отрезка, из которого нужно взять значения функции (a)\n"))
    h = float(input("Введите шаг, с которым необходимо брать узлы (h)\n"))
    b = a + m * h
    values_table = get_values_table(f, a, b, m)
    print_values_table(values_table)

    print_numerical_derivation_results(values_table, f, df, ddf)
    print("Чтобы ввести новые значения, нажмите Enter.")
    input()
    print("------------------------------------------------------------------------------------")


def run():
    k = 1.5 * (12 % 5 + 1)

    def f(x: float):
        return math.exp(k * x)

    def df(x: float):
        return k * math.exp(k * x)

    def ddf(x: float):
        return k * k * math.exp(k * x)

    a = 0.0
    h = 0.1
    m = 30

    print("Задание 3-2. Формулы численного дифференцирования. Вариант 12.")
    print(
        "Задача: Найдите первую и вторую производные функции f(x) в равноотстоящих точках отрезка [a, b] c шагом в h, "
        "используя таблицу из m + 1 значения"
    )
    print("f(x) = e ^ 1.5 * 3 * x")
    interaction_choice = input(
        "Для того, чтобы использовать значения по умолчанию, нажмите 1. Хотите ввести значения - нажмите любую другую "
        "клавишу. \n"
    )
    if interaction_choice == "1":
        values_table = get_values_table(f, a, a + h * m, m)
        print_values_table(values_table)
        print_numerical_derivation_results(values_table, f, df, ddf)
    else:
        while True:
            make_numerical_derivation(f, df, ddf)


if __name__ == "__main__":
    run()
