import sys
from PyQt5 import QtGui, QtWidgets, uic, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import random

#Ventana clase OpenGL
class Viewer3DWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.figurausu = ''
        self.figuraopo = ''
        self.x = 1
        self.y = 1
        n = 1/3
        #Corresponden a las esquinas superiores izquierdas de cada cuadrado
        #Desde es punto es posible obtener los 3 restantes
        self.coords = [ [(-1,1), (-n,1), (n,1)],
                        [(-1,n), (-n,n), (n,n)],
                        [(-1, -n), (-n,-n), (n,-n)] ]
        self.setFocusPolicy(Qt.StrongFocus) 
        self.matrizusu = np.zeros((3,3), dtype = bool)
        self.matrizopo = np.zeros((3,3), dtype = bool)
        self.matrizjuego = np.zeros((3,3), dtype = bool)

    #Funciones protegidas OpenGL
    def paintGL(self):
        glLoadIdentity()
        glMatrixMode( GL_MODELVIEW )
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glEnable(GL_DEPTH_TEST)
        self.dibujar()
        glFlush()
    def resizeGL(self, widthInPixels, heightInPixels):
        glViewport(0, 0, widthInPixels, heightInPixels)
    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
           
    def dibujar(self):
        self.cuadricula()
        self.dibujarentabla(self.figurausu)
        self.dibujarcuadro()
        
    #Función para dibujar la cuadrícula
    def cuadricula(self):
        glColor3fv([255, 255, 255])

        glBegin(GL_LINES)
        glVertex2f(-1,1/3)
        glVertex2f(1,1/3)
        glVertex2f(1/3,-1)
        glVertex2f(1/3,1)
        glEnd()        
        
        glBegin(GL_LINES)
        glVertex2f(-1,-1/3)
        glVertex2f(1,-1/3)
        glVertex2f(-1/3,1)
        glVertex2f(-1/3,-1)
        glEnd()   
        
    #Función para dibujar el cuadro que esta conectado con las flechas, es decir, se dibuja 
    #un nuevo cuadro según las posiciones de x,y conectadas a las flechas del teclado
    def dibujarcuadro(self):
        x,y = self.coords[self.x][self.y]
        n=2/3
        glColor3fv([255,0,0])
        glBegin(GL_QUADS)
        glVertex2f(x,y)
        glVertex2f(x+n,y)
        glVertex2f(x+n,y-n)
        glVertex2f(x,y-n)
        glEnd()
        
    #Función que dibujar la figura según lo que haya elegido el usuario en línea 214
    def dibujarfigura(self,x,y,figurausu,n=2/3):
        if figurausu=='x':
            glBegin(GL_LINES)
            glVertex2f(x,y)
            glVertex2f(x+n,y-n)
            glVertex2f(x+n,y)
            glVertex2f(x,y-n)
            glEnd()
        else:
            distanciax = x+(n/2)
            distanciay = y-(n/2)
            radio=0.33
            glBegin(GL_LINE_LOOP)
            b = np.arange(0,360+1,1)
            for i in b:
                glVertex2f(distanciax+radio*np.cos(np.pi*i/180),distanciay+radio*np.sin(np.pi*i/180))
            glEnd()     
        
    def keyPressEvent(self, evento):
        if ventana.ui.botonx.isChecked() or ventana.ui.botono.isChecked():
            if evento.key() == Qt.Key_Right:
                self.y+=1
                if self.y>2:
                    self.y=2
            elif evento.key() == Qt.Key_Left:
                self.y-=1
                if self.y<0:
                    self.y=0
            elif evento.key() == Qt.Key_Up:
                self.x-=1
                if self.x<0:
                    self.x=0
            elif evento.key() == Qt.Key_Down:
                self.x+=1
                if self.x<0:
                    self.x=0
            elif evento.key()== Qt.Key_Space:
                self.matrizusu[self.x][self.y]=True
                self.matrizjuego = self.matrizusu|self.matrizopo
                self.lista = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
                self.lista2 = self.matrizjuego.flatten().tolist()
                self.dic = dict(zip(self.lista, self.lista2))
                self.a = dict(filter(lambda x: x[1] == False, self.dic.items()))
                self.b = list(self.a.keys())
                
            
                #print(b)
                
                #print(dic)
                #print(lista2)

                #dict_from_list = {lista[i]: lista2[i] for i in range(len(lista))}
                #print(dict_from_list)
                
                #test1 = random.choice(lista)
                #self.x,self.y = test1

                #lista.remove(test1)
                
                self.x,self.y = random.choice(self.b)
                self.matrizopo[self.x][self.y]=True
                self.matrizjuego = self.matrizusu|self.matrizopo
                self.ganador()
            self.dibujar()
            self.updateGL()
            
    #Función que convierte la posición de donde realizó el dibujo a True en la matriz booleana
    #para que así el juego automático sepa dónde realizar el siguiente dibujo desocupado
    def dibujarentabla(self,figurausu):
        for xi in range(3):
            for yi in range(3):
                x,y = self.coords[xi][yi]
                if self.matrizusu[xi][yi]==True:
                    self.dibujarfigura(x,y,self.figurausu)
                elif self.matrizopo[xi][yi]==True:
                    self.dibujarfigura(x,y,self.figuraopo)            
    
    #Función para crear la ventana emergente    
    def VentanaEmergente1(self):
        QtWidgets.QMessageBox.about(self, 'Fin del juego', '¡Ganaste!')
        
    def VentanaEmergente2(self):
        QtWidgets.QMessageBox.about(self, 'Fin del juego', 'Perdiste :(')        
    
    #Función para verificar el ganador
    def ganador(self):
        if (self.matrizusu[0][0]==True and self.matrizusu[0][1]==True and self.matrizusu[0][2]==True) or (self.matrizusu[1][0]==True and self.matrizusu[1][1]==True and self.matrizusu[1][2]==True) or (self.matrizusu[2][0]==True and self.matrizusu[2][1]==True and self.matrizusu[2][2]==True):
            self.VentanaEmergente1()
        elif (self.matrizusu[0][0]==True and self.matrizusu[1][0]==True and self.matrizusu[2][0]==True) or (self.matrizusu[0][1]==True and self.matrizusu[1][1]==True and self.matrizusu[2][1]==True) or (self.matrizusu[0][2]==True and self.matrizusu[1][2]==True and self.matrizusu[2][2]==True):
            self.VentanaEmergente1()
        #Gana diagonal            
        elif (self.matrizusu[0][0]!=0 and self.matrizusu[0][0]==self.matrizusu[1][1] and self.matrizusu[0][0]==self.matrizusu[2][2]) or (self.matrizusu[2][0]!=0 and self.matrizusu[2][0]==self.matrizusu[1][1] and self.matrizusu[2][0]==self.matrizusu[0][2]):
            self.VentanaEmergente1()      
            
        if (self.matrizopo[0][0]==True and self.matrizopo[0][1]==True and self.matrizopo[0][2]==True) or (self.matrizopo[1][0]==True and self.matrizopo[1][1]==True and self.matrizopo[1][2]==True) or (self.matrizopo[2][0]==True and self.matrizopo[2][1]==True and self.matrizopo[2][2]==True):
            self.VentanaEmergente2()
        elif (self.matrizopo[0][0]==True and self.matrizopo[1][0]==True and self.matrizopo[2][0]==True) or (self.matrizopo[0][1]==True and self.matrizopo[1][1]==True and self.matrizopo[2][1]==True) or (self.matrizopo[0][2]==True and self.matrizopo[1][2]==True and self.matrizopo[2][2]==True):
            self.VentanaEmergente2()
        #Gana diagonal            
        elif (self.matrizopo[0][0]!=0 and self.matrizopo[0][0]==self.matrizopo[1][1] and self.matrizopo[0][0]==self.matrizopo[2][2]) or (self.matrizopo[2][0]!=0 and self.matrizopo[2][0]==self.matrizopo[1][1] and self.matrizopo[2][0]==self.matrizopo[0][2]):
            self.VentanaEmergente2()     
            
