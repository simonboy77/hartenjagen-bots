# https://tkdocs.com/tutorial/index.html
# https://tcl.tk/man/tcl8.6/TkCmd/contents.htm

from tkinter import *
from tkinter import ttk

from hand_of_cards import *
from game_manager import *

manager = GameManager(4)
manager.start_game()

while manager.game_update():
    continue

quit()

root = Tk()
root.title("Hartenjagen")
root.geometry("960x540")

mainFrame = ttk.Frame(root)
mainFrame.grid(column=0, row=0)

handFrame = ttk.Frame(mainFrame)
handFrame.grid(column=1,row=1, sticky=S)

hand = HandOfCards(handFrame, 4)
manager = GameManager(4)
manager.start_game()

lbl = ttk.Label(mainFrame, text="Wow")
lbl.grid(column=0, row=0)
lbl.bind('<Enter>', lambda e: lbl.configure(text='OWW'))
lbl.bind('<Leave>', lambda e: lbl.configure(text='Wow'))
lbl.bind('<B3-Motion>', lambda e: lbl.configure(text='right button drag to %d,%d' % (e.x, e.y)))

for child in mainFrame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()