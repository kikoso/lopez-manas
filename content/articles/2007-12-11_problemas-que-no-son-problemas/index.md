---
date: '2007-12-11T13:59:04+00:00'
draft: false
slug: problemas-que-no-son-problemas
title: Problemas que no son problemas
---

Hay ocasiones en las que, en mundos que se supone que existe una mayor profesionalidad que en las revistas del corazón, el comportamiento tiende al periodismo amarillo y la extensión de bulos para ganar unas cuotas de audiencia. Un ejemplo de esto se puede encontrar en la última inyección SQL publicada en <a href="http://securityvulns.com/Sdocument563.html" target="_blank">Security Vuln</a>, que afectaba a nuestro querido CMS Wordpress.

En realidad mi intención era comprobar esta vulnerabilidad, sobre todo de cara a actualizar (o desactualizar) mi CMS para evitar ataques de <a href="http://en.wikipedia.org/wiki/Zero-Day_Attack" target="_blank">0 day</a> que dieran al traste con mi trabajo de los últimos días. Sin embargo, mi gozo en un pozo cuando veo que esta inyección SQL no surte el más mínimo efecto:

<a href="/wp/images/captura.png"><img src="/wp/images/captura.png" height="288" width="462" /></a>

En <a href="http://www.kriptopolis.org/bugs-que-no-son#comments">Kriptópolis</a> también se han hecho eco del asunto.

<strong>Misc:</strong> a todo esto, aquellos que utilicéis un SO Linux sobre alguna máquina que no disponga de la función Impr. Pant (típicamente Macintosh) podéis utilizar el paquete import para tal efecto, con la siguiente sintaxis:

<em> import -pause 3 -window root</em>