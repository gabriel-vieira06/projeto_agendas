import tkinter as tk
import threading
import Pyro4
import Pyro4.naming

class NameServer:
    def __init__(self):
        self.ip     = None
        self.window = None

    def set_ip(self):
        self.ip = entryNameServer.get()
        if self.ip:
            self.launch_name_server()
        else:
            debugLog.insert(tk.END,"ERRO: ENTRADA VAZIA\n")

    def launch_name_server(self):
        threadNameServer = threading.Thread(
            target=Pyro4.naming.startNSloop, kwargs={"host": self.ip}, daemon=True
        )
        debugLog.insert(tk.END,"Servidor de nomes ativo\n")
        threadNameServer.start()

nameServerGui = NameServer()

nameServerGui.window = tk.Tk()
nameServerGui.window.title("IP - Servidor de Nomes")

# Set NameServer IP
# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(nameServerGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=0, padx=5, pady=5, sticky='w')
# Input
entryNameServer = tk.Entry(nameServerGui.window)
entryNameServer.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitNameServer = tk.Button(nameServerGui.window, text="Criar", command=nameServerGui.set_ip)
buttonSubmitNameServer.grid(column=3, row=0, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# DEBUG
labelDebug = tk.Label(nameServerGui.window, text="Debug log :")
labelDebug.grid(column=0, row=1, padx=5, pady=5, sticky='nw')
debugLog = tk.Text(nameServerGui.window)
debugLog.grid(column=1,row=1, padx=5, pady=5, sticky="nsew")

nameServerGui.window.mainloop()