#! /usr/bin/python
#-*- coding: utf-8 -*-

########################################################################
class PynguinoError(ValueError):
    def __init__(self,valor):
        self.valor=valor
    def __str__(self):
        if self.valor==1:
            return u"No se puede establecer la comunicación con Pinguino, revisar que el archivo pynguino.pde este montado correctamente"
        elif self.valor==2:
            return u"El valor del pin debe ser un número entero"
        elif self.valor==3:
            return u"No tiene instalado el módulo PySerial"
        elif self.valor==4:
            return u"Sólo se permiten estas cadenas en mode: 'input' o 'output'"
        elif self.valor==5:
            return u"Sólo se admiten cadenas como: 'high' o 'low'"
        elif self.valor==6:
            return u"Sólo se admiten valores enteros para las entradas y las salidas análogas"
        elif self.valor==7:
            return u"Los valores de las salidas análogas deben estar entre 0 y 1023"
        elif self.valor==8:
            return u"Método no válido"
        elif self.valor==9:
            return u"Lo sentimos, aún no hay soprte disponible para su plataforma %s" %(os.name)
        elif self.valor==10:
            return u"Los valores para servos deben estar entre 1 y 250"
        elif self.valor==11:
            return u"No se puede obtener una lectura análoga, revise la conexión"
        elif self.valor==12:
            return u"No se puede establecer la comunicación con Pinguino, revisar que el archivo pynguinoServo.pde este montado correctamente"
        elif self.valor==13:
            return u"La posición del cursor debe darse en números esteros"
        elif self.valor==14:
            return u"Sólo ints, floats y strings"
        elif self.valor==15:
            return u"Los valores deben darse en entero (45), binario (0b101101) o hexadecimal (0x2d)."
        elif self.valor==16:
            return u"El segundo parámetro debe ser una lista, de enteros, binarios o hexadecimales."