import math
from typing import Callable


def split_roots(f: Callable, a: float, b: float, h: float = 10e-2):
    for segment_start in [a + h * x for x in range(int((b - a) / h))]:
        segment_end = segment_start + h
        if f(segment_end) * f(segment_start) <= 0:
            yield segment_start, segment_end


def bisection(f: Callable, segment_start: float, segment_end: float, eps: float, **kwargs):
    a = segment_start
    b = segment_end
    accuracy = (b - a) / 2
    c = (a + b) / 2  # if segment length / 2 is less than eps, return its middle
    x_0 = c
    iterations = 0
    while accuracy > eps:
        c = (a + b) / 2
        if f(c) * f(a) <= 0:
            b = c
        else:
            a = c
        accuracy = b - a
        iterations += 1
    return x_0, c, iterations, f"Длина последнего отрезка: {accuracy}"


def tangents_method(f: Callable, segment_start: float, segment_end: float, eps: float, **kwargs):
    df = kwargs["df"]
    x_0 = (segment_start + segment_end) / 2
    results = [x_0, x_0 - f(x_0) / df(x_0)]
    while abs(results[-1] - results[-2]) > eps:
        previous = results[-1]
        results.append(previous - f(previous) / df(previous))
    return x_0, results[-1], len(results), f"|x_m - x_(m-1)| = {results[-1] - results[-2]}"


def modified_tangents_method(f: Callable, segment_start: float, segment_end: float, eps: float, **kwargs):
    df = kwargs["df"]
    x_0 = (segment_start + segment_end) / 2
    denominator = df(x_0)
    results = [x_0, x_0 - f(x_0) / denominator]
    while abs(results[-1] - results[-2]) > eps:
        previous = results[-1]
        results.append(previous - f(previous) / denominator)
    return x_0, results[-1], len(results), f"|x_m - x_(m-1)| = {results[-1] - results[-2]}"


def secant_method(f: Callable, segment_start: float, segment_end: float, eps: float, **kwargs):
    results = [segment_start, segment_end]
    while abs(results[-1] - results[-2]) > eps:
        x_k = results[-1]
        x_k_1 = results[-2]
        if abs(f(x_k) - f(x_k_1)) < eps:  # to avoid division by zero
            break
        results.append(x_k - f(x_k) * (x_k - x_k_1) / (f(x_k) - f(x_k_1)))
    x_0 = results[0]
    return x_0, results[-1], len(results), f"|x_m - x_(m-1)| = {results[-1] - results[-2]}"


def print_results(f: Callable, df: Callable, a: float, b: float, eps: float):
    print("Задание 1. Численные методы решения нелинейных уравнений. Вариант 12.")
    print("Задача: найдите все корни нечётной кратности функции f(x) на отрезке [A; B] с точностью eps.")
    print(f"Входные данные: f(x) = 2^-x + 0.5 * x ^ 2 - 10; [A; B] = [{a}; {b}]; eps = {eps}")
    print("------------------------------------------------------------------------")
    print("------------------------------------------------------------------------")
    sign_change_segments = list(split_roots(f, a, b))
    print(f"Функция имеет {len(sign_change_segments)} корней на данном отрезке. Отрезки перемены знака:")
    for segment_start, segment_end in sign_change_segments:
        print(f"[{segment_start}; {segment_end}]")

    for method in bisection, tangents_method, modified_tangents_method, secant_method:
        print("------------------------------------------------------------------------")
        print()
        print(f"Уточнение корней методом {method.__name__}")
        for segment_start, segment_end in sign_change_segments:
            x_0, result, iterations, delta = method(f, segment_start, segment_end, eps, df=df)
            print(f"Отрезок [{segment_start}; {segment_end}], начальное приближение: {x_0}")
            print(f"Корень: {result}, количество шагов для получения результата: {iterations}")
            print(f"{delta}")
            print(f"Модуль невязки: {abs(f(result) - 0)}")
            print()


def run():
    def f(x: float):
        return 2 ** (-x) + 0.5 * (x ** 2) - 10

    def df(x: float):
        return -math.log(2) * 2 ** (-x) + x

    a = -3.0
    b = 5.0
    eps = 1e-8

    print_results(f, df, a, b, eps)
    # по убыванию точности: Ньютона, секущих, модифицированный метод Ньютона, бисекции


if __name__ == "__main__":
    run()
