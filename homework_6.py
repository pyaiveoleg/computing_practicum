import math
from common import Function
from homework_5 import get_points_and_coeffs_gauss
from homework_4_2 import divide_segment


def fit_points_and_coeffs(points: list, coeffs: list, a: float, b: float):
    points = list(map(lambda x: (x * (b - a) / 2 + (a + b) / 2), points))
    coeffs = list(map(lambda x: x * (b - a) / 2, coeffs))
    return points, coeffs


def print_complex_gauss_formula_report(f, p, a=0, b=1):
    print("------------------------------------------")
    print("Составная формула Гаусса")
    print(f"Отрезок интегрирования: [{a}; {b}]")
    print(f"Функция: {f.representation}, вес: {p.representation}.")

    def fi(x):
        return f.function(x) * p.function(x)

    N = int(input("Количество узлов КФ Гаусса (N):"))
    m = int(input("Введите число промежутков деления отрезка (m):"))
    points, coeffs = get_points_and_coeffs_gauss(N)
    print(f"Узлы исходной формулы Гаусса: {points}")
    print(f"Коэффициенты исходной формулы Гаусса: {coeffs}")
    calculated_value = 0
    exact_value = 0.397215491060637049
    for segment_start, segment_end in divide_segment(a, b, m):
        calculated_value += sum(a_k * fi(x_k) for x_k, a_k in zip(
            *fit_points_and_coeffs(points, coeffs, segment_start, segment_end)
        ))
    print(f"Точное значение: {exact_value}")
    print(f"Приближённое значение: {calculated_value}")
    print(f"Абсолютная фактическая погрешность: {abs(exact_value - calculated_value)}")


def run():
    f = Function(
        function=lambda x: math.sin(x),
        representation="sin(x)",
    )
    p = Function(
        function=lambda x: math.sin(2 * x),
        representation="sin(2x)",
    )
    print("Задание 6. Приближённое вычисление интегралов при помощи квадратурных формул НАСТ")
    print("Задача: вычислите интеграл от данной функции при помощи составной КФ Гаусса.")
    print("Вариант 12.")  # как в предыдущих работах
    a = int(input("Введите начало отрезка интегрирования (а):"))
    b = int(input("Введите конец отрезка интегрирования (b):"))
    print_complex_gauss_formula_report(f, p, a, b)
    # print_complex_gauss_formula_report(f, p)


if __name__ == "__main__":
    run()
