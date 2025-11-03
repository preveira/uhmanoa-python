# Assignment 2: Visualizing Higher-Order Derivatives
# Simple program that plots a function and its first, second, and third derivatives
# with minimal UI to change the function and the x-range.
# Uses the import structure recommended in the assignment PDF.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.widgets import RadioButtons, Slider
import time

# --- Preset functions to keep things simple ---
def f_poly(x):
    return x**3 - 3*x

def f_sin(x):
    return np.sin(x)

def f_gauss(x):
    return np.exp(-x**2)

FUNCTIONS = {
    "x^3 - 3x": f_poly,
    "sin(x)": f_sin,
    "exp(-x^2)": f_gauss,
}

def compute_all_derivatives(f, x):
    y = f(x)
    # Numerical derivatives using gradients for simplicity
    y1 = np.gradient(y, x)
    y2 = np.gradient(y1, x)
    y3 = np.gradient(y2, x)
    return y, y1, y2, y3

def main():
    # Initial settings
    xmin, xmax = -5.0, 5.0
    x = np.linspace(xmin, xmax, 1200)
    f = FUNCTIONS["x^3 - 3x"]

    # Compute
    y, y1, y2, y3 = compute_all_derivatives(f, x)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.subplots_adjust(left=0.28, bottom=0.18)  # room for controls

    (line_f,)  = ax.plot(x, y, label="f(x)", linestyle="-")
    (line_d1,) = ax.plot(x, y1, label="f'(x)", linestyle="--")
    (line_d2,) = ax.plot(x, y2, label="f''(x)", linestyle="-.")
    (line_d3,) = ax.plot(x, y3, label="f'''(x)", linestyle=":")

    ax.set_title("Function and First Three Derivatives")
    ax.grid(True, linestyle=":")
    ax.legend(loc="best")

    # --- Radio buttons for function choice ---
    radio_ax = fig.add_axes([0.03, 0.55, 0.20, 0.35])
    radio = RadioButtons(radio_ax, tuple(FUNCTIONS.keys()), active=0)
    radio_ax.set_title("Function")

    # --- Sliders for x-range (simple customization) ---
    smin_ax = fig.add_axes([0.15, 0.09, 0.7, 0.03])
    smax_ax = fig.add_axes([0.15, 0.05, 0.7, 0.03])
    smin = Slider(smin_ax, "xmin", -10.0, 0.0, valinit=xmin)
    smax = Slider(smax_ax, "xmax",  0.0, 10.0, valinit=xmax)

    def update_plot(cur_f, xnew):
        y, y1, y2, y3 = compute_all_derivatives(cur_f, xnew)
        line_f.set_data(xnew, y)
        line_d1.set_data(xnew, y1)
        line_d2.set_data(xnew, y2)
        line_d3.set_data(xnew, y3)
        ax.set_xlim(xnew.min(), xnew.max())
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)
        fig.canvas.draw_idle()

    def on_radio(label):
        cur_f = FUNCTIONS[label]
        xmin_cur = min(smin.val, smax.val - 1e-6)
        xmax_cur = max(smax.val, smin.val + 1e-6)
        xnew = np.linspace(xmin_cur, xmax_cur, 1200)
        update_plot(cur_f, xnew)

    def on_slider(_):
        xmin_cur = min(smin.val, smax.val - 1e-6)
        xmax_cur = max(smax.val, smin.val + 1e-6)
        xnew = np.linspace(xmin_cur, xmax_cur, 1200)
        cur_label = radio.value_selected
        cur_f = FUNCTIONS[cur_label]
        update_plot(cur_f, xnew)

    radio.on_clicked(on_radio)
    smin.on_changed(on_slider)
    smax.on_changed(on_slider)

    plt.show()

if __name__ == "__main__":
    main()
