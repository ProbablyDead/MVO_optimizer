import tkinter as tk
import colorsys


class _Visualizer(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

    def generate_spectrum_colors(self, num_colors):
        return [self.hsv_to_hex(i / num_colors, 0.8, 0.9) for i in range(num_colors)]

    def hsv_to_hex(self, h, s, v):
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return "#{:02X}{:02X}{:02X}".format(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def draw_grid(self, data):
        """Draw bordered arrays with circle labels and row indexes."""
        self.delete("all")  # Clear canvas

        rows, cols = len(data), len(data[0].get_array())

        # Generate row border colors
        row_colors = self.generate_spectrum_colors(rows)

        # Get canvas size
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        # Compute adaptive sizes
        # Adaptive row height
        row_height = max(min(canvas_height // (rows + 1), 100), 50)
        # Ensure circles fit within rows
        circle_size = min(row_height - 20, 40)
        spacing_x = min((canvas_width - 80) // (cols + 2), 50)
        start_x = 60  # Adjust left padding for row labels

        for r, universe in enumerate(data):
            y_top = r * (row_height + 5) + 10
            y_bottom = y_top + row_height
            x_left = start_x - circle_size // 2
            x_right = start_x + cols * spacing_x + circle_size // 2

            # Draw row border
            self.create_rectangle(x_left, y_top, x_right,
                                  y_bottom, outline=row_colors[r]
                                  if r != rows - 1 else "#FFFFFF", width=4)

            # Draw universe index on the left
            self.create_text(start_x - (30 if r != rows-1 else 34),
                             (y_top + y_bottom) // 2,
                             text=str(r+1) if r != rows-1 else "BU",
                             font=("Arial", 14, "bold"),
                             fill="black" if r != rows-1 else "red")

            for c, (v, origin) in enumerate(zip(universe.get_array(), universe.get_origins())):
                x = start_x + c * spacing_x
                y = (y_top + y_bottom) // 2

                color = row_colors[origin] if origin != -1 else "#FFFFFF"

                # Draw circle
                self.create_oval(x, y - circle_size // 2, x + circle_size,
                                 y + circle_size // 2, fill=color, outline="black")

                # Draw index inside circle
                self.create_text(
                    x + circle_size // 2, y, text="%.2f" % v,
                    font=("Arial", 8, "bold"), fill="black")

            # Draw value
            self.create_text(x_right + 30, (y_top + y_bottom) // 2,
                             text="%.4f" % universe.get_inflation_rate(),
                             font=("Arial", 8, "bold"),
                             fill="black" if r != rows-1 else "red")
