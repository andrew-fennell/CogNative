from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import time

ws = Tk()
ws.title('CogNative')
ws.geometry('400x200')


def open_file():
    file_path = askopenfile(mode='r', filetypes=[('Audio Files', '*wav')])
    #print(file_path.name)
    if file_path is not None:
        pass


def uploadFiles():
    pb1 = Progressbar(
        ws,
        orient=HORIZONTAL,
        length=300,
        mode='determinate'
    )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(ws, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)


adhar = Label(
    ws,
    text='Upload the original audio file '
)
adhar.grid(row=0, column=0, padx=10)

adharbtn = Button(
    ws,
    text='Choose File',
    command=lambda: open_file()
)
adharbtn.grid(row=0, column=1)

upld = Button(
    ws,
    text='Upload Files',
    command=uploadFiles
)
upld.grid(row=3, columnspan=3, pady=20, padx=20)

ws.mainloop()