import math

from homework_4_2 import middle_rectangle_complex, get_values_table
from homework_5 import get_polynomial_roots
from common import Function


def print_weighted_gauss_formula_report(f, p, exact_value, a=0, b=1):
    print("-------------------------------------")
    print("Формула Гаусса с весом.")
    print(f"Отрезок интегрирования: [{a}; {b}]")
    print(f"Функция: {f.representation}, вес: {p.representation}.")
    N = 2
    print(f"Количество узлов КФ Гаусса (N) равно {N}")

    m = 10 ** 4
    h = (b - a) / m
    mu = []
    for k in range(2 * N):
        def f_k(x):
            return p.function(x) * (x ** k)

        mu.append(
            middle_rectangle_complex.calculate(
                f_k, [], h, middle_values=get_values_table(f_k, [a + (h / 2) + i * h for i in range(m)])
            )
        )
    print(f"Моменты весовой функции: {mu}")
    # if N == 2:
    a_1 = (-mu[2] * mu[1] + mu[3] * mu[0]) / (mu[1] * mu[1] - mu[0] * mu[2])
    a_2 = (-mu[3] * mu[1] + mu[2] * mu[2]) / (mu[1] * mu[1] - mu[0] * mu[2])  # cramer formulas
    polynomial_coefficients = [a_1, a_2]  # N = 2
    print(f"Коэффициенты ортогонального многочлена: {polynomial_coefficients}")

    def orthogonal_polynomial(x):
        return x ** N + sum((x ** i) * polynomial_coefficients[N - 1 - i] for i in range(N))

    points = get_polynomial_roots(orthogonal_polynomial)
    print(f"Узлы полученной КФ: {points}")
    A_1 = (mu[1] - points[1] * mu[0]) / (points[0] - points[1])
    A_2 = (mu[1] - points[0] * mu[0]) / (points[1] - points[0])
    coeffs = [A_1, A_2]
    print(f"Коэффициенты полученной КФ: {coeffs}")
    calculated_value = 0
    calculated_value += sum(a_k * f.function(x_k) for x_k, a_k in zip(points, coeffs))
    print(f"Точное значение: {exact_value}")
    print(f"Приближённое значение: {calculated_value}")
    print(f"Абсолютная фактическая погрешность: {abs(exact_value - calculated_value)}")


def run():
    f = Function(
        function=lambda x: math.sin(x),
        representation="sin(x)",
    )
    polynomial = Function(
        function=lambda x: x ** 3,
        representation="x ^ 3"
    )
    p = Function(
        function=lambda x: math.sin(2 * x),
        representation="sin(2x)",
    )
    print("Задание 6. Приближённое вычисление интегралов при помощи квадратурных формул НАСТ")
    print("Задача: Вычислите определённый интеграл от заданной функции f(x) с весом p(x).")
    print("Постройте квадратурную формулу наивысшей алгебраической степени точности с весом p(x).")
    print("Вариант 12.")  # как в предыдущих работах
    a = int(input("Введите начало отрезка интегрирования (а):"))
    b = int(input("Введите конец отрезка интегрирования (b):"))
    for function, exact_value in [(f, 0.39722), (polynomial, 0.23694982513301185)]:
        # print_weighted_gauss_formula_report(function, p, exact_value)
        print_weighted_gauss_formula_report(function, p, exact_value, a, b)


if __name__ == "__main__":
    run()
