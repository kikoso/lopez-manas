---
date: '2009-01-14T16:41:56+00:00'
draft: false
slug: resetear-valores-auto-incrementales
title: Resetear valores auto-incrementales
---

Cuando usamos BBDD, y mientras optimizamos configuraciones o interfaces de edición es muy común insertar multitud de valores que posteriormente no necesitaremos, o que formarán parte de un contexto de prueba de la aplicación. En el caso de usar valores autoincrementales como claves primarias de la BBDD (práctica muy común) esto tiene como consecuencia que, al borrar estos datos de prueba, quedan saltos entre los valores incrementales poco estéticos y que en ocasiones no reflejan el estado que uno concibe de la BBDD (secuencias de datos que son insertados conforme a una lógica y un orden). 

Esto puede resolverse de varias maneras: una opción es borrar la tabla y crearla de nuevo (impracticable por naturaleza en la mayoría de los casos). Otra opción más sencilla es utilizar el siguiente comando:

<pre lang="mysql"> 
ALTER TABLE nombre_tabla AUTO_INCREMENT=1
</pre>

Esto permite que el único valor autoincremental que puede existir en una tabla se posicione al valor que le indiquemos.