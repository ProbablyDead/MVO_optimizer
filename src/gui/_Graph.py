import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class _Graph(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.func = None
        self.params = None
        self.idx1 = None
        self.idx2 = None
        self.transposed = False

        self.var1 = tk.DoubleVar(value=0)
        self.var2 = tk.DoubleVar(value=0)

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.transpose_button = tk.Button(
            frame, text="Transpose Graph", command=self.transpose_graph)
        self.transpose_button.pack()

    def set_function(self, func, params, var_indexes, bounds):
        self.func = func
        self.params = params
        self.idx1, self.idx2 = var_indexes
        self.bounds = bounds

    def update_plot(self, *args):
        if self.func is None or self.params is None or self.idx1 is None or self.idx2 is None:
            return

        new_params = self.params[:]
        new_params[self.idx1] = self.var1.get()
        new_params[self.idx2] = self.var2.get()

        chxb = self.bounds[self.transposed]

        x_vals = np.linspace(
            chxb[0],
            chxb[1],
            100
        )
        y_vals = [self.func(
            np.array([
                val if i == self.idx1 else new_params[self.idx1] if i == self.idx2
                else new_params[i] for i in range(len(self.params))
            ])) for val in x_vals]

        self.ax.clear()
        if self.transposed:
            self.ax.plot(y_vals, x_vals, label="Function Output")
            self.ax.set_xlabel(f"Parameter {self.idx2}")
            self.ax.set_ylabel(f"Parameter {self.idx1}")
        else:
            self.ax.plot(x_vals, y_vals, label="Function Output")
            self.ax.set_xlabel(f"Parameter {self.idx1}")
            self.ax.set_ylabel(f"Parameter {self.idx2}")

        # self.ax.legend()
        self.canvas.draw()

    def transpose_graph(self):
        self.transposed = not self.transposed
        self.update_plot()
