---
date: '2012-02-14T10:13:19+00:00'
draft: false
slug: how-intelligent-should-the-ai-be
title: How intelligent should the AI be
---

<img src="http://www.aiai.ed.ac.uk/style/head.jpg" alt="" />

Reading and thinking the last days about how to implement an intelligent system to play Starcraft, I had time to think about the implications of considering a system "intelligent".

Nowadays, we can develop systems that are able to defeat human intelligence in certain genres. Some board games like chess, or most of the shooters are composed *of* a limited set of rules, that can be easily *modeled* and represented with different *combinations* of techniques (an expert system, considering most of the rules for almost all the situations, is a typical choice). As my colleague <a href="http://gamestalesjokers.blogspot.com/2011/01/inteligencia-artificial-o-el-arte-de.html" target="_blank">Bruno</a> points out (Spanish link), we even have to limit the intelligence of those systems by applying "stupidifying" techniques. In one of the examples Bruno provides, we only allow the AI to attack the human player after spotting him; leading *to* very weird situations like the one exposed in the following video


<iframe width="420" height="315" src="http://www.youtube.com/embed/2DZX-Fq5N0I" frameborder="0" allowfullscreen></iframe>

But this does not apply *to* strategy games. Generally, a human player has much more capacity for analysis and improvisation in complex systems like strategy games, so the only way to empower the AI is to make it able to cheat (whether in the form of direct benefits, or having access to information that the human player can't access in the same situation). The approach of *expert systems*, which has been proven to work well in most of the scenarios, can't be applied here: implementing all the possible rules for one single (and simple) situation is an overwhelming task. Cheating AI *is* a well-known aspect of Sid Meier's Civilization series; in those games, the player must build his empire from scratch, while the computer's empire receives additional units at no cost and is freed from most resource restrictions.

How to solve this? Well, one idea could be to apply learning techniques. In the last <a target="_blank" href="http://www.aaai.org/Conferences/AIIDE/aiide.php" target="_blank">AIIDE</a> competition, the Berkeley team designed a special <a href="http://arstechnica.com/gaming/news/2011/01/skynet-meets-the-swarm-how-the-berkeley-overmind-won-the-2010-starcraft-ai-competition.ars/3" target="_blank">training field</a>, aptly named <a href="http://en.wikipedia.org/wiki/Valhalla" target="_blank">Valhalla</a>. Instead of manually adjusting the parameters of the AI, they let the AI fight on its own for a high number of iterations, letting it *analyze* its own results and adjusting the *parameters in* its most convenient way. The result can be seen in the following video: they trained a group of mutalisks to massacre their natural counter unit, something unlikely if a human were controlling the units.

<iframe width="560" height="315" src="http://www.youtube.com/embed/0BS8Mbqbnmk" frameborder="0" allowfullscreen></iframe>


But we are still far away from reaching an AI that can defeat humans in complex scenarios. Although *it has* its <a href="http://en.wikipedia.org/wiki/Moore''s_law#Ultimate_limits_of_the_law" target="_blank">limitations</a>, Moore's law is helping us, but we are not only facing a problem of computing capabilities. We also need to find different ways to model complex scenarios that the human mind is good at analyzing, but the computer is still behind us. And if we finally use cheating to defeat a human intelligence, we have to make it completely transparent: the user will not care as long as beating the AI is still challenging for him.