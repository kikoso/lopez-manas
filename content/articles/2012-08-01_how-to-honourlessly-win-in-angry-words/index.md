---
date: '2012-08-01T13:13:04+00:00'
draft: false
slug: how-to-honourlessly-win-in-angry-words
title: How to (honourlessly) win in Angry Words
---

In my scarce free time I usually play <a href="http://www.angrywords.com/" target="_blank">Angry Words</a>. For those who have never heard about it (quite unlikely if you''re reading this article) Angry Words is basically a <a href="http://en.wikipedia.org/wiki/Scrabble" target="_blank">Scrabble</a> that can be played online against different opponents. There are currently versions for Android and iPhone.

&nbsp;

Recently, in May 2011, a security hole was reported in WhatsApp which left user accounts open for hijacking. Since May 2011 it has been reported that communications made by WhatsApp are not encrypted, and data is sent and received in plaintext, meaning messages can easily be read if packet traces are <a href="http://www.yourdailymac.net/2011/05/whatsapp-leaks-usernames-telephone-numbers-and-messages/" target="_blank">available</a>. Together with the well-known storage of the full set of messages sent and received within the application (that can be easily <a href="http://www.securitybydefault.com/2012/05/descifrando-el-fichero-msgstoredbcrypt.html" target="_blank">cracked</a>) led me to think if that was a concrete, disastrous development, or a generalized trend in most mobile applications. Therefore, I decided to see if it could be possible to do the same with Angry Words.

&nbsp;

If you want to reproduce the steps in this article, you will need to set up your environment to sniff data from your mobile. There are many options to achieve this (install a cracked .apk or .ipa into your emulator and capture the data, root your Android device and capture the data with a sniffer...), but for me, the easiest one was to use my computer as a bridge for my phone, and use <a href="http://www.wireshark.org/download.html" target="_blank">Wireshark</a> to sniff the data. The process is quite simple: you just need to activate the "Internet Sharing" option, using your AirPort as a bridge to your ethernet connection (if you don''t have an ethernet connection, you will surely still have the option to tether your phone). In "Configuration" - "Internet Sharing" proceed as shown in the following image:

&nbsp;
<p style="text-align: center;"><a href="/wp-content/uploads/2012/08/osx_configure_sharing1.png"><img class="size-medium wp-image-126 aligncenter" title="osx_configure_sharing" src="/wp-content/uploads/2012/08/osx_configure_sharing1-300x210.png" alt="" width="300" height="210" /></a></p>
&nbsp;
<p style="text-align: left;">You probably get the idea: the point is connecting the device to your computer and sniff the traffic from there. It is outside the purpose of this article to teach how to use Wireshark, but you can find many tutorials on the Internet. Basically, when your device is connected, start up Wireshark on your computer and attach to the Wi-Fi interface. You normally need to start Wireshark as the super-user in order to have enough rights to capture traffic. You can do this by typing <code>sudo wireshark &amp;</code>.</p>
We want to capture packets on the AirPort interface, which will very likely be the interface en1. Click the leftmost button on the Wireshark toolbar, and then click “Start” next to device en1:
<p style="text-align: center;"><a href="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.20.48.png"><img class="aligncenter  wp-image-128" title="Bildschirmfoto 2012-09-01 um 14.20.48" src="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.20.48.png" alt="" width="372" height="151" /></a></p>
<p style="text-align: left;">When this has been set up, and your device is connected to your computer, you will begin to filter all the packets. Since Wireshark does not discriminate between all the applications, it is a good idea to filter the packets that will be captured. For this purpose, you can create a filter using the following expression:</p>
<p style="text-align: left;">ip.src == xx.xx.xx.xx</p>
<p style="text-align: left;">ip.dst == xx.xx.xx.xx</p>
<p style="text-align: left;">The xx.xx.xx.xx value is the private IP that your phone has been assigned when connecting to your computer. In my case, this IP is 10.2.2.2</p>
<p style="text-align: left;"><a href="/wp-content/uploads/2012/09/wire.png"><img class="aligncenter size-large wp-image-129" title="wire" src="/wp-content/uploads/2012/09/wire-1024x377.png" alt="" width="1024" height="377" /></a></p>
<p style="text-align: left;">Now we will only display the packets corresponding to our device, so it''s time to play. By opening Angry Words and playing, we will see each request sent from the application (and received from the server). We will soon notice some issues:</p>

<ul>
	<li>The application uses plain HTTP, no SSL in between. We can see all the requests sent as web requests. We can log in the application through Facebook Auth, or with our mail and password. If we use the second way, even the password is sent in plain text.</li>
	<li>All the information about each game is stored in the server (since we can access from different devices), which makes it a little bit more complicated to hack an already created game. But it can be achieved using a Man in the Middle attack, which is not hard if we are using our own computer as a proxy (also, we can decide whether a word is right or not).</li>
	<li>With each connection, a cookie value is created. This cookie value has to be sent within each request to validate all the requests.</li>
