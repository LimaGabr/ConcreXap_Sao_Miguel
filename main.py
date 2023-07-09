from tkinter import *
from tkinter import ttk
import pandas as pd
import mysql.connector
import pdfkit
import os
import webbrowser
from pandas import DataFrame
from datetime import datetime as dt
from tkcalendar import Calendar, DateEntry
import tkcalendar
from tkinter import messagebox
import matplotlib.pyplot as plt
import plotly

class Funcs():

    def graficoCimento(self):
        self.conn = mysql.connector.connect(
            host="",
            user="root",
            passwd="",
            database='relatorio'
        )
        self.cursor = self.conn.cursor();
        print("conectando ao banco de dados")
        self.query = (""" SELECT * FROM producao ORDER BY dat ASC
                                                """)
        self.df_mysql = pd.read_sql(self.query, self.conn)
        self.df_mysql.rename(columns={'temp': 'Kg'}, inplace=True)
        pd.options.plotting.backend = 'plotly'
        self.xgrafico = self.dataInicio_entry.get()
        self.ygrafico = self.resultado2
        grafico = self.df_mysql[self.df_mysql['dat'].between(self.xgrafico, self.ygrafico)]
        
        self.grafico = grafico.plot(kind='bar', y='Kg', color = 'dat', text_auto='.4s', title="Gráfico de Cimento")
        self.grafico.show()

    def graficoAgregado(self):
        self.conn = mysql.connector.connect(
            host="",
            user="root",
            passwd="",
            database='relatorio'
        )
        self.cursor = self.conn.cursor();
        print("conectando ao banco de dados")
        self.query = (""" SELECT * FROM producao ORDER BY dat ASC
                                                """)
        self.df_mysql = pd.read_sql(self.query, self.conn)
        self.df_mysql.rename(columns={'dia': 'Kg'}, inplace=True)
        pd.options.plotting.backend = 'plotly'
        self.xgrafico = self.dataInicio_entry.get()
        self.ygrafico = self.resultado2
        grafico = self.df_mysql[self.df_mysql['dat'].between(self.xgrafico, self.ygrafico)]
        self.grafico = grafico.plot(kind='bar', y='Kg', color = 'dat', text_auto='.4s', title="Gráfico de Agregado")
        self.grafico.show()

    def printCliente(self):
        webbrowser.open_new("index.html")

    def gerar(self):
        self.conn = mysql.connector.connect(
            host="",
            user="root",
            passwd="",
            database='relatorio'
        )
        self.cursor = self.conn.cursor();
        print("conectando ao banco de dados")
        self.query = (""" SELECT * FROM producao ORDER BY dat ASC
                                       """)
        self.x = self.dataInicio_entry.get()
        self.y = self.resultado2
        self.df_mysql = pd.read_sql(self.query, self.conn)
        self.df_mysql.rename(columns={'temp': 'Cimento', 'dia': 'Agragado'}, inplace=True)
        self.top5 = self.df_mysql[self.df_mysql['dat'].between(self.x,self.y)]
        self.df_mysql.to_html('C:\\Users\\g_lim\\PycharmProjects\\pythonPrograma\\venv\\index.html')
        pd.set_option('display.colheader_justify', 'center')
        html_string = '''
                       <html>
                         <head><title>HTML Pandas Dataframe with CSS</title></head>
                         <link rel="stylesheet" type="text/css" href="df_style.css"/>
                         <body>

                           <img id="all" src="concrexap.png" alt="some text" width=300 height=150>
                           {table}

                         </body>
                       </html>.
                       '''
        with open('index.html', 'w') as f:
            f.write(html_string.format(table=self.top5.to_html(classes='mystyle')))
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '2.75in',
        }
        self.config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_file("index.html", "out.pdf", configuration=self.config, options=options)
        self.printCliente()

    def conecta_db(self):
        self.conn = mysql.connector.connect(
            host="",
            user="root",
            passwd="",
            database='relatorio'
        )
        self.cursor = self.conn.cursor();
        print("conectando ao banco de dados")
        self.query = (""" SELECT * FROM producao ORDER BY codigo ASC
                        """)
        self.df_mysql = pd.read_sql(self.query, self.conn)
        print(self.df_mysql)

    def desconecta_db(self):
        self.conn.close();
        print("desconectando ao banco de dados")

    def update(self, lista):
        self.listaCli.delete(*self.listaCli.get_children())
        for i in self.lista:
            self.listaCli.insert('', END, values=i)

    def limpa_tela(self):
        self.dataInicio_entry.delete(0, END)
        self.data_entry.delete(0, END)

    def select_lista(self):
        self.conecta_db()
        self.query = (""" SELECT * FROM producao ORDER BY codigo ASC
                """)
        self.cursor.execute(self.query)
        self.lista = self.cursor.fetchall()
        self.update(self.lista)

    def busca_mes(self):
        self.conecta_db()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome = self.dataInicio_entry.get()
        self.final = self.data_entry.get()
        self.dia1 = self.nome[0:2]
        self.mes1 = self.nome[3:5]
        self.ano1 = self.nome[6:10]
        self.resultado = self.ano1+"-"+self.mes1+"-"+self.dia1
        self.testdia = self.final.split("/",1)
        self.diatest = int(self.testdia[0])
        self.diaFinal = self.diatest + 1
        self.dia2 = str(self.diaFinal)
        self.mes2 = self.final[3:5]
        self.ano2 = self.final[6:10]
        self.resultado2 = self.dia2 + "/" + self.mes2 + "/" + self.ano2
        print(self.nome, self.final)
        print(self.resultado2)
        self.data = (self.nome, self.resultado2)
        self.cursor.execute(
            """ SELECT * FROM producao
            WHERE dat between (%s) and (%s) ORDER BY dat ASC  """, self.data)

        self.buscaDatainicial = self.cursor.fetchall()
        for i in self.buscaDatainicial:
            self.listaCli.insert("", END, values=i)

        self.resultadot = (self.buscaDatainicial)
        print(self.resultadot)

    def calendario(self):
        self.imgokdata = PhotoImage(file="okdata.png")
        self.calendario1 = Calendar(self.frame_1, fg="gray75", bg="blue", font=("Verdana", "8"), locale='pt_br')
        self.calendario1.place(relx=0.65, rely=0.0001)
        self.calData = Button(self.frame_1, image=self.imgokdata, command= self.print_cal )
        self.calData.place(relx=0.77, rely=0.85, relheight=0.17, relwidth = 0.08)

    def print_cal(self):
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.dataInicio_entry.delete(0, END)
        self.dataInicio_entry.insert(END, dataIni)
        self.calData.destroy()

    def calendario2(self):
        self.imgokdata2 = PhotoImage(file="okdata.png")
        self.calendario2 = Calendar(self.frame_1, fg="gray75", bg="blue", font=("Verdana", "8"), locale='pt_br')
        self.calendario2.place(relx=0.65, rely=0.0001)
        self.calData2 = Button(self.frame_1, image=self.imgokdata2, command= self.print_cal2 )
        self.calData2.place(relx=0.77, rely=0.85, relheight=0.17, relwidth = 0.08)

    def print_cal2(self):
        dataIni2 = self.calendario2.get_date()
        self.calendario2.destroy()
        self.data_entry.delete(0, END)
        self.data_entry.insert(END, dataIni2)
        self.calData2.destroy()

