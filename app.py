import customtkinter as ctk
import numpy as np
import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)  # type: ignore
from matplotlib.figure import Figure

from config import window, frames, buttons, labels, colors, graph, entries, texts
from lib.Arrow3D import Arrow3D

ctk.set_appearance_mode("dark")


def abs_add(target, amount):
    '''Increases the magnitude of provided target value by amount'''
    return target + (amount * (target // abs(target)))


def grid_configure(container, rows, columns):
    '''Define the number of rows and columns in the provided container'''
    for row in range(rows):
        container.grid_rowconfigure(row, weight=1)

    for column in range(columns):
        container.grid_columnconfigure(column, weight=1)


class VectorHandler:
    def __init__(self, update_dot_product, plot_vecs):
        self.vec_var_a = (ctk.IntVar(), ctk.IntVar(), ctk.IntVar())
        self.vec_var_b = (ctk.IntVar(), ctk.IntVar(), ctk.IntVar())

        self.update_dot_product = update_dot_product
        self.plot_vecs = plot_vecs

    def convert_to_coords(self, vec_comps, point=False, adjust=False):
        '''Converts vector components or dot product to their coordinate forms'''
        # Adjust line coordinates to place arrow tip on desired position
        vec = [abs_add(comp, 0.17) for comp in vec_comps] if adjust else vec_comps

        return (
            np.array(tup) for tup in zip((vec[0] if point else 0, 0, 0), vec)
        )

    def get_limits(self, vec_a, vec_b, dot_product):
        '''Generate limits for each axis depending on the given vector components'''
        coord_pairs = list(zip(vec_a, vec_b))

        # Slice gets first and last element
        return (
            sorted([0, dot_product, *coord_pairs[0]])[0:4:3],
            sorted([0, *coord_pairs[1]])[0:3:2],
            sorted([0, *coord_pairs[2]])[0:3:2]
        )

    def calculate_and_plot(self):
        vec_a = np.array([val.get() for val in self.vec_var_a])
        vec_b = np.array([val.get() for val in self.vec_var_b])

        vec_a_coords = self.convert_to_coords(vec_a, adjust=True)
        vec_b_coords = self.convert_to_coords(vec_b, adjust=True)

        dot_product = np.dot(vec_a, vec_b)
        self.update_dot_product(dot_product)

        dot_product_coords = self.convert_to_coords([dot_product, 0, 0], point=True)
        limits = self.get_limits(vec_a, vec_b, dot_product)

        self.plot_vecs(limits, vec_a_coords, vec_b_coords, dot_product_coords)


class Vector3DApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(texts["title"])
        self.maxsize(**window["dimensions"])
        self.minsize(**window["dimensions"])

        grid_configure(self, rows=4, columns=1)

        self.title_frame = VectorTitleFrame(self)

        self.product_frame = VectorProductFrame(self)
        self.graph_frame = VectorGraphFrame(self)

        self.vec_handler = VectorHandler(
            self.product_frame.update_dot_product,
            self.graph_frame.plot_vectors
        )

        self.input_frame = VectorInputFrame(
            self,
            self.vec_handler.vec_var_a,
            self.vec_handler.vec_var_b,
            self.vec_handler.calculate_and_plot
        )

        self.title_frame.grid(row=0, column=0, **frames["title"])
        self.input_frame.grid(row=1, column=0, **frames["input"])
        self.product_frame.grid(row=2, column=0, **frames["product"])
        self.graph_frame.grid(row=3, column=0, **frames["graph"])


class VectorTitleFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, fg_color="#3a7ebf", *args, **kwargs)

        grid_configure(self, rows=1, columns=1)

        self.title_label = ctk.CTkLabel(self, text=texts["title"], font=("Arial", 40), pady=20)
        self.title_label.grid(row=0, column=0)


class VectorInputField(ctk.CTkFrame):
    def __init__(self, master, vec, vec_label, vec_primary, vec_secondary, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        grid_configure(self, rows=1, columns=7)

        vec_label = ctk.CTkLabel(self, text=vec_label, font=("Arial", 14, "bold"), text_color=vec_primary)
        vec_label.grid(row=0, column=0, **labels["vec"])

        for i, comp in enumerate("ijk"):
            comp_entry = ctk.CTkEntry(self, textvariable=vec[i], width=40, height=20)
            comp_label = ctk.CTkLabel(self, text=comp, font=("Arial", 12, "bold"), text_color=vec_secondary)

            comp_entry.grid(row=0, column=(i * 2 + 1), **entries["comp"])
            comp_label.grid(row=0, column=(i * 2 + 2), **labels["comp"])


class VectorInputFrame(ctk.CTkFrame):
    def __init__(self, master, vec_a, vec_b, plot_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        grid_configure(self, rows=1, columns=3)

        self.vec_a_field = VectorInputField(
            self,
            vec=vec_a,
            vec_label="ᗩ",
            vec_primary=colors["a_primary"],
            vec_secondary=colors["a_secondary"],
        )
        self.vec_b_field = VectorInputField(
            self,
            vec=vec_b,
            vec_label="ᗷ",
            vec_primary=colors["b_primary"],
            vec_secondary=colors["b_secondary"],
        )
        self.generate_button = ctk.CTkButton(self, text=texts["button"], command=plot_callback)

        self.vec_a_field.grid(row=0, column=0, **entries["vector"])
        self.vec_b_field.grid(row=0, column=1, **entries["vector"])
        self.generate_button.grid(row=0, column=2, **buttons["generate"])


class VectorProductFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        grid_configure(self, rows=1, columns=2)

        self.descriptive_label = ctk.CTkLabel(self, text=texts["dp_text"])
        self.placeholder_label = ctk.CTkLabel(self, text=texts["dp_value"])

        self.descriptive_label.grid(row=0, column=0, **labels["dp_text"])
        self.placeholder_label.grid(row=0, column=1, **labels["dp_value"])

    def update_dot_product(self, dot_product):
        self.placeholder_label.configure(text=dot_product)


class VectorGraphFrame(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        grid_configure(self, rows=1, columns=1)

        self.figure = Figure(figsize=(1, 4))
        self.axes = self.figure.add_subplot(projection="3d")

        self.axes.set_xlabel("X")
        self.axes.set_ylabel("Y")
        self.axes.set_zlabel("Z")

        self.axes.autoscale(enable=True, axis="both", tight=None)
        self.axes.autoscale_view(tight=None, scalex=True, scaley=True, scalez=True)

        # Graph as Tkinter widget
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas._tkcanvas.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)  # type: ignore

        # Allows interacting with the 3D graph
        self.canvas.mpl_connect("button_press_event", self.axes._button_press)
        self.canvas.mpl_connect("button_release_event", self.axes._button_release)
        self.canvas.mpl_connect("motion_notify_event", self.axes._on_move)

    def plot_vectors(self, limits, vec_a_coords, vec_b_coords, dot_product_coords):
        self.axes.clear()

        self.axes.set_xlim(limits[0])
        self.axes.set_ylim(limits[1])
        self.axes.set_zlim(limits[2])

        vec_a_line = Arrow3D(
            *vec_a_coords,
            **graph["arrow_style"],
            color=colors["a_primary"]
        )
        vec_b_line = Arrow3D(
            *vec_b_coords,
            **graph["arrow_style"],
            color=colors["b_primary"]
        )
        self.axes.add_artist(vec_a_line)
        self.axes.add_artist(vec_b_line)
        self.axes.plot3D(
            *dot_product_coords,
            marker="o",
            color=colors["dot"]
        )

        self.canvas.draw()
        self.toolbar.update()
