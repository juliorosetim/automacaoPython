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
        "branchLibDes": brancLibDes.get(),
        "branchLibItg": brancLibItg.get(),
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
        branchLibDes.delete(0, tk.END)
        branchLibDes.insert(0, configuracao["branchLibDes"])
        branchLibItg.delete(0, tk.END)
        branchLibItg.insert(0, configuracao["branchLibItg"])        

# Criar a janela principal
root = tk.Tk()
root.title("Gerenciador de Configurações")
root.geometry("700x450")

# Carregar configurações existentes (ou criar um dicionário vazio)
try:
    with open("configuracoes.json", "r") as arquivo:
        configuracoes = json.load(arquivo)
except FileNotFoundError:
    configuracoes = {}

label_em_branco = tk.Label(root, text="")
label_em_branco.pack()

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

label_campo3 = tk.Label(root, text="Branch comum des(liberacao_des):")
label_campo3.pack()
branchLibDes = tk.Entry(root, width=80)
branchLibDes.pack()

label_campo4 = tk.Label(root, text="Branch comum ITG(liberacao_itg):")
label_campo4.pack()
branchLibItg = tk.Entry(root, width=80)
branchLibItg.pack()

# Botão para salvar configuração
botao_salvar = tk.Button(root, text="Salvar Configuração", command=salvar_configuracao)
botao_salvar.pack()

# Botão para carregar configuração selecionada
botao_carregar = tk.Button(root, text="Carregar Configuração", command=carregar_configuracao)
botao_carregar.pack()

def merge():
    repo_path = entry_diretorio_local.get() + '/' + combo_pastas.get()
    branch_pessoal = branchPessoal.get()
    branch_comum = branchComum.get()
    branch_des = branchLibDes.get()
    branch_itg = branchLibItg.get()

    try:
        repo = git.Repo(repo_path)
        print("Pasta do repositorio -> " + entry_diretorio_local.get() + '/' + combo_pastas.get())
        print("  ")
        print("  ")        
        repo.git.checkout(branch_pessoal)
        print("Pull da branch -> " + branch_pessoal)
        repo.remotes.origin.pull(branch_pessoal)

        # Mude para a branch_comum, faça o merge com branch_pessoa e envie para a branch_des
        print("  ")
        print("  ")
        print("Checkout para a branch -> " + branch_comum)
        repo.git.checkout(branch_comum)
        print("  ")
        print("  ")
        print("Merge da branch -> " + branch_pessoal + " para a branch -> " + branch_comum)
        repo.git.merge(branch_pessoal)
        print("  ")
        print("  ")
        print("Push para a branch -> " + branch_comum)
        repo.remotes.origin.push(branch_comum)

        # Merge e push para a branch "branchDes"
        if not branch_des == "":
            print("  ")
            print("  ")
            print("Checkout para a branch -> " + branch_des)
            repo.git.checkout(branch_des)
            print("  ")
            print("  ")
            print("Merge da branch -> " + branch_comum + " para a branch -> " + branch_des)
            repo.git.merge(branch_comum)
            print("  ")
            print("  ")
            print("Push para a branch -> " + branch_des)
            repo.remotes.origin.push(branch_des)
        else:
            print("Branch comun DES não configurada")

        # Merge e push para a branch "branchItg"
        if not branch_des == "":
            print("  ")
            print("  ")
            print("Checkout para a branch -> " + branch_itg)
            repo.git.checkout(branch_itg)
            print("  ")
            print("  ")
            print("Merge da branch -> " + branch_comum + " para a branch -> " + branch_des)
            repo.git.merge(branch_comum)
            print("  ")
            print("  ")
            print("Push para a branch -> " + branch_itg)
            repo.remotes.origin.push(branch_itg)
        else:
            print("Branch comun ITG não configurada")


        print("  ")
        print("  ")
        print("Checkout para a branch -> " + branch_pessoal)
        repo.git.checkout(branch_pessoal)
        print("  ")
        print("  ")
        print("Alterações enviadas com sucesso para as branches de destino.")

    except GitCommandError as e:
        print(f"Erro durante o processo de merge: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Botão para fazer o merge
botao_merge = tk.Button(root, text="Merge", command=merge)
botao_merge.pack()

# Iniciar o loop principal da interface gráfica
root.mainloop()