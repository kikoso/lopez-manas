---
date: '2008-01-30T11:53:03+00:00'
draft: false
slug: microfono-y-camara-isight-ubuntu
title: Micrófono y cámara iSight Ubuntu
---

Ayer, tras un tiempo sin volver a intentarlo, di por fin con la clave para poder configurar el micŕofono y la cámara iSight para Ubuntu en Macintosh. En el mundo de los ordenadores, si tenemos dos soluciones, la que será más correcta y menos problemática será la más sencilla. Pues bien, el problema al que me enfrentaba... era que por defecto, el volumen está al mínimo.

Para solucionarlo, basta con irse al control de volumen (doble click sobre el icono de la barra de tareas), <em>Preferencias,</em> marcamos la casilla <em>Captura</em> y veremos que tenemos una pestaña, <em>Grabando.</em> Basta con subir el volumen :D

Para hacer funcionar la cámara integrada iSight, basta con seguir estos pasos (tomado de los foros de Ubuntu):
<em>* sudo modprobe -r uvcvideo
* sudo mv /lib/modules/$(uname -r)/ubuntu/media/usbvideo/uvcvideo.ko /lib/modules/$(uname -r)/ubuntu/media/usbvideo/uvcvideo.ko.original</em>
<p style="margin: 5px 20px 20px">&nbsp;</p>
Instalamos ciertas librerías que tal vez necesitemos.
<em>*sudo apt-get install libusb-0.1-4 libusb-dev linux-headers-$(uname -r)</em>

Descargamos el nuevo  todo en uno, con firmware de autocarga, como ha sido proporcionado por Ivan N. Zlatev by pinchando <a href="http://files.i-nz.net/projects/linux-kernel/isight/uvcvideo-isight.tar.gz" target="_blank"><u><em>aquí</em></u></a> .
<p style="margin: 5px 20px 20px">&nbsp;</p>
Nos movemos al directorio donde está el tar, y descomprimimos.
<em>* tar -xvf uvcvideo-isight.tar.gz
</em>
<p style="margin: 5px 20px 20px">&nbsp;</p>
Ahora construimos e instalamos
<em>* cd against-revision-140
* sudo make
* sudo make install
</em>

Finalmente, cargamos el módulo

* <em>sudo modprobe uvcvideo</em>
<p style="margin: 5px 20px 20px">&nbsp;</p>
Ahora debería funcionar. Aquí hay una prueba con la que deberíamos verlo en acción.

* <em>gst-launch-0.10 v4l2src ! video/x-raw-yuv,format=\\(fourcc\\)UYVY,width=640,height=480 ! ffmpegcolorspace ! ximagesink</em>