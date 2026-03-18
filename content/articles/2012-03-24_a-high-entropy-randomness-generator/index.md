---
date: '2012-03-24T03:23:05+00:00'
draft: false
slug: a-high-entropy-randomness-generator
title: A high-entropy randomness generator
---

<a href="/wp-content/uploads/2012/03/Bildschirmfoto-2012-03-24-um-03.02.34.png"><img class="aligncenter" style="max-width: 150px;" title="Bildschirmfoto 2012-03-24 um 03.02.34" src="/wp-content/uploads/2012/03/Bildschirmfoto-2012-03-24-um-03.02.34.png" alt="Randomness cartoon" /></a>

&nbsp;

This <a href="http://www.random.org/analysis/dilbert.jpg" target="_blank">cartoon</a> of Dilbert has always fascinated me. You can never be sure about randomness, since the concept of randomness itself provides uncertainty to the process. A few years ago, I even wrote <a href="/articles/generacion-de-numeros-aleatorios/" target="_blank">a post</a> on how to achieve randomness using deterministic methods. Nowadays, entropy can always be improved to obtain a more accurate (in this case, it would be more appropriate to say "less accurate" instead) result. This can lead to many philosophical discussions, which are not my purpose.

The traditional approach has been to take contextual information (such as the UNIX time) to create a seed for the algorithm and give more uncertainty to the process. This might be sufficient for 99% of our purposes, but leads to more complex problems: For instance, it is easy to determine when a user logged into a system, and if at this time a random number is generated to generate some cryptographic keys at the same time, it is easy to establish an interval when the user was logged in (and therefore be closer to the seed of the random algorithm). It is still difficult to determine accurately the exact time, but definitely not impossible: systems of huge relevance face this problem daily.

Recently, I published in the Android Market <a href="https://play.google.com/store/apps/details?id=enrique.chineseradicals" target="_blank">Chinese Radicals</a>, a program to learn Chinese. Since I need to randomly choose the Chinese radicals for the program, I decided to use it as a testbed to extend my experiment from 3 years ago. The approach uses some "contextualization" of the seed, and combines it with a probability density function. The explanation can get really complex, but I'll try to summarize:
<ol>
	<li>At a certain point of execution, I categorize the accessible memory of the thread where the software is running (size and number of memory blocks). This information is stored and modeled for the density function.</li>
	<li>Afterwards, I take the UNIX time of the system. I apply a probability distribution to the model saved in the first step, and then combine it with this second point. I store the current time, and apply a first pass.</li>
	<li>When the generation of the random number is finished, I determine the difference between that time and the time I stored in step two. Since the memory information saved in point 1 (the entropy of the system) might differ, this time will likely be different. Then I apply a second pass to generate, with more certainty, the random number.</li>
</ol>
&nbsp;

I have released this generator as a Java .jar. You can include it in any Java project (Swing, Blackberry, Android, etc). You can download it <a href="/wp-content/uploads/2012/03/Randomizator.jar_.zip" target="_blank">from here</a>. It works as follows:
<ol>
	<li>Import the jar</li>
	<li>Import the class com.randomizator.Randomizator, and create an object Randomizator by using Randomizator myObject = new Randomizator();</li>
	<li>Using randomizator.getInt( interval ) will return you a random number between 0 and the number provided.</li>
</ol>
So far, only the generation of integer values is supported. Please check it out and let me know what you think.

&nbsp;