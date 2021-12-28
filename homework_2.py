import math
from typing import Callable, List, Tuple, Iterable


def get_values_table(f: Callable, segment_start: float, segment_end: float, m: int):
    h = (segment_end - segment_start) / m
    values_table = [(x, f(x)) for x in [segment_start + i * h for i in range(m + 1)]]
    return values_table


def print_values_table(values_table: List[Tuple[float, float]]):
    print("Таблица значений:")
    print("x            | f(x)         ")
    print("----------------------------")
    for x, y in values_table:
        print(f"{'%0.10f' % x} | {'%0.10f' % y}")


def get_omega(values_table, value, control_index):
    res = 1
    for index, item in enumerate(values_table):
        if index != control_index:
            res *= value - item
    return res


def get_multiply(values, value, end_index):
    res = 1
    for index in range(end_index):
        res *= value - values[index]
    return res


def lagrange_interpolate(values_table: List[Tuple[float, float]], x_0: float, n: int):
    result = 0
    values = list(map(lambda x: x[0],  values_table[:n+1]))
    for k in range(0, n + 1):
        result += values_table[k][1] * get_omega(values, x_0, k) / get_omega(values, values[k], k)
    return result


def sorted_values_table(values_table:  Iterable[Tuple[float, float]], x: float):
    return sorted(values_table, key=lambda value: abs(x - value[0]))


def newton_interpolate(values_table: List[Tuple[float, float]], n: int):
    def inner(x: float):
        divided_differences = [[] for _ in range(n + 1)]
        for row_index in range(n + 1):
            divided_differences[0].append(values_table[row_index][1])   # f(x_i)
        points_x = list(map(lambda y: y[0], values_table[:n + 1]))
        for row_index in range(1, n + 1):
            for column_index in range(n - row_index):
                new = (
                    divided_differences[row_index - 1][column_index + 1] -
                    divided_differences[row_index - 1][column_index]
                ) / (
                    points_x[row_index + column_index] -
                    points_x[column_index]
                )
                divided_differences[row_index].append(new)
        return sum(divided_differences[i][0] * get_multiply(points_x, x, i) for i in range(n))
    return inner


def print_interpolation_results(f, x, n, values_table):
    value = f(x)
    values_table = sorted_values_table(values_table, x)
    newton_value = newton_interpolate(values_table, n)(x)
    print(f"Значение интерполяционного многочлена Ньютона: {newton_value}")
    print(f"Абсолютная фактическая погрешность метода Ньютона |f(x) - N(x)|: {abs(value - newton_value)}")
    lagrange_value = lagrange_interpolate(values_table, x, n)
    print(f"Значение интерполяционного многочлена Лагранжа: {lagrange_value}")
    print(f"Абсолютная фактическая погрешность метода Лагранжа |f(x) - L(x)|: {abs(value - lagrange_value)}")


def make_interpolation(f: Callable, values_table, m: int):
    x = float(input("Введите x\n"))
    while True:
        n = int(input(f"Введите степень многочлена N, не превосходящую {m}\n"))
        if n > m + 1:
            print(f"Введённая степень многочлена {n} больше, чем {m + 1}")
            continue
        else:
            break
    print_interpolation_results(f, x, n, values_table)
    input("Чтобы ввести новые значения, нажмите Enter.")
    print("------------------------------------------------------------------------------------")


def run():
    def f(x: float):
        return math.exp(-x) - (x ** 2) / 2

    a = 0.0
    b = 1.0
    x_0 = 0.6
    n = 7
    m = 15

    print("Задание 2. Интерполяционные многочлены Ньютона и Лагранжа. Вариант 12.")
    print("Задача: Найдите значение функции f(x) в точке x, используя таблицу из m значений")
    print("f(x) = (e ^ -x) - (x ^ 2) / 2")
    interaction_choice = input(
        "Для того, чтобы использовать значения по умолчанию, нажмите 1. Хотите ввести значения - нажмите любую другую "
        "клавишу. \n"
    )
    if interaction_choice == "1":
        values_table = get_values_table(f, a, b, m)
        print_values_table(values_table)
        print_interpolation_results(f, x_0, n, values_table)
    else:
        m = int(input("Введите значение m\n"))
        a = float(input("Введите начало отрезка, из которого нужно взять узлы интерполирования (A)\n"))
        b = float(input("Введите конец этого отрезка (B)\n"))
        values_table = get_values_table(f, a, b, m)
        print_values_table(values_table)
        while True:
            make_interpolation(f, values_table, m)


if __name__ == "__main__":
    run()
