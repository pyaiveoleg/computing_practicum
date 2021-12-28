import math
from typing import Callable


class MethodComplex:
    @staticmethod
    def calculate(f: Callable, values_table: list, h: float, **kwargs):
        pass

    @staticmethod
    def name():
        pass


class left_rectangle_complex(MethodComplex):
    @staticmethod
    def calculate(f: Callable, values_table: list, h: float, **kwargs):
        return h * sum(values_table[:-1])

    @staticmethod
    def name():
        return "Формула левого прямоугольника"


class right_rectangle_complex(MethodComplex):
    @staticmethod
    def calculate(f: Callable, values_table: list, h: float, **kwargs):
        return h * sum(values_table[1:])

    @staticmethod
    def name():
        return "Формула правого прямоугольника"


class middle_rectangle_complex(MethodComplex):
    @staticmethod
    def calculate(f: Callable, values_table: list, h: float, **kwargs):
        return h * sum(kwargs["middle_values"])

    @staticmethod
    def name():
        return "Формула среднего прямоугольника"


class trapezoid_complex(MethodComplex):
    @staticmethod
    def calculate(f: Callable, values_table: list, h: float, **kwargs):
        return h / 2 * (values_table[0] + values_table[-1] + 2 * sum(values_table[1: -1]))

    @staticmethod
    def name():
        return "Формула трапеции"


class simpson_complex(MethodComplex):
    @staticmethod
    def calculate(f: Callable, values_table: list, h: float, **kwargs):
        z = values_table[0] + values_table[-1]
        return h / 6 * (z + 2 * sum(values_table[1: -1]) + 4 * sum(kwargs["middle_values"]))

    @staticmethod
    def name():
        return "Формула Симпсона"


def divide_segment(a: float, b: float, m: int):
    segment_size = (b - a) / m
    return [(a + i * segment_size, a + (i + 1) * segment_size) for i in range(m)]


def get_values_table(f: Callable, points: list):
    return [f(x) for x in points]


def print_calculations_for_all_functions(a: float, b: float, m: int, polynomials: list, functions: list):
    for f, integral_f, formula, derivatives in polynomials + functions:
        print(f"Рассматриваем функцию: {formula}")
        h = (b - a) / m
        values_table = get_values_table(f, [a + i * h for i in range(m + 1)])
        middle_values_table = get_values_table(f, [a + (h / 2) + i * h for i in range(m)])
        for const, ast, method in [
            (1 / 2, 0, left_rectangle_complex), (1 / 2, 0, right_rectangle_complex), (1 / 24, 1, middle_rectangle_complex),
            (1 / 12, 1, trapezoid_complex), (1 / 2880, 3, simpson_complex)
        ]:
            print(method.name())
            res = method.calculate(f, values_table, h, middle_values=middle_values_table)
            print(f"h = {h}")
            print(f"Результат вычисления: {res}")
            print(f"Точное значение интеграла: {(integral_f(b) - integral_f(a))}")
            print(f"Абсолютная фактическая погрешность: {abs((integral_f(b) - integral_f(a)) - res)}")
            ma = max(*list(map(abs, get_values_table(derivatives[ast], [a + i * h for i in range(m + 1)]))))
            print(f"Теоретическая погрешность: {const * ma * (b - a) * (h ** (ast + 1))}")
        print("----------------------------------------------")


