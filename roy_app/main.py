import tkinter as tk
from roy_app.roi_selector import ROISelector


def run_app():
    root = tk.Tk()
    root.title("Roy App")
    app = ROISelector(root)
    app.pack()
    root.mainloop()


if __name__ == '__main__':
    run_app()
