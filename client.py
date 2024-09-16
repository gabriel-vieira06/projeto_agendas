import Pyro4
import tkinter as tk
import threading

class Client:
    def __init__(self):
        self.window = None
        self.proxy  = None

    def connect(self):
        self.proxy = Pyro4.Proxy(f"PYRONAME:agenda.{entryAgenda.get()}@{entryNameServer.get()}:9090")

    def add_contact_to_agenda(self) -> None:
        pass

    def remove_contact_from_agenda(self) -> None:
        pass

    def get_contact_from_agenda(self) -> None:
        pass

    def update_contact_on_agenda(self) -> None:
        pass

clientGui = Client()
clientGui.window = tk.Tk()
clientGui.window.title("Aplicação do Cliente")

# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(clientGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=0, padx=5, pady=5,  sticky='w')
# Input
entryNameServer = tk.Entry(clientGui.window)
entryNameServer.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
# Label
labelAgenda = tk.Label(clientGui.window, text="ID da Agenda :")
labelAgenda.grid(column=0, row=1, padx=5, pady=5,  sticky='w')
# Input
entryAgenda = tk.Entry(clientGui.window)
entryAgenda.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitNameServer = tk.Button(clientGui.window, text="Conectar", command=clientGui.connect)
buttonSubmitNameServer.grid(column=3, row=1, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Loop Principal
clientGui.window.mainloop()