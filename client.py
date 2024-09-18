import Pyro4
import tkinter as tk
import threading

class Client:
    def __init__(self):
        self.window = None
        self.proxy  = None

    def connect(self):
        self.proxy = Pyro4.Proxy(f"PYRONAME:agenda.{entryAgenda.get()}@{entryNameServer.get()}:9090")
        debugLog.insert(tk.END,f"Conectado.")

    def choose_op(self):
        choice = opcao.get()

        if choice == 0:
            self.add_contact_to_agenda()
        elif choice == 1:
            self.remove_contact_from_agenda()
        elif choice == 2:
            self.update_contact_on_agenda()
        else:
            self.get_contact_from_agenda()

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

# INPUT NAMESERVER
# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(clientGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=0, padx=5, pady=5,  sticky='w')
# Input
entryNameServer = tk.Entry(clientGui.window)
entryNameServer.grid(column=1, row=0, columnspan=3, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# INPUT AGENDA
# -------------------------------------------------------------------------------------
# Label
labelAgenda = tk.Label(clientGui.window, text="ID da Agenda :")
labelAgenda.grid(column=0, row=1, padx=5, pady=5,  sticky='w')
# Input
entryAgenda = tk.Entry(clientGui.window)
entryAgenda.grid(column=1, row=1, columnspan=3, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitNameServer = tk.Button(clientGui.window, text="Conectar", command=clientGui.connect)
buttonSubmitNameServer.grid(column=4, row=1, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# INPUT CONTATO
# -------------------------------------------------------------------------------------
# Label
labelContatoName = tk.Label(clientGui.window, text="Nome do contato :")
labelContatoName.grid(column=0, row=2, padx=5, pady=5,  sticky='w')
# Input
entryContatoName = tk.Entry(clientGui.window)
entryContatoName.grid(column=1, row=2, columnspan=3, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# INPUT TELEFONE
# -------------------------------------------------------------------------------------
# Label
labelContatoPhone = tk.Label(clientGui.window, text="Telefone do contato :")
labelContatoPhone.grid(column=0, row=3, padx=5, pady=5,  sticky='w')
# Input
entryContatoPhone = tk.Entry(clientGui.window)
entryContatoPhone.grid(column=1, row=3, columnspan=3, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitContato = tk.Button(clientGui.window, text="Conectar", command=clientGui.choose_op)
buttonSubmitContato.grid(column=4, row=3, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# OP SELECT
# -------------------------------------------------------------------------------------
opcao = tk.IntVar()
opcao.set(0)

radio1 = tk.Radiobutton(clientGui.window, text="Adicionar Contato", variable=opcao, value=0)
radio2 = tk.Radiobutton(clientGui.window, text="Remover Contato"  , variable=opcao, value=1)
radio3 = tk.Radiobutton(clientGui.window, text="Atualizar Contato", variable=opcao, value=2)
radio4 = tk.Radiobutton(clientGui.window, text="Consultar Contato", variable=opcao, value=3)
radio1.grid(column=0, row=4, padx=5, pady=5,  sticky='w')
radio2.grid(column=1, row=4, padx=5, pady=5,  sticky='w')
radio3.grid(column=2, row=4, padx=5, pady=5,  sticky='w')
radio4.grid(column=3, row=4, padx=5, pady=5,  sticky='w')
# -------------------------------------------------------------------------------------

# DEBUG
labelDebug = tk.Label(clientGui.window, text="Debug log :")
labelDebug.grid(column=0, row=5, padx=5, pady=5, sticky='nw')
debugLog = tk.Text(clientGui.window)
debugLog.grid(column=1, row=5, padx=5, pady=5, sticky="nsew")

# Loop Principal
clientGui.window.mainloop()