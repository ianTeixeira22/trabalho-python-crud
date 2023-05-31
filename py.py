import tkinter as tk
from tkinter import messagebox
import sqlite3


def criar_tabela_usuarios():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT
        )
    """)

    conexao.commit()
    conexao.close()

def criar_tabela_camisas():
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camisas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()




def janela_cadastro():
    
    def cadastrar_usuario():
        nome_usuario = ent_nome_usuario.get()
        senha = ent_senha.get()
        telefone = ent_telefone.get()
        endereco = ent_endereco.get()

        conexao = sqlite3.connect("database.db")
        cursor = conexao.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (nome_usuario, senha, telefone, endereco) VALUES (?, ?, ?, ?)", (nome_usuario, senha, telefone, endereco))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            limpar_campos()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de usuário já cadastrado.")

        conexao.close()

    
    janela_cadastro = tk.Tk()
    janela_cadastro.title("Cadastro de Usuário")

    
    lbl_nome_usuario = tk.Label(janela_cadastro, text="Nome de Usuário:")
    lbl_nome_usuario.pack()
    ent_nome_usuario = tk.Entry(janela_cadastro)
    ent_nome_usuario.pack()

    lbl_senha = tk.Label(janela_cadastro, text="Senha:")
    lbl_senha.pack()
    ent_senha = tk.Entry(janela_cadastro, show="*")
    ent_senha.pack()

    lbl_telefone = tk.Label(janela_cadastro, text="Telefone:")
    lbl_telefone.pack()
    ent_telefone = tk.Entry(janela_cadastro)
    ent_telefone.pack()

    lbl_endereco = tk.Label(janela_cadastro, text="Endereço:")
    lbl_endereco.pack()
    ent_endereco = tk.Entry(janela_cadastro)
    ent_endereco.pack()

    btn_cadastrar = tk.Button(janela_cadastro, text="Cadastrar", command=cadastrar_usuario)
    btn_cadastrar.pack()

    
    
        
    def limpar_campos():
        ent_nome_usuario.delete(0, tk.END)
        ent_senha.delete(0, tk.END)
        ent_telefone.delete(0, tk.END)
        ent_endereco.delete(0, tk.END)
        
        janela_cadastro.mainloop()


def janela_login():
        def fazer_login():
            nome_usuario = ent_nome_usuario_login.get()
            senha = ent_senha_login.get()

            conexao = sqlite3.connect("database.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE nome_usuario = ? AND senha = ?", (nome_usuario, senha))
            resultado = cursor.fetchone()

            if resultado:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                def adicionar_camisa():
                    nome = ent_nome.get()
                    tamanho = ent_tamanho.get()
                    quantidade = ent_quantidade.get()
                    preco = ent_preco.get()

                    conexao = sqlite3.connect("database.db")
                    cursor = conexao.cursor()

                    try:
                        cursor.execute("INSERT INTO camisas (nome, tamanho, quantidade, preco) VALUES (?, ?, ?, ?)",
                                    (nome, tamanho, quantidade, preco))
                        conexao.commit()
                        messagebox.showinfo("Sucesso", "Camisa adicionada com sucesso!")
                        limpar_campos()
                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                    conexao.close()

                
                def consultar_camisas():
                    conexao = sqlite3.connect("database.db")
                    cursor = conexao.cursor()

                    cursor.execute("SELECT * FROM camisas")
                    rows = cursor.fetchall()

                    resultado = ""
                    for row in rows:
                        resultado += f"ID: {row[0]}\nNome: {row[1]}\nTamanho: {row[2]}\nQuantidade: {row[3]}\nPreço: R${row[4]}\n\n"

                    if resultado:
                        messagebox.showinfo("Camisas", resultado)
                    else:
                        messagebox.showinfo("Camisas", "Nenhum resultado encontrado.")

                    conexao.close()

                
                def atualizar_camisa():
                    id_camisa = ent_id.get()
                    nome = ent_nome.get()
                    tamanho = ent_tamanho.get()
                    quantidade = ent_quantidade.get()
                    preco = ent_preco.get()

                    conexao = sqlite3.connect("database.db")
                    cursor = conexao.cursor()

                    try:
                        cursor.execute("UPDATE camisas SET nome = ?, tamanho = ?, quantidade = ?, preco = ? WHERE id = ?",
                                    (nome, tamanho, quantidade, preco, id_camisa))
                        conexao.commit()
                        messagebox.showinfo("Sucesso", "Camisa atualizada com sucesso!")
                        limpar_campos()
                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                    conexao.close()

                
                def excluir_camisa():
                    id_camisa = ent_id.get()

                    conexao = sqlite3.connect("database.db")
                    cursor = conexao.cursor()

                    try:
                        cursor.execute("DELETE FROM camisas WHERE id = ?", (id_camisa,))
                        conexao.commit()
                        messagebox.showinfo("Sucesso", "Camisa excluída com sucesso!")
                        limpar_campos()
                    except Exception as e:
                        messagebox.showerror("Erro", str(e))

                    conexao.close()

                
                def limpar_campos():
                    ent_id.delete(0, tk.END)
                    ent_nome.delete(0, tk.END)
                    ent_tamanho.delete(0, tk.END)
                    ent_quantidade.delete(0, tk.END)
                    ent_preco.delete(0, tk.END)


                #criar a janela das camisas
                janela = tk.Tk()
                janela.title("Cadastro de Camisas")
                janela.geometry("400x400")
                janela.configure()

                
                frame_adicionar = tk.Frame(janela)
                frame_adicionar.pack(pady=10)

                lbl_bv = tk.Label(frame_adicionar, text='*lembre-se de escrever\ntodos os campos\nantes de adicionar!')
                lbl_bv.grid(row=4, column=5)

                lbl_nome = tk.Label(frame_adicionar, text="Nome:", font='Arial')
                lbl_nome.grid(row=0, column=0)
                ent_nome = tk.Entry(frame_adicionar)
                ent_nome.grid(row=0, column=1)

                lbl_tamanho = tk.Label(frame_adicionar, text="Tamanho:", font='Arial')
                lbl_tamanho.grid(row=1, column=0)
                ent_tamanho = tk.Entry(frame_adicionar)
                ent_tamanho.grid(row=1, column=1)

                lbl_quantidade = tk.Label(frame_adicionar, text="Quantidade:", font='Arial')
                lbl_quantidade.grid(row=2, column=0)
                ent_quantidade = tk.Entry(frame_adicionar)
                ent_quantidade.grid(row=2, column=1)

                lbl_preco = tk.Label(frame_adicionar, text="Preço:", font='Arial')
                lbl_preco.grid(row=3, column=0)
                ent_preco = tk.Entry(frame_adicionar)
                ent_preco.grid(row=3, column=1)

                btn_adicionar = tk.Button(frame_adicionar, text="Adicionar", command=adicionar_camisa, font='Arial')
                btn_adicionar.grid(row=4, column=0, columnspan=2, pady=10)

                
                frame_consultar = tk.Frame(janela)
                frame_consultar.pack(pady=10)

                btn_consultar = tk.Button(frame_consultar, text="Consultar", command=consultar_camisas, font='Arial')
                btn_consultar.pack()

                
                frame_atualizar_excluir = tk.Frame(janela)
                frame_atualizar_excluir.pack(pady=10)

                lbl_id = tk.Label(frame_atualizar_excluir, text="ID:", font='Arial')
                lbl_id.grid(row=0, column=0)
                ent_id = tk.Entry(frame_atualizar_excluir)
                ent_id.grid(row=0, column=1)

                btn_atualizar = tk.Button(frame_atualizar_excluir, text="Atualizar", command=atualizar_camisa, font='Arial')
                btn_atualizar.grid(row=1, column=0, padx=5)

                btn_excluir = tk.Button(frame_atualizar_excluir, text="Excluir", command=excluir_camisa, font='Arial')
                btn_excluir.grid(row=1, column=1, padx=5)

                
                btn_limpar = tk.Button(janela, text="Limpar", command=limpar_campos, font='Arial')
                btn_limpar.pack(pady=10)

                
                janela.mainloop()
                


            else:
             messagebox.showerror("Erro", "Usuário ou senha inválidos.")

            conexao.close()
        #janela de login
        janela_login = tk.Tk()
        janela_login.title("Login")

        
        lbl_nome_usuario_login = tk.Label(janela_login, text="Nome de Usuário:")
        lbl_nome_usuario_login.pack()
        ent_nome_usuario_login = tk.Entry(janela_login)
        ent_nome_usuario_login.pack()

        lbl_senha_login = tk.Label(janela_login, text="Senha:")
        lbl_senha_login.pack()
        ent_senha_login = tk.Entry(janela_login, show="*")
        ent_senha_login.pack()

        btn_login = tk.Button(janela_login, text="Login", command=fazer_login)
        btn_login.pack()

       

        
        janela_login.mainloop()



criar_tabela_usuarios()
criar_tabela_camisas()

#criar a janela principal
janela_principal = tk.Tk()
janela_principal.title("MR. Tronus")


largura = 800
altura = 600


largura_tela = janela_principal.winfo_screenwidth()
altura_tela = janela_principal.winfo_screenheight()


posicao_x = (largura_tela - largura) // 2
posicao_y = (altura_tela - altura) // 2


janela_principal.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")


janela_principal.configure(bg="black")


lbl_boas_vindas = tk.Label(janela_principal, text="Bem-vindo!\nSelecione a opção desejada:", font=("Arial", 24), bg="black", fg='green')
lbl_boas_vindas.pack(pady=20)


btn_cadastro = tk.Button(janela_principal, text="Cadastro", font=("Arial", 16), width=20, bg='green',command=janela_cadastro)
btn_cadastro.pack(pady=10)

btn_login = tk.Button(janela_principal, text="Login", font=("Arial", 16), width=20, bg='green', command=janela_login)
btn_login.pack(pady=10)


janela_principal.mainloop()
