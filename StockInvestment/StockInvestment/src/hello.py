import tkinter as tk
import win32com.client

class Auto_stock_controller:

	def __init__(self, master):
		print ("hello world")
		connect_CpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
		#connect_CpCybos = win32com.client.Dispatch("CpUtil.CpCybos","","")
		isConnect = connect_CpCybos.IsConnect
		if(isConnect == 9):
			print ("Fail Connect")
		else:
			print ("Success Connect")


root = tk.Tk()
app = Auto_stock_controller(root)
root.mainloop()

