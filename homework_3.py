import math
from typing import Callable, List, Tuple


from homework_1 import secant_method  # or bisection
from homework_2 import print_values_table, get_values_table, newton_interpolate, sorted_values_table


def reversed_values_table(values_table, v):
    return sorted_values_table(map(lambda x: (x[1], x[0]), values_table), v)


def print_reverse_interpolation_results(
    f: Callable,
    values_table: List[Tuple[float, float]],  # (x_k, f(x_k)) for k in 1..m
    v: float,  # function value
    n: int,  # interpolation polynomial degree
    a: float,
    b: float,
    eps: float = 1e-12
):
    print("Способ 1: интерполирование обратной функции.")
    value_1 = newton_interpolate(reversed_values_table(values_table, v), n)(v)
    print(f"Значение интерполяционного многочлена Ньютона: {value_1}")
    print(f"Модуль невязки {abs(f(value_1) - v)}")

    print("Способ 2: численное решение уравнения P_n(x) = V.")
    newton_interpolation_polynomial = newton_interpolate(values_table, n)
    value_2 = secant_method(lambda x: newton_interpolation_polynomial(x) - v, a, b, eps)[1]
    print(f"Решение уравнения P_n(x) = V, полученное методом секущих {value_2}")
    print(f"Модуль невязки {abs(f(value_2) - v)}")


def make_reverse_interpolation(
    f: Callable,
    values_table: List[Tuple[float, float]],
    m: int,
    a: float,
    b: float,
    eps: float = 1e-12
):
    v = float(input("Введите значение функции (F)\n"))
    while True:
        n = int(input(f"Введите степень многочлена N, не превосходящую {m}\n"))
        if n > m + 1:
            print(f"Введённая степень многочлена {n} больше, чем {m + 1}")
            continue
        else:
            break
    # eps = float(input("Введите значение eps - необходимую точность вычислений"))
    print(f"Используемое значение eps: {eps}")
    print_reverse_interpolation_results(f, values_table, v, n, a, b, eps)
    input("Чтобы ввести новые значения, нажмите Enter.")
    print("------------------------------------------------------------------------------------")


def run():
    def f(x: float):
        return math.exp(-x) - (x ** 2) / 2

    a = 0.0
    b = 1.0
    v = 0.52
    n = 7
    m = 10

    print("Задание 3. Задача обратного интерполирования. Вариант 12.")
    print("Задача: Найдите точку x, в значение функции f(x) равно заданному F, используя таблицу из m значений")
    print("f(x) = (e ^ -x) - (x ^ 2) / 2")
    interaction_choice = input(
        "Для того, чтобы использовать значения по умолчанию, нажмите 1. Хотите ввести значения - нажмите любую другую "
        "клавишу. \n"
    )
    if interaction_choice == "1":
        values_table = get_values_table(f, a, b, m)
        print_values_table(values_table)
        print_reverse_interpolation_results(f, values_table, v, n, a, b)
    else:
        m = int(input("Введите значение m\n"))
        a = float(input("Введите начало отрезка, из которого нужно взять узлы интерполирования (A)\n"))
        b = float(input("Введите конец этого отрезка (B)\n"))
        values_table = get_values_table(f, a, b, m)
        print_values_table(values_table)
        while True:
            make_reverse_interpolation(f, values_table, m, a, b)


if __name__ == "__main__":
    run()