#Ventana principal
class Ventana(QtWidgets.QMainWindow):    
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('tictactoe.ui')
        self.ui.setWindowTitle('Tic Tac Toe')
        self.ui.setWindowIcon(QtGui.QIcon('uoh.jpg'))
        self.ui.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.viewer3D = Viewer3DWidget(self)                
        self.ui.OpenGLLayout.addWidget( self.viewer3D )
        self.ui.show()
                
        #variables
        self.ui.botonx.toggled.connect(self.jugada)
        self.ui.botono.toggled.connect(self.jugada)
        self.ui.botonx.toggled.connect(self.empiezas)
        self.ui.botono.toggled.connect(self.empiezas)
        self.ui.reiniciarb.clicked.connect(self.reiniciar)
        self.ui.reiniciarb.clicked.connect(self.empiezas)
        
        self.timer=QTimer()
        self.timer.timeout.connect(self.LCDEvent)
        self.s = 0
        self.m = 0
    
    #Función para empezar el tiempo con un ms de 1000
    def empiezas(self):
        self.timer.start(1000)
        self.s=0
        self.m=0
        self.ui.minutos.display(self.m)
        self.ui.segundos.display(self.s)
    
    #Función para darle un valor al qlcdnumber según los minutos y los segundos
    def LCDEvent(self):
        self.s += 1
        self.ui.segundos.display(self.s)
        if self.s>60:
            self.s=0
            self.ui.segundos.display(self.s)
            self.m+=1
            self.ui.minutos.display(self.m)
    
    #Función para empezar el juego
    def jugada(self):
        if self.ui.botonx.isChecked():
            figurausu = 'x'
            figuraopo = 'o'
        else:
            figurausu = 'o'
            figuraopo = 'x'
        self.viewer3D.figurausu = figurausu
        self.viewer3D.figuraopo = figuraopo
        self.viewer3D.updateGL()         
    
    #Función para reiniciar el juego estableciendo los valores principales        
    def reiniciar(self):
        self.viewer3D.matrizusu = np.zeros((3,3), dtype = bool)
        self.viewer3D.matrizopo = np.zeros((3,3), dtype = bool)
        self.viewer3D.matrizjuego = np.zeros((3,3), dtype = bool)
        self.viewer3D.x = 1
        self.viewer3D.y = 1
        self.viewer3D.updateGL()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec_())