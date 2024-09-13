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
        "branchLibDes": branchLibDes.get(),
        "branchLibItg": branchLibItg.get(),
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
root.geometry("800x350")

# Carregar configurações existentes (ou criar um dicionário vazio)
try:
    with open("configuracoes.json", "r") as arquivo:
        configuracoes = json.load(arquivo)
except FileNotFoundError:
    configuracoes = {}

fLinha1 = tk.Frame(root)
fLinha1.pack(padx=5, pady=5, anchor='w')

label_em_branco = tk.Label(fLinha1, text="Configurações", width=30)
label_em_branco.pack(side="left")

# Combobox para selecionar configuração
# combobox_config = ttk.Combobox(root)
combobox_config = ttk.Combobox(fLinha1, width=50)
combobox_config.pack(side="left")
combobox_config.bind("<<ComboboxSelected>>", carregar_configuracao)  # Chamar a função ao selecionar uma configuração
combobox_config["values"] = list(configuracoes.keys())
label_em_branco.pack()

# Campo de entrada para nome da configuração
fLinha2 = tk.Frame(root)
fLinha2.pack(padx=5, pady=5, anchor='w')

label_nome_config = tk.Label(fLinha2, text="Nome da Configuração:", width=30)
label_nome_config.pack(side="left")
entry_nome_config = tk.Entry(fLinha2, width=50)
entry_nome_config.pack(side="left")

# Campo de entrada para a pasta
fLinha3 = tk.Frame(root)
fLinha3.pack(padx=5, pady=5, anchor='w')

label_pasta = tk.Label(fLinha3, text="Diretorio git Local:", width=30)
label_pasta.pack(side="left",)
entry_diretorio_local = tk.Entry(fLinha3, width=50)  
entry_diretorio_local.pack(side="left")

# Botão para listar pastas
botao_listar = tk.Button(fLinha3, text="Listar Pastas", command=listar_pastas)
botao_listar.pack(side="left")

# Combobox para exibir as pastas

fLinha4 = tk.Frame(root)
fLinha4.pack(padx=5, pady=5, anchor='w')

label_campo1 = tk.Label(fLinha4, text="Projetos:", width=30)
label_campo1.pack(side="left")

combo_pastas = ttk.Combobox(fLinha4)
combo_pastas = ttk.Combobox(fLinha4, width=50)
combo_pastas.pack(side="left")


# Campos de entrada para as configurações
fLinha5 = tk.Frame(root)
fLinha5.pack(padx=5, pady=5, anchor='w')

label_campo1 = tk.Label(fLinha5, text="Branch Pessoal:", width=30)
label_campo1.pack(side="left")
branchPessoal = tk.Entry(fLinha5, width=50)
branchPessoal.pack(side="left")

fLinha6 = tk.Frame(root)
fLinha6.pack(padx=5, pady=5, anchor='w')

label_campo2 = tk.Label(fLinha6, text="Branch Comum:", width=30)
label_campo2.pack(side="left")
branchComum = tk.Entry(fLinha6, width=50)
branchComum.pack(side="left")

fLinha7 = tk.Frame(root)
fLinha7.pack(padx=5, pady=5, anchor='w')

label_campo3 = tk.Label(fLinha7, text="Branch comum des(liberacao_des):", width=30)
label_campo3.pack(side="left")
branchLibDes = tk.Entry(fLinha7, width=50)
branchLibDes.pack(side="left")

fLinha8 = tk.Frame(root)
fLinha8.pack(padx=5, pady=5, anchor='w')

label_campo4 = tk.Label(fLinha8, text="Branch comum ITG(liberacao_itg):", width=30)
label_campo4.pack(side="left")
branchLibItg = tk.Entry(fLinha8, width=50)
branchLibItg.pack(side="left")

# Botão para salvar configuração

fLinha9 = tk.Frame(root)
fLinha9.pack(padx=5, pady=5, anchor='center')

botao_salvar = tk.Button(fLinha9, text="Salvar", command=salvar_configuracao)
botao_salvar.pack(side="left")

# Botão para carregar configuração selecionada
botao_carregar = tk.Button(fLinha9, text="Carregar", command=carregar_configuracao)
botao_carregar.pack(side="left")

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
        if not branch_itg == "":
            print("  ")
            print("  ")
            print("Checkout para a branch -> " + branch_itg)
            repo.git.checkout(branch_itg)
            print("  ")
            print("  ")
            print("Merge da branch -> " + branch_comum + " para a branch -> " + branch_itg)
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
botao_merge = tk.Button(fLinha9, text="Merge", command=merge)
botao_merge.pack(side="left")

# Boatão sair
botao_merge = tk.Button(fLinha9, text="Sair", command=root.destroy)
botao_merge.pack(side="left")

# Iniciar o loop principal da interface gráfica
root.mainloop()