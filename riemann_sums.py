"""
Riemann Sums Homework Assignment

Implements all REQUIRED FEATURES:

1. Polynomial input via coefficient list:
   - Accepts [a0, a1, ..., an] for f(x) = a0 + a1 x + ... + an x^n.

2. Interval and partition:
   - Prompts for a, b (with a < b) and n ≥ 2.
   - Computes Δx = (b - a) / n and partition points.

3. Sampling rules (three):
   - Implements Left, Right, and Midpoint Riemann sums.
   - Uses chosen rule to compute S_n.

4. Exact integral for comparison (polynomials):
   - Integrates polynomial analytically from a to b.
   - Reports S_n, I, and absolute error |S_n - I|.

5. Single-figure visualization:
   - Plots f(x) over [a, b].
   - Draws Riemann rectangles for the chosen rule.
   - Displays S_n, I, and |S_n - I| on the figure.

Required Command-Line Interface:
   - Prompts for coeffs, a, b, n, rule (left / right / mid).

----------------------------------------------------------------------
EXTENSIONS (3 substantial analysis-focused features):

EXTENSION 1: Additional numerical methods (Trapezoidal & Simpson)
   - Computes Trapezoidal rule approximation T_n.
   - Computes Simpson’s rule approximation S_simpson (when n is even).
   - Reports their values and absolute errors versus the exact integral.

EXTENSION 2: Convergence study & error plot
   - For n values [4, 8, 16, 32, 64] (when possible on [a, b]),
     computes Left, Midpoint, and Right Riemann sums.
   - Plots |error| vs n on a log-log scale for the three rules.
   - Gives insight into how fast each rule converges for the given polynomial.

EXTENSION 3: Comparative rectangle visualization for all three rules
   - Creates a separate figure with three subplots:
        Left rule rectangles,
        Midpoint rule rectangles,
        Right rule rectangles.
   - Uses the same polynomial, interval, and n.
   - Visually compares the geometric behavior of the three approximations.

All extensions are clearly documented here, in the code, and via printed messages.
"""

import math
from typing import List

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# ---------- Core polynomial utilities ----------

def parse_coeffs(raw: str) -> List[float]:
    """
    Parse a string like '1, -2, 3.5' or '1 -2 3.5' into [1.0, -2.0, 3.5].
    """
    separators = [',', ' ']
    # Replace commas with spaces, then split
    for sep in [',']:
        raw = raw.replace(sep, ' ')
    parts = [p for p in raw.split() if p.strip() != '']
    if not parts:
        raise ValueError("No coefficients provided.")
    coeffs = [float(p) for p in parts]
    return coeffs


def eval_poly(coeffs: List[float], x: float) -> float:
    """
    Evaluate polynomial f(x) = sum_{k=0}^n a_k x^k at scalar x.
    Coeff list is [a0, a1, ..., an].
    """
    value = 0.0
    power = 1.0  # x^0
    for a_k in coeffs:
        value += a_k * power
        power *= x
    return value


def integrate_poly_exact(coeffs: List[float], a: float, b: float) -> float:
    """
    Compute exact integral ∫_a^b f(x) dx analytically by integrating coefficients.
    For f(x) = sum a_k x^k, integral is sum a_k/(k+1) [x^(k+1)]_a^b.
    """
    total = 0.0
    for k, a_k in enumerate(coeffs):
        exponent = k + 1
        factor = a_k / exponent
        total += factor * (b ** exponent - a ** exponent)
    return total


def build_partition(a: float, b: float, n: int) -> List[float]:
    """
    Return partition points x_0, x_1, ..., x_n for [a, b] with n subintervals.
    """
    dx = (b - a) / n
    return [a + i * dx for i in range(n + 1)]


# ---------- Riemann sum rules ----------

def riemann_sum(coeffs: List[float], a: float, b: float, n: int, rule: str) -> float:
    """
    Compute Riemann sum S_n using 'left', 'right', or 'mid' sampling.
    """
    rule = rule.lower()
    if rule not in ("left", "right", "mid", "midpoint"):
        raise ValueError("Rule must be 'left', 'right', or 'mid'/'midpoint'.")

    dx = (b - a) / n
    partition = build_partition(a, b, n)

    if rule == "left":
        sample_points = partition[:-1]  # x_0 through x_{n-1}
    elif rule == "right":
        sample_points = partition[1:]   # x_1 through x_n
    else:  # midpoint
        sample_points = []
        for i in range(n):
            mid = (partition[i] + partition[i + 1]) / 2
            sample_points.append(mid)

    total = 0.0
    for x in sample_points:
        total += eval_poly(coeffs, x)
    return total * dx


# ---------- Extension 1: Trapezoidal & Simpson rules ----------

