import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ._Visualizer import _Visualizer


class _Player(tk.Toplevel):
    def __init__(self, master, latex_func, generator):
        super().__init__(master)
        self.generator = generator
        self.minsize(800, 600)
        self.title("Visualization Player")

        self.latex_frame = tk.Frame(self)
        self.latex_frame.pack(side='top', fill='x')
        self._render_latex(latex_func)

        self.visualization = _Visualizer(self)
        self.visualization.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side='bottom', fill='x')

        self.stop_btn = tk.Button(
            self.button_frame, text='Stop ⏹', command=self._on_stop)
        self.stop_btn.pack(side='left', padx=5, pady=5)

        self.next_btn = tk.Button(
            self.button_frame, text='Next', command=self._next_step)
        self.next_btn.pack(side='left', padx=5, pady=5)

        self.cont_btn = tk.Button(
            self.button_frame, text='Continue ▶', command=self._on_continue)
        self.cont_btn.pack(side='left', padx=5, pady=5)

        self.attributes('-fullscreen', True)

        self._next_step()

    def _render_latex(self, latex_str):
        fig = plt.figure(figsize=(5, 1))
        fig.text(0.5, 0.5, f"${latex_str}$",
                 fontsize=14, ha='center', va='center')
        plt.axis('off')
        canvas = FigureCanvasTkAgg(fig, master=self.latex_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill='x')

    def _next_step(self):
        try:
            self.visualization.draw_grid(next(self.generator))
        except StopIteration:
            self.next_btn.config(state='disabled')
            self.cont_btn.config(state='disabled')
            tk.messagebox.showinfo("End", "No more steps to display.")

    def _on_stop(self):
        stop_win = tk.Toplevel(self)
        stop_win.title("Stopped")
        tk.Label(stop_win, text="Visualization stopped.").pack(
            padx=20, pady=20)

    def _on_continue(self):
        def skip_steps():
            try:
                while True:
                    next(self.generator)
            except StopIteration:
                self.after(0, self._open_continue_window)
        self.after(0, skip_steps)

    def _open_continue_window(self):
        cont_win = tk.Toplevel(self)
        cont_win.title("Continued")
        tk.Label(cont_win, text="All remaining steps skipped.").pack(
            padx=20, pady=20)
        self.destroy()
