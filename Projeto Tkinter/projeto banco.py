from tkinter import *
import tkinter.messagebox 
import pyodbc
import re
from unidecode import unidecode

dados_conexao = ("Driver={SQL Server};"
                 "Server=DESKTOP-AUUUK20;"
                 "Database=tkinter")
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

# Procurar Insumo 
def btn_clicked0():
    nome_insumo = unidecode(entry1.get()).lower()
    comando = f"""SELECT * FROM Insumos WHERE nome_insumo = '{nome_insumo}'"""
    cursor.execute(comando)
    consulta = cursor.fetchall()
    if consulta:
        texto = ''
        for item in consulta:
            texto+= f'Nome Insumo: {item.nome_insumo}\n ID:{item.id_insumo} \n Validade: {item.data_validade} \n Lote: {item.lote} \n Quantidade: {item.qtde}\n\n'
        entry0.delete('1.0', END)
        entry0.insert('1.0', texto)
    else:
        tkinter.messagebox.showwarning('Procurar Insumo', 'Produto não encontrado')
    print("Button Clicked 0")

# Deletar Insumo
def btn_clicked1():
    nome_insumo = unidecode(entry1.get()).lower()
    lote_insumo = entry3.get()
    if nome_insumo and lote_insumo:
        comando = f""" SELECT * FROM Insumos WHERE nome_insumo = '{nome_insumo}' AND lote = '{lote_insumo}' """
        cursor.execute(comando)
        consulta = cursor.fetchall()
        if consulta:
            continuar = tkinter.messagebox.askyesno('Deletar Insumo', 'Tem certeza?')
            if continuar:
                comando = f""" DELETE FROM Insumos WHERE nome_insumo = '{nome_insumo}' AND lote = '{lote_insumo}' """
                cursor.execute(comando)
                cursor.commit()
                tkinter.messagebox.showinfo('Deletar Insumo', f'{nome_insumo} foi deletado')
                del_all()
            else:
                tkinter.messagebox.showwarning('Deletar Insumo', 'Solitação Cancelada')
        else:
            tkinter.messagebox.showerror('Deletar Insumo', f'{nome_insumo} não encontrado no lote {lote_insumo}')
    else:
        tkinter.messagebox.showerror('Deletar Insumo', 'Preenchar os campos')
    print("Button Clicked 1")

# Registrar Insumo
def btn_clicked2():
    nome_insumo = unidecode(entry1.get()).lower()
    lote_insumo = entry3.get()
    qtde_insumo = entry4.get()

    if nome_insumo and lote_insumo and qtde_insumo:
        comando = f""" SELECT * FROM Insumos WHERE nome_insumo = '{nome_insumo}' AND lote = '{lote_insumo}'"""
        cursor.execute(comando)
        consulta = cursor.fetchall()
        if consulta:
            if float(consulta[0].qtde) < float(qtde_insumo):
                tkinter.messagebox.showerror('Registrar Insumo', f'Quantidade Invalida. Temos apenas {consulta[0].qtde} no lote {lote_insumo}')
            else:
                comando = f"""UPDATE Insumos SET qtde = qtde-'{qtde_insumo}' WHERE nome_insumo = '{nome_insumo}' AND lote = '{lote_insumo}'"""
                cursor.execute(comando)
                cursor.commit()
                tkinter.messagebox.showinfo('Registrar Insumo', 'Registro feito com sucesso')
                del_all()
        else:
            tkinter.messagebox.showerror('Registrar Insumo', f'{nome_insumo} não encontrado no lote {lote_insumo}')
    else:
        tkinter.messagebox.showerror('Registrar Insumo', 'Preencha os campos')
    print("Button Clicked 2")