def trapezoidal_rule(coeffs: List[float], a: float, b: float, n: int) -> float:
    """
    Trapezoidal rule approximation of ∫_a^b f(x) dx with n subintervals.
    """
    dx = (b - a) / n
    partition = build_partition(a, b, n)
    total = 0.0
    # Endpoints (1/2 each in the sum)
    total += 0.5 * eval_poly(coeffs, partition[0])
    total += 0.5 * eval_poly(coeffs, partition[-1])
    # Interior points
    for x in partition[1:-1]:
        total += eval_poly(coeffs, x)
    return total * dx


def simpson_rule(coeffs: List[float], a: float, b: float, n: int) -> float:
    """
    Simpson's rule approximation of ∫_a^b f(x) dx with n subintervals (n must be even).
    """
    if n % 2 != 0:
        raise ValueError("Simpson's rule requires an even number of subintervals n.")
    dx = (b - a) / n
    partition = build_partition(a, b, n)

    total = eval_poly(coeffs, partition[0]) + eval_poly(coeffs, partition[-1])
    # Odd and even interior points
    for i in range(1, n):
        x_i = partition[i]
        weight = 4 if i % 2 == 1 else 2
        total += weight * eval_poly(coeffs, x_i)
    return total * dx / 3.0


# ---------- Plotting helpers ----------

def plot_function_only(coeffs: List[float], a: float, b: float, num_points: int = 400):
    """
    Return arrays (x_list, y_list) for plotting f(x) on [a, b].
    """
    dx = (b - a) / num_points
    xs = [a + i * dx for i in range(num_points + 1)]
    ys = [eval_poly(coeffs, x) for x in xs]
    return xs, ys


def plot_riemann_rectangles(
    coeffs: List[float],
    a: float,
    b: float,
    n: int,
    rule: str,
    S_n: float,
    I_exact: float,
    abs_err: float,
):
    """
    REQUIRED visualization:
    - Plot f(x) on [a, b].
    - Draw Riemann rectangles for chosen rule.
    - Show S_n, I_exact, and |error| on the figure.
    """
    rule = rule.lower()
    dx = (b - a) / n
    partition = build_partition(a, b, n)

    # Build sample points for the chosen rule
    if rule == "left":
        sample_points = partition[:-1]
        title_rule = "Left Riemann Sum"
    elif rule == "right":
        sample_points = partition[1:]
        title_rule = "Right Riemann Sum"
    else:
        sample_points = [(partition[i] + partition[i + 1]) / 2 for i in range(n)]
        title_rule = "Midpoint Riemann Sum"

    # Function curve
    xs, ys = plot_function_only(coeffs, a, b)

    fig, ax = plt.subplots()
    ax.plot(xs, ys, label="f(x)")

    # Draw rectangles
    for i in range(n):
        if rule == "left":
            x_left = partition[i]
            sample_x = sample_points[i]
        elif rule == "right":
            x_left = partition[i]
            sample_x = sample_points[i]
        else:  # midpoint
            x_left = partition[i]
            sample_x = sample_points[i]

        height = eval_poly(coeffs, sample_x)
        rect = Rectangle(
            (x_left, 0),
            dx,
            height,
            linewidth=1.0,
            edgecolor="black",
            facecolor="orange",
            alpha=0.3,
        )
        ax.add_patch(rect)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(
        f"{title_rule} (n = {n})\n"
        f"Approx S_n = {S_n:.6f}, Exact I = {I_exact:.6f}, |Error| = {abs_err:.3e}"
    )
    ax.legend()
    fig.tight_layout()


# ---------- Extension 3: comparative rectangle visualization ----------

def plot_all_rules_rectangles(coeffs: List[float], a: float, b: float, n: int):
    """
    EXTENSION 3:
    Create a figure with three subplots visualizing Left, Midpoint, and Right
    Riemann rectangles side-by-side for comparison.
    """
    rules = ["left", "mid", "right"]
    titles = ["Left", "Midpoint", "Right"]
    dx = (b - a) / n
    partition = build_partition(a, b, n)

    xs_full, ys_full = plot_function_only(coeffs, a, b)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for ax, rule, title in zip(axes, rules, titles):
        ax.plot(xs_full, ys_full, label="f(x)")

        if rule == "left":
            sample_points = partition[:-1]
        elif rule == "right":
            sample_points = partition[1:]
        else:  # midpoint
            sample_points = [(partition[i] + partition[i + 1]) / 2 for i in range(n)]

        for i in range(n):
            x_left = partition[i]
            sample_x = sample_points[i]
            height = eval_poly(coeffs, sample_x)
            rect = Rectangle(
                (x_left, 0),
                dx,
                height,
                linewidth=0.8,
                edgecolor="black",
                facecolor="orange",
                alpha=0.3,
            )
            ax.add_patch(rect)

        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_xlabel("x")
        ax.set_title(title)

    axes[0].set_ylabel("f(x)")
    fig.suptitle("Extension 3: Comparative Riemann Rectangles (Left / Midpoint / Right)")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])


# ---------- Extension 2: convergence study ----------

