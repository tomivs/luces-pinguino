#! /usr/bin/python
#-*- coding: utf-8 -*- 

try: import serial
except: PynguinoError(3)

import os
from raiseError import PynguinoError
        
########################################################################
class PinguinoLCD():
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
    def LCD_setCursor(self,par1,par2):
        if type(par1)!=type(1): raise PynguinoError(13)
        if type(par2)!=type(1): raise PynguinoError(13)
        
        self.pinguino.write('setCursor')
        self.pinguino.write(str(par1).rjust(2,'0'))
        self.pinguino.write(str(par2).rjust(2,'0'))
        
    #----------------------------------------------------------------------
    def LCD_begin(self,par1,par2):
        if type(par1)!=type(1): raise PynguinoError(13)
        if type(par2)!=type(1): raise PynguinoError(13)
        
        self.pinguino.write('begin')
        self.pinguino.write(str(par1).rjust(2,'0'))
        self.pinguino.write(str(par2).rjust(2,'0'))
        
    #----------------------------------------------------------------------
    def LCD_print(self,to_send):
        """LCD_prind soporta todo formato (int, float, string)"""
        if not ((type(to_send)==type(1)) or (type(to_send)==type(1.0)) or (type(to_send)==type("N"))): raise PynguinoError(14)
        
        if type(to_send)==type(1): to_send=str(to_send)
        if type(to_send)==type(1.0): to_send=str(to_send)
        self.pinguino.write('print')
        self.pinguino.write(to_send)
        
    #----------------------------------------------------------------------
    def LCD_home(self):
        self.pinguino.write('home')
        
    #----------------------------------------------------------------------
    def LCD_clear(self):
        self.pinguino.write('clear')   
        
    #----------------------------------------------------------------------
    def LCD_leftToRight(self):
        self.pinguino.write('leftToRight')   
        
    #----------------------------------------------------------------------
    def LCD_rightToLeft(self):
        self.pinguino.write('rightToLeft')   
        
    #----------------------------------------------------------------------
    def LCD_scrollDisplayLeft(self):
        self.pinguino.write('scrollDisplayLeft')           
        
    #----------------------------------------------------------------------
    def LCD_scrollDisplayRight(self):
        self.pinguino.write('scrollDisplayRight')   
        
    #----------------------------------------------------------------------
    def LCD_blink(self):
        self.pinguino.write('blink')     
        
    #----------------------------------------------------------------------
    def LCD_cursor(self):
        self.pinguino.write('cursor')   
        
    #----------------------------------------------------------------------
    def LCD_display(self):
        self.pinguino.write('display')   
        
    #----------------------------------------------------------------------
    def LCD_noBlink(self):
        self.pinguino.write('noBlink')
        
    #----------------------------------------------------------------------
    def LCD_noCursor(self):
        self.pinguino.write('noCursor') 
        
    #----------------------------------------------------------------------
    def LCD_noDisplay(self):
        self.pinguino.write('noDisplay')         
      
    #----------------------------------------------------------------------
    def LCD_autoscroll(self):
        self.pinguino.write('autoscroll') 
        
    #----------------------------------------------------------------------
    def LCD_command(self,value):
        if type(value)!=type(1): raise PynguinoError(13)
        
        self.pinguino.write('command') 
        self.pinguino.write(str(value)) 
        
    #----------------------------------------------------------------------
    def LCD_write(self,value):
        if type(value)!=type(1): raise PynguinoError(14)
        
        self.pinguino.write('write') 
        self.pinguino.write(str(value))     
        
    #----------------------------------------------------------------------
    def LCD_contraste(self,pin,value):
        self.pinguino.write('contraste')
        self.pinguino.write(str(pin).rjust(2,'0'))
        self.pinguino.write(str(value).rjust(4,'0'))
        
    #----------------------------------------------------------------------
    def LCD(self,RS,E,P0,P1,P2,P3,P4,P5,P6,P7):
        parametros=[RS,E,P0,P1,P2,P3,P4,P5,P6,P7]
        self.pinguino.write('LCDinit')
        for parametro in parametros:
            self.pinguino.write(str(parametro).rjust(2,'0'))
            
    #----------------------------------------------------------------------
    def LCD_saveChar(self,position,char):
        if type(position)!=type(1): raise PynguinoError(16)

        self.LCD_command(position);
        for fila in char:
            if type(fila)!=type(1): raise PynguinoError(16)
            self.LCD_write(fila)     
            
    #----------------------------------------------------------------------
    def GetPinguinoLCDCode(self):
        print """             
//pynguinoLCD
 
// Yeison Nolberto Cardona Álvarez 2011
// Página del proyecto: http://code.google.com/p/pinno-processing/
// https://sites.google.com/site/yeisoneng/
// contacto: yeison.eng@gmail.com, @YeisonEng

//Si desea utilizar el Pic 18F4550 en vez de el Pic 18F2550 (por defecto),
//descomentar la siguiente línea
//#define PIC18F4550

#include <stdlib.h>

#define RunLed PORTAbits.RA4 //Para controlar el Led de run

int par_1;
int par_2;
float par_3;
int cond;
int pin;
int RS,E,P0,P1,P2,P3,P4,P5,P6,P7;
unsigned char receivedbyte;
unsigned char local_identificador[15];
unsigned char lectura[20];
unsigned char par1[10];
unsigned char par2[10];
unsigned char to_print[21];
unsigned char analogwrite_n[4];
unsigned char pin_n[2];

void setup(){
RunLed=1;
lcd.clear();
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

if (strcmp(lectura, "contraste")==0){	
	cond=1;
	while (cond){
		receivedbyte=CDC.read(pin_n);
		pin_n[receivedbyte]=0;
		pin=atoi(pin_n);
		if (receivedbyte>0) cond=0;}
		pinMode(pin,OUTPUT);
	cond=1;
	while (cond){
		receivedbyte=CDC.read(analogwrite_n);	
		analogwrite_n[receivedbyte]=0;
		if (receivedbyte>0) cond=0;}
		analogWrite(pin,atoi(analogwrite_n));
	}//contraste

if (strcmp(lectura, "LCDinit")==0){
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		RS=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		E=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P0=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P1=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P2=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P3=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P4=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P5=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P6=atoi(par1);
		if (receivedbyte>0) cond=0;}
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		P7=atoi(par1);
		if (receivedbyte>0) cond=0;}
			
	lcd(RS,E,P0,P1,P2,P3,P4,P5,P6,P7);		
	}//LCDinit

if (strcmp(lectura, "home")==0){	//Si la acción corresponde a rotornarnos a la primera posición
		lcd.home();		
	}//home

if (strcmp(lectura, "clear")==0){	//Si la acción corresponde a limpiar el LCD
		lcd.clear();		
	}//clear

if (strcmp(lectura, "leftToRight")==0){	
		lcd.leftToRight();		
	}//leftToRight
	
if (strcmp(lectura, "rightToLeft")==0){	
		lcd.rightToLeft();		
	}//rightToLeft

if (strcmp(lectura, "scrollDisplayLeft")==0){	//Si la acción corresponde a mover un espacio de derecha a izquierda
		lcd.scrollDisplayLeft();		
	}//scrollDisplayLeft

if (strcmp(lectura, "scrollDisplayRight")==0){	//Si la acción corresponde a mover un espacio de izquierda a derecha
		lcd.scrollDisplayRight();		
	}//scrollDisplayRight

if (strcmp(lectura, "autoscroll")==0){	
		lcd.autoscroll();		
	}//autoscroll

if (strcmp(lectura, "blink")==0){	
		lcd.blink();		
	}//blink

if (strcmp(lectura, "cursor")==0){	
		lcd.cursor();		
	}//cursor

if (strcmp(lectura, "display")==0){	
		lcd.display();		
	}//display

if (strcmp(lectura, "noBlink")==0){	
		lcd.noBlink();		
	}//noBlink

if (strcmp(lectura, "noCursor")==0){	
		lcd.noCursor();		
	}//noCursor

if (strcmp(lectura, "noDisplay")==0){
		lcd.noDisplay();		
	}//noDisplay

if (strcmp(lectura, "command")==0){
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		par_1=atoi(par1);
		if (receivedbyte>0) cond=0;}	
		lcd.command(par_1);		
	}//comand

if (strcmp(lectura, "write")==0){
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		par_1=atoi(par1);
		if (receivedbyte>0) cond=0;}	
		lcd.write(par_1);		
	}//write

if (strcmp(lectura, "setCursor")==0){	
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		par_1=atoi(par1);
		if (receivedbyte>0) cond=0;}	
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par2);
		par2[receivedbyte]=0;
		par_2=atoi(par2);
		if (receivedbyte>0) cond=0;}
	cond=1;
	lcd.setCursor(par_1, par_2);
	}//setCursor

if (strcmp(lectura, "begin")==0){	
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par1);
		par1[receivedbyte]=0;
		par_1=atoi(par1);
		if (receivedbyte>0) cond=0;}		
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(par2);
		par2[receivedbyte]=0;
		par_2=atoi(par2);
		if (receivedbyte>0) cond=0;}
	lcd.begin(par_1, par_2);
	}//begin

if (strcmp(lectura, "print")==0){	
	cond=1;
	while (cond){	
		receivedbyte=CDC.read(to_print);
		to_print[receivedbyte]=0;
		if (receivedbyte>0) cond=0;}		
		lcd.print(to_print);		
	}//print
		
}//ciclo de acciones
}//loop"""