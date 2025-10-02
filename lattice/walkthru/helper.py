from typing import Tuple
import math

Vector2D = Tuple[int, int]

def dot_product_2d(v: Vector2D, w: Vector2D) -> int:
    return v[0] * w[0] + v[1] * w[1]

def squared_norm_2d(v: Vector2D) -> int:
    return dot_product_2d(v, v)

def euclidean_norm_2d(v: Vector2D) -> float:
    return math.sqrt(float(squared_norm_2d(v)))

def nearest_integer_ratio_half_away_from_zero(numer: int, denom: int) -> int:
    if denom == 0:
        raise ZeroDivisionError("denominator is zero")
    if denom < 0:
        numer, denom = -numer, -denom
    if numer >= 0:
        return (numer + denom // 2) // denom
    return -(((-numer) + denom // 2) // denom)

def swap_order_by_norm(v1: Vector2D, v2: Vector2D) -> Tuple[Vector2D, Vector2D, bool]:
    if squared_norm_2d(v2) < squared_norm_2d(v1):
        return v2, v1, True
    return v1, v2, False

def compute_gauss_m(v1: Vector2D, v2: Vector2D) -> int:
    n1 = squared_norm_2d(v1)
    ip = dot_product_2d(v1, v2)
    return nearest_integer_ratio_half_away_from_zero(ip, n1)

def update_v2_with_m(v2: Vector2D, v1: Vector2D, m: int) -> Vector2D:
    return (v2[0] - m * v1[0], v2[1] - m * v1[1])

def is_gauss_size_reduced(v1: Vector2D, v2: Vector2D) -> bool:
    return 2 * abs(dot_product_2d(v1, v2)) <= squared_norm_2d(v1)

def angle_degrees_between(v1: Vector2D, v2: Vector2D) -> float:
    n1 = euclidean_norm_2d(v1)
    n2 = euclidean_norm_2d(v2)
    if n1 == 0.0 or n2 == 0.0:
        return float("nan")
    cos_theta = dot_product_2d(v1, v2) / (n1 * n2)
    cos_theta = max(-1.0, min(1.0, cos_theta)) 
    return math.degrees(math.acos(cos_theta))

def print_matrix(M):
    if not M or not all(isinstance(row, list) for row in M):
        print("Invalid matrix format.")
        return

    max_len = max(len(str(x)) for row in M for x in row)

    for row in M:
        row_str = " ".join(f"{str(x):>{max_len}}" for x in row)
        print(f"[ {row_str} ]")

def gauss_pseudocode_pass(v1: Vector2D, v2: Vector2D):
    v1, v2, swapped = swap_order_by_norm(v1, v2)
    mu = compute_gauss_m(v1, v2)
    v2 = update_v2_with_m(v2, v1, mu)
    return v1, v2, mu, swapped