</ul>
Let''s see some examples of captured data. In the following, we are requesting information about a particular game:

<a href="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.41.06.png"><img class="aligncenter size-large wp-image-131" title="Bildschirmfoto 2012-09-01 um 14.41.06" src="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.41.06-1024x563.png" alt="" width="1024" height="563" /></a>

After sending a request to check if a word is right, we also receive all the information in plain text.

<a href="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.45.31.png"><img class="aligncenter size-large wp-image-134" title="Bildschirmfoto 2012-09-01 um 14.45.31" src="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.45.31-1024x568.png" alt="" width="1024" height="568" /></a>

<a href="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.43.37.png"><img class="aligncenter size-large wp-image-132" title="Bildschirmfoto 2012-09-01 um 14.43.37" src="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.43.37-1024x577.png" alt="" width="1024" height="577" /></a>

Here begins the interesting part: this is how we can send a tile to the server:

<a href="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.44.20.png"><img class="aligncenter size-large wp-image-133" title="Bildschirmfoto 2012-09-01 um 14.44.20" src="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.44.20-1024x573.png" alt="" width="1024" height="573" /></a>

We also can see how to resign a game:

<a href="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.46.42.png"><img class="aligncenter size-large wp-image-135" title="Bildschirmfoto 2012-09-01 um 14.46.42" src="/wp-content/uploads/2012/09/Bildschirmfoto-2012-09-01-um-14.46.42-1024x680.png" alt="" width="1024" height="680" /></a>

&nbsp;

So, after analyzing all the game interactions, we can conclude the following:
<ul>
	<li>We can retrieve all the information about a user''s games by calling the following address: <a href="http://www.blogger.com/goog_477396173">http://api.apalabrados.com/api/users/[USER_ID]</a><a href="http://api.apalabrados.com/api/users/[mi_usuario_ID]/games">/games</a> .</li>
	<li>We can check the validity of a word using GET <a href="http://api.apalabrados.com/api/dictionaries/EN?words=wordtocheck" target="_blank">http://api.apalabrados.com/api/dictionaries/EN?words=wordtocheck</a> . We will get a JSON <em>{"answer":true,"wrong":[],"ok":["word</em><em>"]}</em> if the word is valid, or <em>{"answer":false,"wrong":["word</em><em>"],"ok":[]} if it is not.</em></li>
	<li>We can also pass or resign a game. By calling the address <a href="http://www.blogger.com/goog_477396165">http://api.apalabrados.com/api/users/[USER_ID]</a><a href="http://www.blogger.com/goog_477396165">/games/[GAME_ID]</a><a href="http://api.apalabrados.com/api/users/[mi_usuario_ID]/games/[juego_ID]/turns">/turns</a> , and adding either the value <em>{"type":"PASS"} </em>or<em> <em>{"type":"RESIGN"}</em>,</em> the server changes the status of the game.</li>
	<li>If we are connected to a WiFi network, doing a MiM and manipulating the data being sent back to the user is just trivial. Connecting through 3G or a GSM network makes things harder.</li>
</ul>
In each of those requests (except to check the validity of a word) we need to insert the value of a cookie. To create custom HTTP Requests, and depending on your Operating System, I would recommend you use <a href="http://www.fiddler2.com/fiddler2/" target="_blank">Fiddler</a> for Windows. For Mac, I''m not sure whether FireBug allows you to create custom HTTP requests, but I''m using <a href="https://chrome.google.com/webstore/detail/fhjcajmcbmldlhcimfajhfbgofnpcjmb?hl=de" target="_blank">Simple Rest Client</a> for this article, and it works pretty well. But there are <a href="https://chrome.google.com/webstore/search/HTTP%20debugger?hl=de" target="_blank">plenty of tools</a> around there to be used.

&nbsp;

<strong>How can this be solved?</strong>

&nbsp;

The obvious thing is to use an SSL connection, but this might require some changes and time in the server configuration. Also, to manipulate the requests (unless we automate it) some time is required, so creating a suitable timeout is also a good idea. I want to emphasize that, although the requests can be sent from a computer or automated programs, manipulating the data sent back is only possible through a wireless network. So, if you are suspicious that your AngryWords partner might be a hacker, disconnect your WiFi while you''re playing against him or her.

&nbsp;

You can contact me at my <a href="mailto:eenriquelopez@gmail.com" target="_blank">private email</a>, or leave a message as a comment. If the post has been helpful for you, consider being nice and cite me if you use it.