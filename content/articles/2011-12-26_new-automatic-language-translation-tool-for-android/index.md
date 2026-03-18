---
date: '2011-12-26T18:48:33+00:00'
draft: false
slug: new-automatic-language-translation-tool-for-android
title: New automatic language translation tool for Android
---

Since I have been working in Barcelona, I got so much more in touch with Android and mobile developers than in Germany, since my work there was a little bit more theoretical rather than applied.

Although I don't use on a regular basis <a href="http://translate.google.com/" target="_blank">Google Translate</a> or any engine to translate my applications (this is a problem of quality vs. quantity, where I bet quality should prevail), I realized that many developers of successful applications are using Google Translate to generate new string files of their projects. And it is, in fact, much more widespread than what I thought. When I have been talking with those developers, they confess after one or two beers that they use web powered engines (i.e., Google Translate) and they usually don't perform a peer check or a professional review of their generated tokens. Without judging this behavior, I was interested in the procedure, and the first question to arise was: have you automated the process? The most recurrent answer was a "No", while they began to stare at the floor.

I thought it could be interesting for some projects, so I thought I could expand the translation tool I published a <a title="Language Assistant program for Android" href="/?p=49" target="_blank">few months ago</a>. Why couldn't we just perform the translation systematically? And that's why I'm presenting the second version of the tool.

The <a href="http://code.google.com/intl/de-DE/apis/language/translate/overview.html" target="_blank">Google Translate API</a> is not free, and since I don't want to offer my API key and see a huge bill at the end of the month in my bank account, I'm offering two different versions of the tool: the first version allows you to insert your own key and perform the translation. And if you don't want to deal with the registration and Google Checkout, you can get a paid version which uses my own API key for only $5. So if you think this tool can be helpful for you, those $5 will make you save a lot of time and I will get a few extra beers and some support to develop projects on my free time. As shown on the following screen, you just need to type your API key in the following edit text.

<a href="/wp-content/uploads/2011/12/Bildschirmfoto-2011-12-26-um-18.43.12.png"><img class="alignnone size-medium wp-image-73" title="Bildschirmfoto 2011-12-26 um 18.43.12" src="/wp-content/uploads/2011/12/Bildschirmfoto-2011-12-26-um-18.43.12-300x247.png" alt="" width="300" height="247" /></a>

There are still some upcoming tasks to be performed, but this can be considered a working alpha version.

This tool will not be released as GPL software as the previous one. However, if you need the source code for any purpose you can always send me an email in order to convince me.

The free version can be downloaded from <a href="http://code.google.com/p/language-assistant-android/downloads/list" target="_blank">here</a> (version 2.0). If you want the paid version, feel free to drop me <a href="mailto:eenriquelopez@gmail.com">a line</a> or contact me via <a href="http://twitter.com/#!/eenriquelopez" target="_blank">Twitter</a> or <a href="http://www.facebook.com/#!/eenriquelopez" target="_blank">Facebook</a>