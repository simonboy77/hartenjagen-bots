from tkinter import *
from tkinter import ttk

def press_btn(*args):
    print("Pressed")

root = Tk()
root.title("Hartenjagen")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="1", command=press_btn).grid(column=2, row=2)
ttk.Button(mainframe, text="2", command=press_btn).grid(column=3, row=2)
ttk.Button(mainframe, text="3", command=press_btn).grid(column=4, row=2)
ttk.Button(mainframe, text="4", command=press_btn).grid(column=5, row=2)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.bind("<Return>", press_btn)

root.mainloop()