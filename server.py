import tkinter as tk
import threading
import Pyro4
import Pyro4.errors
import Pyro4.naming

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.contacts = {}  # Dicionario de contatos {nome: telefone}
        self.replicas = []  # lista de replicas
        self.uri      = None
    
    def add_replica(self, replica_uri):
        self.replicas.append(replica_uri)
    
    def synchronize(self):
        for uri in self.replicas:
            try:
                replica = Pyro4.Proxy(uri)
                replica.add_replica(self.uri)
                self.contacts.update(replica.get_contacts())
            except Pyro4.errors.CommunicationError:
                debugLog.insert(tk.END, f"Replica {uri} offline, não pode ser sincronizada\n")
    
    def get_contacts(self):
        return self.contacts
    
    def get_replicas(self):
        return self.replicas
    
    def set_uri(self, uri):
        self.uri = uri

    def add_contacts(self, name, phone):
        if name in self.contacts:
            debugLog.insert(tk.END, "Contato já existe.\n")
            raise ValueError("Contato já existe.")
        self.contacts[name] = phone
        self._propagate_change('update', name, phone)
    
    def remove_contact(self, name):
        if name not in self.contacts:
            debugLog.insert(tk.END, "Contato não encontrado.\n")
            raise ValueError("Contato não encontrado.")
        del self.contacts[name]
        self._propagate_change('remove', name)

    def update_contact(self, name, new_phone):
        if name not in self.contacts:
            debugLog.insert(tk.END, "Contato não encontrado.\n")
            raise ValueError("Contato não encontrado.")
        self.contacts[name] = new_phone
        self._propagate_change('update', name, new_phone)
    
    def _propagate_change(self, action, name, phone=None):
        for uri in self.replicas:
            try:
                replica = Pyro4.Proxy(uri)
                if action == 'add':
                    replica.add_contact(name, phone)
                elif action == 'remove':
                    replica.remove_contact(name)
                elif action == 'update':
                    replica.update_contact(name, phone)
            except Pyro4.errors.CommunicationError:
                debugLog.insert(tk.END, f"Falha ao propagar mudança para {uri}.\n")

def launch_remote_server():
    ip = entryIpAgenda.get()
    port = int(entryPortAgenda.get())
    name = entryIdAgenda.get()

    threadRemoteServer = threading.Thread(
        target=start_remote_server, kwargs={"ip": ip, "port": port, "name": name}, daemon=True
    )
    threadRemoteServer.start()

def start_remote_server(ip, port, name):
    daemon  = Pyro4.Daemon(host=ip, port=port)
    try:
        ns  = Pyro4.locateNS(host=ip, port=9090)
        agenda = Agenda()
        replicas = ns.list(prefix="agenda.")
        for _, agenda_uri in replicas.items():
            agenda.add_replica(agenda_uri)
        agenda.synchronize()
        uri = daemon.register(agenda)
        agenda.set_uri(uri)
        ns.register(f"agenda.{name}", uri)
        debugLog.insert(tk.END, f"Agenda{name} criada.\n")
        daemon.requestLoop()
    except Exception as e:
        debugLog.insert(tk.END, f"{e}\n")    

agendaGui = tk.Tk()
agendaGui.title("Conexão da agenda")

# -------------------------------------------------------------------------------------
# Label
labelIpAgenda = tk.Label(agendaGui, text="IP do Servidor de nomes :")
labelIpAgenda.grid(column=0, row=0, padx=5, pady=5, sticky='w')
# Input
entryIpAgenda = tk.Entry(agendaGui)
entryIpAgenda.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------

# Label
labelPortAgenda = tk.Label(agendaGui, text="Porta para acesso da agenda (9091 ~ 49151) :")
labelPortAgenda.grid(column=0, row=1, padx=5, pady=5, sticky='w')
# Input
entryPortAgenda = tk.Entry(agendaGui)
entryPortAgenda.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Label
labelIdAgenda = tk.Label(agendaGui, text="ID da agenda :")
labelIdAgenda.grid(column=0, row=2, padx=5, pady=5, sticky='w')
# Input
entryIdAgenda = tk.Entry(agendaGui)
entryIdAgenda.grid(column=1, row=2, columnspan=2, padx=5, pady=5, sticky="nsew")
# -------------------------------------------------------------------------------------

# Button
buttonSubmitAgenda = tk.Button(agendaGui, text="Iniciar", command=launch_remote_server)
buttonSubmitAgenda.grid(column=3, row=2, padx=5, pady=5, sticky="nsew")

# DEBUG
labelDebug = tk.Label(agendaGui, text="Debug log :")
labelDebug.grid(column=0, row=3, padx=5, pady=5, sticky='nw')
debugLog = tk.Text(agendaGui)
debugLog.grid(column=1,row=3, padx=5, pady=5, sticky="nsew")

agendaGui.mainloop()