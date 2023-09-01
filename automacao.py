import tkinter as tk
from tkinter import ttk
import json
import git
from git.exc import GitCommandError
import os

def listar_pastas():
    pasta = entry_diretorio_local.get()
    if os.path.exists(pasta) and os.path.isdir(pasta):
        pastas = [item for item in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, item))]
        combo_pastas["values"] = pastas
    else:
        combo_pastas["values"] = []

def salvar_configuracao():
    nome_config = entry_nome_config.get()
    configuracao = {
        "configuracoes": combobox_config.get(),
        "nomeConfiguracao": entry_nome_config.get(),
        "diretorio": entry_diretorio_local.get(),
        "pasta": combo_pastas.get(),
        "branchPessoal": branchPessoal.get(),
        "branchComum": branchComum.get(),
    }
    configuracoes[nome_config] = configuracao
    with open("configuracoes.json", "w") as arquivo:
        json.dump(configuracoes, arquivo)
    combobox_config["values"] = list(configuracoes.keys())
    combobox_config.set(nome_config)

def carregar_configuracao(event=None):
    nome_config = combobox_config.get()
    if nome_config in configuracoes:
        configuracao = configuracoes[nome_config]
        entry_nome_config.delete(0, tk.END)
        entry_nome_config.insert(0, configuracao["nomeConfiguracao"])
        combobox_config.delete(0, tk.END)
        combobox_config.insert(0, configuracao["configuracoes"])
        entry_diretorio_local.delete(0, tk.END)
        entry_diretorio_local.insert(0, configuracao["diretorio"])      
        combo_pastas.delete(0, tk.END)
        combo_pastas.insert(0, configuracao["pasta"])               
        branchPessoal.delete(0, tk.END)
        branchPessoal.insert(0, configuracao["branchPessoal"])        
        branchComum.delete(0, tk.END)
        branchComum.insert(0, configuracao["branchComum"])    

# Criar a janela principal
root = tk.Tk()
root.title("Gerenciador de Configurações")
root.geometry("600x400")

# Carregar configurações existentes (ou criar um dicionário vazio)
try:
    with open("configuracoes.json", "r") as arquivo:
        configuracoes = json.load(arquivo)
except FileNotFoundError:
    configuracoes = {}

# Combobox para selecionar configuração
#combobox_config = ttk.Combobox(root, values=list(configuracoes.keys()))
combobox_config = ttk.Combobox(root)
combobox_config = ttk.Combobox(root, width=80)
combobox_config.pack()
combobox_config.bind("<<ComboboxSelected>>", carregar_configuracao)  # Chamar a função ao selecionar uma configuração

combobox_config["values"] = list(configuracoes.keys())

# Campo de entrada para nome da configuração
label_nome_config = tk.Label(root, text="Nome da Configuração:")
label_nome_config.pack()
entry_nome_config = tk.Entry(root, width=80)
entry_nome_config.pack()

# Campo de entrada para a pasta
label_pasta = tk.Label(root, text="Diretorio git Local:")
label_pasta.pack()
entry_diretorio_local = tk.Entry(root, width=80)  
entry_diretorio_local.pack()

# Botão para listar pastas
botao_listar = tk.Button(root, text="Listar Pastas", command=listar_pastas)
botao_listar.pack()

# Combobox para exibir as pastas
combo_pastas = ttk.Combobox(root)
combo_pastas = ttk.Combobox(root, width=80)
combo_pastas.pack()


# Campos de entrada para as configurações
label_campo1 = tk.Label(root, text="Branch Pessoal:")
label_campo1.pack()
branchPessoal = tk.Entry(root, width=80)
branchPessoal.pack()

label_campo2 = tk.Label(root, text="Branch Comum:")
label_campo2.pack()
branchComum = tk.Entry(root, width=80)
branchComum.pack()

# Botão para salvar configuração
botao_salvar = tk.Button(root, text="Salvar Configuração", command=salvar_configuracao)
botao_salvar.pack()

# Botão para carregar configuração selecionada
botao_carregar = tk.Button(root, text="Carregar Configuração", command=carregar_configuracao)
botao_carregar.pack()

# Iniciar o loop principal da interface gráfica
root.mainloop()