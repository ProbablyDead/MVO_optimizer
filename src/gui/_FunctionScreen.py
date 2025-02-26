import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from ._Selector import _Selector
from ._Graph import _Graph


class _FunctionScreen(tk.Toplevel):
    def __init__(self, master, function, best_solution):
        super().__init__(master)

        self.function = function
        self.best_solution = best_solution

        self.latex_frame = tk.Frame(self)
        self.latex_frame.pack(side='top', fill='x')
        self._render_latex(function.visualisation)

        self._add_graph()
        self._add_selector()
        self._add_reset_params_button()

    def _add_graph(self):
        self.graph = _Graph(
            self,
        )
        self.graph.pack()

    def _render_latex(self, latex_str):
        fig = plt.figure(figsize=(5, 1))
        fig.text(0.5, 0.5, f"${latex_str}$",
                 fontsize=14, ha='center', va='center')
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=self.latex_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill='x')

    def _add_selector(self):
        arr = self.best_solution.get_array()
        lb = self.function.lower_bounds \
            if isinstance(self.function.lower_bounds, list) \
            else [self.function.lower_bounds]*self.function.dim
        ub = self.function.upper_bounds \
            if isinstance(self.function.upper_bounds, list) \
            else [self.function.upper_bounds]*self.function.dim

        self.selectors = []

        for i in range(self.function.dim):
            s = _Selector(
                self,
                i,
                tk.DoubleVar,
                lower_bound=lb[i],
                upper_bound=ub[i],
                default_value=arr[i],
                is_checkbox=True,
                horizontal=False,
                is_checkbox_blocked=self._check_if_two_checkboxes_are_selected,
                on_update_value_callback=self._update_graph
            )
            self.selectors.append(s)
            s.pack(side="left", expand=True)

    def _add_reset_params_button(self):
        ttk.Button(self, text="Reset to best",
                   command=self._set_params_to_best).pack(side="bottom")

    def _set_params_to_best(self):
        arr = self.best_solution.get_array()

        for i, s in enumerate(self.selectors):
            s.set_value(arr[i])

    def _check_if_two_checkboxes_are_selected(self):
        i = 0
        for s in self.selectors:
            i += s.is_selected()

        if i < 2:
            return False
        elif i == 2:
            self._update_graph()
            return False
        elif i > 2:
            return True

    def _update_graph(self):
        idxs = list(self._get_selected_indexes())
        bounds = [[self.selectors[i].lb, self.selectors[i].ub] for i in idxs]

        self.graph.set_function(
            self.function.function,
            self._get_params_values(),
            idxs,
            bounds
        )
        self.graph.update_plot()

    def _get_params_values(self):
        return [s.get_value() for s in self.selectors]

    def _get_selected_indexes(self) -> (int, int):
        for i, s in enumerate(self.selectors):
            if s.is_selected():
                yield i
