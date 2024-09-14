import Pyro4
import tkinter as tk
import threading

class Client:
    def __init__(self) -> None:
        pass

    def connect(self) -> None:
        pass

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

# Get Username
# -------------------------------------------------------------------------------------
# Label
labelUsername = tk.Label(clientGui.window, text="Nome de usuário :")
labelUsername.grid(column=0, row=0, padx=5, pady=5, sticky='w')
# Input
entryUsername = tk.Entry(clientGui.window)
entryUsername.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Get NameServer IP
# -------------------------------------------------------------------------------------
# Label
labelNameServer = tk.Label(clientGui.window, text="IP do Servidor de Nomes :")
labelNameServer.grid(column=0, row=1, padx=5, pady=5,  sticky='w')
# Input
entryNameServer = tk.Entry(clientGui.window)
entryNameServer.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitNameServer = tk.Button(clientGui.window, text="Conectar", command=clientGui.connect)
buttonSubmitNameServer.grid(column=3, row=1, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Add Contact
# -------------------------------------------------------------------------------------
# Label
labelContact = tk.Label(clientGui.window, text="Adicionar contato :")
labelContact.grid(column=0, row=2, padx=5, pady=5,  sticky='w')
# Input
entryContact = tk.Entry(clientGui.window)
entryContact.grid(column=1, row=2, columnspan=2, padx=5, pady=5, sticky="nsew")
# Button
buttonSubmitContact = tk.Button(clientGui.window, text="Enviar", command=clientGui.add_contact_to_agenda)
buttonSubmitContact.grid(column=3, row=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Loop Principal
clientGui.window.mainloop()