---
date: '2008-01-28T21:53:59+00:00'
draft: false
slug: port-knocking
title: Port Knocking
---

Quizá esta información sea novedosa para muchos de vosotros. A pesar de no tratarse de un tema novedoso, ya que hay literatura al respecto desde el 2003, quizás sea un concepto desconocido, al menos para la comunidad de habla hispana en internet.

Es sabido que la seguridad electrónica nunca puede basarse en una sola medida o nivel de seguridad. Así, hablaremos de sistemas con doble, triple o con niveles más altos de seguridad, según exista una combinación de medidas que ayuden a asegurar y hacer impenetrable un sistema (por ejemplo: a la hora de asegurar un router que provee acceso inalámbrico, un filtro a nivel de MAC + una encriptación WPA a 256 + una elección de direcciones IP no estándares + servidor DHCP deshabilitado constituiría un cuádruple nivel de seguridad).

<strong>¿Qué es "Port Knocking"?
</strong>
Todos hemos jugado de pequeños con nuestros amigos a tener algún código común que debíamos compartir para poder identificarnos entre nosotros. Pues básicamente, se trata del mismo sistema aplicado a la seguridad.

Computacionalmente, este concepto consistiría en enviar paquetes a ciertos puertos, siguiendo una secuencia determinada con el fin de realizar un propósito concreto. Al llegar al último puerto, siempre y cuando hayamos realizado el barrido de puertos de una manera específica y no aleatoria, este podría responder de una determinada manera (generalmente abriéndonos un servicio esencial para la máquina, como una identificación por SSH, o un servicio de transferencia de ficheros). De esta manera, cualquier atacante que realizase un barrido aleatorio sobre el ordenador destino, sería incapaz de ver el puerto deseado, recibiendo del firewall una simple respuesta DROP.

Tomemos como ejemplo un demonio sshd escuchando en el puerto 22/TCP. Elegimos como secuencia de barrido la sucesión 43, 6540 y 82. El puerto 22 se abrirá si, y solo si, un usuario inicializa conexiones TCP hacia los puertos 43, 6540 y 82 en ese orden exacto. En caso contrario, el usuario recibirá como respuesta un RST/ACK cuando intenta comenzar una
conexión hacia el puerto 22.

Si la secuencia correcta de inicializaciones ha sido efectuada, el puerto 22 se abrirá durante un lapso de tiempo determinado y únicamente para la IP que completó la secuencia previa. Una vez el puerto 22 se
halle abierto, se pueden llevar a cabo medidas adicionales de autenticación.

A pesar de la buena idea que a priori puede parecer, muchos son los que defienden que "Port Knocking" no es una capa de
seguridad sino una medida de ofuscación ("security by obscurity"). Como en todos los campos, la verdad (o lo más cercano a la verdad) suele encontrarse en el centro geométrico de todas las afirmaciones.

La autenticación clásica se basa en tres premisas: que sabes, que eres y que tienes. Este mecanismo estaría claramente encuadrado en el primer apartado. <strong>Sabemos</strong> cómo acceder a un servicio. Lógicamente, en el momento en el que un atacante conociese esta medida y pudiese escuchar el tráfico en cualquiera de los dos lados, esta medida de seguridad individualmente sería tan débil como una contraseña enviada en texto plano. Como se comentó inicialmente, esta medida no podría (debería) ser utilizada de manera individual, sino en combinación con algún otro nivel de defensa que proporcionase seguridad adicional en caso de que la medida fuese comprometida, para alcanzar un nivel de robustez aceptable.

Algunas consideraciones

* Un ataque de fuerza bruta podría ser ejecutado con la intención de descubrir la secuencia de puertos correcta. No obstante, el ataque sería fácilmente detectable, y con los movimientos correctos por parte del administrador de sistemas, esta medida tendría probabilidades de éxito casi nulas. Para una secuencia de 3 puertos, suponiendo el rango de ataque entre los puertos 1-65535, implicaría un escaneo del orden de 655353 tentativas, con una media situada en la mitad de este valor, con lo que serían necesarios unos 140 billones de paquetes para conseguir la apertura del puerto deseado. Obviamente, incrementar la longitud de la secuencia incrementaría exponencialmente la dificultad del objetivo.

* Si un supuesto atacante se hace con la secuencia de puerto, no se interpone nada entre él y el servicio ocultado. Por lo tanto, algún tipo de medida al respecto sería interesante (algún hash con información adicional, como información temporal, estado físico de la memoria, etc), o alguna otra medida que evitase los ataques por replay. No obstante, esta medida sería difícil de implementar en sistemas con múltiples clientes.

* Un ataque sencillo sería un DoS. Debido al lapso que existe entre cada inicialización de cada conexión, un atacante puede enviar paquetes malintencionados para interrumpir la secuencia que trate de construir el usuario legítimo. No sería técnicamente difícil forjar paquetes con la dirección IP de un usuario legítimo y enviar un continuo flujo a la máquina objetivo, lo que le impediría en la práctica de poder ofrecer el servicio.

* Un Port Knocking podría ser confundido con un escaneo de puertos para un IDS, lo que podría añadir complejidad de configuración al mismo y generar ruido en sus logs.

<strong>Conclusión</strong>

Un sistema protegido por Port Knocking añade un excelente método de protección al mismo. A la mayoría de posibles intrusos, les parecerá que no se ofrece ningún servicio tras el firewall, y dada su relativa poca extensión, la mayoría desconocerán igualmente esta posibilidad. No obstante, como ya se ha dicho numerosas veces, conviene no utilizarlo como última línea de defensa, sino en combinación con diferentes niveles de protección.