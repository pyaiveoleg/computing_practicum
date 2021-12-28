import math
from typing import Callable
from common import Function
from homework_1 import secant_method, split_roots


def get_polynomial_roots(f: Callable, a=-1, b=1, h=10e-4, eps=10e-12, verbose=False):
    roots = []
    for segment_start, segment_end in split_roots(f, a, b, h):
        root = secant_method(f, segment_start, segment_end, eps)[1]
        if verbose:
            print(f"root in segment [{segment_start}, {segment_end}] is: {root}")
        roots.append(root)
    return roots


def get_legendre_polynomial_lambda(n: int):  # полиномы Лежандра до n включительно
    def inner(x):
        if n == 0:
            return 1
        if n == 1:
            return x
        else:
            prev = get_legendre_polynomial_lambda(n - 1)(x)
            prev_prev = get_legendre_polynomial_lambda(n - 2)(x)
            return (2 * n - 1) / n * prev * x - (n - 1) / n * prev_prev
    return inner


def get_a_k(x_k: float, n: int, legendre_polynomial_n_1: Callable):
    return (2 * (1 - x_k ** 2)) / ((n ** 2) * (legendre_polynomial_n_1(x_k) ** 2))


def get_points_and_coeffs_gauss(n: int):
    points = get_polynomial_roots(get_legendre_polynomial_lambda(n))
    coeffs = [get_a_k(x_k, n, get_legendre_polynomial_lambda(n - 1)) for x_k in points]
    return points, coeffs


def get_points_and_coeffs_meler(n: int):
    points = [math.cos((2 * k - 1) / (2 * n) * math.pi) for k in range(1, n + 1)]
    coeffs = [math.pi / n] * n
    return points, coeffs


def fit_points_and_coeffs(points: list, coeffs: list):
    points = list(map(lambda x: (x + 1) / 2, points))
    coeffs = list(map(lambda x: x / 2, coeffs))
    return points, coeffs


def get_test_functions():
    polynomials = [
        Function(
            function=lambda x: x ** 5 - 14 * (x ** 4) + 8 * (x ** 3) - 7 * (x ** 2) + 239,
            representation="x ** 5 - 14 * (x ** 4) + 8 * (x ** 3) - 7 * (x ** 2) + 239",
            integral=lambda x: (1.0 / 6) * x ** 6 - 14.0 / 5 * (x ** 5) + 2.0 * (x ** 4) - 7.0 * (
                    x ** 3) / 3 + 239.0 * x
        ),
        Function(
            function=lambda x: 8 * x ** 7 - 100 * x ** 6 + 34 * x ** 5 + 14 * (x ** 4) - 8 * (x ** 3) - 7 * (
                    x ** 2) + 239,
            representation="8 * x ** 7 - 100 * x ** 6 + 34 * x ** 5 + 14 * (x ** 4) - 8 * (x ** 3) -"
                           " 7 * (x ** 2) + 239",
            integral=lambda x: x ** 8 - (100 / 7) * x ** 7 + (34 / 6) * x ** 6 + 14 * (x ** 5) / 5 - 2 * (x ** 4) -
                           7 * (x ** 3) / 3 + 239 * x
        ),
        Function(
            function=lambda x: -10 * x ** 9 + x ** 8 - 8 * x ** 7 - 100 * x ** 6 + 34 * x ** 5 + 14 * (x ** 4) - 8 * (
                    x ** 3) - 7 * (x ** 2) + 239,
            representation="-10 * x ** 9 + x ** 8 - 8 * x ** 7 - 100 * x ** 6 + 34 * x ** 5 + 14 * (x ** 4) "
                           "- 8 * (x ** 3) - 7 * (x ** 2) + 239",
            integral=lambda x: - x ** 10 + (1 / 9) * x ** 9 - x ** 8 - (100 / 7) * x ** 7 + (34 / 6) * x ** 6 + 14 * (
                    x ** 5) / 5 - 2 * (x ** 4) - 7 * (x ** 3) / 3 + 239 * x
        )
    ]
    gauss_function = Function(
        function=lambda x: math.sqrt(x) / (1 + x ** 2),
        representation="math.sqrt(x) / (1 + x ** 2)"
    )
    meler_function = Function(
        function=lambda x: math.log(x + 2),
        representation="log(x + 2)"
    )
    return polynomials, gauss_function, meler_function


def print_inaccuracy(exact_value, function, coeffs, points):
    calculated_value = sum(a_k * function(x_k) for a_k, x_k in zip(coeffs, points))
    print(f"Точное значение: {exact_value}")
    print(f"Приближённое значение: {calculated_value}")
    print(f"Абсолютная фактическая погрешность: {abs(exact_value - calculated_value)}")


def print_test_function_results(formula, name, test_function, exact_value):
    print("------------------------------------------")
    print(name)
    while True:
        n = int(input("Введите число узлов (n):"))
        points, coeffs = formula(n)
        if name == "Формула Гаусса":
            points, coeffs = fit_points_and_coeffs(points, coeffs)
        print(f"Коэффициенты при N = {n}: {coeffs}")
        print(f"Узлы при N = {n}: {points}")
        print_inaccuracy(exact_value, test_function.function, coeffs, points)


def run():
    polynomials, gauss_function, meler_function = get_test_functions()
    print("Задание 5. КФ Гаусса и Мелера: их узлы и коэффициенты.")
    print("Задача: Вычислите определённый интеграл от заданной функции f(x), используя КФ Гаусса и Мелера.")
    print("Выведите на экран значения узлов и коэффициентов формул Гаусса и Мелера.")
    print("Вариант 12.")
    max_n = 8
    print("Вычисление интеграла по КФ Гаусса")
    for n in range(1, max_n + 1):
        print("--------------------------------------------")
        points, coeffs = get_points_and_coeffs_gauss(n)
        print(f"Коэффициенты при N = {n}: {coeffs}")
        print(f"Узлы при N = {n}: {points}")
        if n in [3, 4, 5]:
            print(f"N = {n}, проверяем точность на полиноме степени {2 * n - 1}:")
            current_polynomial = polynomials[n - 3]
            exact_value = current_polynomial.integral(1) - current_polynomial.integral(-1)
            print_inaccuracy(exact_value, current_polynomial.function, coeffs, points)
    print("------------------------------------------")
    print("Рассматриваем тестовую функцию из варианта")
    print_test_function_results(get_points_and_coeffs_gauss, "Формула Гаусса", gauss_function, 0.487495)
    print_test_function_results(get_points_and_coeffs_meler, "Формула Мелера", meler_function, 1.9597591637624661976336)


if __name__ == "__main__":
    run()
