from tkinter import*
from tkinter import ttk
import tkinter as tk 
from Reconocimiento import main

#logo
from PIL import Image, ImageTk  

print("Librerias leidas")

#-------------------------------------------
#            FUNCIONES
#-------------------------------------------

class Login(ttk.Frame):
    """Pestaña 1, Login"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        # Variables Login
        self.registroUser = ('login1','David','login2')
        self.registroPass = ('david')
        # Funciones
        self.widgets()
        self.crear_cuadro()
    
    def crear_cuadro(self):
        self.canvas1 = Canvas(self.master, height=170, width=170)
        self.canvas1.grid(row=0, column=1, sticky="NW", padx=350, pady=50)

        self.IconoImagen0 = Image.open('Img/login.png')
        self.IconoImagen0 = self.IconoImagen0.resize((160, 160), Image.ANTIALIAS)
        self.IconoImagen0 = ImageTk.PhotoImage(self.IconoImagen0)     
        self.canvas1.create_image(5, 5, anchor=NW, image=self.IconoImagen0)

    def widgets(self):
        self.Usuario = tk.StringVar()
        self.Password = tk.StringVar()  

        self.label1 = ttk.Label(self.master, text="Usuario:").grid(row=0, column=1, sticky='NW', padx=300, pady=240)
        self.textbox1 = ttk.Entry(self.master, textvariable=self.Usuario).grid(row=0, column=1, sticky='NW', padx=380, pady=240)

        self.label2 = ttk.Label(self.master, text="Password:").grid(row=0, column=1, sticky='NW', padx=300, pady=280)
        self.textbox2 = ttk.Entry(self.master, show='*', textvariable=self.Password).grid(row=0, column=1, sticky='NW', padx=380, pady=280)

        #----------Buttons
        self.button1 = ttk.Button(self.master, text="Ingresar", cursor="hand2", command=self.ValidarLogin).grid(row=0, column=1, sticky='NW', padx=400, pady=320) 

    def Registro(self,  Usuario_input, Password_input):
        if self.Usuario_input in self.registroUser:
            if self.Password_input in self.registroPass:
                return 1
            else:
                self.mensaje = Label(self.master, text="Usuario o contraseña  invalido").grid(row=0, column=1, sticky='NW', padx=360, pady=350)
                #print("\n\tLas contraseñas no coinciden...\n")
        else:
            return 2

    def ValidarLogin(self):

        #----------Extraccion
        self.Usuario_input = self.Usuario.get()
        self.Password_input = self.Password.get()

        if self.Registro(self.Usuario_input , self.Password_input)==1:
            self.progreso()
            #print('Bienvenido',self.Usuario_input)
            #self.mensaje = Label(self.master, text="Bienvenido").grid(row=0, column=1, sticky='NW', padx=400, pady=380)
            self.master.destroy()
            main()
        else:
            #self.mensaje = Label(self.master, text="Usuario no registrado").grid(row=0, column=1, sticky='NW', padx=400, pady=353)
            return 1

    def progreso(self):

        self.i = 0
        self.progressbar = ttk.Progressbar(self.master, orient=HORIZONTAL, length=200, mode='determinate')
        self.progressbar.grid(row=0, column=1, sticky="NW", padx=350, pady=380)
        
        while(self.progressbar["value"] < self.progressbar["maximum"]):
            self.progressbar.update()
            self.progressbar["value"] = self.i**2
            self.i += 0.01
    
        self.progressbar.destroy()

#-------------------------------------------
#            INTERFAZ
#-------------------------------------------
def main1():

    ventana = Tk()
    ventana.title('Reconocimiento biometrico')
    ventana.resizable(0,0) #Tamaño estatico
    ventana.iconbitmap("img/logo3.ico")
    ventana.geometry("900x610")

    #Preparando notebook (tabs)
    notebook = Login(ventana)

    #Main loop
    notebook.mainloop()

if __name__ == '__main__':
    main1()