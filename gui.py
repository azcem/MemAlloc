import tkinter as tk

root = tk.Tk()

text_size = tk.Label(root, text="Enter memory size in bytes")
g_size = tk.Entry(root)

holes_size = tk.Label(root, text="Enter Holes: address1, size1; address2, size2; etc.")
g_hsize = tk.Entry(root)

processes = tk.Label(root, text="Enter processes")
g_proc = tk.Entry(root)

alg = tk.IntVar()
R1 = tk.Radiobutton(root, text="First Fit", variable=alg, value=1)
R2 = tk.Radiobutton(root, text="Best Fit", variable=alg, value=2)
R3 = tk.Radiobutton(root, text="Worst Fit", variable=alg, value=3)

comp = tk.IntVar()
C1 = tk.Checkbutton(root, text="Compaction", variable=comp, onvalue=1, offvalue=0)

dloc = tk.Label(root, text="Enter a process name to deallocate")
g_dp = tk.Entry(root)
g_dpb = tk.Button(root, text="Deallocate")

Show_B = tk.Button(root, text="Show Memory Content")

text_size.pack()
g_size.pack()
holes_size.pack()
g_hsize.pack()
processes.pack()
g_proc.pack()
R1.pack()
R2.pack()
R3.pack()
C1.pack()
dloc.pack()
g_dp.pack()
Show_B.pack()
root.mainloop()