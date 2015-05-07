#! /usr/bin/python
#-*- coding: utf-8 -*-  

#                            PIC-18F2550                                                       PIC-18F4550              
#
#                       Reset -#######- Digital I/O 7                                   Reset -###########- Digital I/O 7  
#                Analog In 13 -#     #- Digital I/O 6                            Analog In 13 -#         #- Digital I/O 6  
#                Analog In 14 -#     #- Digital I/O 5                            Analog In 14 -#         #- Digital I/O 5
#                Analog In 15 -#     #- Digital I/O 4                            Analog In 15 -#         #- Digital I/O 4 
#                Analog In 16 -#     #- Digital I/O 3                            Analog In 16 -#         #- Digital I/O 3 
#                         Run -#     #- Digital I/O 2                                      Run-#         #- Digital I/O 2
#                Analog In 17 -#     #- Digital I/O 1                            Analog In 17 -#         #- Digital I/O 1 
#                         GND -#     #- Digital I/O 0                            Analog In 18 -#         #- Digital I/O 0 
#                       OSC 1 -#     #- VCC                                      Analog In 19 -#         #- VCC
#                       OSC 2 -#     #- GND                                      Analog In 20 -#         #- GND
#              Digital I/O 10 -#     #- Digital I/O 9                                     VCC -#         #- Digital I/O 28   
#  Digital I/O, Analog Out 11 -#     #- Digital I/O 8                                     GND -#         #- Digital I/O 27
#  Digital I/O, Analog Out 12 -#     #- D+                                               OSC 1-#         #- Digital I/O 26
#                        VUSB -#######- D-                                               OSC 2-#         #- Digital I/O 25
#                                                                              Digital I/O 10 -#         #- Digital I/O 9
#                                                                  Digital I/O, Analog Out 11 -#         #- Digital I/O 8
#                                                                  Digital I/O, Analog Out 12 -#         #- D+
#                                                                                        VUSB -#         #- D-
#                                                                              Digital I/O 21 -#         #- Digital I/O 24
#                                                                              Digital I/O 22 -###########- Digital I/O 23 

try: import serial
except: PynguinoError(3)

import os
from raiseError import PynguinoError
        
