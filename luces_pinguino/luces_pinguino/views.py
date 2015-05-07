# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import LucesForm
import json, socket, sys


def home(request):
   quiere_hackear = False
   encendido = [0]
   
   HOST, PORT = "localhost", 55555
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   if x_forwarded_for:
      ip = x_forwarded_for.split(',')[0]
   else:
      ip = request.META.get('REMOTE_ADDR')
   print ip
   
   if request.method == 'POST':
      form = LucesForm(request.POST)
      
      if form.is_valid():
         estado = form.cleaned_data['estado']
         if not(estado=='si' or estado=='no'): quiere_hackear = True
         if not(quiere_hackear):
            #import PBpinguino
            #a = PBpinguino.TAPinguino()
            #a.pin_mode(10, "output")
            
            if estado == 'si':
               #a.digital_write(10, "high")
               try:
                  sock.connect((HOST, PORT))
                  sock.sendall("1\n")
               finally:
                  sock.close()
               data = [1]
               json.dump(data, open('luces_pinguino/encendido.json', 'w'))
            else:
               #a.digital_write(10, "low")
               try:
                  sock.connect((HOST, PORT))
                  sock.sendall("0\n")
               finally:
                  sock.close()
               data = [0]
               json.dump(data, open('luces_pinguino/encendido.json', 'w'))
      else:
         quiere_hackear = True
      try:
         encendido = json.loads(open("luces_pinguino/encendido.json").read())
      except Exception, e:
         print "Hubo un error al intentar leer el archivo de configuracion:"
         print "La excepcion original es:"
         raise e
   else:
      try:
         encendido = json.loads(open("luces_pinguino/encendido.json").read())
      except Exception, e:
         print "Hubo un error al intentar leer el archivo de configuracion:"
         print "La excepcion original es:"
         raise e
      

   ctx = {
   'encendido' : encendido[0],
   'quiere_hackear' : quiere_hackear
   }
   return render_to_response('index.html', ctx, context_instance=RequestContext(request))

def acerca(request):
   ctx = {
      'name'    : 'Control de Luces',
      'version' : '1.0',
      'autor'   : 'Tomás Vielma',
      'website' : 'http://tomivs.com/'
   }
   return render_to_response('acerca.html', ctx, context_instance=RequestContext(request))
