import tkinter as tk
from tkinter import ttk
import json
import git
from git.exc import GitCommandError
import os
from tkinter import filedialog

# def listar_pastas():
#     pasta = entry_diretorio_local.get()
#     if os.path.exists(pasta) and os.path.isdir(pasta):
#         pastas = [item for item in os.listdir(pasta) if os.path.isdir(os.path.join(pasta, item))]
#         combo_pastas["values"] = pastas
#     else:
#         combo_pastas["values"] = []

def listar_pastas():
    pasta_selecionada = filedialog.askdirectory(initialdir="/home")
    entry_diretorio_local.delete(0, tk.END)  # Limpa o campo de entrada
    entry_diretorio_local.insert(0, pasta_selecionada) 
    if os.path.exists(pasta_selecionada) and os.path.isdir(pasta_selecionada):
        pastas = [item for item in os.listdir(pasta_selecionada) if os.path.isdir(os.path.join(pasta_selecionada, item))]
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
        "branchPessoal": entry_branchPessoal.get(),
        "branchComum": entry_branchComum.get(),
        "branchLibDes": entry_branchLibDes.get(),
        "branchLibItg": entry_branchLibItg.get(),
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
        entry_branchPessoal.delete(0, tk.END)
        entry_branchPessoal.insert(0, configuracao["branchPessoal"])     
        entry_branchComum.delete(0, tk.END)
        entry_branchComum.insert(0, configuracao["branchComum"]) 
        entry_branchLibDes.delete(0, tk.END)
        entry_branchLibDes.insert(0, configuracao["branchLibDes"])
        entry_branchLibItg.delete(0, tk.END)
        entry_branchLibItg.insert(0, configuracao["branchLibItg"])        

def nova_configuracao(event=None):
    entry_nome_config.delete(0, tk.END)
    combobox_config.delete(0, tk.END)
    entry_diretorio_local.delete(0, tk.END)
    combo_pastas.delete(0, tk.END)
    entry_branchPessoal.delete(0, tk.END)
    entry_branchComum.delete(0, tk.END)
    entry_branchLibDes.delete(0, tk.END)
    entry_branchLibItg.delete(0, tk.END)

# Criar a janela principal
root = tk.Tk()
root.title("Gerenciador de Configurações")
root.geometry("800x350")

# Carregar configurações existentes (ou criar um dicionário vazio)
try:
    with open("configuracoes.json", "r") as arquivo:
        configuracoes = json.load(arquivo)
except FileNotFoundError:
    configuracoes = {}

frameLinha1 = tk.Frame(root)
frameLinha1.pack(padx=5, pady=5, anchor='w')

label_configuracoes = tk.Label(frameLinha1, text="Configurações", width=30)
label_configuracoes.pack(side="left")

# Combobox para selecionar configuração
# combobox_config = ttk.Combobox(root)
combobox_config = ttk.Combobox(frameLinha1, width=50)
combobox_config.pack(side="left")
combobox_config.bind("<<ComboboxSelected>>", carregar_configuracao)  # Chamar a função ao selecionar uma configuração
combobox_config["values"] = list(configuracoes.keys())


# Campo de entrada para nome da configuração
frameLinha2 = tk.Frame(root)
frameLinha2.pack(padx=5, pady=5, anchor='w')

label_nome_config = tk.Label(frameLinha2, text="Nome da Configuração:", width=30)
label_nome_config.pack(side="left")
entry_nome_config = tk.Entry(frameLinha2, width=50)
entry_nome_config.pack(side="left")

# Campo de entrada para a pasta
frameLinha3 = tk.Frame(root)
frameLinha3.pack(padx=5, pady=5, anchor='w')

label_pasta = tk.Label(frameLinha3, text="Diretorio git Local:", width=30)
label_pasta.pack(side="left",)
entry_diretorio_local = tk.Entry(frameLinha3, width=50)  
entry_diretorio_local.pack(side="left")

# Botão para listar pastas
botao_listar = tk.Button(frameLinha3, text="Listar Pastas", command=listar_pastas)
botao_listar.pack(side="left")

# Combobox para exibir as pastas

