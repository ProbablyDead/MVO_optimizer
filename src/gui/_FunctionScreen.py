import tkinter as tk
from tkinter import ttk
from ._Selector import _Selector


class _FunctionScreen(tk.Toplevel):
    def __init__(self, master, function, best_solution):
        super().__init__(master)

        self.function = function
        self.best_solution = best_solution

        self._add_graph()
        self._add_selector()
        self._add_reset_params_button()

    def _add_graph(self):
        pass

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
                is_checkbox_blocked=self._check_if_two_checkboxes_are_selected
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
            i1, i2 = self._get_selected_indexes()
            return False
        elif i > 2:
            return True

    def _get_selected_indexes(self) -> (int, int):
        for i, s in enumerate(self.selectors):
            if s.is_selected():
                yield i
