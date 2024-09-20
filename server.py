import tkinter as tk
from tkinter import ttk
import threading
import Pyro4
import Pyro4.errors
import Pyro4.naming

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Agenda:
    def __init__(self):
        self.contacts = {}  # Dicionario de contatos {nome: telefone}
        self.replicas = []  # lista de replicas (uris)
        self.uri      = None
    
    def add_replica(self, replica_uri):
        try:
            self.replicas.append(replica_uri)
            debugLog.insert(tk.END, f"Replica {replica_uri} adicionada.\n")
        except Exception as e:
            debugLog.insert(tk.END, f"{e}.\n")

    def synchronize(self):
        for uri in self.replicas:
            try:
                replica = Pyro4.Proxy(uri)
                replica.add_replica(self.uri)
                self.contacts.update(replica.get_contacts())
            except Pyro4.errors.CommunicationError:
                debugLog.insert(tk.END, f"Replica {uri} não sincronizada.\n")
            except Exception as e:
                debugLog.insert(tk.END, f"{e}.\n")
        
        for name, phone in self.contacts.items():
            tree.insert("", tk.END, values=(name, phone))
    
    def get_contacts(self):
        return self.contacts
    
    def get_replicas(self):
        return self.replicas
    
    def get_uri(self):
        return self.uri
    
    def set_uri(self, uri):
        self.uri = uri
        debugLog.insert(tk.END,f"URI: {self.uri}\n")

    def add_contacts(self, name, phone):
        if name in self.contacts:
            raise ValueError("Contato já existe.")
        self.contacts[name] = phone
        tree.insert("", tk.END, values=(name, phone))
        self.propagate_change('add', name, phone)
    
    def remove_contact(self, name):
        if name not in self.contacts:
            raise ValueError("Contato não encontrado.")
        del self.contacts[name]
        for item in tree.get_children():
            valores = tree.item(item, "values")
            if valores[0] == name:
                tree.delete(item)
                break
        self.propagate_change('remove', name)

    def update_contact(self, name, new_phone):
        if name not in self.contacts:
            raise ValueError("Contato não encontrado.")
        
        for contact_name, contact_phone in self.contacts.items():
            if contact_name == name and contact_phone == new_phone:
                raise ValueError("Contato atualizado.")

        self.contacts[name] = new_phone
        for item in tree.get_children():
            valores = tree.item(item, "values")
            if valores[0] == name:
                tree.item(item, values=(valores[0], new_phone))
                break
        self.propagate_change('update', name, new_phone)
    
    def propagate_change(self, action, name, phone=None):
        for uri in self.replicas:
            try:
                replica = Pyro4.Proxy(uri)
                if action == 'add':
                    replica.add_contacts(name, phone)
                elif action == 'remove':
                    replica.remove_contact(name)
                elif action == 'update':
                    replica.update_contact(name, phone)
            except Pyro4.errors.CommunicationError:
                debugLog.insert(tk.END, f"Falha de sincronização para {uri}.\n")
            except ValueError:  # Exceção = Fim da recursão, não faz nada nem aponta erros
                pass
            except Exception as e:
                debugLog.insert(tk.END, f"{e}\n")

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
        uri = daemon.register(agenda)
        agenda.set_uri(uri)
        agenda.synchronize()
        ns.register(f"agenda.{name}", uri)
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

# Agenda Tabela
labelTree = tk.Label(agendaGui, text="Tabela de contatos :")
labelTree.grid(column=0, row=4, padx=5, pady=5, sticky='nw')
tree = ttk.Treeview(agendaGui, columns=("Nome", "Telefone"), show='headings')
tree.heading("Nome", text="Nome")
tree.heading("Telefone", text="Telefone")
tree.grid(column=1,row=4, padx=5, pady=5, sticky="nsew")

agendaGui.mainloop()