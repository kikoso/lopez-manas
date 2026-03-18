---
date: '2008-02-04T16:09:43+00:00'
draft: false
slug: navegacion-anonima
title: Navegación anónima
---

Muchas veces hemos navegado por Internet con nuestro navegador favorito y sabemos que vamos dejando nuestro rastro allá por donde vamos, o bién queremos opinar en algún foro como una persona distinta, o bién queremos votar más de una vez en alguna votación, mandar un correo electrónico y que no se sepa el origen, etc etc etc.  En el otro lado de la balanza, realizar un ataque sobre un objetivo o dejar una dirección IP falsa en un registro es otro de los propósitos

Pues bién, la solución a todos estos problemas son los proxys abiertos, los cuales son <a href="http://es.wikipedia.org/wiki/Proxy" target="_blank">proxys</a> mal configurados por administradores o usuarios particulares que los tienen para compartir una conexión a Internet y por tanto cualquiera puede usar ese mismo proxy desde fuera de la red donde se encuentra.

Configurando la conexión en nuestro navegador web para que pase a través de un proxy abierto, se elimina la ip que poseemos y se sustituye por la ip del proxy (en algunos casos se pasa como cabecera de la petición a la página con lo que no se elimina del todo), pudiendo asi interactuar con la web que hayamos visitado sin que sepa realmente quienes somos (normalmente no se sabe quienes somos, y menos si tenemos ip dinámica, pero con esto se dobla el anonimato en la navegación).

Se puede acceder a ftp, http, https desde un proxy (siempre que este configurado para permitirlo) y conectarnos a otros puertos si usamos la tecnología SOCKS v4 o v5 (igualmente debe estar configurado para permitirlo), con lo que prácticamente se
puede hacer de todo en internet a través de un proxy. Es más, si estas en tu empresa y te capan todos los puertos menos el puerto 80 para salir a Internet, con un proxy podrás acceder al resto de puertos sin mayor peoblema.

Hay muchas listas de proxys abiertos por Internet, en <a href="http://en.wikipedia.org/wiki/Open_proxy" target="_blank">Wikipedia</a> tenemos más información al respecto