class Application(Funcs):
    def __init__(self):
        self.root = Tk()
        self.root.title("Relatórios ConcreXap")
        self.root.configure(background='#B0E0E6')
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.maxsize(width=1200, height=1000)
        self.root.minsize(width=400, height=300)
        self.root.focus_force()
        self.tela()
        self.root.mainloop()

    def tela(self):
        self.frames_de_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.select_lista()


    def frames_de_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#F0F8FF', highlightbackground='#C0C0C0', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.365)
        self.frame_2 = Frame(self.root, bd=4, bg='#F0F8FF', highlightbackground='#C0C0C0', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.4, relwidth=0.96, relheight=0.55)

    def widgets_frame1(self):
        self.lb_pesquisa = Label(self.frame_1, text="Pesquisa", bg='#F0F8FF', fg='silver',font=('verdana', 8, 'bold'))
        self.lb_pesquisa.place(relx=0.20, rely=0.24)
        self.imgbotao=PhotoImage (file="variante.png")
        self.lb_dataInicio = Button(self.frame_1,image=self.imgbotao,bg= 'silver', height=16, width=28, command= self.calendario)
        self.lb_dataInicio.place(relx=0.12, rely=0.40)
        self.dataInicio_entry = Entry(self.frame_1)
        self.dataInicio_entry.place(relx=0.18, rely=0.41, relwidth=0.15)
        self.lb_dataFinal = Button(self.frame_1, image=self.imgbotao, bg= 'silver',height=16, width=28, command= self.calendario2)
        self.lb_dataFinal.place(relx=0.12, rely=0.51)
        self.data_entry = Entry(self.frame_1)
        self.data_entry.place(relx=0.18, rely=0.52, relwidth=0.15)
        self.imglogo = PhotoImage(file="logoconcrexap.png")
        self.l_rodape = Label(self.frame_1, image=self.imglogo)
        self.l_rodape.place(relx=0.73, rely=0.000)
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.busca_mes)
        self.bt_buscar.place(relx=0.10, rely=0.70, relwidth=0.11, relheight=0.10)
        self.bt_imprimir = Button(self.frame_1, text="Imprimir", bd=2, bg='#107db2', fg='white',
                                  font=('verdana', 8, 'bold'), command=self.gerar)
        self.bt_imprimir.place(relx=0.25, rely=0.70, relwidth=0.11, relheight=0.10)
        self.bt_grafico = Button(self.frame_2, text="Cimento", bd=2, bg='#107db2', fg='white',
                                  font=('verdana', 8, 'bold'), command=self.graficoCimento)
        self.bt_grafico.place(relx=0.80, rely=0.55, relwidth=0.165, relheight=0.10)
        self.bt_grafico2 = Button(self.frame_2, text="Agregado", bd=2, bg='#107db2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.graficoAgregado)
        self.bt_grafico2.place(relx=0.80, rely=0.67, relwidth=0.165, relheight=0.10)
        self.imggrafico = PhotoImage(file="grafico4.png")
        self.l_rodape = Label(self.frame_2, image=self.imggrafico)
        self.l_rodape.place(relx=0.795, rely=0.08)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Cimento")
        self.listaCli.heading("#3", text="Agregado")
        self.listaCli.heading("#4", text="Data/Hora")
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=25)
        self.listaCli.column("#2", width=50)
        self.listaCli.column("#3", width=50)
        self.listaCli.column("#4", width=100)
        self.listaCli.place(relx=0.01, rely=0.01, relwidth=0.75, relheight=0.98)
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.735, rely=0.025, relwidth=0.02, relheight=0.95)

Application()
