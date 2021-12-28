import math
from typing import Callable


class Method:
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        pass

    @staticmethod
    def name():
        pass


class left_rectangle(Method):
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        return f(a) * (b - a)

    @staticmethod
    def name():
        return "Формула левого прямоугольника"


class right_rectangle(Method):
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        return f(b) * (b - a)

    @staticmethod
    def name():
        return "Формула правого прямоугольника"


class middle_rectangle(Method):
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        return f((a + b) / 2) * (b - a)

    @staticmethod
    def name():
        return "Формула среднего прямоугольника"


class trapezoid(Method):
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        return (f(a) + f(b)) / 2 * (b - a)

    @staticmethod
    def name():
        return "Формула трапеции"


class simpson(Method):
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))

    @staticmethod
    def name():
        return "Формула Симпсона"


class three_eights(Method):
    @staticmethod
    def calculate(f: Callable, a: float, b: float):
        h = (b - a) / 3
        return (b - a) * (f(a) + 3 * f(a + h) + 3 * f(a + 2 * h) + f(b)) / 8

    @staticmethod
    def name():
        return "Формула 3 / 8"


def run():
    polynomials = [
        (lambda x: 5, lambda x: 5 * x, "y = 5"),
        (lambda x: 3.7 * x - 2.39, lambda x: 3.7 * (x ** 2) / 2 - 2.39 * x, "y = 3.7 * x - 2.39"),
        (lambda x: x ** 2 - 4 * x + 1.18, lambda x: (x ** 3) / 3 - 2 * x ** 2 + 1.18 * x, "y = x ** 2 - 4 * x + 1.18"),
        (
            lambda x: -17 * x ** 3 - 118 * x ** 2 + 10 * x + 27,
            lambda x: -17 * (x ** 4) / 4 - 118 * (x ** 3) / 3 + 10 * (x ** 2) / 2 + 27 * x,
            "y = -17 * x ** 3 - 118 * x ** 2 + 10 * x + 27"
        )
    ]

    functions = [
        (lambda x: math.exp(-x) - (x ** 2) / 2, lambda x: -math.exp(-x) - (x ** 3) / 6, "y = math.exp(-x) - (x ** 2) / 2")
    ]

    print("Задание 4. Приближённое вычисление интеграла по квадратурным формулам.")
    print("Задача: Вычислите определённый интеграл от заданной функции f(x), используя квадратурные формулы.")
    print("Введите нижний предел интегрирования (a):")
    a = float(input())
    print("Введите верхний предел интегрирования (b):")
    b = float(input())
    print("----------------------------------------------")

    for f, integral_f, formula in polynomials + functions:
        print(f"Рассматриваем функцию: {formula}")
        for method in [right_rectangle, left_rectangle, middle_rectangle, trapezoid, simpson, three_eights]:
            print(method.name())
            res = method.calculate(f, a, b)
            print(f"Результат вычисления: {res}")
            print(f"Точное значение интеграла: {(integral_f(b) - integral_f(a))}")
            print(f"Абсолютная фактическая погрешность: {abs((integral_f(b) - integral_f(a)) - res)}")
        print("----------------------------------------------")


if __name__ == "__main__":
    run()
