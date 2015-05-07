luces-pinguino
==============
Proyecto/Experimento con el cual se busca controlar una o varias luces usando la placa Pingüino (PIC18F4550) conectada al servidor web por USB.

Requisitos
==========
* Placa Pingüino con su cable USB
* `Git`
* `Python 2.7.x`
* `Django`
* Tener previamente instalada la `IDE de Pingüino` funcionando correctamente

Instalación
===========
Es necesario guardar el PDE de la librería `pynguino` en nuestro Pingüino, por lo tanto, vamos a descargar su contenido y, posteriormente subirlo, usando la IDE.

Entonces:
* Descargar el archivo de: `http://tomivs.com/recursos/pynguino.pde` y subirlo a nuestro Pingüino usando la IDE.

Luego de eso, nuestro Pingüino estará listo para ser controlado por USB con la librería `pynguino`

**NOTA**: Después de subir el PDE y conectar nuestro Pingüino, el LED de ejecución no encenderá sino hasta que comienze a comunicarse con la computadora.


* Clonar el repositorio: `$ git clone https://github.com/tomivs/luces-pinguino.git`
* Entramos a la carpeta del repositorio: `$ cd luces-pinguino`
* Conectamos nuestra placa Pingüino por USB

**NOTA**: Esto funciona con un LED conectado al PIN número `10` de nuestro Pingüino, si se desea cambiar el PIN de salida u otras cosas, es necesario modificar el archivo `daemon.py`

* Ejecutamos el Servidor Socket como root: `$ sudo python daemon.py `

**NOTA**: El Servidor Socket debe mantenerse ejecutando en una consola, si se cierra, no va a seguir funcionando. Por otra parte, luego de ejecutar este comando satisfactoriamente el LED de ejecución de nuestro Pingüino debería encender.

* En otra consola aparte entramos en el directorio del repositorio y luego en el de Django: `$ cd luces_pinguino`
* Y ejecutamos el servidor web: `$ python2 manage.py runserver`

Luego de eso, podremos abrir en el navegador la dirección: `http://localhost:8000`

Con eso, solo se podrá acceder a esa dirección desde la misma computadora, si en su lugar, queremos que sea visible por otras personas conectadas a tu misma red debemos ejecutarlo de esta forma: `$ python2 manage.py runserver 0.0.0.0:8000`

Después de ejecutar eso, si la IP de nuestra computadora es: `192.168.1.15` entonces solo será necesario abrir desde cualquier navegador (móvil o de escritorio), `http://192.168.1.15:8000` incluso, podemos colocarlo en el puerto `80` pero este debe estar libre y es necesario ejecutarlo como root.