def print_more_accurate_values(a: float, b: float, m: int, l_: int, polynomials: list, functions: list):
    for f, integral_f, formula, derivatives in polynomials + functions:
        print(f"Рассматриваем функцию: {formula}")
        h = (b - a) / m
        values_table = get_values_table(f, [a + i * h for i in range(m + 1)])
        middle_values_table = get_values_table(f, [a + (h / 2) + i * h for i in range(m)])

        m_l = m * l_
        h_l = (b - a) / m_l
        values_table_l = get_values_table(f, [a + i * h_l for i in range(m_l + 1)])
        middle_values_table_l = get_values_table(f, [a + (h_l / 2) + i * h_l for i in range(m_l)])

        for const, ast, method in [
            (1 / 2, 0, left_rectangle_complex), (1 / 2, 0, right_rectangle_complex), (1 / 24, 1, middle_rectangle_complex),
            (1 / 12, 1, trapezoid_complex), (1 / 2880, 3, simpson_complex)
        ]:
            vt = get_values_table(derivatives[ast], [a + i * h_l for i in range(m_l + 1)])
            ma = max(*list(map(abs, vt)))
            print(method.name())
            J_h = method.calculate(f, values_table, h, middle_values=middle_values_table)
            J_h_l = method.calculate(f, values_table_l, h_l, middle_values=middle_values_table_l)
            print(f"h = {h}")
            print(f"Результат вычисления J_(h/l): {J_h_l}")
            print(f"Точное значение интеграла: {(integral_f(b) - integral_f(a))}")
            print(f"Абсолютная фактическая погрешность: {abs((integral_f(b) - integral_f(a)) - J_h_l)}")
            print(f"Теоретическая погрешность: {const * ma * (b - a) * (h ** (ast + 1))}")
            J_middle = (l_ ** (ast + 1) * J_h_l - J_h) / (l_ ** (ast + 1) - 1)
            print(f"Уточнённые по принципу Рунге значения интеграла: {J_middle}")
            print(f"Абсолютная фактическая погрешность после уточнения: {abs((integral_f(b) - integral_f(a)) - J_middle)}")
        print("----------------------------------------------")


def run():
    polynomials = [
        (
            lambda x: 5, lambda x: 5 * x, "y = 5",
            [lambda x: 0, lambda x: 0, lambda x: 0, lambda x: 0]
        ),
        (
            lambda x: 3.7 * x - 2.39, lambda x: 3.7 * (x ** 2) / 2 - 2.39 * x, "y = 3.7 * x - 2.39",
            [lambda x: 3.7, lambda x: 0, lambda x: 0, lambda x: 0]
        ),
        (
            lambda x: x ** 2 - 4 * x + 1.18, lambda x: (x ** 3) / 3 - 2 * x ** 2 + 1.18 * x, "y = x ** 2 - 4 * x + 1.18",
            [lambda x: 2 * x - 4, lambda x: 2, lambda x: 0, lambda x: 0]
        ),
        (
            lambda x: -17 * x ** 3 - 118 * x ** 2 + 10 * x + 27,
            lambda x: -17 * (x ** 4) / 4 - 118 * (x ** 3) / 3 + 10 * (x ** 2) / 2 + 27 * x,
            "y = -17 * x ** 3 - 118 * x ** 2 + 10 * x + 27",
            [lambda x: -51 * (x ** 2) - 118 * 2 * x + 10, lambda x: -102 * x - 118 * 2, lambda x: -102, lambda x: 0]
        )
    ]

    functions = [
        (
            lambda x: math.exp(-x) - (x ** 2) / 2, lambda x: -math.exp(-x) - (x ** 3) / 6, "y = math.exp(-x) - (x ** 2) / 2",
            [lambda x: -math.exp(-x) - x, lambda x: math.exp(-x) - 1, lambda x: -math.exp(-x), lambda x: math.exp(-x)]
        )
    ]

    print("Задание 4 - 2. Приближённое вычисление интеграла по квадратурным формулам.")
    print("Задача: Вычислите определённый интеграл от заданной функции f(x), используя составные квадратурные формулы.")
    print("Введите нижний предел интегрирования (a):")
    a = float(input())
    print("Введите верхний предел интегрирования (b):")
    b = float(input())
    print("Введите количество промежутков деления [A; B] (m):")
    m = int(input())
    print("----------------------------------------------")
    print_calculations_for_all_functions(a, b, m, polynomials, functions)

    while True:
        print("Введите, во сколько раз необходимо увеличить количество промежутков деления (l):")
        l_ = int(input())
        print(f"Вычисления со значением m = {m * l_}")
        print_more_accurate_values(a, b, m, l_, polynomials, functions)


if __name__ == "__main__":
    run()
