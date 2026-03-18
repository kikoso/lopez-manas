---
date: '2008-04-07T19:16:36+00:00'
draft: false
slug: tecnicas-de-ofuscacion-sencillas-para-troyanos
title: Técnicas de ofuscación sencillas para troyanos
---

Hola,

Recientemente tuve que conectarme en un ordenador desconocido para consultar el correo. El ordenador no provenía de una fuente hostil, pero si era potencialmente peligroso conectarme allí sin ningún tipo de prevención. Me llevó a pensar como podría saltear las típicas técnicas de captación de contraseñas utilizadas por malware o cualquier tipo de software malicioso.

Una manera muy típica de capturar las contraseñas es mediante el uso de <a target="_blank" href="http://es.wikipedia.org/wiki/Keylogger">keyloggers</a>. Un keylogger es un programa que captura todas las pulsaciones de teclado, entre ellas todas las contraseñas que debemos teclear para poder acceder a distintos servicios a través de internet (foros, clientes de mensajería.... y hasta otros más sensibles como correo electrónico o bancos). Tras ello, las envían a algún remoto lugar, en el que seguramente no se limiten a hacer un estudio estadístico. Los keyloggers son programas sencillos, que no siempre son detectados por los antivirus y que pueden ser introducidos con mucha facilidad en un ordenador remoto (bajando un "programa de conexión" de una página pornográfica, de warez o similar, a través de redes P2P, por email...). Las vías de ataque son numerosas, y están en continuo cambio y evolución.

Estos keyloggers generalmente almacenan la información en un fichero de texto. Algunos más sofisticados son capaces de discernir todo el comportamiento del usuario, de manera que si escribimos:

<code>hotmail.compepitoeldelospalotescontraseñamalaQuerido ciervo</code>

...sabrá en que sitio hemos introducido qué datos.

Cuando nos conectamos en un cyber, o en un ordenador desconocido, podemos evitar estos problemas. La técnica más inmediata es escribir en otras pestañas o lugares, ya que el keylogger sólo detectará las letras que hemos pulsado, y no donde lo hemos hecho. Por ejemplo, si tras escribir hotmail.com, y el usuario, escribimos letras aleatorias en la ventana de búsqueda al mismo tiempo que la contraseña, el keylogger podría recibir algo como lo que sigue:

<code>hotmail.compepitoeldelospalotesdfsdCjdoatndsftdarkeoosppejjñkakiMjaolka</code>

Con lo que habremos evitado satisfactoriamente el primer vector de ataque en estas máquinas.

Esta sencilla solución de baja tecnología no evita todos los problemas. Como de costumbre ha de ser utilizada en combinación con otros métodos, pero es sencilla de poner en práctica. 

Existen <a target="_blank" href="http://www.hispasec.com/laboratorio/troyano_captura_banesto.htm">troyanos</a> que realizan capturas de pantalla sobre el foco del ratón cuando lo pulsamos, con lo cual este método no sería del todo útil.
