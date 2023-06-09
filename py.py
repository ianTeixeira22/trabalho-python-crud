import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

def criar_banco_camisas():
    conexao = sqlite3.connect("tronos.db")
    cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS camisas (codigo INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cor TEXT, tamanho TEXT, quantidade INTEGER, preco REAL)")
    conexao.commit()
    conexao.close()

def criar_banco_usuarios():
    conexao = sqlite3.connect("tronos.db")
    cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (cpf INTEGER PRIMARY KEY, nome TEXT, senha INTEGER, telefone INTEGER)")
    conexao.commit()
    conexao.close()


janela = tk.Tk()
janela.title('Mr. Tronos')

largura_janela = 500
altura_janela = 300

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
janela.resizable(width=0, height=0)


def fazer_login():
    usuario = ent_usuario.get()
    senha = ent_senha.get()

    conexao = sqlite3.connect("tronos.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?",(usuario, senha))
    resultado = cursor.fetchone()
    if resultado:
        messagebox.showinfo('acesso liberado', 'login bem sucedido!\nclique em *ok* para ter acesso ao sistema')
        janela.destroy()
        
        janela_camisas = tk.Tk()
        janela_camisas.title('Mr.Tronos')

        largura_janela = 700
        altura_janela = 500

        largura_tela = janela_camisas.winfo_screenwidth()
        altura_tela = janela_camisas.winfo_screenheight()

        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2

        janela_camisas.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        janela_camisas.resizable(width=1, height=1)

        def limpar_campos():
            ent_nome_camisa.delete(0,tk.END)
            ent_cor_camisa.delete(0,tk.END)
            ent_tamanho_camisa.delete(0,tk.END)
            ent_quantidade_camisa.delete(0,tk.END)
            ent_preco_camisa.delete(0,tk.END)
            ent_cod_camisa.delete(0,tk.END)

        def cadastrar_camisa():
            
            nome_camisa = ent_nome_camisa.get()
            cor_camisa = ent_cor_camisa.get()
            tamanho_camisa = ent_tamanho_camisa.get()
            quantidade_camisa = ent_quantidade_camisa.get()
            preco_camisa = ent_preco_camisa.get()
            
            if nome_camisa and cor_camisa and tamanho_camisa and quantidade_camisa and preco_camisa:
                try:
                    conexao = sqlite3.connect("tronos.db")
                    cursor = conexao.cursor()
                    cursor.execute("INSERT INTO camisas (nome, cor, tamanho, quantidade, preco) VALUES (?, ?, ?, ?, ?)", (nome_camisa, cor_camisa, tamanho_camisa, quantidade_camisa, preco_camisa))
                    conexao.commit()
                    messagebox.showinfo('sucesso', 'camisa cadastrada')
                    limpar_campos()
                except Exception as e:
                    print(f'Erro: {str(e)}')
                finally:
                    conexao.close()
            else:
                messagebox.showerror("erro","Por favor, preencha todos os campos")

        def excluir_camisa():
            codigo = ent_cod_camisa.get()

            if codigo:
                try:
                    conexao = sqlite3.connect("tronos.db")
                    cursor = conexao.cursor()
                    cursor.execute("DELETE FROM camisas WHERE codigo = ?", (codigo,))
                    conexao.commit()
                    messagebox.showinfo('sucesso','camisa excluida')
                    limpar_campos()
                except Exception as e:
                    print(f'Erro: {str(e)}')
                finally:
                    conexao.close()
            else:
                messagebox.showerror('erro',  'preencha todos os campos')

        def ver_camisas():
            #janela_camisas.destroy()

            def sair():
                janela_estoque.destroy()
                
            janela_estoque = tk.Tk()
                
            def carregar_dados():
                treeview.delete(*treeview.get_children())
                conexao = sqlite3.connect("tronos.db")
                cursor = conexao.cursor()
                cursor.execute("SELECT codigo, nome, cor, tamanho, quantidade, preco FROM camisas")
                resultados = cursor.fetchall()
                for resultado in resultados:
                    treeview.insert(parent="", index="end", values=resultado)

                conexao.close()
            
            def inserir():
                quantidade = ent_quantidade.get()
                preco = ent_preco.get()
                codigo = ent_codigo.get()
                if quantidade and preco and codigo:
                    try:
                        conexao = sqlite3.connect("tronos.db")
                        cursor = conexao.cursor()
                        cursor.execute("UPDATE camisas SET quantidade = ?, preco = ? WHERE codigo = ?", (quantidade, preco, codigo))
                        conexao.commit()
                        messagebox.showinfo("sucesso", "valores alterados")

                    except:
                        messagebox.showerror('erro', 'erro ao inserir')
                        return
                    finally:
                        conexao.close()

                    carregar_dados()
                    ent_quantidade.delete(0, tk.END)
                    ent_preco.delete(0, tk.END)
                    ent_codigo.delete(0, tk.END)

                    
                else:
                    messagebox.showerror('erro', 'preencha todos os campos!')
                    return

                    
                    #ent_quantidade.focus()




            treeview = ttk.Treeview(janela_estoque)
            treeview["columns"] = ("codigo","nome", "cor", "tamanho", "quantidade", "preco")
            treeview.column("0", width=50)
            treeview.column("codigo", width=50)
            treeview.column("nome", width=100)
            treeview.column("cor", width=50)
            treeview.column("tamanho", width=100)
            treeview.column("quantidade", width=100)
            treeview.column("preco", width=100)
            treeview.heading("#0", text="")
            treeview.heading("codigo", text="id")
            treeview.heading("nome", text="nome")
            treeview.heading("cor", text='cor')
            treeview.heading("tamanho", text="tamanho")
            treeview.heading("quantidade", text="quantidade")
            treeview.heading("preco", text="preco")

            #adicionar itens no treeview
            carregar_dados()
            treeview.pack()
            janela_estoque.title('Estoque')
            janela_estoque.geometry("700x500+250+200")
            janela_estoque.resizable(width=1, height=1)

            frm_a = tk.LabelFrame(janela_estoque, text='Alterar Quantidade ou Preço')
            frm_a.pack(fill='both', expand='yes', padx=10, pady=10)

            lbl_quantidade = tk.Label(frm_a, text='quantidade')
            lbl_quantidade.pack(side='left')
            ent_quantidade = tk.Entry(frm_a)
            ent_quantidade.pack(side='left', padx=10)
            lbl_preco = tk.Label(frm_a, text='preco')
            lbl_preco.pack(side='left')
            ent_preco = tk.Entry(frm_a)
            ent_preco.pack(side='left', padx=10)
            lbl_codigo = tk.Label(frm_a, text="codigo")
            lbl_codigo.pack(side='left')
            ent_codigo = tk.Entry(frm_a)
            ent_codigo.pack(side='left', padx=10)
            btn_inserir = tk.Button(frm_a, text='inserir', command=inserir)
            btn_inserir.pack(side='left', padx=10)
            btn_voltar = tk.Button(janela_estoque, text='sair', command=sair)
            btn_voltar.pack(side='right', padx=10)


            """ txt = tk.Text(janela_estoque, font='Arial', width=500, height=300)
            txt.pack() 
 """

            """ conexao = sqlite3.connect("tronos.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM camisas")
            #rows = cursor.fetchall()

            
             for row in rows:
                txt.insert("end",f'Codigo: {row[0]}\nNome: {row[1]}\nCor: {row[2]}\nTamanho: {row[3]}\nQuantidade: {row[4]}\nPreco: R${row[5]}\n\n')
 
            conexao.close()
             """
            janela_estoque.mainloop()
        

            

        def alterar_camisa():
            
            nome_camisa = ent_nome_camisa.get()
            cor_camisa = ent_cor_camisa.get()
            tamanho_camisa = ent_tamanho_camisa.get()
            quantidade_camisa = ent_quantidade_camisa.get()
            preco_camisa = ent_preco_camisa.get()
            codigo = ent_cod_camisa.get()

            
            if nome_camisa and cor_camisa and tamanho_camisa and quantidade_camisa and preco_camisa and codigo:
                try:
                    conexao = sqlite3.connect("tronos.db")
                    cursor = conexao.cursor()
                    cursor.execute("UPDATE camisas SET nome = ?, cor = ?, tamanho = ?, quantidade = ?, preco = ? WHERE codigo = ?", (nome_camisa, cor_camisa, tamanho_camisa, quantidade_camisa, preco_camisa, codigo))
                    conexao.commit()
                    messagebox.showinfo('sucesso','camisa alterada')
                    limpar_campos()
                except Exception as e:
                    messagebox.showerror(f'Erro: {str(e)}')
                finally:
                    conexao.close()
            else: 
                messagebox.showerror("erro", "por favor preencha todos os campos")


        lbl_nome_camisa = tk.Label(janela_camisas, text='nome:')
        lbl_nome_camisa.pack(padx=10, pady=1)
        ent_nome_camisa = tk.Entry(janela_camisas)
        ent_nome_camisa.pack(padx=10, pady=1)

        lbl_cor_camisa = tk.Label(janela_camisas, text='cor:')
        lbl_cor_camisa.pack(padx=10, pady=1)
        ent_cor_camisa = tk.Entry(janela_camisas)
        ent_cor_camisa.pack(padx=10, pady=1)

        lbl_tamanho_camisa = tk.Label(janela_camisas, text='tamanho:')
        lbl_tamanho_camisa.pack(padx=10, pady=1)
        ent_tamanho_camisa = tk.Entry(janela_camisas)
        ent_tamanho_camisa.pack(padx=10, pady=1)
        
        lbl_quantidade_camisa = tk.Label(janela_camisas, text='quantidade:')
        lbl_quantidade_camisa.pack(padx=10, pady=1)
        ent_quantidade_camisa = tk.Entry(janela_camisas)
        ent_quantidade_camisa.pack(padx=10, pady=1)

        lbl_preco_camisa = tk.Label(janela_camisas, text='preco:')
        lbl_preco_camisa.pack(padx=10, pady=1)
        ent_preco_camisa = tk.Entry(janela_camisas)
        ent_preco_camisa.pack(padx=10, pady=1)

        btn_cadastrar_camisa = tk.Button(janela_camisas, text='Cadastrar Camisa',command=cadastrar_camisa)
        btn_cadastrar_camisa.pack(padx=10, pady=10)

        lbl_orientacao_1 = tk.Label(janela_camisas, text='*Informe o codigo da camisa e escolha a operação desejada!*')
        lbl_orientacao_1.pack(padx=10, pady=10)

        lbl_cod_camisa = tk.Label(janela_camisas, text='Codigo camisa:')
        lbl_cod_camisa.pack(padx=10, pady=1)
        ent_cod_camisa = tk.Entry(janela_camisas)
        ent_cod_camisa.pack(padx=10, pady=1)

        btn_excluir_camisa = tk.Button(janela_camisas, text='Excluir camisa', command=excluir_camisa)
        btn_excluir_camisa.pack(padx=10, pady=10)

        btn_alterar_camisa = tk.Button(janela_camisas, text='Alterar camisa', command=alterar_camisa)
        btn_alterar_camisa.pack(padx=10, pady=10)
        
        btn_ver_camisas = tk.Button(janela_camisas, text='Estoque', command=ver_camisas)
        btn_ver_camisas.pack(padx=10, pady=10)
        


        janela_camisas.mainloop()

    else:
        messagebox.showerror('acesso negado','usuário ou senha incorretos!')

