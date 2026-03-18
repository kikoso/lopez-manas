---
date: '2007-12-20T16:17:53+00:00'
draft: false
slug: instalacion-minima-de-ubuntu
title: 'Instalación mínima de Ubuntu '
---

Un principio básico de seguridad nos dice que hemos de mantener únicamente la cantidad de software indispensable en un sistema operativo con funciones de servidor para hacerlo funcionar. Cualquier aplicación adicional que instalemos, y que no sea realmente necesaria, puede comprometer a nuestro equipo seriamente. Aplicaciones ofimáticas, juegos, navegadores... presentan bugs explotables tales como desbordamientos de buffer, ataques de flood, apertura de puertos... que pueden representar un vector de ataque en el futuro.

Este principio casa mal con el de usabilidad. Muchos técnicos inexpertos instalan cantidad de aplicaciones, a priori innecesarias, desequilibrando la balanza en favor de la facilidad de uso. En concreto, este artículo viene a raíz de haber tenido que montar en el trabajo un servidor de login con Ubuntu.

Ubuntu provee dos versiones básicas de su sistema operativo: la versión Server, y la versión Desktop. A pesar de la obviedad de los nombres, aclararé que la primera se trata de una versión mínima de Linux, mientras que la segunda incluye aplicaciones típicas para un PC de oficina.

A la hora de montar un servidor con ciertos requisitos de seguridad, es ideal utilizar una instalación basada en Ubuntu server, e ir añadiendo los paquetes a medida que lo necesitemos. Pero para el usuario neonato la pregunta es: ¿qué hago con mis X (interfaz gráfica para el escritorio)? En este pequeño artículo intentaré dar una introducción.

Es por esto que en esta entrada veremos como hacer una instalación gráfica mínima de Ubuntu. Es decir, vamos a instalar un sistema que incluya un entorno de escritorio, pero con el mínimo posible de aplicaciones. Aquí vamos:
1.-Una vez instalada tu distribución server, deberemos editar nuestro fichero de repositorio apt para añadir todos los repositorios Universe.
<blockquote><em>sudo nano /etc/apt/sources.list</em></blockquote>
Una vez abierto el fichero, descomentamos las lineas que representan los repositorios “universe” de Ubuntu. Guardamos y salimos.

2.- Actualizamos el repositorio para obtener la última versión de los paquetes
<blockquote><em>sudo apt-get update</em></blockquote>
3- Instalamos las X y el escritorio mínimos (en este caso, Gnome):
<blockquote><em>sudo apt-get install x-window-system-core gnome-core</em></blockquote>
4- Una vez instalado, ejecutamos con <em>startx</em> nuestro nuevo escritorioTodo lo que incluye el menú es: “Accesorios” (con editor de texto y terminal) e “Internet” (con Firefox) y nada más <img src="http://www.kickbill.com/wp-includes/images/smilies/icon_smile.gif" alt=":-)" class="wp-smiley" />

Después de esto, podrás instalar todo aquello que vayas necesitando. De esta manera, te asegurarás de disponer de un servidor con un número mínimo de vectores de ataque, ideal para montar un servidor de cualquier tipo reduciendo al máximo la tasa de fallos.