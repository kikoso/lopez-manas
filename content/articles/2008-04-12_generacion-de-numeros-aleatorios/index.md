---
date: '2008-04-12T12:22:39+00:00'
draft: false
slug: generacion-de-numeros-aleatorios
title: Generación de números aleatorios
---

La generación de <a target="_blank" href="http://en.wikipedia.org/wiki/Random_number_generation">números aleatorios</a> con métodos computacionales es una de las técnicas básicas utilizadas en multitud de disciplinas como la criptografía, los videojuegos, la estadística, la simulación... Existen dos métodos de generación de números aleatorios, básicamente: los números pseudo-aleatorios, que generan una secuencia partiendo de un primer número semilla, o los aleatorios, que siguen unos algoritmos de generación más complejos, tomando generalmente datos del contexto informático en el que se generan (tales como posición del puntero, porcentaje de ocupación de la RAM, etc.) para tener suficiente entropía. En este post, trataré sobre los primeros.

Como ya he mencionado, utilizando este tipo de métodos escogeremos una semilla o valor aleatorio inicial, a partir del cual generaremos el resto de números (combinar este método con uno aleatorio real para generar una ristra de números aleatorios verdaderos es otra opción, en la que ahorraremos potencia de cálculo al generar un número aleatorio tan solo inicialmente).

Como veremos en el siguiente código, declararemos una variable "semilla" que inicializaremos a un valor dado. Será idealmente una variable estática, es decir, una variable global accesible solo por las rutinas de este mismo archivo. 

<pre lang="cpp">
#include  <iostream.h>

static long _random= 0;

//Valor inicial o semilla que proporcionaremos al algoritmo
void InicializaRnd(long l)
{
  _random = l;
}

//Rnd() generará números aleatorios
double Rnd()
{
  _random= (25173L * _random + 12849L) % 65536L;
  return double(_random) / double(65536);
}

//Llamada a main
void main()
{
  int i;
  InicializaRnd(100);  

  cout << endl << "Diez números aleatorios :"  <<endl;
  for (i= 0; i < 10; i++)
  {
    cout << Rnd() << "  ";
  }

  cout << endl << "Diez números aleatorios entre 1 y 100 :"  <<endl;
  for (i= 0; i < 10; i++)
  {
    cout << int(Rnd()*100) +1 << "  ";
  }
}
</pre>

Con la sección de código

<pre lang=cpp>
    cout << int(Rnd()*100) +1 << "  ";
</pre>

generaremos los números aleatorios entre los valores que nosotros deseemos.