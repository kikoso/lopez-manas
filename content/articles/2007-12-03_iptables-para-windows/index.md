---
date: '2007-12-03T23:37:15+00:00'
draft: false
slug: iptables-para-windows
title: IPTables para Windows
---

Trabajo con los tres sistemas operativos mayoritarios del mercado en mayor o menor cuantía, y en función de la necesidad específica que requiera (en mi trabajo como HiWi en la universidad me desenvuelvo prácticamente con Linux, para usar muchas aplicaciones de programación o de diseño comerciales utilizo Windows en su versión XP, Macintosh principalmente con propósitos domésticos...)

Desde hace un tiempo me rondaba la cabeza encontrar un firewall específico para Windows que tuviese las características de IPTables para Linux. Con el tiempo, y evaluando varias alternativas, he conseguido llegar a <a href="http://wipfw.sourceforge.net/" target="_blank">WIPFW</a> . WIPFW es un firewall software para plataformas Windows basado en IPFW1, un firewall bastante popular para la familia BSD.

La <a href="http://mesh.dl.souhttp://switch.dl.sourceforge.net/sourceforge/wipfw/qtfw_win-beta.zip">GUI</a> y la<a href="http://mesh.dl.sourceforge.net/sourceforge/wipfw/wipfw-0.2.8.zip"> aplicación </a>en línea de comandos pueden descargarse por separado desde la página del proyecto en sourceforge. La aplicación ha sido liberada bajo licencia BSD, con todas las ventajas que ello reporta. La sintaxis de configuración recuerda bastante a la del propio IPTables (puede verse en la <a href="http://wipfw.sourceforge.net/doc.html" target="_blank">documentación</a> de la página oficial).

Como el propio IPTables, este firewall no es la mejor elección para usuarios neonatos o noveles, dada su no-simplicidad de uso. No obstante, para entornos más industriales y/o comerciales, ofrece bastante adaptabilidad y versatilidad.