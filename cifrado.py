import math
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tabulate import tabulate
import numpy as np
import random
from tkinter import messagebox as MessageBox

class Programa:
    
    caracteresAscii = []
    codigoCaracteres = []
    mensajeEncriptado = []
    mensajeDesencriptado = []
    clave = []
    claveCodigo = []

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Programa de cifrado")        
        self.miFrame=Frame(self.root, width=1000, height=650)
        self.miFrame.pack()

        self.lblCaracteres=Label(self.miFrame, text="Caracteres aceptados: ", font=18)
        self.lblCaracteres.grid(row=1, column=0, padx=5, pady=5)
        self.txtCaracteres = ScrolledText(self.miFrame,width=25, height=35, wrap=WORD)
        self.txtCaracteres.grid(row=2, column=0, rowspan=3, padx=10, pady=10)
        
        self.lblTexto=Label(self.miFrame, text="Texto a analizar: ", font=18)
        self.lblTexto.grid(row=1, column=1, padx=5, pady=5)
        self.txtContenido = ScrolledText(self.miFrame,width=60, height=15, wrap=WORD)
        self.txtContenido.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        self.lblEncriptado=Label(self.miFrame, text="Texto encriptado: ", font=18)
        self.lblEncriptado.grid(row=3, column=1, padx=5, pady=5)
        self.txtEncriptado = ScrolledText(self.miFrame,width=60, height=15, wrap=WORD)
        self.txtEncriptado.grid(row=4, column=1,columnspan=4, padx=10, pady=10)

        self.lblClave=Label(self.miFrame, text="Clave: ", font=18)
        self.lblClave.grid(row=1, column=5, padx=5, pady=5)
        self.txtClave = ScrolledText(self.miFrame,width=60, height=15, wrap=WORD)
        self.txtClave.grid(row=2, column=5,columnspan=4, padx=10, pady=10)

        self.lblDesencriptado=Label(self.miFrame, text="Texto desencriptado: ", font=18)
        self.lblDesencriptado.grid(row=3, column=5, padx=5, pady=5)
        self.txtDesencriptado = ScrolledText(self.miFrame,width=60, height=15, wrap=WORD)
        self.txtDesencriptado.grid(row=4, column=5,columnspan=4, padx=10, pady=10)

        
        #----------------Botón Seleccionar archivo
        botonArchivo=Button(self.miFrame, text="Seleccionar archivo", command=self.seleccionarArchivo)
        botonArchivo.grid(row=0, column=1, padx=10, pady=10)
        #----------------Botón Analizar------------------------
        botonAnalizar=Button(self.miFrame, text="Encriptar", command=self.encriptar)
        botonAnalizar.grid(row=0, column=2, padx=10, pady=10)
        #---------------Botón Limpiar texto-------------------------
        botonLimpiar=Button(self.miFrame, text="Limpiar", command=self.limpiar)
        botonLimpiar.grid(row=0, column=3, padx=10, pady=10)
        #---------------ComboBoxCifrado----------------------
        self.lblDesencriptado=Label(self.miFrame, text="Tipo de cifrado: ", font=18)
        self.lblDesencriptado.grid(row=0, column=5, padx=5, pady=5)
        self.comboBox = Combobox(self.miFrame, state="readonly", values=["Clave unica", "Clave aleatoria"])
        self.comboBox.grid(row=0, column=6, padx=5, pady=5)

        self.obtenerAscii()
        self.root.mainloop()
        
    #--------------------------Obtener los caracteres permitidos por medio de Ascii-----------
    def obtenerAscii(self):
        #Añadir el salto de linea
        self.caracteresAscii.append(chr(10))
        self.codigoCaracteres.append(0)
        
        j=1
        for i in range(32,127):
            self.caracteresAscii.append(chr(i))
            self.codigoCaracteres.append(j)
            j+=1
        
        tablaDatos = [ [0 for columna in range(2)] for fila in range (len(self.caracteresAscii))]
        for i in range(len(self.caracteresAscii)):
            tablaDatos[i][0] = self.caracteresAscii[i]
            tablaDatos[i][1] = self.codigoCaracteres[i]

        self.txtCaracteres.insert("1.0", tabulate(tablaDatos, headers=["Caracter","Codigo"], tablefmt="pretty"))

    #-----------------------Encontrar el código de un caracter----------
    def encontrarCodigo(self, caracter):
        j = 0
        codigo = ""

        for i in self.caracteresAscii:
            if i == caracter:
                codigo = self.codigoCaracteres[j]
                break
            j+=1
        
        return codigo

    #-----------------------Encontrar el caracter de un codigo----------
    def encontrarCaracter(self, codigo):
        j = 0
        caracter = ""

        for i in self.codigoCaracteres:
            if i == codigo:
                caracter = self.caracteresAscii[j]
                break
            j+=1
        
        return caracter

    #---------------------Función para obtener los caracteres del texto
    def obtenerCaracteres(self):
        texto = self.txtContenido.get("1.0", "end-1c")
        caracteresCo = []
        caracteres = []
        
        for i in texto:
            for j in self.caracteresAscii:
                if  i == j:
                    caracteres.append(j)
                    caracteresCo.append(self.encontrarCodigo(j))
        
        self.generarClave(texto)
        return caracteres, caracteresCo

    #------------------Generar clave--------------------------
    def generarClave(self, texto):

        condicion = self.comboBox.get()
        if condicion == "Clave unica":
            caracter = self.txtClave.get("1.0", "end-1c")
            if caracter:
                for i in range(len(texto)):
                    self.clave.append(caracter)
                    self.claveCodigo.append(self.encontrarCodigo(caracter))
            else:
                MessageBox.showwarning("Alerta", "Escribir la clave unica")
                self.limpiar()

        elif condicion == "Clave aleatoria":
            for i in range(len(texto)):
                caracter = random.choice(self.caracteresAscii)
                self.clave.append(caracter)
                self.claveCodigo.append(self.encontrarCodigo(caracter))
        else:
            MessageBox.showwarning("Alerta", "Selecciona el tipo de cifrado")
            self.limpiar()

        self.txtClave.insert("1.0", "".join(map(str, self.clave)))

    #------------Función para encriptar texto---------------------
    def encriptar(self):
        caracteres, caracteresCo= self.obtenerCaracteres()
        mensajeEncriptadoCodigo = []
        
        for i in range(len(caracteresCo)):
            suma = (caracteresCo[i] + self.claveCodigo[i])%(len(self.caracteresAscii)+1)
            self.mensajeEncriptado.append(self.encontrarCaracter(suma))
            mensajeEncriptadoCodigo.append(suma)
        self.txtEncriptado.insert("1.0", "".join(map(str, self.mensajeEncriptado)))

        self.desencriptar(mensajeEncriptadoCodigo)

    #--------------Función para desencriptar------------------------
    def desencriptar(self, mensajeCodigo):

        for i in range(len(mensajeCodigo)):
            suma = (mensajeCodigo[i] - self.claveCodigo[i])%(len(self.caracteresAscii)+1)
            self.mensajeDesencriptado.append(self.encontrarCaracter(suma))
        self.txtDesencriptado.insert("1.0", "".join(map(str, self.mensajeDesencriptado)))
        

    #-------------Función para abrir un archivo-------------------
    def seleccionarArchivo(self):
        archivo = askopenfile(mode='r', filetypes=[('Archivo de texto', '*.txt')])
        
        if archivo is not None:
            contenido = archivo.read()
            self.txtContenido.insert("1.0", contenido)

    #-------------Función para limpiar los datos------------------
    def limpiar(self):
        self.txtContenido.delete("1.0","end")
        self.txtEncriptado.delete("1.0", "end")
        self.txtDesencriptado.delete("1.0", "end")
        self.txtClave.delete("1.0", "end")
        self.mensajeEncriptado.clear()
        self.mensajeDesencriptado.clear()
        self.clave.clear()
        self.claveCodigo.clear()

programa = Programa()