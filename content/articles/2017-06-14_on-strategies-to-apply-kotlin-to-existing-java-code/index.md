---
title: "On Strategies to apply Kotlin to existing Java code"
author: "Enrique López-Mañas"
date: 2017-06-14T04:59:29.689Z
lastmod: 2025-06-09T09:48:51+02:00

description: ""

subtitle: "Since the latest announcement at the Google I/O, things have been crazy. At the Kotlin Weekly Mail List we had an increase in subscribers…"

image: "/articles/2017-06-14_on-strategies-to-apply-kotlin-to-existing-java-code/images/1.jpeg" 
images:
 - "/articles/2017-06-14_on-strategies-to-apply-kotlin-to-existing-java-code/images/1.jpeg"
 - "/articles/2017-06-14_on-strategies-to-apply-kotlin-to-existing-java-code/images/2.png"
 - "/articles/2017-06-14_on-strategies-to-apply-kotlin-to-existing-java-code/images/3.png"


aliases:
    - "/on-strategies-to-apply-kotlin-to-existing-java-code-6317974717ec"

---


Since the latest announcement at the Google I/O, things have been crazy. At the [Kotlin Weekly](http://www.kotlinweekly.net/) Mail List we had an increase in subscribers over 20% in the last two weeks, over 200% increase in article submissions, and at a Meetup I organise ([Kotlin Users Group Munich](https://www.meetup.com/Kotlin-User-Group-Munich/)) we had a huge increase in attendees. And all this combined with the general blast in the developers community.

![image](/articles/2017-06-14_on-strategies-to-apply-kotlin-to-existing-java-code/images/2.png#layoutTextWidth)
A trend that will only continue to grow.



It is somehow obvious now where the future is leading. Although Google promised to keep support for Java, the legal battle between [Google and Oracle](https://en.wikipedia.org/wiki/Oracle_America,_Inc._v._Google,_Inc.) and the clear fact that Kotlin is a more succinct, effective and powerful language is marking the direction in a sea of reads. I found this tweet to be fairly predictive.

> [](https://twitter.com/lehtimaeki/status/864936555860963328)


A few months ago, when I was present in a Kotlin related environment, probably the most recurrent question was whether it was a good time to start a migration into Kotlin. My answer was always invariably **YES**. There were many benefits and almost no drawbacks if you proceeded with a Kotlin migration. The only technical drawback I could think of was increasing the method count number, since kotlin-stdlib adds (currently) [7191 new methods](https://blog.jetbrains.com/kotlin/2016/03/kotlins-android-roadmap/). Considering the new benefits on the table, that was a more than acceptable disadvantage.

Now that the answer to that question is affirmative without any kind of palliatives, I realised there is another question floating around: _how is the process to start adopting Kotlin?_

In this article I am aiming to provide a few ideas for those of you confused about where to start or looking for new ideas.

### 1.- Start with the tests

Yes, I am aware that tests are limited in nature. A Unit Test means exactly that: you are testing individual units and modules. It is hard to develop complex architectural nets when all you have is a bunch of single classes and maybe a few helper ones. But this is a very cheap and effective way to build awareness and spread knowledge of the new language.

One recurrent argument against Kotlin I have heard is to avoid deploying into production code lines written in Kotlin. As much as I think this is a   
highly-coloured problem, I want to emphasise with you. If you start with the tests, no code is being actually deployed. Instead, this code is being used likely in your CI environment and as a way to extend knowledge.

Start writing new tests in Kotlin, they can cooperate and talk directly to other Java classes. When you have some idle time, [migrate the Java classes](https://www.jetbrains.com/help/idea/2017.1/converting-a-java-file-to-kotlin-file.html), check the resulting code and apply whatever transformation you find required. In my personal experience, 60% of the transformed code is directly usable, and a bigger percentage for simple classes with no complex functionality. I find this first step as a very safe scenario to start with.

### 2.- Migrate existing code

You have started writing some code. You know some of the basics of the language. Now you are [Kotlin-ready for production](https://www.youtube.com/watch?v=-3uiFhI18g8)!

When you first start dealing with your productive code, I have found effective to start first with the classes of less impact: [DTOs](https://en.wikipedia.org/wiki/Data_transfer_object) and models. This classes have an extremely low impact, and they can be easily refactored in an exceptionally short time span. Is the perfect time to get to know [data classes](https://kotlinlang.org/docs/reference/data-classes.html) and seriously reduce the size of your codebase.

![image](/articles/2017-06-14_on-strategies-to-apply-kotlin-to-existing-java-code/images/3.png#layoutTextWidth)
This is the PR you want to send



After this, start to migrate unitary classes. Maybe the **LanguageHelper**, or the **Utils** class. Although widely used, this kind of classes tend to provide a set of functionality limited in relationships and impact.

At some point you will feel comfortable enough to tackle the bigger and central classes of your architecture. Do not be scared. Pay special attention to the **nullability**, this is one of the most important features of Kotlin. It will require a new mindset if you have been programming in Java for a few years, but the new paradigm essentially will set in your mind, believe me.

Remember: you do not need to stress about migrating the entire codebase. Kotlin and Java can seamlessly interact, and there is no need now to have a 100% Kotlin code. Do it until it feels comfortable.

### 3.- Go wild with Kotlin

At this point you can definitely start writing all the new code in Kotlin. Think of this as a previous relationship, and do not look back. At the top of the mentioned **nullability**, when you are starting to write your first features in pure Kotlin pay attention as well to the defaulted parameters. Think in terms of extension functions, rather than inheritance. Do Pull Requests and Code Reviews, and talk with your colleagues how things can be done better and improved.

And the ultimate tip, enjoy!

### Resources to learn Kotlin

The following is a list with links I have tried and can recommend to learn Kotlin. I am particularly fond of books, although some people dislike them. I find pretty important to read them loud, writing over them and practicing on the computer at the same time to sediment knowledge better.

1.  [Kotlin Slack](http://slack.kotlinlang.org/): many JetBrains folks and Kotlin aficionados together.
2.  [Kotlin Weekly](http://kotlinweekly.net/): a mailing list I manage with a weekly selection of Kotlin topics.
3.  [Kotlin Koans](https://kotlinlang.org/docs/tutorials/koans.html): a series of online exercises to practice and solidify your Kotlin skills.
4.  [Kotlin in Action](https://www.manning.com/books/kotlin-in-action): book from some of the people working on Kotlin at JetBrains.
5.  [Kotlin for Android developers](https://transactions.sendowl.com/stores/7146/39165): book focusing on how to apply book to develop for Android.
6.  [Resources to Learn Kotlin](https://developer.android.com/kotlin/resources.html): Google website with more resources to learn Kotlin.

I write my thoughts about Software Engineering and life in general in my [Twitter account](https://twitter.com/eenriquelopez). If you have liked this article or it did help you, feel free to share it, ♥ it and/or leave a comment. This is the currency that fuels amateur writers.
