import tkinter as tk
from tkinter import ttk
from ._Selector import _Selector

EMPTY_CHOOSE = "Choose function"


class AppMainScreen:
    def __init__(self, functions, optimizer, root=tk.Tk()):
        self.functions = functions
        self.optimizer = optimizer
        self.hyperparameters_widgets = {}
        self.root = root
        self.__customize_window()

        self.__selected_function = tk.StringVar(self.root)
        self.__create_function_selector()

        self.__add_hyper_parameters()

        self.__add_continue_button()

    def __customize_window(self):
        self.root.title("Multi Verse Optimizer")
        self.root.geometry("450x300")
        self.root.minsize(450, 300)

    def __create_function_selector(self):
        drop_down_array = [EMPTY_CHOOSE] + \
            [f.function_name for f in self.functions]

        self.__function_selector = tk.OptionMenu(
            self.root,
            self.__selected_function,
            *drop_down_array,
        )

        self.__selected_function.set(drop_down_array[0])

        self.__function_selector.pack()

    def __add_hyper_parameters(self):
        self.hyperparameters_widgets["N"] = _Selector(
            self.root,
            "N",
            tk.IntVar,
            lower_bound=0,
            default_value=500,
            is_checkbox=False,
            is_scale=False,
            horizontal=True)
        self.hyperparameters_widgets["N"].pack(pady=10, padx=10, fill="x")

        self.hyperparameters_widgets["Max iterations"] = _Selector(
            self.root,
            "Max iterations",
            tk.IntVar,
            lower_bound=0,
            default_value=1000,
            is_checkbox=False,
            is_scale=False,
            horizontal=True)
        self.hyperparameters_widgets["Max iterations"].pack(
            pady=10, padx=10, fill="x")

        self.hyperparameters_widgets["WEP_min"] = _Selector(
            self.root,
            "WEP_min",
            tk.DoubleVar,
            lower_bound=0,
            upper_bound=1,
            default_value=0.2,
            is_checkbox=False,
            horizontal=True)
        self.hyperparameters_widgets["WEP_min"].pack(
            pady=10, padx=10, fill="x")

        self.hyperparameters_widgets["WEP_max"] = _Selector(
            self.root,
            "WEP_max",
            tk.DoubleVar,
            lower_bound=0,
            upper_bound=1,
            default_value=0.6,
            is_checkbox=False,
            horizontal=True,
        )
        self.hyperparameters_widgets["WEP_max"].pack(
            pady=10, padx=10, fill="x")

        self.hyperparameters_widgets["p"] = _Selector(
            self.root,
            "p",
            tk.DoubleVar,
            lower_bound=0,
            default_value=6,
            is_checkbox=False,
            is_scale=False,
            horizontal=True)
        self.hyperparameters_widgets["p"].pack(pady=10, padx=10, fill="x")

    def __add_continue_button(self):
        ttk.Button(self.root, text="Optimize",
                   command=self.__handle_continue).pack()

    def __get_selected_function(self, func_name):
        return next(
            filter(lambda x: x.function_name == func_name,
                   self.functions)
        )

    def __handle_continue(self):
        func = self.__selected_function.get()
        if func != EMPTY_CHOOSE:
            self.__optimize(self.__get_selected_function(func))

    def __optimize(self, function):
        print(
            self.hyperparameters_widgets["N"].get_value(),
            self.hyperparameters_widgets["Max iterations"]
            .get_value(),
            self.hyperparameters_widgets["WEP_min"].get_value(),
            self.hyperparameters_widgets["WEP_max"].get_value(),
            self.hyperparameters_widgets["p"].get_value(),
        )
        self.__openNewWindow(self.optimizer(
            function.function,
            function.dim,
            function.lower_bounds,
            function.upper_bounds,
            N=self.hyperparameters_widgets["N"].get_value(),
            max_time=self.hyperparameters_widgets["Max iterations"]
            .get_value(),
            wep_min=self.hyperparameters_widgets["WEP_min"].get_value(),
            wep_max=self.hyperparameters_widgets["WEP_max"].get_value(),
            p=self.hyperparameters_widgets["p"].get_value(),
            is_minimization=function.is_mininization
        ).optimize()[1])

    def __openNewWindow(self, v):
        newWindow = tk.Toplevel(self.root)
        newWindow.title("New Window")
        newWindow.geometry("200x200")
        ttk.Label(newWindow,
                  text=v).pack()

    def start_app(self):
        self.root.mainloop()
