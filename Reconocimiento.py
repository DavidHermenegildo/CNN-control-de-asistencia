from tkinter import*
from tkinter import ttk
import tkinter as tk 

#webcam
import cv2
from PIL import Image, ImageTk
#acceso
import os
#capturar
import time
import PIL.Image, PIL.ImageTk
#mensajebox
from tkinter import messagebox

from keras.saving.saving_utils import model_call_inputs

from Entrenamiento import Entrenamiento
from threading import Thread

#Entrenamiento
from keras.models import load_model
from scipy.ndimage.measurements import label
import numpy as np
#Reconocimeinto
import datetime
import pandas as pd
import csv

print("Librerias leidas")

#-------------------------------------------
#            FUNCIONES
#-------------------------------------------

class RegistrarRostro(ttk.Frame):
    """Pestaña 1, Capturar rostros y entrenar"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        #-------Detector facial OpenCV
        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    #-------Funciones
        self.Crear_Widgets()
        self.crear_cuadro()
        #self.Iniciar()

    def crear_cuadro(self):
        self.canvas = Canvas(self, height=500, width=620)
        self.canvas.grid(column=0, row=0, sticky='NW', padx=0, pady=40)
        self.canvas.create_rectangle(20, 20, 620, 500, fill="white", outline="gainsboro")
        
        self.canvas1 = Canvas(self, height=155, width=155)
        self.canvas1.grid(row=0, column=1, sticky="NW", padx=60, pady=250)       
        self.canvas1.create_rectangle(5, 5, 150, 150, fill="white", outline="gainsboro")


    def Crear_Widgets(self):
        #----------text variables
        self.Codigo = tk.StringVar()
        self.Nombre = tk.StringVar()    
        self.Apellidos = tk.StringVar()
        self.Edad = tk.StringVar()

        #----------Buttons
        self.button1 = ttk.Button(self, text="Prender", cursor="hand2", command=self.prender).grid(row=0, column=0, sticky='NW', padx=20, pady=10) 
        self.button2 = ttk.Button(self, text="Apagar", cursor="hand2", command=self.apagar_webcam).grid(row=0, column=0, sticky="NW", padx=120, pady=10)
        self.button3 = ttk.Button(self, text="Enviar", cursor="hand2", command=self.crear_capeta).grid(row=0, column=1, sticky="NW", padx=150, pady=170)
        self.button4 = ttk.Button(self, text="Capturar", cursor="hand2", command=self.capturar_rostro).grid(row=0, column=1, sticky="NW", padx=60, pady=450)
        self.button5 = ttk.Button(self, text="Guardar", cursor="hand2", command=self.guardar).grid(row=0, column=1, sticky="NW", padx=150, pady=450)
        self.button6 = ttk.Button(self, text="Entrenar", cursor="hand2", command=self.entrenarImg).grid(row=0, column=0, sticky="NW", padx=20, pady=570)
        #----------Label
        self.label1 = ttk.Label(self, text="Nombre:").grid(row=0, column=1, sticky='NW', padx=20, pady=90)
        self.label3 = ttk.Label(self, text="Código:").grid(row=0, column=1, sticky='NW', padx=20, pady=120)

        #capturar
        self.mensaje1 = ttk.Label(self, text="Imagen:").grid(row=0, column=1, sticky='NW', padx=100, pady=230)
        self.label2 = ttk.Label(self, text="Obtenga entre 0-200 imágenes").grid(row=0, column=1, sticky='NW', padx=60, pady=410)
        
        #----------Text boxes
        self.textbox3 = ttk.Entry(self, textvariable=self.Nombre).grid(row=0, column=1, sticky='NW', padx=100, pady=90)
        self.textbox4 = ttk.Entry(self, textvariable=self.Codigo).grid(row=0, column=1, sticky='NW', padx=100, pady=120)
    
    def prender(self):
        #video capture
        self.cap = None
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.webcamtk()

    def webcamtk(self):
        if self.cap is not None:
            ret, self.frame = self.cap.read()
            if ret == True:
                self.frame = cv2.flip(self.frame, 1)
                self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                
                #self.Reco_Facial(self.image)
                self.deteccion_facial(self.image)

                self.image = Image.fromarray(self.image)
                self.image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(20, 20, anchor=tk.NW, image=self.image)
                
                self.master.after(10, self.webcamtk)
            else:
                #self.master.image = ""
                self.cap.release()
    
    def deteccion_facial(self, img):
        self.faces = self.faceClassif.detectMultiScale(img, 1.2, 5)

        for(x, y, w, h) in self.faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img = cv2.putText(img,'PRESIONE CAPTURAR',(10,20), 2, 0.5,(0, 255, 0),1,cv2.LINE_AA)
    
    def crear_capeta(self):
        global ruta, id_nombre, progressbar
        self.count = 0
        messagebox.showinfo(message="Datos registrados correctamente", title="Título")

        if not os.path.exists('Data/'):
            os.makedirs('Data/')
        
        #----------Buttons
        #self.button4 = ttk.Button(self, text="Capturar", cursor="hand2", command=self.capturar_rostro).grid(row=0, column=0, sticky="NW", padx=20, pady=550)
        #self.button5 = ttk.Button(self, text="Entrenar", cursor="hand2", command=self.Entrenamiento).grid(row=0, column=0, sticky="NE", padx=2, pady=550)
        
        #----------Extraccion
        self.id_nombre = self.Nombre.get()
        self.id_codigo = self.Codigo.get()

        self.ruta = r'Data/' + self.id_nombre
        if not os.path.exists(self.ruta):
            os.makedirs(self.ruta)
        #---------cvs
        global serial 
        serial = 0
        self.Columnas_tb = ['SERIE','','CODIGO','', 'NOMBRE',]
        self.exists = os.path.isfile("D:/14_CNN_Proyecto/Deatalles/Detalle_estu.csv")

        if self.exists:
            with open("D:/14_CNN_Proyecto/Deatalles/Detalle_estu.csv", 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    serial = serial + 1
            serial = (serial // 2)
            csvFile1.close()
        else:
            with open("D:/14_CNN_Proyecto/Deatalles/Detalle_estu.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(self.Columnas_tb)
                serial = 1
            csvFile1.close()
        
        self.row = [serial, '',self.id_codigo, '',self.id_nombre]
        with open('D:/14_CNN_Proyecto/Deatalles/Detalle_estu.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(self.row)
    
    def capturar_rostro(self):
        
        self.var = tk.IntVar()
        ret, self.frame = self.cap.read()
        if ret:
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.faces = self.faceClassif.detectMultiScale(self.gray, 1.3, 5)
            for(x, y, w, h) in self.faces:
                self.rostro = self.gray[y:y+h, x:x+w]
                self.rostro = cv2.resize(self.rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                    
                cv2.imwrite(self.ruta + '/rostro_{}.jpg'.format(self.count), self.rostro)
                
                #Mostrar rostro capturado y catidad
                self.foto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.rostro))
                self.canvas1.create_image(5,5, anchor=tk.NW, image=self.foto)
                self.var.set(self.count)
                self.mensaje = ttk.Label(self, textvariable=self.var).grid(row=0, column=1, sticky='NW', padx=150, pady=230)

                self.count += 1
                print(self.count)
            #time.sleep(0)
        if self.count < 200:
            return False
        else:
            messagebox.showinfo(message="Excediendo límite de imagenes", title="Título")
    
    def entrenarImg(self):
        smsBox = messagebox.askquestion('Entrenamieto','Desea Entrenar')
        if smsBox == 'yes':
            Thread(target = Entrenamiento).start()
            Thread(target = self.progreso()).start()
            #Entrenamiento()
            #self.progreso()
        else:
            return 1

    def progreso(self):
        
        self.i = 0
        self.progressbar = ttk.Progressbar(self, orient=HORIZONTAL, length=200, mode='determinate')
        self.progressbar.grid(row=0, column=0, sticky="NW", padx=120, pady=570)
        
        while(self.progressbar["value"] < self.progressbar["maximum"]):
            self.progressbar.update()
            self.progressbar["value"] = self.i**2
            self.i += 0.001
    
        self.progressbar.destroy()

    def guardar(self):
        self.Nombre.set("")
        self.Codigo.set("")
        self.foto = ""
        #self.mensaje.
        #self.var.set("")
    def apagar_webcam(self):
        self.image = ""
        self.cap.release()

class ReconocimientoFacial(ttk.Frame):
    """Pestaña 2, Reconocimiento Facial"""

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        #-------Detector facial OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        self.nom = ""
        self.bb = ""
        
        #global val
        self.val = True
        self.temp = []

        #-------Funciones
        self.crear_Widgets_2()
        self.crear_cuadro_2()
        self.Ingresar_Carpeta()
    
    def crear_cuadro_2(self):
        self.canvas = Canvas(self, height=450, width=480)
        self.canvas.grid(column=0, row=0, sticky='NW', padx=0, pady=40)
        self.canvas.create_rectangle(20, 20, 500, 440, fill="white", outline="gainsboro")
    
    def crear_Widgets_2(self):
        #---------- Buttons
        self.button1_F = ttk.Button(self, text="Prender", cursor="hand2", command=self.prender_2).grid(row=0, column=0, sticky='NW', padx=20, pady=10) 
        self.button2_F = ttk.Button(self, text="Apagar", cursor="hand2", command=self.apagar_webcam2).grid(row=0, column=0, sticky="NW", padx=120, pady=10)

        #---------- Tabla
        #self.style = ttk.Style()
        global tabla

        self.tabla = ttk.Treeview(self, height=25, columns=('nombre','fecha','hora'))
        self.tabla.column('#0',width=90)
        self.tabla.column('nombre',width=120)
        self.tabla.column('fecha',width=90)
        self.tabla.column('hora',width=90)
        self.tabla.grid(row=0, column=1, sticky="NW", padx=20, pady=60)
        self.tabla.heading('#0',text ='CODIGO')
        self.tabla.heading('nombre',text ='NOMBRE')
        self.tabla.heading('fecha',text ='FECHA')
        self.tabla.heading('hora',text ='HORA')

        #---------- Scrollbar
        self.scroll = ttk.Scrollbar(self, orient='vertical',command=self.tabla.yview)
        self.scroll.grid(row=0,column=1, padx=415, pady=60,sticky='NS')
        self.tabla.configure(yscrollcommand=self.scroll.set)


    def prender_2(self):
        #video capture
        self.cap = None
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #self.cap = cv2.resize(self.cap, dsize=(400, 400))
        #self.cap.set(3, 640)
        #self.cap.set(4, 480)
        self.webcamtk_2()

    def webcamtk_2(self):

        if self.cap is not None:
            ret, self.frame = self.cap.read()
            self.frame = cv2.resize(self.frame, dsize=(460, 420))#tamaño webcam
            if ret == True:
                self.frame = cv2.flip(self.frame, 20)
                self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                
                #self.Reco_Facial(self.image)
                self.Reconocimiento_Facial(self.image)

                self.image = Image.fromarray(self.image)
                self.image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(20, 20, anchor=tk.NW, image=self.image)
                
                self.master.after(10, self.webcamtk_2)
            else:
                self.master.image = ""
                self.cap.release()

    def Ingresar_Carpeta(self):
        global classes, model 
        #val = True
        model = load_model('D:/14_CNN_Proyecto/CNN/Model_Biometrico.h5py')
        dataP = 'D:/14_CNN_Proyecto/Data'
        classes = os.listdir(dataP)
        #classes=['Joel','Paola', 'jose']
        print("Clases: ", classes)

    def Reconocimiento_Facial(self, frame):
        #while True:
        self.datosEstudiante = []
        
        x=0
        y=0
        w=0
        h=0
        faces = self.face_cascade.detectMultiScale(self.frame, 1.3, 5)
        self.nom_colunas = ['Nombre', '', 'Codigo', '', 'Fecha', '', 'Hora']
        self.arch_est = os.path.isfile("D:/14_CNN_Proyecto/Deatalles/Detalle_estu.csv")

        if self.arch_est:
            self.df = pd.read_csv("D:/14_CNN_Proyecto/Deatalles/Detalle_estu.csv")
        else:
            return 1
             
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            face = frame[y:y+h, x:x+w]
            #if type(face) is np.ndarray:
            face = cv2.resize(face, (150, 150), interpolation= cv2.INTER_CUBIC)
            im = Image.fromarray(face, 'RGB')
            img_array = np.array(im)
            img_array = np.expand_dims(img_array, axis=0)
            pred = model.predict(img_array)
            label=classes[pred.argmax()]

            #cv2.putText(frame, '{}'.format(label), (x,y-5), 1,1.3, (255,255,0),1, cv2.LINE_AA)
            #pred.any()
            count = 0
        #if self.val == True:
            #count=+1
            ts = time.time()
            fecha = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            hora = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            aa = self.df.loc[self.df['NOMBRE'] == label]['NOMBRE'].values
            ID = self.df.loc[self.df['NOMBRE'] == label]['CODIGO'].values
            ID = str(ID)
            ID = ID[1:-1]
            self.bb = str(aa)
            self.bb = self.bb[2:-2]

            #self.datosEstudiante = [self.bb,'',str(ID),'',str(fecha), '', str(hora)]
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            exists = os.path.isfile("D:/14_CNN_Proyecto/Asistencia/Asistencia3_" + date + ".csv")

            if self.val == True:
                self.tabla.insert('', 0 , text=str(ID), values=(str(self.bb), str(fecha), str(hora)))
                self.datosEstudiante = [self.bb,'',str(ID),'',str(fecha), '', str(hora)]
                if exists:
                    with open("D:/14_CNN_Proyecto/Asistencia/Asistencia3_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(self.datosEstudiante)
                    csvFile1.close()
                else:
                    with open("D:/14_CNN_Proyecto/Asistencia/Asistencia3_" + date + ".csv", 'a+') as csvFile1:
                        writer = csv.writer(csvFile1)
                        writer.writerow(self.nom_colunas)
                        writer.writerow(self.datosEstudiante)
                    csvFile1.close()
                self.nom = self.bb
                self.temp.append(self.nom)
                print(self.temp)
                self.val = False

            elif self.bb != self.nom:
                if (self.bb in self.temp) == False:
                    self.tabla.insert('', 0 , text=str(ID), values=(str(self.bb), str(fecha), str(hora)))
                    self.datosEstudiante = [self.bb,'',str(ID),'',str(fecha), '', str(hora)]
                    if exists:
                        with open("D:/14_CNN_Proyecto/Asistencia/Asistencia3_" + date + ".csv", 'a+') as csvFile1:
                            writer = csv.writer(csvFile1)
                            writer.writerow(self.datosEstudiante)
                        csvFile1.close()
                    else:
                        with open("D:/14_CNN_Proyecto/Asistencia/Asistencia3_" + date + ".csv", 'a+') as csvFile1:
                            writer = csv.writer(csvFile1)
                            writer.writerow(self.nom_colunas)
                            writer.writerow(self.datosEstudiante)
                        csvFile1.close()
                    self.nom = self.bb
                    self.temp.append(self.nom)

        cv2.putText(frame, self.bb, (x,y-5), 1,1.3, (255,255,0),1, cv2.FONT_HERSHEY_SIMPLEX)

        
        
        



    def apagar_webcam2(self):
        self.image = ""
        self.cap.release()

#-------------------------------------------
#            INTERFAZ
#-------------------------------------------
def main():

    ventana = Tk()
    ventana.title('Reconocimiento biometrico')
    #ventana.resizable(0,0) #Tamaño estatico
    ventana.iconbitmap("img/logo3.ico")
    ventana.geometry("930x650")

    #Preparando notebook (tabs)
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill='both', expand='yes')

    Pes1 = ttk.Frame(notebook)
    Pes2 = ttk.Frame(notebook)
    
    notebook.add(Pes1, text="Registrar Rostros")
    notebook.add(Pes2, text="Reconocimiento Facial")
    
    #Crear marcos de pestañas
    Pestana1 = RegistrarRostro(master=Pes1)
    Pestana1.grid()

    Pestana2 = ReconocimientoFacial(master=Pes2)
    Pestana2.grid()

    #Main loop
    ventana.mainloop()

if __name__ == '__main__':
    main()