########################################################################
class PinguinoProcessing():
	
	# Modificado Jue 7 Julio 2011 - Para Adaptar a PinguiBLOQUES
    pin_modes=range(29)
    pin_states=range(29)
    
    #----------------------------------------------------------------------
    def Conect(self,puerto):
        """Inicializa la comunicación"""
        try:
            self.pinguino=serial.Serial(puerto,timeout=1)
            self.pinguino.write('PinnoProcessing')
            if self.pinguino.read(9)=='Conectado':
                self.pin_modes=range(29)
                self.pin_states=range(29)
                return True
        except: raise PynguinoError(1)
        
    #----------------------------------------------------------------------
    def RecursiveConect(self,max_puertos=20):
        """Se conecta estomáticamente con el primer pinguino que encuentre habilitado."""
        cont=0
        while cont<=max_puertos:
            try:
                if os.name=='posix':
                    self.Conect('/dev/ttyACM'+str(cont))
                elif os.name=='nt':
                    self.Conect('COM'+str(cont))
                return True
            except: pass
            cont+=1         
        return False 
    
    #----------------------------------------------------------------------
    def pinMode(self,pin,mode):
        """Define como se comportará el pin, como entrada o como salida"""
        if type(pin)!=type(1): raise PynguinoError(2)
        if not(mode=='input' or mode=='output'): raise PynguinoError(4)
        
        self.pinguino.write('setup')
        self.pinguino.write(str(pin).rjust(2,'0'))
        self.pinguino.write(mode)
        self.pin_modes[pin]=mode
    
    #----------------------------------------------------------------------
    def digitalRead(self,pin):
        """Lee el estado de un pin"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        
        self.pinguino.write('read')
        self.pinguino.write(str(pin).rjust(2,'0'))
        self.pinguino.write('digital')
        read=self.pinguino.read(1)
        if read=='1': return 'high'
        elif read=='0': return 'low'
            
    #----------------------------------------------------------------------
    def analogRead(self,pin):
        """Lee el estado de un pin análogo"""
        if not(type(pin)==type(1)): raise PynguinoError(2) 
        
        self.pinguino.write('read')
        self.pinguino.write(str(pin).rjust(2,'0'))
        self.pinguino.write('analog')
        #Para evitar ValueError: null byte in argument for int()
        #simplemente se eliminan todos los'\x00'
        #más una función de recursividad 
        cont=0
        while cont<=10:
            try:
                read_analog=self.pinguino.read(5)
                value=int(read_analog.replace('\x00',''))
                return value
            except: cont+=1
        raise PynguinoError(11)
    
    #----------------------------------------------------------------------
    def digitalWrite(self,pin,value):
        """Establece el estado de un pin, alto o bajo"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        if not(value=='high' or value=='low'): raise PynguinoError(5)
        
        self.pinguino.write('write')
        self.pinguino.write(str(pin).rjust(2,'0'))
        self.pinguino.write('digital')
        if value=='high': self.pinguino.write('1')
        elif value=='low': self.pinguino.write('0')
        self.pin_states[pin]=value
    
    #----------------------------------------------------------------------
    def analogWrite(self,pin,value):
        """Establece el estado de un pin análogo"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        if not(type(value)==type(1)): raise PynguinoError(6)
        if value<0 or value>1023: raise PynguinoError(7)
        
        self.pinguino.write('write')
        self.pinguino.write(str(pin).rjust(2,'0'))
        self.pinguino.write('analog')
        self.pinguino.write(str(value).rjust(4,'0'))
        
    #----------------------------------------------------------------------
    def GetPinMode(self,pin):
        """Retorna el modo de un pin basado en la informacion enviada"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        
        if type(self.pin_modes[pin])==type(1): return 'output'
        else: return self.pin_modes[pin]
    
    #----------------------------------------------------------------------
    def GetPinState(self,pin):
        """Retorna el estado de un pin basado en la informacion enviada"""
        if not(type(pin)==type(1)): raise PynguinoError(2)
        
        if type(self.pin_states[pin])==type(1): return 'low'
        else: return self.pin_states[pin]
        
    #----------------------------------------------------------------------
    def allInput(self):
        """Establece todos los pines como entrada"""
        self.pinguino.write('allInput')
    
    #----------------------------------------------------------------------
    def allOutput(self):
        """Establece todos los pines como salida y los fija en estado bajo"""
        self.pinguino.write('allOutput')
    
    #----------------------------------------------------------------------
    def allHigh(self):
        """Establece todos los pines como salida y los fija en estado alto"""
        self.pinguino.write('allHigh')
        
    #----------------------------------------------------------------------
    def allLow(self):
        """Establece todos los pines como salida y los fija en estado bajo"""
        self.pinguino.write('allLow')
        
    #----------------------------------------------------------------------
    def reset(self):
        """Resetea el pinguino"""
        self.pinguino.write('reset')
        
    #----------------------------------------------------------------------
    def setProcessingTimeout(self,value):
        """Cabia el timeout del interprete"""
        self.pinguino.setTimeout(value)
    
    #----------------------------------------------------------------------
    def setProcessingWriteTimeout(self,value):
        """Cambia el writeTimeout del interprete"""
        self.pinguino.setWriteTimeout(value)
    
    #----------------------------------------------------------------------
    def ProcessingClose(self):
        """Cierra el puerto"""
        self.pinguino.close()
    
    #----------------------------------------------------------------------
    def GetPinguinoCode(self):
        print """      
//pynguino

// Yeison Nolberto Cardona Álvarez 2011
// Página del proyecto: http://code.google.com/p/pinno-processing/
// contacto: yeison.eng@gmail.com, @YeisonEng

//Si desea utilizar el Pic 18F4550 en vez de el Pic 18F2550 (por defecto),
//descomentar la siguiente línea
//#define PIC18F4550

#include <stdlib.h>

#define RunLed PORTAbits.RA4 //Para controlar el Led de run

int cond;
int i;
int pin;
int value;
unsigned char receivedbyte;
unsigned char local_identificador[15];
unsigned char lectura[15];
unsigned char pin_n[2];
unsigned char mode[6];
unsigned char type[7];
char lectura_n[5];
unsigned char digitalwrite_n[1];
unsigned char analogwrite_n[4];
unsigned char function[15];


void setup(){
RunLed=1;
}//setup

void loop(){

cond=1;
while (cond){	//Creamos un ciclo hasta hasta realizar una lectura
	receivedbyte=CDC.read(local_identificador);
	local_identificador[receivedbyte]=0;
	if (receivedbyte>0)
		if (strcmp(local_identificador, "PinnoProcessing")==0){	//Comparamos la lectura con un identificador para comprobar una comunicación con el módulo Pynguino
			CDC.print("Conectado",9);
			RunLed=0;
			cond=0;}	}

while (1){	//Se crea un ciclo en el que se realizan todas las acciones

cond=1;
while (cond){	//Leemos un cadena para identificar la acción
	receivedbyte=CDC.read(lectura);
	lectura[receivedbyte]=0;
	if (receivedbyte>0) cond=0;}

if (strcmp(lectura, "setup")==0){	//Si la acción corresponde a modificar el modo de un pin
	cond=1;
	while (cond){	//Leemos el número del pin
		receivedbyte=CDC.read(pin_n);
		pin_n[receivedbyte]=0;
		pin=atoi(pin_n);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	//Leemos el modo del pin (input o outout)
		receivedbyte=CDC.read(mode);
		mode[receivedbyte]=0;
		if (receivedbyte>0) cond=0;}
		if (strcmp(mode, "input")==0) pinMode(pin,INPUT);	//Definimos un el pin como entrada o salida
		else if (strcmp(mode, "output")==0) pinMode(pin,OUTPUT);
	}//setup_n

else if (strcmp(lectura, "read")==0){ //Si la acción corresponde a leer un estado
	cond=1;
	while (cond){	//Leemos el número del pin
		receivedbyte=CDC.read(pin_n);
		pin_n[receivedbyte]=0;
		pin=atoi(pin_n);
		if (receivedbyte>0) cond=0;}
		
	cond=1;
	while (cond){	//Leemos el tipo de lectura
		receivedbyte=CDC.read(type);
		type[receivedbyte]=0;
		if (receivedbyte>0) cond=0;}
		
	if (strcmp(type, "digital")==0){	//Si queremos leer un pin digital
		if (digitalRead(pin)==0) CDC.print("0",1);
		else if (digitalRead(pin)==1) CDC.print("1",1);}

	else if (strcmp(type, "analog")==0){	//Ó un pin análogo
		value=analogRead(pin);
		itoa(value, lectura_n, 10);
		CDC.print(lectura_n,5);}
	}//read_n

else if (strcmp(lectura, "write")==0){	//Si la acción corresponde a fijar el estado de un pin
	cond=1;
	while (cond){	//Leemos el número del pin
		receivedbyte=CDC.read(pin_n);
		pin_n[receivedbyte]=0;
		pin=atoi(pin_n);
		if (receivedbyte>0) cond=0;}
		
	cond=1;
	while (cond){	//Leemos el tipo de valor a fijar
		receivedbyte=CDC.read(type);
		type[receivedbyte]=0;
		if (receivedbyte>0) cond=0;}

	if (strcmp(type, "digital")==0){	//Si es del tipo digital
	cond=1;
	while (cond){
		receivedbyte=CDC.read(digitalwrite_n);
		digitalwrite_n[receivedbyte]=0;
		if (receivedbyte>0) cond=0;}
		if (digitalwrite_n[0]=='1') digitalWrite(pin,HIGH);	//establecemos el valor correspondiente
		else if (digitalwrite_n[0]=='0') digitalWrite(pin,LOW);}

	else if (strcmp(type, "analog")==0){	//Si es del tipo análogo
	cond=1;
	while (cond){
		receivedbyte=CDC.read(analogwrite_n);	//Leemos el valor a fijar
		analogwrite_n[receivedbyte]=0;
		if (receivedbyte>0){
			cond=0;
			analogWrite(pin,atoi(analogwrite_n));}	}	}	//y lo estblecemos
	}//write

else if (strcmp(lectura, "allOutput")==0){	//Si la acción corresponde a fijar todos los pines como salida
	for (i=0;i<=17;i++){
		pinMode(i,OUTPUT);
		digitalWrite(i,LOW);}	//también los dejamos en un estado bajo
	}//all_output

else if (strcmp(lectura, "allInput")==0){	//Si la acción corresponde a fijar todos los pines como entrada
	for (i=0;i<=17;i++)
		pinMode(i,INPUT);
	}//all_input

else if (strcmp(lectura, "allHigh")==0){	//Si la acción corresponde a poner en alto todos los pines
	for (i=0;i<=17;i++){
		pinMode(i,OUTPUT);
		digitalWrite(i,HIGH);}
	}//all_high

else if (strcmp(lectura, "allLow")==0){	//Si la acción corresponde a poner en bajo todos los pines
	for (i=0;i<=17;i++){
		pinMode(i,OUTPUT);
		digitalWrite(i,LOW);}
	}//all_low
	
else if (strcmp(lectura, "reset")==0) reset();	//Si la acción corresponde a resetear pinguino

receivedbyte=0;
}//ciclo de acciones
}//loop"""