def convergence_study(coeffs: List[float], a: float, b: float, I_exact: float):
    """
    EXTENSION 2:
    For n in [4, 8, 16, 32, 64] (if they fit well), compute errors for
    Left, Midpoint, and Right sums. Plot |error| vs n on log-log axes.
    """
    candidate_ns = [4, 8, 16, 32, 64]
    Ns = [n for n in candidate_ns if n >= 2]

    errors_left = []
    errors_mid = []
    errors_right = []

    for n in Ns:
        S_left = riemann_sum(coeffs, a, b, n, "left")
        S_mid = riemann_sum(coeffs, a, b, n, "mid")
        S_right = riemann_sum(coeffs, a, b, n, "right")
        errors_left.append(abs(S_left - I_exact))
        errors_mid.append(abs(S_mid - I_exact))
        errors_right.append(abs(S_right - I_exact))

    fig, ax = plt.subplots()
    ax.loglog(Ns, errors_left, marker="o", label="Left")
    ax.loglog(Ns, errors_mid, marker="s", label="Midpoint")
    ax.loglog(Ns, errors_right, marker="^", label="Right")
    ax.set_xlabel("n (number of subintervals)")
    ax.set_ylabel("|Error| = |S_n - I|")
    ax.set_title("Extension 2: Convergence of Riemann Sums (log-log)")
    ax.legend()
    fig.tight_layout()


# ---------- Command-line interface ----------

def main():
    print("=== Riemann Sums for Polynomials ===")
    print("This program implements Left, Right, and Midpoint Riemann sums,")
    print("computes the exact integral for a polynomial, and visualizes the")
    print("Riemann rectangles. It also includes 3 analysis-focused extensions.\n")

    # Prompt for coefficient list
    raw_coeffs = input(
        "Enter polynomial coefficients [a0, a1, ..., an] for f(x) = a0 + a1 x + ... + an x^n\n"
        "(separate by spaces or commas, e.g. '1, -2, 3' or '1 -2 3'): "
    )
    coeffs = parse_coeffs(raw_coeffs)

    # Prompt for interval [a, b]
    a = float(input("Enter the left endpoint a: "))
    b = float(input("Enter the right endpoint b (must be > a): "))
    if b <= a:
        raise ValueError("Need an interval with b > a.")

    # Prompt for number of subintervals n ≥ 2
    n = int(input("Enter the number of subintervals n (n >= 2): "))
    if n < 2:
        raise ValueError("n must be at least 2.")

    # Prompt for rule
    rule = input("Choose Riemann sum rule (left / right / mid): ").strip().lower()
    if rule not in ("left", "right", "mid", "midpoint"):
        raise ValueError("Rule must be 'left', 'right', or 'mid'/'midpoint'.")

    # Core computations
    S_n = riemann_sum(coeffs, a, b, n, rule)
    I_exact = integrate_poly_exact(coeffs, a, b)
    abs_err = abs(S_n - I_exact)

    print("\n--- Core Riemann Sum Results ---")
    print(f"Chosen rule         : {rule.capitalize() if rule != 'midpoint' else 'Midpoint'}")
    print(f"Interval [a, b]     : [{a}, {b}]")
    print(f"Number of subintervals n : {n}")
    print(f"Approximation S_n   : {S_n:.10f}")
    print(f"Exact integral I    : {I_exact:.10f}")
    print(f"Absolute error |S_n - I| : {abs_err:.10e}")

    # EXTENSION 1: Trapezoidal & Simpson’s rule
    print("\n--- Extension 1: Trapezoidal and Simpson Approximations ---")
    T_n = trapezoidal_rule(coeffs, a, b, n)
    err_trap = abs(T_n - I_exact)
    print(f"Trapezoidal T_n     : {T_n:.10f}  |Error| = {err_trap:.10e}")

    try:
        S_simpson = simpson_rule(coeffs, a, b, n)
        err_simp = abs(S_simpson - I_exact)
        print(f"Simpson S_simpson   : {S_simpson:.10f}  |Error| = {err_simp:.10e}")
    except ValueError as e:
        print(f"Simpson's rule      : not computed ({e})")

    # REQUIRED: main visualization of chosen rule
    plot_riemann_rectangles(coeffs, a, b, n, rule, S_n, I_exact, abs_err)

    # EXTENSION 3: comparative rectangles (Left, Midpoint, Right)
    plot_all_rules_rectangles(coeffs, a, b, n)

    # EXTENSION 2: convergence study
    convergence_study(coeffs, a, b, I_exact)

    print("\nFigures generated:")
    print("  1) Chosen rule Riemann rectangles with f(x) curve.")
    print("  2) Comparative rectangles for Left / Midpoint / Right (Extension 3).")
    print("  3) Convergence plot of |error| vs n for all three rules (Extension 2).")
    print("Close the plots to end the program.")

    plt.show()


if __name__ == "__main__":
    main()
