import tkinter as tk
import globcfg

window = tk.Tk()
window.title('my window')
window.geometry('200x100')

var = tk.StringVar()
l = tk.Label(window, textvariable=var, bg='green', font=('Arial', 12), width=30,
             height=2)
#l = tk.Label(window, text='OMG! this is TK!', bg='green', font=('Arial', 12), width=15, height=2)
l.pack()

var.set('Writer')
on_hit = False
def prior():
    global on_hit
    if on_hit == False:
        globcfg.priority = 'Reader'
        on_hit = True
        var.set('Reader')
    else:
        globcfg.priority = 'Writer'
        on_hit = False
        var.set('Writer')

b = tk.Button(window, text='Writer/Reader (default:writer)', width=30,
              height=2, command=prior)
b.pack()

window.mainloop()