frameLinha4 = tk.Frame(root)
frameLinha4.pack(padx=5, pady=5, anchor='w')

label_campo1 = tk.Label(frameLinha4, text="Projetos:", width=30)
label_campo1.pack(side="left")

combo_pastas = ttk.Combobox(frameLinha4)
combo_pastas = ttk.Combobox(frameLinha4, width=50)
combo_pastas.pack(side="left")


# Campos de entrada para as configurações
frameLinha5 = tk.Frame(root)
frameLinha5.pack(padx=5, pady=5, anchor='w')

label_campo1 = tk.Label(frameLinha5, text="Branch Pessoal:", width=30)
label_campo1.pack(side="left")
entry_branchPessoal = tk.Entry(frameLinha5, width=50)
entry_branchPessoal.pack(side="left")

frameLinha6 = tk.Frame(root)
frameLinha6.pack(padx=5, pady=5, anchor='w')

label_campo2 = tk.Label(frameLinha6, text="Branch Comum:", width=30)
label_campo2.pack(side="left")
entry_branchComum = tk.Entry(frameLinha6, width=50)
entry_branchComum.pack(side="left")

frameLinha7 = tk.Frame(root)
frameLinha7.pack(padx=5, pady=5, anchor='w')

label_campo3 = tk.Label(frameLinha7, text="Branch comum des(liberacao_des):", width=30)
label_campo3.pack(side="left")
entry_branchLibDes = tk.Entry(frameLinha7, width=50)
entry_branchLibDes.pack(side="left")

frameLinha8 = tk.Frame(root)
frameLinha8.pack(padx=5, pady=5, anchor='w')

label_campo4 = tk.Label(frameLinha8, text="Branch comum ITG(liberacao_itg):", width=30)
label_campo4.pack(side="left")
entry_branchLibItg = tk.Entry(frameLinha8, width=50)
entry_branchLibItg.pack(side="left")

# Botão para salvar configuração

frameLinha9 = tk.Frame(root)
frameLinha9.pack(padx=5, pady=5, anchor='center')

# Botão para salvar configuração
botao_novo = tk.Button(frameLinha9, text="Novo", command=nova_configuracao)
botao_novo.pack(side="left")

botao_salvar = tk.Button(frameLinha9, text="Salvar", command=salvar_configuracao)
botao_salvar.pack(side="left")

# Botão para carregar configuração selecionada
botao_carregar = tk.Button(frameLinha9, text="Carregar", command=carregar_configuracao)
botao_carregar.pack(side="left")

def merge():
    repo_path = entry_diretorio_local.get() + '/' + combo_pastas.get()
    branch_pessoal = entry_branchPessoal.get()
    branch_comum = entry_branchComum.get()
    branchLibDes = entry_branchLibDes.get()
    branchLibItg = entry_branchLibItg.get()

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
        if not branchLibDes == "":
            print("  ")
            print("  ")
            print("Checkout para a branch -> " + branchLibDes)
            repo.git.checkout(branchLibDes)
            print("  ")
            print("  ")
            print("Merge da branch -> " + branch_comum + " para a branch -> " + branchLibDes)
            repo.git.merge(branch_comum)
            print("  ")
            print("  ")
            print("Push para a branch -> " + branchLibDes)
            repo.remotes.origin.push(branchLibDes)
        else:
            print("Branch comun DES não configurada")

        # Merge e push para a branch "branchItg"
        if not branchLibItg == "":
            print("  ")
            print("  ")
            print("Checkout para a branch -> " + branchLibItg)
            repo.git.checkout(branchLibItg)
            print("  ")
            print("  ")
            print("Merge da branch -> " + branch_comum + " para a branch -> " + branchLibItg)
            repo.git.merge(branch_comum)
            print("  ")
            print("  ")
            print("Push para a branch -> " + branchLibItg)
            repo.remotes.origin.push(branchLibItg)
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
botao_merge = tk.Button(frameLinha9, text="Merge", command=merge)
botao_merge.pack(side="left")

# Boatão sair
botao_merge = tk.Button(frameLinha9, text="Sair", command=root.destroy)
botao_merge.pack(side="left")

# Iniciar o loop principal da interface gráfica
root.mainloop()