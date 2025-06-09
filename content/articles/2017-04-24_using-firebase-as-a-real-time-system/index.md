---
title: "Using Firebase as a Real Time System"
author: "Enrique López-Mañas"
date: 2017-04-24T01:58:31.968Z
lastmod: 2025-06-09T09:48:43+02:00

description: ""

subtitle: "I have been an avid user of Firebase since more than a year now. When Parse.com announced it would be shutting off, I was attending a…"

image: "/articles/2017-04-24_using-firebase-as-a-real-time-system/images/1.jpeg" 
images:
 - "/articles/2017-04-24_using-firebase-as-a-real-time-system/images/1.jpeg"
 - "/articles/2017-04-24_using-firebase-as-a-real-time-system/images/2.png"
 - "/articles/2017-04-24_using-firebase-as-a-real-time-system/images/3.png"
 - "/articles/2017-04-24_using-firebase-as-a-real-time-system/images/4.png"
 - "/articles/2017-04-24_using-firebase-as-a-real-time-system/images/5.png"


aliases:
    - "/using-firebase-as-a-real-time-system-d360265aa678"

---

I was captivated by exposed pictures since I was a child. Is a unique way to capture movement in a static image.

I have been an avid user of Firebase since more than a year now. When [Parse.com](https://en.wikipedia.org/wiki/Parse_%28company%29) announced it would be shutting off, I was attending a Google Launchpad in Mountain View as a mentor. If you haven’t heard of the [Google Launchpads](https://developers.google.com/startups/), they are great. Not only for the startups, which get a fair amount of advising and mentoring from people in different fields (UX, Tech, Marketing, Monetizing and Fund raising…) but also for mentors itself! Besides getting to know what top-notch startups are doing around the world and helping them, we also get to talk with each other and get to know first hand what other folks are experiencing too. It ressembles a swinging party where knowledge is the currency to be exchanged. It has always been one of those events where you wake up early and excited, just thinking of following up with all the people you have met the previous day.

Nevermind, I remember after Parse shutting down, there was a lot of talks about Firebase and its future. Knowing what Firebase was able to do, I could not conceive how Parse (a competitor aiming to occupy the same space) was not succesful. We are always biased in our little universe, and as developers our initial thought is “if the IT execution was so good, why they got in trouble?”. The further you work with people belonging to other universes the more you realise how you need to be succesful in different fields. I am not sure where Parse failed, but the truth is that its failure smoothed the way for Firebase success.

I publish a poll each Monday on my twitter account. They do not aim to represent a scientific and meticulous analysis of my followers, but more as a fun activity and a gymnastic exercise for my brain (coming up with a non meaningless question once per week is harder than you think!). I wrote it about [it recently](https://medium.com/google-developer-experts/an-overview-of-polls-for-android-mobile-developers-in-2016-4c41059a47a9). In any manner, being a Firebase aficionado I thought it would make sense to ask about the relationship of the poll participants with Firebase (I also knew from many of the community events where I participate that Firebase was not that well-known). I came up with this result:

> [](https://twitter.com/eenriquelopez/status/820846181618106368)


Twitter polls cannot follow by definition a scientific method, but I wonder how many people that voted for the latest option did indeed know about Firebase and opted for not using it. I realised at that moment how many people were not aware one of the potential of one of the tools that can certainly level up their game when it comes to develop software.

#### Firebase Realtime Database

Is not the purpose of this article to provide an intense overview of all the features of Firebase, since there are already a bunch of resources that can help you to get there. I can particularly recommend you their [YouTube channel](https://www.youtube.com/user/Firebase/playlists), is pretty cool to watch and more interactive than other options. This article is here to explain you how you can use Firebase to develop real time systems using the Real Time Database.

When you start getting into Firebase, sooner than later you get to see this diagram in your browser:

![image](/articles/2017-04-24_using-firebase-as-a-real-time-system/images/2.png#layoutTextWidth)


Firebase has a family of products that can help you in three fields: **growing**, **earning** and **development**. In this latest group, there is a tool called Real Time Database. This database stores information in NoSQL (to keep it simple, think of it as a huge JSON file) hosted in the Google Cloud. The greatness of the Real Time Database is mainly composed by three points:

1.  It is Real Time: There is no batching and grouping of data before being sent. When the information is altered, is instantly synchronised with the Cloud within milliseconds.
2.  Offline handling: if you are a mobile developer, online data synchronization is a thing. Google Expert Dan Lew [wrote about how they achieve this at Trello](http://blog.danlew.net/2017/02/14/airplane-mode-enabling-trello-mobile-offline/), and you can imagine is not a simple problem to solve. You do not have to worry about synchronization or conflict solving, Firebase will do it for you.
3.  Automagic synchronization: devices can subscribe to sections of the database and retrieve automagically the required data when it is being altered. No more pull and refresh.

Part of the magic of how Firebase achieves this is also the simplicity in the code. You do not need to spend hours coding. This can literally be achieved within minutes.

For the sake of simplicity, this tutorial will provide the code for Android. As you may know, Firebase do provide SDKs for iOS and the web with an equal plethora of simplicity. Let’s see (configuration and setup of our application aside) how could we write a value in the Real Time Database (RTD from now on)

```Java
FirebaseDatabase database = FirebaseDatabase.getInstance();
DatabaseReference myRef = database.getReference("message");
myRef.setValue("Hello, World!");
```



If we execute this code in our client, the RTD will reflect the changes in its structure:

![image](/articles/2017-04-24_using-firebase-as-a-real-time-system/images/3.png#layoutTextWidth)


With Firebase we can also push nodes into our RTD. That way, the RTD generates a unique key:


```Java
FirebaseDatabase database = FirebaseDatabase.getInstance();
database.getReference().push().setValue("Hello world");
```

Which also creates the result in RTD, this time with a unique key as an ID:

![image](/articles/2017-04-24_using-firebase-as-a-real-time-system/images/4.png#layoutTextWidth)


I have previously mentioned that apps get notified wherever data has been changed in the RTD out of the box. With the following code, we will subscribe to any value that is changed in the specified node (in this case, the node “message”):


```Java
FirebaseDatabase database = FirebaseDatabase.getInstance();
DatabaseReference myRef = database.getReference("message");
myRef.addValueEventListener(new ValueEventListener() {
  @Override
	public void onDataChange(DataSnapshot dataSnapshot) {
	  Log.i("MyApp","Data changed");
	}

	@Override
	public void onCancelled(DatabaseError databaseError) {
	  Log.i("MyApp","Data canceled");
	}
});
```

As you can see in the following video, the app gets automatically notified when a value has been changed:


{{< youtube 5cSNT_7Mw6Q >}}



We have now some code snippets and some basic fundamentals. The first approach to RTD is “cool, a database where I can store data and share it with other devices”. But there is much more than can be done.

You can probably take from here a few ideas on how to save time and resources to implement a Real Time system with Firebase. How can we use this creatively?

#### Real Time Chat with Firebase

Implementing a chat can be tough. I remember my first attempt was implementing a Jabber client at the university, and at that time it looked to me a task of mastodontic complexity. Over time different protocols arised. XMPP was always a clear candidate to be used, and while exploring it I always thought it was overly complex and had a few limitations the deeper you dived in. Whatever alternative was chosen, it was a task requiring a significant amount of effort.

If you have been reading this article, you probably have reached your own conclusion: this could be damm easy to implement with Firebase! Fortunately things can get even easier. [Firechat](https://firechat.firebaseapp.com/) is an open implementation based on Firebase. It might not be exactly what you are looking for, but is definitely a great option if you want to prototype something fast to check assumptions on your business idea.

![image](/articles/2017-04-24_using-firebase-as-a-real-time-system/images/5.png#layoutTextWidth)


#### Map with real time locations

In my previous company, one of the tasks I had to confront was to implement a real time map to display locations of two devices that were constantly updating each other (think of something like Uber). At that time the task was tedious as well. The solution we adopted at the time was an MQTT server that was receiving updates from both devices, taking some server side decisions and then updating the devices of the position from their respective counter-partner if required. As good as it worked out, I always thought of the adopted solution and wished something more efficient and simple could have been done. I wish I could have known of Firebase at that time.

You can also imagine that implementing this with Firebase can be done relatively easily. Matthieu Moquet, web engineer at Blablacar, wrote about how to do something similar a [couple of years ago](https://moquet.net/blog/realtime-geolocation-tracking-firebase/). Although Firebase might have some limitations (and obviously the server logic that can be implemented is limited) I see this as a fantastic tool for prototyping, which is one of the most important phases of software development.

Also, Firebase has created for this purpose a library called [GeoFire](https://github.com/firebase/geofire)! This library is also opensource, and simplifies a lot the process of creating your own location aware app.

#### Rankings

Ever used a game? I did and do, and one of the fundamental components is to design a ranking that can be filtered based on location or other characteristics of each player.

With Firebase this can easily be done as well. Imagine a RTD where you are storing for each user the games that have been played and a total ranking of points, that gets updated each time the user is scoring.

**Further ideas?**

I am sure this is just a small introduction to what RTD can do for you in Firebase, and many other folks can benefit of the Real Time capabilities it offers. If you are diving deeper in this topic, I absolutely recommend you to check the following video on [Firebase Security](https://www.youtube.com/watch?v=PUBnlbjZFAI), which will teach you how to create roles for users and rules to determine which content can they access.

Happy coding!

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, like it and/or leave a comment. This is the currency that fuels amateur writers.
