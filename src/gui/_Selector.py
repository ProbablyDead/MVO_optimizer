import tkinter as tk
from tkinter import ttk


class _Selector(tk.Frame):
    def __init__(self,
                 master,
                 name,
                 value_type,
                 lower_bound=None,
                 upper_bound=None,
                 default_value=None,
                 horizontal=False,
                 is_checkbox=True,
                 is_scale=True,
                 is_checkbox_blocked=None,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.is_checkbox = is_checkbox
        self.is_scale = is_scale
        self.is_int = value_type == tk.IntVar

        self.horizontal = horizontal

        self.container = tk.Frame(self)
        self.container.pack()
        self.is_checkbox_blocked = is_checkbox_blocked

        self.label = tk.Label(self.container, text=name, anchor="center")

        if self.is_checkbox:
            self.var_checkbox = tk.BooleanVar(value=False)
            self.checkbox = tk.Checkbutton(
                self.container, text="", variable=self.var_checkbox,
                command=self.__check_possibility)

        self.var = value_type(value=default_value if default_value else
                              (lower_bound+upper_bound)/2)
        if self.is_scale:
            self.scale = ttk.Scale(self.container, from_=lower_bound,
                                   to=upper_bound, variable=self.var)

        vcmd = self.register(self.__validate_entry)

        self.entry = tk.Entry(self.container,
                              validate="all", validatecommand=(vcmd, '%P'),
                              textvariable=self.var, justify="center", width=5,
                              command=None)

        self.__update_layout()

    def __validate_entry(self, v):
        if self.is_int:
            return str.isdigit(v) or v == ""

        try:
            float(v)
            return True
        except ValueError:
            return False

    def __update_layout(self):
        for widget in self.container.winfo_children():
            widget.pack_forget()

        if self.horizontal:
            self.label.pack(side="left", padx=5)
            if self.is_checkbox:
                self.checkbox.pack(side="left", padx=5)
            if self.is_scale:
                self.scale.config(orient="horizontal")
                self.scale.pack(side="left", padx=5)
            self.entry.pack(side="left", padx=5)
        else:
            self.label.pack(anchor="center", pady=2)
            if self.is_checkbox:
                self.checkbox.pack(anchor="center", pady=2)
            if self.is_scale:
                self.scale.config(orient="vertical")
                self.scale.pack(pady=2)
            self.entry.pack(pady=2)

    def __check_possibility(self):
        if self.var_checkbox.get():
            v = not self.is_checkbox_blocked()
            self.var_checkbox.set(v)
            if v:
                self.scale.config(state="disabled")
                self.entry.config(state="disabled")
        else:
            self.var_checkbox.set(False)
            self.scale.config(state="normal")
            self.entry.config(state="normal")

    def set_value(self, value):
        self.var.set(value)

    def is_selected(self):
        return self.var_checkbox.get()

    def get_value(self):
        return self.var.get()
