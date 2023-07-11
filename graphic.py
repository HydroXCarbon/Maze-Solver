import sys
from tkinter import Tk, BOTH, Canvas, Button, messagebox
import tkinter as tk
import time

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = None
        self.create_canvas(width, height)
        self.__running = False

        # Bind the close event to the custom handler
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_close)

    def create_canvas(self, width, height):
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)

    def __on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close()

    def get_root(self):
        return self.__root
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")
        sys.exit()  # Exit the program when the window is closed

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def clear(self):
        time.sleep(1)
        self.__canvas.delete("all")
        self.redraw()

    def close(self):
        self.__running = False
        self.__root.destroy()

class CustomButton:
    def __init__(self, win):
        self._win = win
        self.response = None
        self.dfs_button = Button(win.get_root(), text="DFS", command=lambda: self.DFS())
        self.bfs_button = Button(win.get_root(), text="BFS", command=lambda: self.BFS())
        self.next_button = Button(win.get_root(), text="Next maze", command=lambda: self.next())
        self.exit_button = Button(win.get_root(), text="Exit", command=lambda: self.exit())
        
        self.exit_button.pack(side="bottom")
        self.next_button.pack(side="bottom")
        self.dfs_button.pack(side="bottom")
        self.bfs_button.pack(side="bottom")

    def next(self):
        self.response = "NEXT"
        self.disable_buttons()
        self._win.get_root().quit()

    def DFS(self):
        self.response = "DFS"
        self.disable_buttons()
        self._win.get_root().quit()

    def BFS(self):
        self.response = "BFS"
        self.disable_buttons()
        self._win.get_root().quit()

    def exit(self):
        self.response = "EXIT"
        self._win.get_root().quit()

    def enable_buttons(self):
        self.dfs_button.configure(state="normal") 
        self.bfs_button.configure(state="normal")
        self.next_button.configure(state="normal")

    def disable_buttons(self):
        self.dfs_button.configure(state="disabled") 
        self.bfs_button.configure(state="disabled")
        self.next_button.configure(state="disabled")

    def wait_for_response(self):
        self.enable_buttons()
        self._win.get_root().mainloop()
        return self.response

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)

