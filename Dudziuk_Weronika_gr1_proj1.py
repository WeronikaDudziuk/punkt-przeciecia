# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:57:18 2019

@author: Weronika Dudziuk
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QLineEdit, QGridLayout,QColorDialog,QMessageBox,QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
import os
import math

class Window(QWidget): #stworzenie klasy dla okna aplikacji
    def __init__(self):
        QWidget.__init__(self)
        
        self.button = QPushButton('Rysuj', self) #tworzenie przycisków, etykiet oraz obiektow do wpisywania danych
        self.xlabel = QLabel("XA", self)
        self.xEdit = QLineEdit()
        self.ylabel = QLabel("YA", self)
        self.yEdit = QLineEdit()
        self.xlabel1 = QLabel("XB", self)
        self.xEdit1 = QLineEdit()
        self.ylabel1 = QLabel("YB", self)
        self.yEdit1 = QLineEdit()
        self.xlabel2 = QLabel("XC", self)
        self.xEdit2 = QLineEdit()
        self.ylabel2 = QLabel("YC", self)
        self.yEdit2 = QLineEdit()
        self.xlabel3 = QLabel("XD", self)
        self.xEdit3 = QLineEdit()
        self.ylabel3 = QLabel("YD", self)
        self.yEdit3 = QLineEdit()
        self.clrChoose = QPushButton('Wybierz kolor', self)
        self.loadData = QPushButton('Wczytaj dane z pliku',self)
        self.clear = QPushButton('Usuń wprowadzone dane',self)
        self.saveData = QPushButton('Zapisz wynik',self)
        
        self.XPlabel = QLabel('XP',self)
        self.XPlab = QLabel()
        self.YPlabel = QLabel('YP',self)
        self.YPlab = QLabel()
        self.inflabel = QLabel('Informacja o położeniu punktu',self)
        self.inflab = QLabel()
        
        self.distAlabel=QLabel()
        self.distBlabel=QLabel()
        self.distClabel=QLabel()
        self.distDlabel=QLabel()
        
        self.distADescription=QLabel('|AP|', self)
        self.distBDescription=QLabel('|BP|', self)
        self.distCDescription=QLabel('|CP|', self)
        self.distDDescription=QLabel('|DP|', self)
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        
        layout =  QGridLayout(self) # usytuowanie poszczególnych elementów aplikacji
        
        layout.addWidget(self.xlabel, 1, 1)
        layout.addWidget(self.xEdit, 1, 2)
        layout.addWidget(self.ylabel, 2, 1)
        layout.addWidget(self.yEdit, 2, 2)
        
        layout.addWidget(self.xlabel1, 3, 1)
        layout.addWidget(self.xEdit1, 3, 2)
        layout.addWidget(self.ylabel1, 4, 1)
        layout.addWidget(self.yEdit1, 4, 2)
        
        layout.addWidget(self.xlabel2, 5, 1)
        layout.addWidget(self.xEdit2, 5, 2)
        layout.addWidget(self.ylabel2, 6, 1)
        layout.addWidget(self.yEdit2, 6, 2)
        
        layout.addWidget(self.xlabel3, 7, 1)
        layout.addWidget(self.xEdit3, 7, 2)
        layout.addWidget(self.ylabel3, 8, 1)
        layout.addWidget(self.yEdit3, 8, 2)
        
        layout.addWidget(self.XPlabel,3,3)
        layout.addWidget(self.XPlab,3,4)
        layout.addWidget(self.YPlabel,4,3)
        layout.addWidget(self.YPlab,4,4)
        
        layout.addWidget(self.inflabel,1,5)
        layout.addWidget(self.inflab,2,5)
        
        
        layout.addWidget(self.distADescription,5,3)
        layout.addWidget(self.distBDescription,6,3)
        layout.addWidget(self.distCDescription,7,3)
        layout.addWidget(self.distDDescription,8,3)
        
        layout.addWidget(self.distAlabel,5,4)
        layout.addWidget(self.distBlabel,6,4)
        layout.addWidget(self.distClabel,7,4)
        layout.addWidget(self.distDlabel,8,4)
        
        
        layout.addWidget(self.button, 10, 1, 1, -1) 
        layout.addWidget(self.canvas, 9, 1, 1, -1)
        layout.addWidget(self.clrChoose, 11, 1, 1, -1)
        layout.addWidget(self.loadData,12, 1, 1, -1)
        layout.addWidget(self.clear,13, 1, 1, -1)
        layout.addWidget(self.saveData,14, 1, 1, -1)
        
        
        self.button.clicked.connect(self.handleButton) # połączenie przycisku (signal) z akcją (slot)
        self.clrChoose.clicked.connect(self.clrChooseF)
        self.loadData.clicked.connect(self.loadDatA)
        self.clear.clicked.connect(self.clearAll)
        self.saveData.clicked.connect(self.saveDatA)
        
        
    def checkValues(self,lineE):   #funkcja sprawdzająca wprowadzone przez uzytkownika wartosci
        if lineE.text().lstrip('-').replace('.','').isdigit():
            return float(lineE.text())
        else:
            return None
        

    def rysuj(self,clr='m'):    #funkcja rysujaca wykres i obliczajaca wspolrzedne punktu przeciecia
        x = self.checkValues(self.xEdit)
        y = self.checkValues(self.yEdit)
        
        x1 = self.checkValues(self.xEdit1)
        y1 = self.checkValues(self.yEdit1)
        
        x2 = self.checkValues(self.xEdit2)
        y2 = self.checkValues(self.yEdit2)
        
        x3 = self.checkValues(self.xEdit3)
        y3 = self.checkValues(self.yEdit3)
        
        if x == None or y == None or x1 == None or y1 == None or x2 == None or y2 == None or x3 == None or y3 ==None:
            msg_err = QMessageBox()   #wyswietlenie komunikatu w przypadku wprowadzenia przez uzytkownika danych w niepoprawnym formacie
            msg_err.setIcon(QMessageBox.Warning)
            msg_err.setWindowTitle('Błąd')
            msg_err.setStandardButtons(QMessageBox.Ok)
            msg_err.setText('Wprowadzono niepoprawne współrzędne')
            msg_err.exec_()
            self.figure.clear()
            self.canvas.draw()
            return
            
        P1, P2=[x, x1],[y, y1]
        P3, P4=[x2, x3],[y2, y3]
        
        S=[x,y,
           x1,y1,
           x2,y2,
           x3,y3]
        M=(S[2]-S[0])*(S[7]-S[5])-(S[3]-S[1])*(S[6]-S[4])

        if M != 0:
            t1=((S[4]-S[0])*(S[7]-S[5])-(S[5]-S[1])*(S[6]-S[4]))/((S[2]-S[0])*(S[7]-S[5])-(S[3]-S[1])*(S[6]-S[4]))
            t2=((S[4]-S[0])*(S[3]-S[1])-(S[5]-S[1])*(S[2]-S[0]))/((S[2]-S[0])*(S[7]-S[5])-(S[3]-S[1])*(S[6]-S[4]))       
            XP=S[4]+t2*(S[6]-S[4])
            YP=S[5]+t2*(S[7]-S[5])
            if t1>=0 and t1<=1 and t2>=0 and t2<=1: # warunki defiuniujace polozenie punktu przeciecia
                self.XPlab.setText(str('{:.3f}'.format(XP)))
                self.YPlab.setText(str('{:.3f}'.format(YP)))
                self.inflab.setText('Na przecięciu dwóch odcinków')
            elif 0<=t1<=1:
                self.XPlab.setText(str('{:.3f}'.format(XP)))
                self.YPlab.setText(str('{:.3f}'.format(YP)))
                self.inflab.setText('Na przedłużeniu odcinka CD')
                
            elif 0<=t2<=1:
                self.XPlab.setText(str('{:.3f}'.format(XP)))
                self.YPlab.setText(str('{:.3f}'.format(YP)))
                self.inflab.setText('Na przedłużeniu odcinka AB')
            else:
                self.XPlab.setText(str('{:.3f}'.format(XP)))
                self.YPlab.setText(str('{:.3f}'.format(YP)))
                self.inflab.setText('Na przedłużeniu obu odcinków')
                
            self.distAlabel.setText(str('{:.3f}'.format(self.getPointsDistance(x, y, XP, YP))))
            self.distBlabel.setText(str('{:.3f}'.format(self.getPointsDistance(x1, y1, XP, YP))))
            self.distClabel.setText(str('{:.3f}'.format(self.getPointsDistance(x2, y2, XP, YP))))
            self.distDlabel.setText(str('{:.3f}'.format(self.getPointsDistance(x3, y3, XP, YP))))
            
        else:
            msg_err = QMessageBox()    #wyswietlenie komunikatu w przypadku wprowadzenia przez uzytkownika danych dla ktorych punkt przeciecia nie istnieje
            msg_err.setIcon(QMessageBox.Warning)
            msg_err.setWindowTitle('Błąd')
            msg_err.setStandardButtons(QMessageBox.Ok)
            msg_err.setText('Dzielenie przez zero. Nie można obliczyć współrzędnych punktu przecięcia. Wprowadź inne współrzędne.')
            msg_err.exec_()
            self.figure.clear()
            self.canvas.draw()
    
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, 'o',color=clr)
        ax.text(x,y,'  A['+str(x)+','+str(y)+']') #tworzenie etykiet dla poszczegolnych punktow
        ax.plot(x1, y1, 'o', color=clr)
        ax.text(x1,y1,'  B['+str(x1)+','+str(y1)+']')
        ax.plot(x2, y2, 'o', color=clr)
        ax.text(x2,y2,'  C['+str(x2)+','+str(y2)+']')
        ax.plot(x3, y3, 'o', color=clr)
        ax.text(x3,y3,'  D['+str(x3)+','+str(y3)+']')
        ax.plot((x,x1), (y,y1),'-',color=clr)
        ax.plot((x2,x3), (y2,y3),'-',color=clr)
        
        if M != 0:
            ax.plot(XP,YP,'o',color='black')
            ax.text(XP,YP,'  P['+str('{:.3f}'.format(XP))+','+str('{:.3f}'.format(YP))+']')
            ax.plot((x,XP), (y,YP),'--',dashes=(1,5),color=clr)  #rysowanie przedluzen odcinkow
            ax.plot((x1,XP),(y1,YP),'--',dashes=(1,5),color=clr)
            ax.plot((x2,XP),(y2,YP),'--',dashes=(1,5),color=clr)
            ax.plot((x3,XP),(y3,YP),'--',dashes=(1,5),color=clr)
        self.canvas.draw()
            

    def handleButton(self): #funkcja wykonujaca cala metode rysuj
        self.rysuj()
        
    def clrChooseF(self):  #funkcja umozliwiajaca wybor koloru wykresu
        color=QColorDialog.getColor()
        if color.isValid():
            self.rysuj(color.name())
            
    def getPointsDistance(self, x1, y1, x2, y2): #funkcja liczaca odleglosc punktu przeciecia od kolejnych punktow
        x = math.pow(x2-x1, 2)
        y = math.pow(y2-y1, 2)
        return math.sqrt(x + y)

    def loadDatA(self):  #funcja pozwalajaca na wczytanie danych z pliku .txt
        filter = "Pliki txt (*.txt)" 
        currentPath = os.getcwd() 
        fileName, _ = QFileDialog.getOpenFileName(None, "Otworz plik", currentPath, filter) 
        myFile = open(fileName, "r") 
        lines = myFile.readlines()
        editsElementsList = [[self.xEdit, self.yEdit], [self.xEdit1, self.yEdit1], 
                             [self.xEdit2, self.yEdit2], [self.xEdit3, self.yEdit3]]
        for i, line in enumerate(lines[1:], 0): 
            coords = line.split(',') 
            editsElementsList[i][0].setText(coords[0].strip())
            editsElementsList[i][1].setText(coords[1].strip())
        
    def clearAll(self):  #funkcja pozwalajaca na wyczyszczenie wszystkich wprowadzonych danych oraz wykresu
        self.xEdit.clear()
        self.yEdit.clear()
        self.xEdit1.clear()
        self.yEdit1.clear()
        self.xEdit2.clear()
        self.yEdit2.clear()
        self.xEdit3.clear()
        self.yEdit3.clear()
        self.XPlab.clear()
        self.YPlab.clear()
        self.inflab.clear()
        
        self.distAlabel.clear()
        self.distBlabel.clear()
        self.distClabel.clear()
        self.distDlabel.clear()
        
        self.figure.clear()
        self.canvas.draw()
        
    def saveDatA(self):  #funkcja pozwalajaca na zapis obliczonych wspolrzednych punktu przeciecia oraz informacji o jego polozeniu do pliku tekstowego
        fileOut = open('wyniki.txt', 'a')
        fileOut.write(55*'-')
        fileOut.write('\n|{:^10}|{:^10}|{:^30}|\n'.format('XP', 'YP','Informacja o położeniu punktu'))
        fileOut.write(55*'-')
        fileOut.write('\n|{:^10}|{:^10}|{:^30}|\n'.format(self.XPlab.text(), self.YPlab.text(), self.inflab.text()))

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app=QApplication.instance()
    window = Window()
    window.show()
    sys.exit(app.exec_())