---
date: '2009-01-09T14:50:26+00:00'
draft: false
slug: backup-en-mysql
title: Backup en MySQL
---

Tradicionalmente he ejecutado backups en MySQL utilizando únicamente comandos desde consola. Se podía conseguir de una manera sencilla utilizando código SQL. Para hacer los backups bastaba con:

<pre lang="mysql">
BACKUP TABLE example TO `/backups/` 
</pre>
Para posteriormente restaurar la copia de seguridad:

<pre lang="mysql">
RESTORE TABLE pedidos FROM `/backups/`
</pre>

Hay que mencionar que con este comando obtenemos una copia de seguridad de los ficheros que integran la BD y no un script SQL, que suele ser más sencillo de usar. Además, este comando sólo funciona con las tablas de tipo MyIsam, lo que deja fuera un porcentaje de tablas no desdeñable.

Pasé a utilizar <a target="_blank" href="http://dev.mysql.com/downloads/gui-tools/5.0.html">MySQL administrator</a>, que como todas las aplicaciones que ejecutan desde una GUI mejoran notablemente la velocidad de ejecución de ciertas tareas rutinarias, al reducirlas a unos cuantos clicks de ratón. No obstante, recientemente he tenido que hacer un backup de una máquina con ciertas peculiaridades: se trataba de un servidor virtual "subalojado" en otro servidor, con lo que el acceso desde MySQL administrator no era trivial (debía tunelizarlo para poder acceder al puerto del servidor MySQL de la máquina virtual, lo que añadía un tiempo extra a la ejecución de la tarea).

Lo solucioné usando <strong>mysqldump</strong>, una sencilla aplicación. Tan sólo basta con los dos siguientes comandos para hacerla funcionar:

<pre lang="bash">mysqldump --opt --password=miclave --user=miuser mibasededatos > archivo.sql</pre>

<pre lang="bash">mysql --password=miclave --user=miuser mibase < archivo.sql</pre>

Como se hace evidente, mysqldump almacena en un script el backup, con lo que es fácilmente mantenible, modificable y versátil.
