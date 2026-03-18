---
date: '2012-03-18T17:03:35+00:00'
draft: false
slug: flirting-with-sentimental-analysis-my-experience
title: 'Flirting with sentimental analysis: my own approach and some case-scenario
  applications'
---

Lately I have been interested in applying data analysis to information sources, particularly Twitter. Twitter has all the necessary features to provide an effective real time analysis: the API they provide allows us to access all the required features for analysis, and the volume of information is just huge. I strongly believe that Twitter has already changed the way to perform intelligent analytics, since it just contains millions of thematic tweets that can be accessed with no limitation.


Since I began to write my own intelligent agent for <a href="http://www.teamliquid.net/forum/viewmessage.php?topic_id=303062" target="_blank">SCAI</a> (a tournament to develop an AI agent able to play Starcraft) I really got very interested in modeling human intelligence. So of course there is a lot to do in this field, and doesn''t make any sense to list those well-known challenges still open. One of the fields that always attracted me was the <a href="http://en.wikipedia.org/wiki/Sentiment_analysis" target="_blank">Sentimental Analysis</a>. How interesting is the idea of extracting sentimental information of texts? Furthermore, this field deeps into many interesting areas of the Artificial Intelligence. 

A few months ago I began to develop my own Sentimental Analyzer. It wasn''t easy at the beginning: there are so many different approaches that the task seemed overwhelming. Since the project aimed to have a little more impact that traditional sentimental analyzers, I used a different approach: most of the ideas use keywords approach. They are pretty effective, but they do not ensure recall and it is more difficult to train the analyzer (i.e., train it automatically by using Twitter as a learning source). So I decided to use it using classifiers from different machine learning algorithms. The analyzer has been trained only for English, although it learns every day and I''m considering to expand it to some other languages (fundamentally Spanish and German)

And the experiment is working, and pretty accurate I would like to say. I have developed two applications to show them as testbeds for the analyzer:

	<ul>
<li><a href="https://play.google.com/store/apps/details?id=com.happinessobserver" target="_blank">The Happinness Observer</a>, which determines the happiness for a certain concept</li>
<li><a href="https://play.google.com/store/apps/details?id=com.citymood" target="_blank">City Mood</a>. This application determines the position of the user and throw information of the mood state of the city, based on the tweets from the people referencing it.</li>
</ul>
<br/>
Feel free to download the applications and let me know what you think.

Last but not least, I have decided to give free access to the API for those who are interested. The idea is quite simple: you can call to this URL:

http://feeling-analyzer.appspot.com/feeling_analyzer/feeling?text=I+love+this+guy

In the parameter text you should send the text (HTTP codified) you want to analyze. You will need to register for a key to use the application (and add it as a parameter on the same way: &key=providedKey). <a href="mailto:eenriquelopez@gmail.com">Drop me a line</a> if you need a key and I will provide you one.

The application return a value corresponding the the polarity of the text: 0 means negative, 2 means neutral and 4 means positive. As a further enhancement of the algorithm I''m planning to extend the polarity of the analysis to support multi-values (i.e., not just providing discret values but a full continuous range of them, from 0 to 100 for example). 

Enrique López-Mañas

