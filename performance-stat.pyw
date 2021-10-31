from tkinter.constants import BOTH, CENTER, E, LEFT, RIGHT, TOP, W, YES, X
import psutil
import tkinter as tk

def main():
  def gui():
    root = tk.Tk()
    root.title("STATS")
    root.attributes('-topmost', True)

    #Change the name in the window
    def change_label(labelname, text):
      labelname.configure(text=text)

    def mem_stats():
      return str(round(psutil.virtual_memory().total/1000000)) + '/' + str(round(psutil.virtual_memory().used/1000000))

    def update_usage():
      change_label(label_cpu_percentage, psutil.cpu_percent())
      change_label(label_mem_percentage, psutil.virtual_memory().percent)
      change_label(label_mem_used, mem_stats())
      root.after(300, update_usage)

    frame_cpu = tk.Frame(root)

    label_cpu = tk.Label(frame_cpu, text='CPU', font='Calibri 18',width=10, anchor=W)
    label_cpu_percentage = tk.Label(frame_cpu, text=psutil.cpu_percent(), font='Calibri 18',width=10, anchor=W)
    label_cpu.pack(side=LEFT,fill=X)
    label_cpu_percentage.pack(side=LEFT,fill=X)

    frame_cpu.pack(fill=BOTH, expand=YES)

    frame_mem = tk.Frame(root)

    label_mem = tk.Label(frame_mem, text='MEM', font='Calibri 18',width=10, anchor=W)
    label_mem_percentage = tk.Label(frame_mem, text=psutil.virtual_memory().percent, font='Calibri 18',width=10, anchor=W)

    label_mem_used = tk.Label(frame_mem, text=mem_stats(), font='Calibri 18',width=10, anchor=W)

    label_mem.pack(side=LEFT,fill=X)
    label_mem_percentage.pack(side=LEFT,fill=X)
    label_mem_used.pack(side=LEFT,fill=X)

    frame_mem.pack(fill=BOTH, expand=YES)

    
    root.after(300, update_usage)

    root.mainloop()

  gui()

if __name__ == "__main__":
    main()