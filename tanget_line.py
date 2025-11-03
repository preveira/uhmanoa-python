# Assignment 1: Tangent Line Visualization
# Simple, interactive plot of a function and its tangent line at a user-controlled point.
# Uses the import structure recommended in the assignment PDF.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.widgets import Slider
import time

# --- Function definition (simple default) ---
def f(x):
    # You can change this function if you want to explore others
    return x**3 - 3*x

# --- Numerical derivative using central difference ---
def df(x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2*h)

def main():
    # --- Domain for plotting ---
    xmin, xmax = -5.0, 5.0
    x = np.linspace(xmin, xmax, 800)

    # --- Get an initial point from the user (fallback to 0.0 if invalid) ---
    try:
        user_in = input("Enter the x-value where you want the tangent line (e.g., 1.0): ").strip()
        x0 = float(user_in) if user_in != "" else 0.0
    except Exception:
        x0 = 0.0

    # Clamp x0 into the plotting window
    x0 = max(min(x0, xmax), xmin)

    # --- Initial computations ---
    y = f(x)
    m = df(x0)
    y0 = f(x0)
    tangent = m*(x - x0) + y0

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(7, 4.5))
    plt.subplots_adjust(bottom=0.22)  # leave room for slider

    func_line, = ax.plot(x, y, label="f(x)")
    tan_line, = ax.plot(x, tangent, linestyle="--", label="Tangent at x0")
    point_dot, = ax.plot([x0], [y0], marker="o", linestyle="none")

    ax.set_title("Function and Tangent Line")
    ax.set_xlim(xmin, xmax)
    ax.grid(True, linestyle=":")
    ax.legend(loc="best")

    # --- Slider to move x0 in real time ---
    slider_ax = fig.add_axes([0.15, 0.08, 0.7, 0.05])
    x0_slider = Slider(slider_ax, "x0", xmin, xmax, valinit=x0, valstep=(xmax - xmin)/1000.0)

    def on_change(val):
        x0_new = x0_slider.val
        m_new = df(x0_new)
        y0_new = f(x0_new)
        tan_line.set_ydata(m_new*(x - x0_new) + y0_new)
        point_dot.set_data([x0_new], [y0_new])
        fig.canvas.draw_idle()

    x0_slider.on_changed(on_change)

    plt.show()

if __name__ == "__main__":
    main()
