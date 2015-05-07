#! /usr/bin/python
#-*- coding: utf-8 -*-

import socket, time
from raiseError import PynguinoError

#----------------------------------------------------------------------
def detectar_metodo(cadena):
    comandos_processing=("Conect","RecursiveConect","pinMode","digitalWrite","digitalRead","analogRead","analogWrite",
                          "GetPinMode","GetPinState","allInput","allOutput","allHigh","allLow","reset","setProcessingTimeout",
                          "setProcessingWriteTimeout","ProcessingClose","GetPinguinoCode")
    if comandos_processing.count(cadena[:cadena.find("(")])!=0:
        ret=[]
        ret.append(cadena[:cadena.find("(")])
        ret.append(cadena[cadena.find("(")+1:cadena.find(",")])
        if cadena.count(",")==1:
            ret.append(cadena[cadena.find(",")+1:cadena.find(")")])
        return ret
    else: raise PynguinoError(8)

########################################################################
class ComandosPynguino:
    #----------------------------------------------------------------------
    def Conect(self,puerto):
        """Inicializa la comunicación"""
        self.Send("Conect('"+str(puerto)+"')")
        
    #----------------------------------------------------------------------
    def RecursiveConect(self,max_puertos=20):
        """Se conecta estomáticamente con el primer pinguino que encuentre habilitado."""
        self.Send("RecursiveConect("+str(max_puertos)+")")

    #----------------------------------------------------------------------
    def pinMode(self,pin,mode):
        """Define como se comportará el pin, como entrada o como salida"""
        if type(pin)!=type(1): raise PynguinoError(2)
        if not(mode=='input' or mode=='output'): raise PynguinoError(4)        
        
        self.Send("pinMode("+str(pin)+",'"+mode+"')")
    
    #----------------------------------------------------------------------
    def digitalRead(self,pin):
        """Lee el estado de un pin"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        
        self.Send("digitalRead("+str(pin)+")")
            
    #----------------------------------------------------------------------
    def analogRead(self,pin):
        """Lee el estado de un pin análogo"""      
        if not(type(pin)==type(1)): raise PynguinoError(2) 
        
        self.Send("analogRead("+str(pin)+")")
        
    #----------------------------------------------------------------------
    def digitalWrite(self,pin,value):
        """Establece el estado de un pin, alto o bajo"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        if not(value=='high' or value=='low'): raise PynguinoError(5)
        
        self.Send("digitalWrite("+str(pin)+",'"+str(value)+"')")
    
    #----------------------------------------------------------------------
    def analogWrite(self,pin,value):
        """Establece el estado de un pin análogo"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        if not(type(value)==type(1)): raise PynguinoError(6)
        if value<0 or value>1023: raise PynguinoError(7)
        
        self.Send("analogWrite("+str(pin)+","+str(value)+")")
        
    #----------------------------------------------------------------------
    def GetPinMode(self,pin):
        """Retorna el modo de un pin basado en la informacion enviada"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        
        self.Send("GetPinMode("+str(pin)+")")
    
    #----------------------------------------------------------------------
    def GetPinState(self,pin):
        """Retorna el estado de un pin basado en la informacion enviada"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        
        self.Send("GetPinState("+str(pin)+")")
        
    #----------------------------------------------------------------------
    def allInput(self):
        """Establece todos los pines como entrada"""
        self.Send("allInput()")
    
    #----------------------------------------------------------------------
    def allOutput(self):
        """Establece todos los pines como salida y los fija en estado bajo"""
        self.Send("allOuput()")
    
    #----------------------------------------------------------------------
    def allHigh(self):
        """Establece todos los pines como salida y los fija en estado alto"""
        self.Send("allHigh()")
        
    #----------------------------------------------------------------------
    def allLow(self):
        """Establece todos los pines como salida y los fija en estado bajo"""
        self.Send("allLow()")
        
    #----------------------------------------------------------------------
    def reset(self):
        """Resetea el pinguino"""
        self.Send("reset()")
        
    #----------------------------------------------------------------------
    def setProcessingTimeout(self,value):
        """Cabia el timeout del interprete"""
        self.Send("setProcessingTimeout("+str(value)+")")
    
    #----------------------------------------------------------------------
    def setProcessingWriteTimeout(self,value):
        """Cambia el writeTimeout del interprete"""
        self.Send("setProcessingWriteTimeout("+str(value)+")")
    
    #----------------------------------------------------------------------
    def ProcessingClose(self):
        """Cierra el puerto"""
        self.Send("ProcessingClose("+str(value)+")")
    
        
########################################################################
class PinguinoSockets(ComandosPynguino):
    #----------------------------------------------------------------------
    def SetServer(self,host_server,port_server,init=False):
        """Configura las conexiones según los paramétros,
        si el parámetro opcional init es True también se inicia el Customer."""
        self.pinguino_server=socket.socket()
        self.pinguino_server.bind((host_server,port_server)) 
        self.pinguino_server.listen(1)
        if init: pynguino_customer, (host_c, port_c) = self.pinguino_server.accept()
            
    #----------------------------------------------------------------------
    def InitServer(self):
        """Inicializa el Server"""
        self.pinguino_customer, (host_c, port_c) = self.pinguino_server.accept()
        
    #----------------------------------------------------------------------
    def SetCustomer(self,host_server,port_server):
        """onfigura el Customer según los parámetros."""
        self.pinguino_customer=socket.socket()
        self.pinguino_customer.connect((host_server,port_server))
        
    #----------------------------------------------------------------------
    def Recv(self,max_bytes):
        """Retorna una cadena que haya sido enviada, como parámetro en número máximo de bytes a recibir"""
        return self.pinguino_customer.recv(max_bytes)
    
    #----------------------------------------------------------------------
    def Send(self,string,pause=0.05):
        """"Envía una cadena"""
        self.pinguino_customer.send(string) 
        
        #Pausa muy importante para evitar que la otra parte del programa
        #interprete 2 envíos sucesivos como si fueran 1.
        time.sleep(pause) 
    
    #----------------------------------------------------------------------
    def ServerClose(self):
        self.pinguino_customer.close()
        self.pinguino_server.close()
        
    #----------------------------------------------------------------------
    def CustomerClose(self):
        self.pinguino_customer()
        
    #----------------------------------------------------------------------
    def SetPinguinoObject(self,objeto):
        """Determinamos el objeto pinguino por defecto para comunicarse."""
        self.pinguino_object=objeto
        
    #----------------------------------------------------------------------
    def process_method(self,str_metodo):
        """Decodifica la cadena recibida para que el pynguino pueda interpretar las ordenes"""
        metodo=detectar_metodo(str_metodo)
        if metodo[0]=="Conect":
            self.pinguino_psc=self.pinguino_object
            self.pinguino_psc.Conect(metodo[1][1:-1])
        elif metodo[0]=="RecursiveConect":
            self.pinguino_psc=self.pinguino_object
            self.pinguino_psc.RecursiveConect(int(metodo[1]))  
        elif metodo[0]=="pinMode":
            print metodo[1]
            print metodo[2]
            print metodo[2][1:-1]
            self.pinguino_psc.pinMode(int(metodo[1]),metodo[2][1:-1])
        elif metodo[0]=="digitalRead":
            self.pinguino_psc.digitalRead(int(metodo[1]))
        elif metodo[0]=="analogRead":
            self.pinguino_psc.analogRead(int(metodo[1]))
        elif metodo[0]=="digitalWrite":
            self.pinguino_psc.digitalWrite(int(metodo[1]),metodo[2][1:-1])
        elif metodo[0]=="analogWrite":
            self.pinguino_psc.analogWrite(int(metodo[1]),int(metodo[2]))
        elif metodo[0]=="GetPinMode":
            self.pinguino_psc.GetPinMode(int(metodo[1]))
        elif metodo[0]=="GetPinState":
            self.pinguino_psc.GetPinState(int(metodo[1]))
        elif metodo[0]=="allInput":
            self.pinguino_psc.allInput()
        elif metodo[0]=="allOutput":
            self.pinguino_psc.allOutput()
        elif metodo[0]=="allHigh":
            self.pinguino_psc.allHigh()
        elif metodo[0]=="allLow":
            self.pinguino_psc.allLow()
        elif metodo[0]=="reset":
            self.pinguino_psc.reset()
        elif metodo[0]=="setProcessingTimeout":
            self.pinguino_psc.setProcessingTimeout(int(metodo[1]))
        elif metodo[0]=="setProcessingWriteTimeout":
            self.pinguino_psc.setProcessingWriteTimeout(int(metodo[1]))
        elif metodo[0]=="ProcessingClose":
            self.pinguino_psc.ProcessingClose()    
