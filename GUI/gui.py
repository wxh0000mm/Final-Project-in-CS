import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from imports import *


class MainFrame(tk.Frame):
    """Your application's main window content frame. Meant for subclassing.
    Override the content() method to add your widgets.
    """

    def __init__(self, parent, title, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        #self.parent.protocol("WM_DELETE_WINDOW", parent.destroy())
        self.content_frame = tk.Frame(self, width=300, height=400)
        self.content(self.content_frame)
        self.content_frame.pack(expand=True)
        self.pack(expand=True, fill=tk.BOTH, padx=100, pady=100)

        # Center parent window
        parent.update_idletasks()
        width = parent.winfo_width()
        frame_width = parent.winfo_rootx() - parent.winfo_x()
        window_width = width + 2*frame_width
        height = parent.winfo_height()
        titlebar_height = parent.winfo_rooty() - parent.winfo_y()
        window_height = height + titlebar_height + frame_width
        x = parent.winfo_screenwidth() // 2 - window_width // 2
        y = parent.winfo_screenheight() // 2 - window_height // 2
        parent.geometry("{}x{}+{}+{}".format(width, height, x, y))

        # Run parent window
        parent.deiconify()
        parent.title(title)
        parent.attributes('-zoomed', True)
        parent.update_idletasks()
        #parent.mainloop()
        self.parent.mainloop()

    def content(self, master):
        pass


if __name__=="__main__":
    class Main(MainFrame):
        def content(self, master):
            # self.button = tk.Button(
            #     master,
            #     text = "Run attack (running run.sh)",
            #     command = self.on_click_hello
            # )
            # self.button.pack(padx=2, pady=2, fill=tk.X)
            '''Initializing the console inside a scrollbar area'''
            self.console = 
            
            '''Initializing and displaying graph inside a canvas'''
            self.canvas = FigureCanvasTkAgg(calc_and_parse_graph(), master=self.parent)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.grid(column=0, row=0, colspan=2, rowspan=2)
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            #self.canvas.toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
            #self.canvas.toolbar.update()

        def on_click_hello(self):
            print("hello world!")
root = tk.Tk()
def on_closing():
    print(analyze_key('out.txt'))
    print('DETECTED CLOSING EVENT')
    root.destroy()
    exit(1)

root.protocol("WM_DELETE_WINDOW", on_closing)
Main(root, "Side Channel Attacking Toolkit GUI")