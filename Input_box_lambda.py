import tkinter as tk
import globcfg

window = tk.Tk()
window.title('my window')
window.geometry('500x300')

e = tk.Entry(window)
e.pack()
def insert_point():
    var = e.get()
    globcfg.lamGen = int(var)
    t.insert('insert', var)

b1 = tk.Button(window, text='Enter lamGen value in small box and then press me.', width=50,height=2, command=insert_point)
b1.pack()
t = tk.Text(window, height=5)
t.pack()

e2 = tk.Entry(window)
e2.pack()
def insert_point2():
    var = e2.get()
    globcfg.lamRW = int(var)
    t2.insert('insert', var)
    return var
b2 = tk.Button(window, text='Enter lamRW value in small box and then press me.', width=50, height=5, command= insert_point2)
b2.pack()
t2 = tk.Text(window, height=9)
t2.pack()

window.mainloop()
