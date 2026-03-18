---
date: '2008-04-01T17:26:26+00:00'
draft: false
slug: jre-cannot-be-found
title: JRE cannot be found
---

Actualicé mi versión de JDK y mi versión de Eclipse todo al mismo tiempo. Intuía ligeramente que podría darme algún problema realizarlo de manera simultánea. Tras la actualización (incluyendo la descarga de todas las actualizaciones del proyecto Calipso, WPA y otros) , quería depurar una aplicación web, así que cambié a la perspectiva J2EE e intenté inicializar Tomcat desde el panel del servidor. Recibí este amistoso mensaje de error:
<strong>The JRE could not be found. Edit the server and change the JRE location.</strong>

La manera de solucionarlo es la siguiente: Preferencias desde el menú <em>Window</em>, expandir la opción <em>server</em>, seleccionar <em>Installed Runtimes</em>. Posiblemente, se haya quedado activada la opción <em>Workbench default JRE</em>. Deberás cambiarla manualmente desde esta misma localización a la que estés utilizando para que todo funcione. No obstante, esto significa que Eclipse no es capaz de reconocer estos cambios de JDK/JRE, así que deberás tenerlo en cuenta cada vez que actualices alguna de las aplicaciones relatadas.

Saludos.