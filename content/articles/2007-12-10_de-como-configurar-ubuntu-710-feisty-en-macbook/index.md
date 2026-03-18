---
date: '2007-12-10T15:18:54+00:00'
draft: false
slug: de-como-configurar-ubuntu-710-feisty-en-macbook
title: De como configurar Ubuntu 7.10 Feisty en Macbook
---

Tras un tiempo buscando información, en ocasiones dispersa, he conseguido configurar para la mayor parte de las funcionalidades que utilizo con frecuencia.

El Macbook que poseo es el previo al modelo actual, liberado por Apple el mes pasado.  En concreto es el modelo intermedio, con 100 G. de disco duro, 1 G. de ram y un procesador Intel Core 2 Duo a 2.16 Ghz. La tarjeta de red inalámbrica posee un chipset Atheros en los nuevos modelos. Este chipset nos proporciona multitud de ventajas para trabajar con nuestra tarjeta y realizar algunas tareas específicas.

Dado que cualquier visitante puede encontrar de utilidad ayuda para la configuración del Macbook, he aquí una pequeña guía al respecto:

<!--more-->

1.- El primer cambio a realizar debería ser configurar <strong>el teclado</strong>. Macintosh, en el lugar que correspondería a AltGr, viene con una manzanita que nos impide teclear bastante símbolos. En el escritorio por defecto (GNome) basta con acceder a las preferencias del teclado y marcar la opción <em>Pulsar la tecla Windows derecha para elegir el 3er nivel</em> en la pestaña <em>Opciones de distribución. </em>No obstante este cambio sólo afectaría al usuario actual: si quisiésemos extenderlo a toda la máquina, deberíamos hacer lo siguiente:

<em>sudo sed -i~ ''s/RCTL/KPEN/'' /etc/X11/xkb/symbols/pc</em>

<em>sudo sed -i~ ''/xkb_symbols "ralt_switch" {/a  include "level3(rwin_switch)"''</em>

Con este comando también podríamos utilizar la tecla de Control inferior

2.- La segunda acción a ejecutar bien podría ser la configuración de la <strong>tarjeta de red</strong>. Por defecto, la instalación de Ubuntu no nos la reconocerá, por lo que deberemos hacer unos pequeños trucos ayudados de ndiswrapper para hacerla funcionar.

Actualicé la versión que tenía por defecto en Ubuntu a la última disponible en el repositorio (manualmente se puede encontrar <a href="http://superb-east.dl.sourceforge.net/sourceforge/ndiswrapper/" target="_blank">aquí</a>). Si acabas de instalar Linux, te recomiendo el mágico poder de las herramientas de compilado básicas. Pueden ser instaladas con un sencillo <em>sudo aptitude install build-essential. </em>

Una vez que tengas la última versión de ndiswrapper instalada en tu ordenador, deberías descargar un paquete de drivers adecuado para poder hacer funcionar la tarjeta. Los drivers que use los descargué de la página de drivers de Lenovo, pero funcionan correctamente. Puedes conseguirlos en el siguiente <a href="http://www-307.ibm.com/pc/support/site.wss/document.do?lndocid=MIGR-66449" title="lenovo support for wireless driver">enlace</a>.

Si quieres asegurarte que el driver es compatible con tu sistema, puedes ejecutar los siguientes dos comandos, y verificar que el hardware es soportado:

<em>lspci</em>

Esto es lo que me contestó lspci
02:00.0 Network controller: Atheros Communications, Inc. Unknown device 0024 (rev 01)

Entonces, un sencillo

<em>lspci -n | grep 02:00.0 </em>(nótese que estoy filtrando la salida que he encontrado en el paso anterior, si has obtenido algo distinto deberías cambiarlo)

El resultado que obtienes aquí es la PCI-ID de tu tarjeta, (por ejemplo: 02:00.0 0280: 168c:0024 (rev 01)
). En este momento deberías coger <em>168c:0024</em> y comprobar si es compatible en la <a href="http://ndiswrapper.sourceforge.net/mediawiki/index.php/List" title="ndiswrapper supported hardware list">lista de hardware de ndiswrapper</a>. (Puede parecer complicado, pero en realidad, una vez que tienes localizada la compatibilidad, lo siguiente será inmediato)

Ahora que has comprobado el ID de tu tarjeta y descargado el driver, deberías instalarlo con:

<em>sudo ndiswrapper -i NET5416.INF</em>

Ahora, comprobaremos si el sistema está contento con este driver:

<em>sudo ndiswrapper -l</em>

Con suerte deberás obtener una salida similar a la siguiente:
<em>net5416 : driver installed
device (168C:0024) present</em>

Si ha ido todo bien hasta aquí (nótese de nuevo que el número de dispositivo concuerde con la información que te proporcionó lspci), puedes cargar el módulo ndiswrapper y empezar a navegar.

<em>sudo modprobe ndiswrapper</em>

Comprueba si el dispositivo ha sido creado correctamente:

<em>iwconfig</em>

...y que lo cargarás de manera automática en cada reinicio del ordenador

<em>sudo ndiswrapper -m</em>

En este momento tu tarjeta debería estar funcionando correctamente. Sólo te quedaría configurarla acorde a la red bajo la que te encuentres, bien usando el nm-applet de GNome, bien usando la línea de comandos.

3.- Si habéis intentado subir, bajar o desactivar el sonido desde el teclado, veréis que, a pesar de que un icono luce en la pantalla, no tiene ningún efecto sobre el sistema.  Esto es porque por defecto estas teclas controlan el canal Master, cuando el canal a controlar debería ser PCM. Para poder modificarlo, accedes a GNome, preferencias de sonido, fila PCM y cierras el diálogo.

4.- La cámara iSight. Para los que no hayáis actualizado a Leopard aquí tenéis un posible juego de instrucciones a segui, sustituyendo sdax por la partición donde tengas instalado Mac:

<em>sudo mount -t hfsplus /dev/sdax /mnt
sudo cp /mnt/System/Library/Extensions/IOUSBFamily.kext/Contents/PlugIns/AppleUSBVideoSupport.kext/Contents/MacOS/* /lib/firmware/2.6.22-14-generic/</em>

También, en /etc/default/acpi-support, edita la línea que empieza con MODULES tal como sigue:
<pre><em>MODULES="isight_usb"</em></pre>
Reinicia para que todos los cambios se efectúen. Una vez que el firmware es funcional, la cámara iSight debería poder ser usada con el programa ekiga o skype, entre otros.

Para instalar Ekiga y todas sus dependencias, haz lo siguiente:

<em>sudo apt-get install ekiga libpt-plugins-v4l2
ekiga </em>
<ol type="1">
	<li>Configuración. Tienes que seleccionar el dispositivo iSight Edit &gt; Preferences &gt; Devices &gt; Video Devices &gt;</li>
	<li>Video plugin: <a href="https://help.ubuntu.com/community/V4L2" class="nonexistent">V4L2</a></li>
	<li>Input device: Built-in iSight</li>
</ol>
Si quieres usar el modo 640 x 480, entonces:

<em>gconftool-2 --type integer --set /apps/ekiga/devices/video/size</em> 1

Queda pendiente:
<ul>
	<li>Hacer funcionar el micrófono integrado en iSight. Con mi versión de kernel (2.6.22-14-generic) puede funcionar un micrófono externo (incorporado).</li>
</ul>