# Adicionar Insumo
def btn_clicked3():
    nome_insumo = unidecode(entry1.get()).lower()
    data_insumo = entry2.get()
    lote_insumo = entry3.get()
    qtde_insumo = entry4.get()

    if nome_insumo and data_insumo and lote_insumo and qtde_insumo:
        padrao = re.compile(r'\d+/\d+/\d\d\d\d')
        resultado = re.findall(padrao, data_insumo)

        comando = f"""SELECT * FROM Insumos
            WHERE nome_insumo = '{nome_insumo}' AND lote = '{lote_insumo}';
            """
        cursor.execute(comando)
        consulta = cursor.fetchall()

        if not resultado:
            tkinter.messagebox.showerror('Erro Adicionar Insumos', message='Data Invalida. Adicione no padrão: dd/mm/aaa')
        elif consulta:
            continuar = tkinter.messagebox.askyesno('Adicionar Insumos', message=f'Já existe um insumo registrado com o nome "{nome_insumo}" no lote {lote_insumo}. Deseja acrescentar nele?')
            if continuar:
                comando = f"""UPDATE Insumos
                    SET qtde = qtde + {qtde_insumo}
                    WHERE nome_insumo = '{nome_insumo}';
                    """
                cursor.execute(comando)
                cursor.commit()
                tkinter.messagebox.showinfo('Adicionar Insumos', message='Inclusão realizada com sucesso')
                del_all()
        else:
            comando = f"""INSERT INTO Insumos(nome_insumo, data_validade, lote, qtde) VALUES ('{nome_insumo}', '{data_insumo}', '{lote_insumo}', '{qtde_insumo}')"""
            cursor.execute(comando)
            cursor.commit()
            tkinter.messagebox.showinfo('Adicionar Insumos', message=f'{nome_insumo} adicionado ao lote {lote_insumo}')
            del_all()
    else:
        tkinter.messagebox.showerror('Erro Adicionar Insumos', message='Preencha todos os campos')

    print("Button Clicked 3")
    # print(entry1.get()) -> Nome Insumo
    # print(entry2.get()) -> Data Validade
    # print(entry3.get()) -> Lote
    # print(entry4.get()) -> Quantidade

def del_all():
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)

window = Tk()

window.geometry("711x646")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 646,
    width = 711,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"images/background.png")
background = canvas.create_image(
    355.5, 323.0,
    image=background_img)

img0 = PhotoImage(file = f"images/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked0,
    relief = "flat")

b0.place(
    x = 479, y = 195,
    width = 178,
    height = 38)

img1 = PhotoImage(file = f"images/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked1,
    relief = "flat")

b1.place(
    x = 247, y = 197,
    width = 178,
    height = 36)

img2 = PhotoImage(file = f"images/img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked2,
    relief = "flat")

b2.place(
    x = 479, y = 123,
    width = 178,
    height = 35)

img3 = PhotoImage(file = f"images/img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked3,
    relief = "flat")

b3.place(
    x = 247, y = 125,
    width = 178,
    height = 34)

entry0_img = PhotoImage(file = f"images/img_textBox0.png")
entry0_bg = canvas.create_image(
    455.0, 560.0,
    image = entry0_img)

entry0 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 250, y = 502,
    width = 410,
    height = 114)

entry1_img = PhotoImage(file = f"images/img_textBox1.png")
entry1_bg = canvas.create_image(
    517.0, 294.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 377, y = 278,
    width = 280,
    height = 31)

entry2_img = PhotoImage(file = f"images/img_textBox2.png")
entry2_bg = canvas.create_image(
    517.0, 340.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry2.place(
    x = 377, y = 324,
    width = 280,
    height = 31)

entry3_img = PhotoImage(file = f"images/img_textBox3.png")
entry3_bg = canvas.create_image(
    517.0, 388.5,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry3.place(
    x = 377, y = 372,
    width = 280,
    height = 31)

entry4_img = PhotoImage(file = f"images/img_textBox4.png")
entry4_bg = canvas.create_image(
    517.0, 436.5,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry4.place(
    x = 377, y = 420,
    width = 280,
    height = 31)

window.resizable(False, False)
window.mainloop()