def janela_cadastro_usuario():
    
    def voltar():
        janela_cd_usuario.destroy()
    
    def limpar_campos():
        ent_cpf.delete(0, tk.END)
        ent_nome.delete(0,tk.END)
        ent_senha.delete(0, tk.END)
        ent_telefone.delete(0, tk.END)
    
    def cadastrar_usuario():
        cpf = ent_cpf.get()
        nome = ent_nome.get()
        senha = ent_senha.get()
        telefone = ent_telefone.get()

        if cpf and nome and senha and telefone:

            try:
                conexao = sqlite3.connect("tronos.db")
                cursor = conexao.cursor()
                cursor.execute("INSERT INTO usuarios (cpf, nome, senha, telefone) VALUES (?, ?, ?, ?)", (cpf, nome, senha, telefone))
                conexao.commit()
                limpar_campos()
                messagebox.showinfo('sucesso', 'usuario cadastrado')

            except Exception as e:
                    messagebox.showerror(f'Erro: {str(e)}')
            finally:
                    conexao.close()
        else:
                messagebox.showerror('erro', 'por favor, preencha todos os campos')

    
    
        
    janela_cd_usuario = tk.Tk()
    janela_cd_usuario.title('Cadastrar Usuario')
    janela_cd_usuario.geometry('500x300')

    lbl_cpf = tk.Label(janela_cd_usuario, text='CPF')
    lbl_cpf.pack(padx=10, pady=0)
    ent_cpf = tk.Entry(janela_cd_usuario)
    ent_cpf.pack(padx=10, pady=0)

    lbl_nome = tk.Label(janela_cd_usuario, text='Usuário')
    lbl_nome.pack(padx=10, pady=0)
    ent_nome = tk.Entry(janela_cd_usuario)
    ent_nome.pack(padx=10, pady=0)

    lbl_senha = tk.Label(janela_cd_usuario, text='Senha\n*apenas numeros*')
    lbl_senha.pack(padx=10, pady=0)
    ent_senha = tk.Entry(janela_cd_usuario, show='*', )
    ent_senha.pack(padx=10, pady=0)

    lbl_telefone = tk.Label(janela_cd_usuario, text='Telefone')
    lbl_telefone.pack(padx=10, pady=0)
    ent_telefone = tk.Entry(janela_cd_usuario)
    ent_telefone.pack(padx=10, pady=0)

    btn_cadastrar_usuario = tk.Button(janela_cd_usuario, text='Cadastrar', command=cadastrar_usuario)
    btn_cadastrar_usuario.pack(padx=10, pady=10)

    btn_voltar = tk.Button(janela_cd_usuario, text='Voltar', command=voltar)
    btn_voltar.pack(padx=10, pady=10)
    

    janela_cd_usuario.mainloop()
    

    



lbl_bv = tk.Label(janela,text= 'Mr. Tronos')
lbl_bv.pack(padx=10, pady=20)



lbl_usuario = tk.Label(janela, text='Usuário:')
lbl_usuario.pack()
ent_usuario = tk.Entry(janela)
ent_usuario.pack(padx=10,pady=1)

lbl_senha = tk.Label(janela, text='Senha:')
lbl_senha.pack()
ent_senha = tk.Entry(janela, show='*')
ent_senha.pack(padx=10, pady=1)

btn_login = tk.Button(janela, text='Login', command=fazer_login)
btn_login.pack(padx=10, pady=10)

btn_janela_usuario = tk.Button(janela, text='Cadastrar Usuário', command=janela_cadastro_usuario)
btn_janela_usuario.pack(padx=10, pady=10)


criar_banco_usuarios()
criar_banco_camisas()

janela.mainloop()
