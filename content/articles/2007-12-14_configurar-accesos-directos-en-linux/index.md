---
date: '2007-12-14T14:15:46+00:00'
draft: false
slug: configurar-accesos-directos-en-linux
title: Configurar accesos directos en Linux
---

Una aplicación interesante en Linux es aquella que nos permite lanzar una consola con tan sólo presionar una tecla, un navegador, el cliente de correo... pero no sólo eso, también nos permite ejecutar comandos más específicos (montar una imagen o unidad virtual, activar la tarjeta WiFi con ndiswrapper, etc). En realidad es bastante sencillo.

En mi Macintosh buscaba una aplicación que darle a mi tecla manzanita, tan útil en mi Leopard, tan poco útil en mi Ubuntu. Decidí asignarle la consola, para no tener que llevar el botón del puntero continuamente hasta el acceso directo. Para ello, basta seguir los siguientes pasos:

1.- Obtener la información numérica sobre la tecla. Para ello nos dirigimos a un terminal y escribimos el comando <strong>xev</strong>. A partir de ahora, veremos la información que se genera al apretar cualquiera de las teclas de nuestro teclado:

<em>KeyPress event, serial 31, synthetic NO, window 0x3600001,
root 0x59, subw 0x3600002, time 3636949642, (50,44), root:(725,96),
state 0x2000, <strong>keycode 46</strong> (keysym 0x6c,<strong> l</strong>), same_screen YES,
XLookupString gives 1 bytes: (6c) "l"
XmbLookupString gives 1 bytes: (6c) "l"
XFilterEvent returns: False
</em>
La información destacada en negrita es la que nos interesa para nuestros propósitos.

Ahora, ejecutaremos gconf-editor para asociar la pulsación a un evento. Nos dirigiremos hacia apps-&gt;metacity-&gt;global-keybindings-&gt;run_command_1 y le daremos el valor que hemos recibido del anterior comando (bien el nombre bien el valor numérico). En el caso de la tecla de windows, por ejemplo, el valor típico es <strong>Super_L</strong>.

Ahora abrimos la clave apps-&gt;metacity-&gt;keybinding_commands-&gt;command_1 e introducimos el comando que queramos ejecutar. En el caso de la consola, gnome-terminal.

Recordad que este sistema sólo funciona, lógicamente, con Gnome. Cada entorno tiene sus variantes.

Un saludo.